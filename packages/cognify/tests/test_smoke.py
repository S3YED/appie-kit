"""Smoke tests. The local-backend e2e is skipped unless an LLM key is set
(it makes one cheap API call per chunk)."""
import os

import cognify
from cognify.loader import load
from cognify.extractor import Extraction, _parse


def test_chunking():
    doc = load("# A\n" + "word " * 800 + "\n# B\nshort tail here for a second segment.",
               is_path=False, title="t")
    assert doc.chunks and all(c.text for c in doc.chunks)
    assert len({c.id for c in doc.chunks}) == len(doc.chunks)  # unique ids


def test_extraction_parse():
    ex = _parse('{"entities":[{"name":"Clark","type":"Product"},{"name":"Neo4j","type":"Technology"}],'
                '"relations":[{"subject":"Clark","predicate":"USES","object":"Neo4j"}]}')
    assert isinstance(ex, Extraction)
    assert {e.name for e in ex.entities} == {"Clark", "Neo4j"}
    assert ex.relations[0].predicate == "USES"


def test_parse_drops_ungrounded_relations():
    ex = _parse('{"entities":[{"name":"Clark","type":"Product"}],'
                '"relations":[{"subject":"Clark","predicate":"USES","object":"Ghost"}]}')
    assert ex.relations == ()  # object not in entities -> dropped


def test_local_e2e():
    if not (os.environ.get("COGNIFY_LLM_KEY") or os.environ.get("OPENROUTER_API_KEY")):
        import pytest
        pytest.skip("no LLM key set")
    import tempfile
    os.environ["COGNIFY_DATA_DIR"] = tempfile.mkdtemp()
    be = cognify.get_backend("local")
    r = cognify.ingest(be, "Clark uses Neo4j and TurboVec for memory.",
                       is_path=False, tenant="t", namespace="n")
    assert r.chunks == 1
    res = cognify.recall(be, "what does Clark use?", tenant="t")
    assert res.chunks
    be.close()
