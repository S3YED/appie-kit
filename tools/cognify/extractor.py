#!/usr/bin/env python3
"""
LLM entity + relation extractor for the Cognify ECL pipeline.

This is the piece our giga-graph was missing: instead of only linking chunks by
semantic similarity, we ask a cheap LLM to pull TYPED entities (Person, Project,
Technology, ...) and TYPED relations (WORKS_AT, USES, ...) out of each chunk, so
the resulting Neo4j graph carries real meaning, not just "these two look alike".

Token discipline: routes to the cheapest competent tier. Default is OpenRouter
(configurable model), but the base URL + model are env-overridable so a caller
can point it at Spark Atlas (free local Qwen) or any OpenAI-compatible endpoint.

Env:
  COGNIFY_LLM_BASE   default https://openrouter.ai/api/v1
  COGNIFY_LLM_MODEL  default google/gemini-2.0-flash-001
  COGNIFY_LLM_KEY    falls back to OPENROUTER_API_KEY
  COGNIFY_LLM_KEYENV name of the env var holding the key (default OPENROUTER_API_KEY)

Everything here is pure-function and immutable: extract() returns a new
Extraction dataclass, never mutates its inputs.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field, asdict
from typing import Optional

import requests

# Controlled vocabulary keeps the graph queryable. The LLM is told to map every
# entity onto one of these and every relation onto an UPPER_SNAKE predicate.
ENTITY_TYPES = (
    "Person", "Organization", "Project", "Product", "Technology",
    "Location", "Concept", "Event", "Document", "Metric",
)

_DEF_BASE = "https://openrouter.ai/api/v1"
# Cheapest competent model confirmed available on this OpenRouter account that
# also honours response_format json_object. Override via COGNIFY_LLM_MODEL.
_DEF_MODEL = "openai/gpt-4o-mini"

_SYSTEM = (
    "You extract a knowledge graph from text. Return STRICT JSON only, no prose. "
    "Schema: {\"entities\":[{\"name\":str,\"type\":one-of " + "|".join(ENTITY_TYPES) + "}],"
    "\"relations\":[{\"subject\":str,\"predicate\":UPPER_SNAKE_verb,\"object\":str}]}. "
    "Rules: entity names are canonical (no pronouns, no articles), deduplicate, "
    "predicates are short verbs like WORKS_AT/USES/BUILT/OWNS/PART_OF/LOCATED_IN/"
    "DEPENDS_ON/PRODUCES/MENTIONS. Only relations whose subject AND object both "
    "appear in entities. If nothing meaningful, return empty arrays."
)


@dataclass(frozen=True)
class Entity:
    name: str
    type: str


@dataclass(frozen=True)
class Relation:
    subject: str
    predicate: str
    object: str


@dataclass(frozen=True)
class Extraction:
    entities: tuple[Entity, ...] = ()
    relations: tuple[Relation, ...] = ()

    def to_dict(self) -> dict:
        return {
            "entities": [asdict(e) for e in self.entities],
            "relations": [asdict(r) for r in self.relations],
        }


def _key() -> Optional[str]:
    if os.environ.get("COGNIFY_LLM_KEY"):
        return os.environ["COGNIFY_LLM_KEY"]
    keyenv = os.environ.get("COGNIFY_LLM_KEYENV", "OPENROUTER_API_KEY")
    if os.environ.get(keyenv):
        return os.environ[keyenv]
    # Fall back to the secrets file used fleet-wide.
    secrets = os.path.expanduser("~/.weblyfe-secrets/.env")
    if os.path.exists(secrets):
        want = keyenv
        with open(secrets) as f:
            for line in f:
                line = line.strip()
                if line.startswith("export "):
                    line = line[len("export "):]
                if line.startswith(want + "="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse(content: str) -> Extraction:
    """Pull the first JSON object out of the model response and validate it."""
    if not content:
        return Extraction()
    m = _JSON_RE.search(content)
    raw = m.group(0) if m else content
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return Extraction()

    valid_types = set(ENTITY_TYPES)
    seen_e: set[str] = set()
    ents: list[Entity] = []
    for e in data.get("entities", []) or []:
        name = str(e.get("name", "")).strip()
        etype = str(e.get("type", "Concept")).strip()
        if not name:
            continue
        if etype not in valid_types:
            etype = "Concept"
        k = name.lower()
        if k in seen_e:
            continue
        seen_e.add(k)
        ents.append(Entity(name=name, type=etype))

    names = {e.name.lower() for e in ents}
    seen_r: set[tuple] = set()
    rels: list[Relation] = []
    for r in data.get("relations", []) or []:
        subj = str(r.get("subject", "")).strip()
        pred = str(r.get("predicate", "")).strip().upper().replace(" ", "_")
        obj = str(r.get("object", "")).strip()
        if not (subj and pred and obj):
            continue
        # Keep only relations grounded in extracted entities.
        if subj.lower() not in names or obj.lower() not in names:
            continue
        key = (subj.lower(), pred, obj.lower())
        if key in seen_r:
            continue
        seen_r.add(key)
        rels.append(Relation(subject=subj, predicate=pred, object=obj))

    return Extraction(entities=tuple(ents), relations=tuple(rels))


def extract(text: str, *, timeout: int = 60) -> Extraction:
    """Extract a typed entity/relation graph from one chunk of text.

    Returns an empty Extraction on any failure (network, auth, bad JSON) so the
    pipeline degrades to "chunks + semantic edges" rather than crashing. Failures
    are surfaced via the raised-and-caught path in core, never silently lost.
    """
    text = (text or "").strip()
    if len(text) < 40:
        return Extraction()

    base = os.environ.get("COGNIFY_LLM_BASE", _DEF_BASE).rstrip("/")
    model = os.environ.get("COGNIFY_LLM_MODEL", _DEF_MODEL)
    key = _key()
    if not key:
        raise RuntimeError("No LLM key found (set COGNIFY_LLM_KEY or OPENROUTER_API_KEY)")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": text[:6000]},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    resp = requests.post(f"{base}/chat/completions", json=payload, headers=headers, timeout=timeout)
    if resp.status_code == 400:
        # Some models reject response_format; retry without it.
        payload.pop("response_format", None)
        resp = requests.post(f"{base}/chat/completions", json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    return _parse(content)


if __name__ == "__main__":
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else (
        "Seyed runs Weblyfe and built Clark, an AI back-office agent that uses "
        "Neo4j and TurboVec for memory. Clark is deployed on Orgo cloud boxes."
    )
    ex = extract(sample)
    print(json.dumps(ex.to_dict(), indent=2))
