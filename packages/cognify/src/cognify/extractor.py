"""
LLM entity + relation extractor — the Cognify step.

Asks a cheap LLM to pull TYPED entities (Person, Project, Technology, ...) and
TYPED relations (WORKS_AT, USES, ...) out of a chunk of text, so the graph
carries real meaning rather than just "these two look similar".

OpenAI-compatible: point COGNIFY_LLM_BASE at OpenRouter, OpenAI, a local vLLM,
Ollama, anything that speaks /chat/completions.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict

import requests

from . import config

ENTITY_TYPES = (
    "Person", "Organization", "Project", "Product", "Technology",
    "Location", "Concept", "Event", "Document", "Metric",
)

_SYSTEM = (
    "You extract a knowledge graph from text. Return STRICT JSON only, no prose. "
    "Schema: {\"entities\":[{\"name\":str,\"type\":one-of " + "|".join(ENTITY_TYPES) + "}],"
    "\"relations\":[{\"subject\":str,\"predicate\":UPPER_SNAKE_verb,\"object\":str}]}. "
    "Rules: canonical entity names (no pronouns/articles), deduplicate, predicates "
    "are short verbs like WORKS_AT/USES/BUILT/OWNS/PART_OF/LOCATED_IN/DEPENDS_ON/"
    "PRODUCES. Only relations whose subject AND object both appear in entities. "
    "If nothing meaningful, return empty arrays."
)
_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


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
        return {"entities": [asdict(e) for e in self.entities],
                "relations": [asdict(r) for r in self.relations]}


def _parse(content: str) -> Extraction:
    if not content:
        return Extraction()
    m = _JSON_RE.search(content)
    try:
        data = json.loads(m.group(0) if m else content)
    except json.JSONDecodeError:
        return Extraction()

    valid = set(ENTITY_TYPES)
    seen_e, ents = set(), []
    for e in data.get("entities", []) or []:
        name = str(e.get("name", "")).strip()
        if not name or name.lower() in seen_e:
            continue
        etype = str(e.get("type", "Concept")).strip()
        seen_e.add(name.lower())
        ents.append(Entity(name=name, type=etype if etype in valid else "Concept"))

    names = {e.name.lower() for e in ents}
    seen_r, rels = set(), []
    for r in data.get("relations", []) or []:
        subj = str(r.get("subject", "")).strip()
        pred = str(r.get("predicate", "")).strip().upper().replace(" ", "_")
        obj = str(r.get("object", "")).strip()
        if not (subj and pred and obj):
            continue
        if subj.lower() not in names or obj.lower() not in names:
            continue
        key = (subj.lower(), pred, obj.lower())
        if key in seen_r:
            continue
        seen_r.add(key)
        rels.append(Relation(subject=subj, predicate=pred, object=obj))
    return Extraction(entities=tuple(ents), relations=tuple(rels))


def _call_openai(text: str, key: str, timeout: int) -> str:
    """Any OpenAI-compatible /chat/completions endpoint (OpenRouter, OpenAI, vLLM, Ollama)."""
    payload = {
        "model": config.LLM_MODEL,
        "messages": [{"role": "system", "content": _SYSTEM},
                     {"role": "user", "content": text[:6000]}],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    url = f"{config.LLM_BASE}/chat/completions"
    resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
    if resp.status_code == 400:  # some models reject response_format
        payload.pop("response_format", None)
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _call_anthropic(text: str, key: str, timeout: int) -> str:
    """Native Anthropic (Claude) messages API."""
    payload = {
        "model": config.ANTHROPIC_MODEL,
        "max_tokens": 1024,
        "temperature": 0,
        "system": _SYSTEM + " Respond with ONLY the JSON object.",
        "messages": [{"role": "user", "content": text[:6000]}],
    }
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    resp = requests.post(f"{config.ANTHROPIC_BASE}/v1/messages", json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    blocks = resp.json().get("content", [])
    return "".join(b.get("text", "") for b in blocks if b.get("type") == "text")


def extract(text: str, *, timeout: int = 60) -> Extraction:
    """Extract a typed entity/relation graph from one chunk. Works with Claude
    (provider=anthropic) or any OpenAI-compatible endpoint (provider=openai).
    Raises on transport errors so the caller can degrade; empty on bad JSON."""
    text = (text or "").strip()
    if len(text) < 40:
        return Extraction()
    key = config.llm_key()
    if not key:
        raise RuntimeError("No LLM key (set COGNIFY_LLM_KEY, ANTHROPIC_API_KEY, or OPENROUTER_API_KEY)")
    if config.LLM_PROVIDER == "anthropic":
        content = _call_anthropic(text, key, timeout)
    else:
        content = _call_openai(text, key, timeout)
    return _parse(content)
