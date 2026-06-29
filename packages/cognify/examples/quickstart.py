"""Ingest a sample doc and run a hybrid recall. Run after ./setup.sh + .env."""
import json
from pathlib import Path

import cognify

be = cognify.get_backend("local")  # zero external services
doc = Path(__file__).parent / "sample_docs" / "acme.md"

r = cognify.ingest(be, str(doc), tenant="demo", namespace="docs")
print("ingested:", json.dumps(r.__dict__))

res = cognify.recall(be, "what does Pathfinder run on and who owns it?", tenant="demo")
print("\nchunks:")
for c in res.chunks:
    print(f"  {c['score']:.3f}  {c['text'][:70]}")
print("\nentities:", [f"{e['name']} ({e['etype']})" for e in res.entities])
print("relations:", [f"{x['subject']} -{x['predicate']}-> {x['object']}" for x in res.relations])
be.close()
