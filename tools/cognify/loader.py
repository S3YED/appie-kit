#!/usr/bin/env python3
"""
Document loader + heading-aware chunker for the Cognify ECL pipeline.

Handles the "Extract" stage: turn a file path or raw text into a clean list of
~512-token chunks with stable ids. Supports .md / .txt / .pdf (pypdf) and raw
strings. Mirrors the chunking strategy of the existing knowledge indexer so the
two stay consistent, but is standalone (no import of the non-package indexer).

Immutable: every function returns new values; nothing is mutated in place.
"""
from __future__ import annotations

# pypdf -> xml.parsers.expat needs Homebrew's expat on this Mac (DYLD), and macOS
# strips DYLD_* from inherited env, so set it before any heavy import.
import os
os.environ.setdefault("DYLD_LIBRARY_PATH", "/opt/homebrew/opt/expat/lib:/opt/homebrew/lib")

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

CHUNK_CHARS = 2048        # ~512 tokens
OVERLAP_CHARS = 256
MIN_CHUNK_CHARS = 40

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class Chunk:
    id: str
    doc_id: str
    ord: int
    heading: str
    text: str


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    source: str          # original path or "inline"
    chunks: tuple[Chunk, ...]


def _doc_id(source: str, text: str) -> str:
    h = hashlib.sha256((source + "::" + text[:512]).encode()).hexdigest()
    return h[:16]


def read_file(path: str) -> str:
    """Read a document file into plain text. Supports md/txt/pdf."""
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(str(p))
        return "\n\n".join((page.extract_text() or "") for page in reader.pages)
    return p.read_text(errors="replace")


def _strip_frontmatter(text: str) -> str:
    m = _FRONTMATTER_RE.match(text)
    return text[m.end():] if m else text


def _split_segments(text: str) -> list[tuple[str, str]]:
    """Split on markdown headings into (heading, body) segments."""
    segments: list[tuple[str, str]] = []
    last_end = 0
    heading = ""
    for m in _HEADING_RE.finditer(text):
        body = text[last_end:m.start()].strip()
        if body:
            segments.append((heading, body))
        heading = m.group(2).strip()
        last_end = m.end()
    tail = text[last_end:].strip()
    if tail:
        segments.append((heading, tail))
    if not segments:
        segments = [("", text.strip())]
    return segments


def _subchunk(text: str) -> list[str]:
    """Window a long segment into overlapping ~CHUNK_CHARS pieces, snapping to
    sentence boundaries where possible."""
    if len(text) <= CHUNK_CHARS:
        return [text]
    out: list[str] = []
    start = 0
    while start < len(text):
        end = start + CHUNK_CHARS
        if end >= len(text):
            out.append(text[start:])
            break
        snap = text.rfind(". ", start, end)
        if snap == -1 or snap < start + CHUNK_CHARS // 2:
            snap = end
        else:
            snap += 2
        out.append(text[start:snap])
        start = max(start + 1, snap - OVERLAP_CHARS)
    return out


def chunk_text(text: str, *, source: str = "inline", title: Optional[str] = None) -> Document:
    """Turn raw text into a Document with heading-aware chunks."""
    text = _strip_frontmatter(text or "")
    doc_id = _doc_id(source, text)
    if not title:
        title = Path(source).stem if source != "inline" else (text[:60].strip() or "untitled")

    chunks: list[Chunk] = []
    ordinal = 0
    for heading, body in _split_segments(text):
        for piece in _subchunk(body):
            piece = piece.strip()
            if len(piece) < MIN_CHUNK_CHARS:
                continue
            cid = f"{doc_id}_{ordinal}"
            chunks.append(Chunk(id=cid, doc_id=doc_id, ord=ordinal, heading=heading, text=piece))
            ordinal += 1

    return Document(id=doc_id, title=title, source=source, chunks=tuple(chunks))


def load(path_or_text: str, *, is_path: Optional[bool] = None, title: Optional[str] = None) -> Document:
    """Load a Document from a file path or a raw string.

    is_path: force interpretation. If None, auto-detect (a short string that
    exists on disk is treated as a path)."""
    if is_path is None:
        is_path = len(path_or_text) < 1024 and "\n" not in path_or_text and Path(path_or_text).exists()
    if is_path:
        text = read_file(path_or_text)
        return chunk_text(text, source=path_or_text, title=title)
    return chunk_text(path_or_text, source="inline", title=title)


if __name__ == "__main__":
    import sys, json
    doc = load(sys.argv[1] if len(sys.argv) > 1 else "Hello world. " * 50)
    print(json.dumps({"id": doc.id, "title": doc.title, "n_chunks": len(doc.chunks)}, indent=2))
