---
name: srt-subtitles
description: Parse, search, and process .srt (SubRip) subtitle files. SRT is plain text — blokken gescheiden door lege regels, timestamps in HH:MM:SS,mmm formaat. Parser en zoekfunctie in scripts/parse-srt.py.
related_skills:
  - drive-knowledge-ingestion
---

## File format

```
1
00:00:01,500 --> 00:00:04,000
This is the subtitle text
                             ← lege regel
2
00:00:05,000 --> 00:00:08,500
Line one
Line two                      ← meerdere regels toegestaan
```

- Sequentiële nummers (1, 2, 3...)
- Timestamps: `HH:MM:SS,mmm --> HH:MM:SS,mmm`
- Tekst: plain text, kan `<i>`, `<b>`, `<font>` HTML-tags bevatten
- Blokken gescheiden door lege regel (`\n\n`)

## How to read

SRT is plain text — no converter needed.

```bash
# From Drive
gog drive download <FILE_ID> --out /tmp/sub.srt && cat /tmp/sub.srt

# Local file
cat file.srt
read_file path="file.srt"
```

## Parsed output (script)

```bash
cat file.srt | python3 scripts/parse-srt.py
```

Returns JSON array:
```json
[
  {"seq": 1, "start": "00:00:01,500", "end": "00:00:04,000", "text": "Hello"},
  {"seq": 2, "start": "00:00:05,000", "end": "00:00:08,500", "text": "Line one\\nLine two"}
]
```

## Use cases

- Extract text from video subtitles for search/indexing
- Translate subtitles (feed parsed text to LLM)
- Repurpose subtitle text for content
- Transcript extraction from video content in Drive