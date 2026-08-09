# CLOUD.md - Cloud agent voice runtime

## Default TTS

Cloud-running Hermes agents use Fish Audio S2.1 Pro Free through OpenRouter as their default text-to-speech engine.

- Model: `fish-audio/s2.1-pro-free:free`
- Endpoint: `https://openrouter.ai/api/v1/audio/speech`
- Hermes provider: `fish-audio` via the supported custom command-provider interface
- Credential: the agent's own `OPENROUTER_API_KEY` in its active Hermes `.env`
- Output: MP3 from Fish Audio, converted by Hermes or the channel bridge to Ogg/Opus where native voice notes require it
- Emotion: preserve Fish S2.1 cues such as `[warm]`, `[excited]`, or `[calm and reassuring]` in the input text

Never copy an operator's OpenRouter credential to a customer or another agent. If a node has no key, configure the provider but report the credential block instead of borrowing one.

Kokoro is retired for fleet and client-bot TTS. Do not install, download, prewarm, or start Kokoro models. Dedicated application routes that explicitly use ElevenLabs, including locked WAI voice identities, remain separate and are not rewritten by this default.

The free Fish endpoint is an external service with no uptime guarantee. A production tenant may override `FISH_AUDIO_MODEL` with a paid Fish model while keeping the same command layer.
