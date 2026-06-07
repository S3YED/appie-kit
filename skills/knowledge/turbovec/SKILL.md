---
name: turbovec
description: Local vector search with turbovec (Google TurboQuant, Rust+Python). Use for embeddings indexing, semantic search, local RAG, or filtered vector retrieval without external services like Pinecone.
---

# turbovec — local vector index

Rust vector index on Google's TurboQuant quantizer. 10M float32 docs (31GB) fit in ~4GB. Faster than FAISS. No train step: add vectors, they are indexed. Fully local — nothing leaves the machine.

## Installation (v0.7.0)

```bash
pip install turbovec==0.7.0
```

Create a dedicated venv and install there; do not pip-install into a system Python.

## API (v0.7.0 — differs from upstream README)

```python
import numpy as np
from turbovec import TurboQuantIndex

idx = TurboQuantIndex(dim=1536, bit_width=4)
idx.add(vecs)                      # 2D float32, C-contiguous: np.ascontiguousarray(x.astype(np.float32))

scores, ids = idx.search(q, k=10)  # q must be 2D (batch): vecs[7:8], not vecs[7]
                                   # returns 2D arrays (one row per query)

mask = np.zeros(len(idx), dtype=bool)   # filtered search: bool mask over slots
mask[allowed_slots] = True
scores, ids = idx.search(q, k=10, mask=mask)

idx.write("index.tq")              # persistence round-trips exactly
idx = TurboQuantIndex.load("index.tq")
```

Gotchas:
- Queries MUST be 2D; a 1D vector raises `TypeError: 'ndarray' object cannot be cast as 'ndarray'`.
- `mask` is a bool array of length `len(idx)` (slot-based), not an id allowlist. The README's `IdMapIndex.add_with_ids`/`allowlist=` API is newer than the 0.7.0 wheel.
- `bit_width=4` is the standard memory/recall tradeoff; pair with any local embedding model for an air-gapped RAG stack.

## When to use
- Semantic search over local corpora (memory, knowledge base, transcripts)
- RAG retrieval where privacy/latency matters (no Pinecone round-trip)
- Hybrid retrieval: narrow candidates with SQL/BM25 first, then dense rerank via `mask`
