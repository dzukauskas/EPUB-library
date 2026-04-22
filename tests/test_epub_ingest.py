"""
tests/test_epub_ingest.py

Smoke tests for the EPUB ingest pipeline.

The tests build a minimal synthetic EPUB in memory (without writing a real
.epub file that requires a full validation toolchain) and verify that:
- segments are extracted with deterministic IDs;
- state.json is written with the correct shape;
- epub_raw/ is populated with the expected container structure.
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from medtranslate.epub_ingest.extractor import EPUBIngestor, _collect_text, _positional_xpath

# ---------------------------------------------------------------------------
# Helpers — build a minimal synthetic EPUB on disk
# ---------------------------------------------------------------------------

MINIMAL_CONTAINER = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

MINIMAL_OPF = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">urn:uuid:test-book-001</dc:identifier>
    <dc:title>Test Book</dc:title>
    <dc:language>en</dc:language>
  </metadata>
  <manifest>
    <item id="ch01" href="ch01.xhtml" media-type="application/xhtml+xml"/>
    <item id="ch02" href="ch02.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="ch01"/>
    <itemref idref="ch02"/>
  </spine>
</package>
"""

CH01 = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Chapter 1</title></head>
<body>
  <h1>Introduction</h1>
  <p>First paragraph of chapter one.</p>
  <p>Second paragraph of chapter one.</p>
</body>
</html>
"""

CH02 = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Chapter 2</title></head>
<body>
  <h1>Methods</h1>
  <p>Only paragraph of chapter two.</p>
</body>
</html>
"""


def _make_epub(path: Path) -> None:
    """Write a minimal valid EPUB 3 archive to *path*."""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("mimetype", "application/epub+zip")
        zf.writestr("META-INF/container.xml", MINIMAL_CONTAINER)
        zf.writestr("OEBPS/content.opf", MINIMAL_OPF)
        zf.writestr("OEBPS/ch01.xhtml", CH01)
        zf.writestr("OEBPS/ch02.xhtml", CH02)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def epub_file(tmp_path: Path) -> Path:
    p = tmp_path / "test_book.epub"
    _make_epub(p)
    return p


@pytest.fixture()
def output_dir(tmp_path: Path) -> Path:
    d = tmp_path / "out"
    d.mkdir()
    return d


# ---------------------------------------------------------------------------
# Unit tests — pure helpers
# ---------------------------------------------------------------------------

class TestCollectText:
    def test_simple_element(self):
        from lxml import etree
        el = etree.fromstring(b"<p>Hello <em>world</em>.</p>")
        assert _collect_text(el) == "Hello world ."

    def test_empty_element(self):
        from lxml import etree
        el = etree.fromstring(b"<p>   </p>")
        assert _collect_text(el) == ""


# ---------------------------------------------------------------------------
# Integration tests — EPUBIngestor
# ---------------------------------------------------------------------------

class TestEPUBIngestor:
    def test_run_creates_segments_json(self, epub_file, output_dir):
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book")
        ingestor.run()
        assert (output_dir / "segments.json").exists()

    def test_run_creates_state_json(self, epub_file, output_dir):
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book")
        ingestor.run()
        assert (output_dir / "state.json").exists()

    def test_run_creates_epub_raw(self, epub_file, output_dir):
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book")
        ingestor.run()
        raw = output_dir / "epub_raw"
        assert raw.is_dir()
        assert (raw / "META-INF" / "container.xml").exists()
        assert (raw / "OEBPS" / "content.opf").exists()
        assert (raw / "OEBPS" / "ch01.xhtml").exists()
        assert (raw / "OEBPS" / "ch02.xhtml").exists()

    def test_segments_have_deterministic_ids(self, epub_file, output_dir):
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book")
        ingestor.run()
        segs = json.loads((output_dir / "segments.json").read_text())
        ids = [s["segment_id"] for s in segs]
        # IDs must be unique.
        assert len(ids) == len(set(ids))
        # IDs must follow the pattern SSSS_EEEEEE.
        import re
        pattern = re.compile(r"^\d{4}_\d{6}$")
        for sid in ids:
            assert pattern.match(sid), f"Unexpected segment_id format: {sid!r}"

    def test_segments_count_matches_state(self, epub_file, output_dir):
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book")
        ingestor.run()
        segs = json.loads((output_dir / "segments.json").read_text())
        state = json.loads((output_dir / "state.json").read_text())
        assert state["segments_count"] == len(segs)

    def test_state_spine_fully_processed(self, epub_file, output_dir):
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book")
        ingestor.run()
        state = json.loads((output_dir / "state.json").read_text())
        assert state["spine_total"] == state["spine_processed"]
        assert state["completed_at"] is not None

    def test_state_book_slug(self, epub_file, output_dir):
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book")
        ingestor.run()
        state = json.loads((output_dir / "state.json").read_text())
        assert state["book_slug"] == "test-book"

    def test_each_segment_has_required_keys(self, epub_file, output_dir):
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book")
        ingestor.run()
        segs = json.loads((output_dir / "segments.json").read_text())
        required = {"segment_id", "book_slug", "spine_idx", "href", "elem_idx", "tag", "xpath", "text"}
        for seg in segs:
            missing = required - seg.keys()
            assert not missing, f"Segment {seg['segment_id']} missing keys: {missing}"

    def test_segment_text_non_empty(self, epub_file, output_dir):
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book")
        ingestor.run()
        segs = json.loads((output_dir / "segments.json").read_text())
        for seg in segs:
            assert seg["text"].strip(), f"Empty text in segment {seg['segment_id']}"

    def test_resume_does_not_duplicate_segments(self, epub_file, output_dir):
        """Running the ingestor twice with resume=True must not duplicate segments."""
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book", resume=True)
        ingestor.run()
        first_count = len(json.loads((output_dir / "segments.json").read_text()))

        ingestor2 = EPUBIngestor(epub_file, output_dir, book_slug="test-book", resume=True)
        ingestor2.run()
        second_count = len(json.loads((output_dir / "segments.json").read_text()))

        assert first_count == second_count

    def test_no_resume_resets(self, epub_file, output_dir):
        """Running with resume=False must produce the same result as a fresh run."""
        EPUBIngestor(epub_file, output_dir, book_slug="test-book", resume=False).run()
        c1 = len(json.loads((output_dir / "segments.json").read_text()))
        EPUBIngestor(epub_file, output_dir, book_slug="test-book", resume=False).run()
        c2 = len(json.loads((output_dir / "segments.json").read_text()))
        assert c1 == c2

    def test_known_text_in_segments(self, epub_file, output_dir):
        ingestor = EPUBIngestor(epub_file, output_dir, book_slug="test-book")
        ingestor.run()
        segs = json.loads((output_dir / "segments.json").read_text())
        texts = [s["text"] for s in segs]
        assert any("Introduction" in t for t in texts)
        assert any("First paragraph" in t for t in texts)
        assert any("Methods" in t for t in texts)
