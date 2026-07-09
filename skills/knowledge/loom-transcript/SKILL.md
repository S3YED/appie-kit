---
name: loom-transcript
description: Fetch the FULL transcript from any Loom share link and turn it into clean markdown, ready to ingest into a knowledge base. Use when given a loom.com/share/... URL and asked to get its transcript, notes, or text.
---

# Loom transcript fetch

Loom's transcript file sits behind a SIGNED CloudFront URL, so the plain
`cdn.loom.com/.../transcription/<id>.json` returns "Missing Key-Pair-Id". The
trick: render the share page in a real browser, capture the signed transcription
request from the network log, then fetch the full transcript JSON from it.

## Use it

```bash
./loom-to-kb.sh "https://www.loom.com/share/<32-hex-id>" [output-dir]
```

Prints the path to a clean `.md` (title + Loom's auto-summary + chapters + the
FULL transcript). Default output dir: `~/clawd/knowledge/loom-transcripts`.

## How it works (if you need to adapt it)

1. `agent-browser network requests --clear` then `agent-browser open <url>` — the
   browser fetches the signed transcript on load.
2. `agent-browser network requests --filter transcription` → grab the signed
   `https://cdn.loom.com/mediametadata/transcription/<id>-N.json?Policy=...&Signature=...` URL.
3. `curl` that signed URL → JSON with `phrases[]`, each `{ts, value}`. Join the
   `value` fields (NOT `text` — that key is empty) for the full transcript.
4. Title from `agent-browser eval "document.title"`. Summary/chapters from
   `agent-browser read`.

## Dependencies

- `agent-browser` (fleet default browser CLI) — required.
- `python3`, `curl`.

## Then ingest into a KB

```bash
# fleet shared KB (our own knowledge):
curl -s http://127.0.0.1:8765/cognify/ingest -H 'content-type: application/json' \
  -d "{\"tenant\":\"fleet\",\"namespace\":\"loom-calls\",\"title\":\"<title>\",\"text\":\"<md>\"}"
# a client bot's isolated memory: cognify --tenant <client> ingest <file.md>
```

Gotcha: signed URLs are time-limited (~minutes) — fetch immediately after capture.
Loom's transcript panel is virtualized, so reading the DOM only gets a partial;
always use the signed-URL path for the full transcript.
