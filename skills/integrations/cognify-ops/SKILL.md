---
name: cognify-ops
description: Operating patterns for Cognify knowledge graph ingestion — model selection, key sourcing, batch strategy, Drive/Typeform extraction, and priority source ranking for the ramzy tenant.
---

# Cognify operations (ingestion patterns)

## Model selection (CRITICAL)
Default to `openai/gpt-4o-mini` for entity extraction. DeepSeek V4 Flash hangs on
multi-chunk documents. gpt-4o-mini completes the same document in 25-40s.

Set: `COGNIFY_LLM_MODEL=openai/gpt-4o-mini` in `/root/cognify/.env`

## Key sourcing
Cognify's `.env` key goes stale. When extraction fails with "No LLM key", source the
working key from Hermes' env. **Use Python to write `.env`, never shell heredocs** —
special chars in API keys cause silent corruption.

```python
import subprocess
r = subprocess.run(["grep", "-v", "^#", "/root/.hermes/.env"], capture_output=True, text=True)
for line in r.stdout.split('\n'):
    if 'OPENROUTER_API_KEY' in line and '=' in line:
        key = line.split('=', 1)[1].strip().strip('"').strip("'")
        with open("/root/cognify/.env", "w") as f:
            f.write(f"OPENROUTER_API_KEY={key}\n")
            f.write("COGNIFY_LLM_BASE=https://openrouter.ai/api/v1\n")
            f.write("COGNIFY_LLM_MODEL=openai/gpt-4o-mini\n")
            f.write("COGNIFY_LLM_KEYENV=OPENROUTER_API_KEY\n")
            f.write("COGNIFY_BACKEND=local\n")
            f.write("COGNIFY_EXTRACT_WORKERS=4\n")
        break
```

## Batch ingestion strategy
Combine many small files into batches before ingesting. Use `ingest-dir` with workers:

```bash
cd /root/cognify && set -a && . ./.env && set +a && export COGNIFY_DATA_DIR=/root/.cognify
./.venv/bin/cognify --tenant ramzy ingest-dir /path/to/dir --workers 4
```

Performance (gpt-4o-mini, 4 workers): ~17K chars/25s, ~35K chars/38s, ~42K chars/42s.

## Google Drive transcript extraction
`gws drive files export` returns 401 even when `gws drive files list` works.
Workaround: direct Drive API with access token from `~/.config/gws/tokens.json`.

Refresh expired tokens: `python3 /root/.hermes/scripts/refresh_google_token.py`

## Typeform response extraction
Contact blocks have nested sub-fields. Recursively parse form definition for ref→label map
before extracting response answers. See `references/typeform-extraction.md`.

## Priority sources for KG (ramzy tenant)
1. Giveaway Notes — lead profiles with pain points, blocks, plays
2. Call transcripts (Gemini notes in Google Drive) — conversation data, closes
3. Typeform responses (form `N4LbJCHT`) — structured lead intake
4. Testimonials (`~/ibrahim-lowticket/*.txt`) — client stories for voice
5. Funnel blueprint, VSL scripts, roster — business strategy===ME:memory/cognify-ops