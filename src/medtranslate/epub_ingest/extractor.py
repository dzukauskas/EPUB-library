"""
EPUB ingest pipeline.

Responsibilities
----------------
1. Open an EPUB file with ebooklib.
2. Walk the spine in canonical reading order.
3. Parse each XHTML document with lxml and extract text-bearing segments via
   XPath.
4. Assign a deterministic ``segment_id`` to every segment so that re-runs
   always produce the same identifiers for the same source file.
5. Persist ``segments.json`` and ``state.json`` so that interrupted runs can
   be resumed without re-processing already-completed spine items.
6. Extract the full EPUB container (META-INF/, OEBPS/, OPF, NAV, …) to an
   ``epub_raw/`` directory alongside the output files.

Deterministic segment_id scheme
---------------------------------
``segment_id = f"{spine_idx:04d}_{elem_idx:06d}"``

- ``spine_idx`` — zero-based position of the spine item in the publication's
  reading order.  Stable as long as the EPUB's spine does not change.
- ``elem_idx`` — sequential zero-based counter of *extracted* text-bearing
  elements within that spine document.  Stable for a fixed XPath query set.

Usage (Python)
--------------
    from medtranslate.epub_ingest.extractor import EPUBIngestor

    ingestor = EPUBIngestor(
        epub_path="path/to/book.epub",
        output_dir="path/to/output",   # segments.json / state.json / epub_raw/
        book_slug="my-book",
    )
    ingestor.run()
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ebooklib
from ebooklib import epub
from lxml import etree

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# XPath configuration
# ---------------------------------------------------------------------------

# Namespace map used for all XHTML queries.
XHTML_NS = "http://www.w3.org/1999/xhtml"
_NS = {"h": XHTML_NS}

# Tags that carry meaningful translatable text (in XPath local-name form).
# Headings and body paragraphs are the primary targets; lists, table cells, and
# captions are included so that structured content is not silently dropped.
_TEXT_TAGS = (
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p",
    "li",
    "td", "th",
    "figcaption", "caption",
    "blockquote",
    "dt", "dd",
)

# Build an XPath expression that matches any of the above tags in either the
# XHTML namespace or no namespace (some EPUBs strip the namespace).
_XHTML_EXPR = " | ".join(
    f"//h:{tag}" for tag in _TEXT_TAGS
)
_NO_NS_EXPR = " | ".join(
    f"//{tag}" for tag in _TEXT_TAGS
)


def _collect_text(element: etree._Element) -> str:
    """Return the normalised inner text of *element* (all descendant text joined)."""
    parts = []
    for text in element.itertext():
        text = text.strip()
        if text:
            parts.append(text)
    return " ".join(parts)


def _positional_xpath(element: etree._Element) -> str:
    """
    Return a stable positional XPath string for *element* relative to its
    document root.  Used only for human-readable context — not for matching.
    """
    parts: list[str] = []
    node = element
    while node is not None and isinstance(node.tag, str):
        parent = node.getparent()
        if parent is None:
            tag = etree.QName(node.tag).localname if node.tag else "root"
            parts.append(tag)
            break
        # Count siblings with the same local tag name.
        local = etree.QName(node.tag).localname
        siblings = [
            c for c in parent
            if isinstance(c.tag, str) and etree.QName(c.tag).localname == local
        ]
        idx = siblings.index(node) + 1  # 1-based XPath convention
        parts.append(f"{local}[{idx}]")
        node = parent
    parts.reverse()
    return "/" + "/".join(parts)


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _file_sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            data = fh.read(chunk)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Core ingestor
# ---------------------------------------------------------------------------

class EPUBIngestor:
    """
    Orchestrates the full EPUB ingest pipeline for a single book.

    Parameters
    ----------
    epub_path:
        Absolute or relative path to the ``.epub`` source file.
    output_dir:
        Directory where ``segments.json``, ``state.json``, and ``epub_raw/``
        will be written.  Created automatically if it does not exist.
    book_slug:
        Machine-safe identifier for the book (e.g. ``"robbins-pathology"``).
        Stored in state and segment metadata.
    resume:
        If ``True`` (default), load an existing ``state.json`` and skip spine
        items that are already marked as processed.
    """

    SEGMENTS_FILE = "segments.json"
    STATE_FILE = "state.json"
    RAW_DIR = "epub_raw"

    def __init__(
        self,
        epub_path: str | Path,
        output_dir: str | Path,
        book_slug: str,
        *,
        resume: bool = True,
    ) -> None:
        self.epub_path = Path(epub_path).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.book_slug = book_slug
        self.resume = resume

        self._segments_path = self.output_dir / self.SEGMENTS_FILE
        self._state_path = self.output_dir / self.STATE_FILE
        self._raw_dir = self.output_dir / self.RAW_DIR

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> dict[str, Any]:
        """
        Execute the full ingest pipeline.

        Returns the final ``state`` dictionary.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        state = self._load_or_init_state()
        segments: list[dict[str, Any]] = self._load_existing_segments(state)

        if state.get("epub_raw_extracted") and self._raw_dir.exists():
            logger.info("epub_raw/ already extracted — skipping.")
        else:
            logger.info("Extracting EPUB container to epub_raw/ …")
            self._extract_raw()
            state["epub_raw_extracted"] = True
            self._save_state(state)

        book = self._open_epub()
        spine_items = self._ordered_spine_items(book)
        state["spine_total"] = len(spine_items)

        start_idx = state.get("spine_processed", 0)

        if start_idx >= len(spine_items):
            logger.info("All spine items already processed.")
        else:
            for abs_idx, item in enumerate(spine_items):
                if abs_idx < start_idx:
                    continue  # skip already-done items (resume)

                href = item.get_name()
                logger.info("Processing spine[%04d]: %s", abs_idx, href)

                new_segs = self._extract_segments_from_item(item, abs_idx)
                segments.extend(new_segs)

                state["spine_processed"] = abs_idx + 1
                state["last_processed_href"] = href
                state["segments_count"] = len(segments)

                # Persist after every spine document so resume works at
                # document granularity.
                self._save_segments(segments)
                self._save_state(state)

        state["completed_at"] = _now_iso()
        state["segments_count"] = len(segments)
        self._save_state(state)

        logger.info(
            "Ingest complete: %d segments from %d spine items.",
            len(segments),
            len(spine_items),
        )
        return state

    # ------------------------------------------------------------------
    # EPUB helpers
    # ------------------------------------------------------------------

    def _open_epub(self) -> epub.EpubBook:
        logger.debug("Opening EPUB: %s", self.epub_path)
        return epub.read_epub(str(self.epub_path), options={"ignore_ncx": True})

    @staticmethod
    def _ordered_spine_items(book: epub.EpubBook) -> list[epub.EpubHtml]:
        """
        Return the spine documents in canonical reading order.

        ebooklib's ``book.spine`` is a list of ``(idref, linear)`` tuples.
        We resolve each ``idref`` to an ``EpubHtml`` item, skipping any
        non-HTML items (e.g. nav-only NCX entries).
        """
        items: list[epub.EpubHtml] = []
        for idref, _linear in book.spine:
            item = book.get_item_with_id(idref)
            if item is None:
                logger.warning("Spine idref %r not found in manifest — skipping.", idref)
                continue
            if not isinstance(item, epub.EpubHtml):
                logger.debug("Spine item %r is not EpubHtml — skipping.", idref)
                continue
            items.append(item)
        return items

    # ------------------------------------------------------------------
    # Segment extraction
    # ------------------------------------------------------------------

    def _extract_segments_from_item(
        self,
        item: epub.EpubHtml,
        spine_idx: int,
    ) -> list[dict[str, Any]]:
        """
        Parse the XHTML content of *item* with lxml and return a list of
        segment dictionaries.
        """
        raw_bytes: bytes = item.get_body_content()
        if not raw_bytes:
            logger.debug("Spine[%04d] %s: empty body — skipping.", spine_idx, item.get_name())
            return []

        try:
            # Use an HTML-tolerant parser as a fallback when the document is
            # not well-formed XML (common in real-world EPUBs).
            try:
                root = etree.fromstring(raw_bytes)
            except etree.XMLSyntaxError:
                root = etree.fromstring(raw_bytes, parser=etree.HTMLParser())

        except etree.Error as exc:
            logger.warning(
                "Spine[%04d] %s: lxml parse error (%s) — skipping.",
                spine_idx, item.get_name(), exc,
            )
            return []

        # Try the XHTML-namespaced query first; fall back to no-namespace.
        elements = root.xpath(_XHTML_EXPR, namespaces=_NS)
        if not elements:
            elements = root.xpath(_NO_NS_EXPR)

        segments: list[dict[str, Any]] = []
        for elem_idx, element in enumerate(elements):
            text = _collect_text(element)
            if not text:
                continue  # skip empty or whitespace-only nodes

            segment_id = f"{spine_idx:04d}_{elem_idx:06d}"
            tag = etree.QName(element.tag).localname if isinstance(element.tag, str) else str(element.tag)

            seg: dict[str, Any] = {
                "segment_id": segment_id,
                "book_slug": self.book_slug,
                "spine_idx": spine_idx,
                "href": item.get_name(),
                "elem_idx": elem_idx,
                "tag": tag,
                "xpath": _positional_xpath(element),
                "text": text,
            }

            # Preserve a small set of semantically relevant attributes.
            relevant_attrs = {}
            for attr_name in ("id", "class", "epub:type", "role"):
                val = element.get(attr_name)
                if val:
                    relevant_attrs[attr_name] = val
            if relevant_attrs:
                seg["attrs"] = relevant_attrs

            segments.append(seg)

        return segments

    # ------------------------------------------------------------------
    # Raw EPUB extraction
    # ------------------------------------------------------------------

    def _extract_raw(self) -> None:
        """
        Unzip the EPUB container into ``epub_raw/``, preserving the internal
        directory layout (META-INF/, OEBPS/, OPF, NAV, etc.).
        """
        if self._raw_dir.exists():
            shutil.rmtree(self._raw_dir)
        self._raw_dir.mkdir(parents=True)

        with zipfile.ZipFile(self.epub_path, "r") as zf:
            zf.extractall(self._raw_dir)

        logger.debug("EPUB container extracted to: %s", self._raw_dir)

    # ------------------------------------------------------------------
    # State / segments persistence
    # ------------------------------------------------------------------

    def _load_or_init_state(self) -> dict[str, Any]:
        if self.resume and self._state_path.exists():
            with self._state_path.open(encoding="utf-8") as fh:
                state = json.load(fh)
            logger.info(
                "Resuming from state: %d/%d spine items processed.",
                state.get("spine_processed", 0),
                state.get("spine_total", 0),
            )
            return state

        return {
            "book_slug": self.book_slug,
            "epub_path": str(self.epub_path),
            "epub_sha256": _file_sha256(self.epub_path),
            "started_at": _now_iso(),
            "completed_at": None,
            "phase": "ingest",
            "spine_total": 0,
            "spine_processed": 0,
            "last_processed_href": None,
            "segments_count": 0,
            "epub_raw_extracted": False,
        }

    def _load_existing_segments(self, state: dict[str, Any]) -> list[dict[str, Any]]:
        if self.resume and self._segments_path.exists() and state.get("spine_processed", 0) > 0:
            with self._segments_path.open(encoding="utf-8") as fh:
                return json.load(fh)
        return []

    def _save_state(self, state: dict[str, Any]) -> None:
        tmp = self._state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self._state_path)

    def _save_segments(self, segments: list[dict[str, Any]]) -> None:
        tmp = self._segments_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self._segments_path)
