---
name: cognitive-memory
description: Implementation and troubleshooting of the Cognitive Memory (Cognify) system in Hermes Agent.
version: 1.0.0
---

# Cognitive Memory (Cognify)

The Cognitive Memory system (PR #727, codenamed "Cognify") provides Hermes Agent with semantic recall, auto-encoding, contradiction detection, and exponential forgetting.

## Architecture

- `cognitive_memory/`: Core logic (store, embeddings, recall, encoding, extraction).
- `tools/cognitive_memory_tool.py`: Agent-facing `cognitive_recall` tool.
- Database: `~/.hermes/cognitive_memory.db` (SQLite).

## Setup & Configuration

Enable in `~/.hermes/config.yaml`:

```yaml
cognitive_memory:
  enabled: true
  embedding:
    model: "text-embedding-3-small"
```

## Known Issues & Workarounds

### Dependency: litellm
Cognify depends on `litellm`. On macOS systems with Homebrew Python, you may encounter `pyexpat` errors related to `Symbol not found: _XML_SetAllocTrackerActivationThreshold`.

**Fix:**
```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib
python3.13 -m pip install litellm --break-system-packages
```

### Manual Installation (from PR branch)
If the system is not yet merged, files must be extracted from the `cognitive-memory` branch:
1. `git fetch origin pull/727/head:cognitive-memory`
2. `git show cognitive-memory:path/to/file > path/to/file`
3. Tools must be registered in `tools/registry.py` (standard auto-discovery usually handles this if `cognitive_memory_tool.py` is in the `tools/` dir).

## Tool usage: cognitive_recall

- `action='store', content='...'`: Saves to semantic memory.
- `action='recall', query='...'`: Retrieves by meaning.
- `action='forget', query='...'`: Deletes matching items.
- `action='status'`: Shows database stats.
