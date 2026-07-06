---
name: whisper-transcription
description: Speech-to-text workflows using Whisper locally or via the OpenAI transcription API. Use when transcribing audio, choosing a Whisper runtime, or producing text, SRT, or JSON transcripts.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [whisper, transcription, speech-to-text, audio, subtitles]
    related_skills: [whisper]
---

# Whisper Transcription

## Overview
Use this umbrella for audio transcription tasks regardless of whether the runtime is local Whisper or the OpenAI API.

## Choose a Path
- **Local CLI:** when you want offline transcription and already have the Whisper binary.
- **OpenAI API:** when you want hosted transcription, JSON output, or proxy-compatible API access.

## Workflow
1. Identify the source audio format and desired output (txt, srt, json).
2. Pick local or API based on latency, privacy, and environment constraints.
3. Set model/language/prompt hints only when they improve the transcript.
4. Verify the transcript against the audio length and obvious speaker names.

## References
- `references/path-selection.md` for runtime choice and output-format notes.

## Pitfalls
- Don’t keep separate skills for local and API Whisper when the task class is identical.
- Don’t overfit model choice; prefer the simplest path that meets quality needs.
- Don’t forget to specify output format and destination.
