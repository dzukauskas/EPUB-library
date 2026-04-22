"""
medtranslate CLI entry point.

Usage
-----
    medtranslate ingest --epub path/to/book.epub \\
                        --out  books/my-book/source \\
                        --slug my-book

    medtranslate ingest --help
"""

from __future__ import annotations

import argparse
import logging
import sys


def _cmd_ingest(args: argparse.Namespace) -> int:
    from medtranslate.epub_ingest.extractor import EPUBIngestor

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s  %(name)s  %(message)s",
    )

    ingestor = EPUBIngestor(
        epub_path=args.epub,
        output_dir=args.out,
        book_slug=args.slug,
        resume=not args.no_resume,
    )
    state = ingestor.run()
    print(f"Done. {state['segments_count']} segments written to {args.out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="medtranslate",
        description="Lithuanian medical EPUB translation pipeline CLI.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- ingest sub-command --------------------------------------------------
    ingest_p = sub.add_parser(
        "ingest",
        help="Parse an EPUB and extract text segments.",
    )
    ingest_p.add_argument(
        "--epub", required=True, metavar="PATH",
        help="Path to the source .epub file.",
    )
    ingest_p.add_argument(
        "--out", required=True, metavar="DIR",
        help="Output directory for segments.json, state.json, epub_raw/.",
    )
    ingest_p.add_argument(
        "--slug", required=True, metavar="SLUG",
        help="Machine-safe book identifier (e.g. robbins-pathology).",
    )
    ingest_p.add_argument(
        "--no-resume", action="store_true",
        help="Ignore existing state.json and start fresh.",
    )
    ingest_p.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable DEBUG-level logging.",
    )
    ingest_p.set_defaults(func=_cmd_ingest)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
