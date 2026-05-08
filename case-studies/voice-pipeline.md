# Case Study: Voice Note Pipeline

Turn a 30-second voice message into a completed task, summarized thread, or sent reply, without touching a keyboard.

---

## The Problem

Voice notes are fast to send but create async dead zones. You send a voice note at 7am. Your AI employee doesn't hear it. You get to your desk at 9am, the context is gone, and you're back to typing.

The same problem in the other direction: you want your agent to brief you verbally, not with a wall of text, because you're in the car, on a run, or away from a screen.

This case study documents the full round-trip pipeline:

- **Inbound:** voice note from Telegram → faster-whisper transcription → agent processing → structured output
- **Outbound:** agent response → ElevenLabs TTS → voice note sent back to Telegram

---

## Stack

| Component | Tool | Cost |
|-----------|------|------|
| Voice-to-text | faster-whisper (local, large-v3 model) | $0 |
| Agent | Hermes Agent + MiniMax M2.7 | ~$0.01/session |
| Text-to-voice | ElevenLabs API (v3, Callum voice) | ~$0.10/min of audio |
| Delivery | Telegram Bot API | $0 |

Total per round-trip (30s voice note in, 30s reply out): approximately $0.13.

---

## Architecture

```
[User] → Telegram voice note
 → Telegram webhook receives OGG file
 → faster-whisper transcribes → text
 → Hermes agent processes task
 → ElevenLabs generates MP3 reply
 → Telegram sends voice note back to user
[User] ← receives voice reply
```

Processing time: 8-15 seconds for a 30-second voice note (transcription 2s, LLM 4-8s, TTS 2-4s).

---

## Part 1: Inbound Voice Transcription

### Setup: faster-whisper

faster-whisper is a Python library that runs OpenAI's Whisper model locally, 4x faster than the original implementation.

```bash
pip install faster-whisper
# Download the large-v3 model on first use (downloads ~1.5 GB)
```

### Skill: voice-inbound

This skill is triggered when the agent receives a voice message via Telegram.

```python
# voice-transcribe.py
from faster_whisper import WhisperModel
import os

def transcribe(audio_path: str) -> str:
 """Transcribe an audio file using faster-whisper large-v3."""
 model = WhisperModel("large-v3", device="cpu", compute_type="int8")
 segments, info = model.transcribe(audio_path, beam_size=5)
 
 text = " ".join(segment.text.strip() for segment in segments)
 return text

if __name__ == "__main__":
 import sys
 result = transcribe(sys.argv[1])
 print(result)
```

Performance on Apple M2:
- 30-second voice note: ~2 seconds to transcribe
- 5-minute voice note: ~15 seconds to transcribe
- Accuracy: near-perfect for clear speech, very good with accents

### Handling the OGG format

Telegram delivers voice notes as `.ogg` (Opus codec). faster-whisper handles this natively, but if you need to convert:

```bash
ffmpeg -i input.ogg -ar 16000 -ac 1 output.wav
```

### SKILL.md frontmatter

```yaml
---
name: voice-inbound
description: Transcribe incoming voice notes (Telegram OGG, WhatsApp m4a, or any audio file) using faster-whisper locally. Returns clean text ready for agent processing. Triggers on attachment of type voice/audio.
version: 1.0.0
prerequisites:
 env_vars: []
 python_packages: [faster-whisper]
 commands: [python3]
---
```

---

## Part 2: Agent Processing

Once transcribed, the text is processed as a normal message. The transcription is injected with a context header so the agent knows it came from a voice note:

```
[VOICE NOTE TRANSCRIPTION]
<transcribed text here>

Note: This was a voice message. Respond conversationally and concisely, the reply will be sent as a voice note.
```

The "respond conversationally" hint matters. Without it, the agent responds in its default style (markdown, bullets, headers) which sounds terrible when read aloud.

### Prompt pattern for voice-appropriate responses

Add this to your SOUL.md under a "Voice Mode" section:

```
## Voice Mode
When responding to a voice note (messages prefixed with [VOICE NOTE TRANSCRIPTION]):
- Keep response under 100 words unless the task demands more
- No markdown, no bullet points, no headers
- Write as spoken sentences
- Summarize complex answers rather than exhausting detail
- End with a clear action or conclusion
```

---

## Part 3: Outbound Voice Reply

### ElevenLabs setup

```bash
pip install elevenlabs
```

```python
# voice-reply.py
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import os

def generate_voice_reply(text: str, output_path: str = "/tmp/reply.mp3") -> str:
 """Generate a voice reply using ElevenLabs v3 API."""
 client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
 
 audio = client.generate(
 text=text,
 voice="Callum", # or your preferred voice ID
 model="eleven_turbo_v2_5",
 voice_settings=VoiceSettings(
 stability=0.3, # lower = more expressive
 similarity_boost=0.75,
 style=0.4,
 use_speaker_boost=True
 )
 )
 
 with open(output_path, "wb") as f:
 for chunk in audio:
 f.write(chunk)
 
 return output_path
```

### Voice selection notes

The voice you choose shapes the personality of the agent significantly. Tested voices for professional assistant use:

| Voice | Style | Best for |
|-------|-------|----------|
| Callum | Warm, clear, slightly energetic | General assistant |
| Daniel | Deep, authoritative | Business/finance tasks |
| Rachel | Friendly, approachable | Customer-facing |
| Adam | Neutral, reliable | Technical/factual reports |

Use `eleven_turbo_v2_5` model for the fastest generation. Use `eleven_v3` for highest quality (slower, higher cost).

### Sending back via Telegram

The Telegram Bot API accepts voice notes as MP3 or OGG files:

```bash
curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendVoice" \
 -F "chat_id=$CHAT_ID" \
 -F "voice=@/tmp/reply.mp3" \
 -F "caption=Voice reply"
```

In Hermes, the voice-inbound skill can trigger the voice-outbound skill automatically when the reply text is ready. The agent handles the round-trip without manual intervention.

---

## Complete Round-Trip Flow

```bash
# Step 1: Telegram webhook delivers OGG file to agent
# Step 2: Agent detects voice attachment, routes to voice-inbound skill

python3 voice-transcribe.py /tmp/voice_note.ogg
# → "Can you check if I have anything on Thursday afternoon and block 2 hours for deep work?"

# Step 3: Agent processes the request against Google Calendar skill

# Step 4: Agent generates text response
# → "Thursday afternoon is free after 3pm. I've blocked 3pm to 5pm as deep work. No conflicts."

# Step 5: Agent generates voice reply
python3 voice-reply.py "Thursday afternoon is free after 3pm. I've blocked 3pm to 5pm as deep work. No conflicts."

# Step 6: Agent sends voice note back via Telegram
```

---

## Real-World Results

From the Weblyfe production deployment (6 months of use):

- Average round-trip time: 12 seconds
- Tasks completed via voice in a typical week: 15-25 (calendar blocks, email drafts, research queries)
- Time saved vs switching to a keyboard: estimated 3-5 minutes per voice interaction for tasks done on the go
- Transcription accuracy: 97%+ for English, 94%+ for mixed English/Dutch

The highest-value use case turned out to be commute tasks: recording voice notes about client conversations on the drive home, having them summarized and added to the relevant Notion page before arriving.

---

## Skill Installation

```bash
cp -r skills/knowledge/faster-whisper ~/.hermes/skills/
```

Configure your ElevenLabs key:
```bash
echo "ELEVENLABS_API_KEY=your-key-here" >> .env.secrets
```

The voice ID for Callum is `N2lVS1w4EtoT3dr4eOWO`. To find other voice IDs, visit elevenlabs.io/voice-library.
