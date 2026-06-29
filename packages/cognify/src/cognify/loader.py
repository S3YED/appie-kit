"""
Document loader + heading-aware chunker — the Extract step.

Turns a file (md/txt/pdf) or raw string into stable ~512-token chunks.
"""
from __future__ import annotations

from . import config  # noqa: F401  (imports set DYLD on macOS before pypdf)

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

CHUNK_CHARS = 2048
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
    source: str
    chunks: tuple[Chunk, ...]


def _doc_id(source: str, text: str) -> str:
    return hashlib.sha256((source + "::" + text[:512]).encode()).hexdigest()[:16]


def read_file(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        return "\n\n".join((pg.extract_text() or "") for pg in PdfReader(str(p)).pages)
    return p.read_text(errors="replace")


def _strip_frontmatter(text: str) -> str:
    m = _FRONTMATTER_RE.match(text)
    return text[m.end():] if m else text


def _split_segments(text: str) -> list[tuple[str, str]]:
    segs, last, heading = [], 0, ""
    for m in _HEADING_RE.finditer(text):
        body = text[last:m.start()].strip()
        if body:
            segs.append((heading, body))
        heading, last = m.group(2).strip(), m.end()
    tail = text[last:].strip()
    if tail:
        segs.append((heading, tail))
    return segs or [("", text.strip())]


def _subchunk(text: str) -> list[str]:
    if len(text) <= CHUNK_CHARS:
        return [text]
    out, start = [], 0
    while start < len(text):
        end = start + CHUNK_CHARS
        if end >= len(text):
            out.append(text[start:])
            break
        snap = text.rfind(". ", start, end)
        snap = end if (snap == -1 or snap < start + CHUNK_CHARS // 2) else snap + 2
        out.append(text[start:snap])
        start = max(start + 1, snap - OVERLAP_CHARS)
    return out


def chunk_text(text: str, *, source: str = "inline", title: Optional[str] = None) -> Document:
    text = _strip_frontmatter(text or "")
    doc_id = _doc_id(source, text)
    if not title:
        title = Path(source).stem if source != "inline" else (text[:60].strip() or "untitled")
    chunks, ordinal = [], 0
    for heading, body in _split_segments(text):
        for piece in _subchunk(body):
            piece = piece.strip()
            if len(piece) < MIN_CHUNK_CHARS:
                continue
            chunks.append(Chunk(id=f"{doc_id}_{ordinal}", doc_id=doc_id, ord=ordinal,
                                heading=heading, text=piece))
            ordinal += 1
    return Document(id=doc_id, title=title, source=source, chunks=tuple(chunks))


def load(path_or_text: str, *, is_path: Optional[bool] = None, title: Optional[str] = None) -> Document:
    if is_path is None:
        is_path = (len(path_or_text) < 1024 and "\n" not in path_or_text
                   and Path(path_or_text).exists())
    if is_path:
        return chunk_text(read_file(path_or_text), source=path_or_text, title=title)
    return chunk_text(path_or_text, source="inline", title=title)
