---
name: semantic-recall
description: Semantic (vector) memory recall for Clark. Finds facts by MEANING, not just keywords — use when the lexical memory (holographic FTS) misses paraphrases or synonyms, or when you want the most conceptually-relevant stored facts about a topic (owner, projects, tokens, tools, business). Complements the built-in memory; does not replace it.
tools: Bash
origin: weblyfe
---

# semantic-recall: Vector Memory Layer

Clark's holographic memory is lexical (FTS5 + Jaccard token overlap + SHA-256 hash HRR). It misses synonyms and paraphrases. This skill adds a real learned-embedding semantic layer (fastembed BAAI/bge-small-en-v1.5, ONNX, no torch) over the same `memory_store.db` facts.

## When to use
- A recall by exact words returned nothing useful but the concept is likely stored.
- You want the top conceptually-similar facts about a person, project, credential, or tool.

## Recall a query

```bash
/usr/local/lib/hermes-agent/venv/bin/python /root/.hermes/semantic/semantic.py recall "<your natural-language query>" 5
```

Returns JSON: `[{fact_id, score, category, content}, ...]` ranked by semantic similarity (higher score = closer).

## Re-index after new memories (normally the cron does this every 6h)

```bash
/usr/local/lib/hermes-agent/venv/bin/python /root/.hermes/semantic/semantic.py index
```

Incremental: only embeds new/changed facts, prunes deleted ones. Output JSON: `{indexed, deleted, total_facts}`.

## Stats / health

```bash
/usr/local/lib/hermes-agent/venv/bin/python /root/.hermes/semantic/semantic.py stats
```
