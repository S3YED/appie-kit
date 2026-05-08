# Appie Kit - Skill Discovery

155 public skills, 8 categories. Sourced from a live 7-agent fleet running Hermes Agent and OpenClaw.

Each skill is a directory with a `SKILL.md` file. Drop any skill folder into `~/.hermes/skills/` or `~/.openclaw/skills/` and it is immediately available in your next session.

---

## Categories

### automation (19 skills)
Agent self-management, fleet coordination, workflow orchestration, and inter-agent dispatch.

[Browse automation skills](skills/automation/INDEX.md) | [Readme](skills/automation/README.md)

Highlights: `clawflow`, `kanban-orchestrator`, `dispatch-multiple-agents`, `brain-sync`, `memory-search`, `coding-agent`

---

### communication (6 skills)
Messaging platform integrations: Telegram, Discord, Slack, iMessage, WhatsApp, voice calls.

[Browse communication skills](skills/communication/INDEX.md) | [Readme](skills/communication/README.md)

Highlights: `discord`, `slack`, `bluebubbles` (iMessage), `wacli` (WhatsApp), `voice-call`

---

### content (49 skills)
UI/UX design, image generation, video production, SEO, copywriting, Next.js, TTS, and more. The largest creative category.

[Browse content skills](skills/content/INDEX.md) | [Readme](skills/content/README.md)

Highlights: `frontend-design-3`, `ui-ux-pro-max`, `tips-landing-pages`, `design`, `nextjs-expert`, `video-editing-pro`, `seo-checklist`, `stable-diffusion`, `comfyui`, `sherpa-onnx-tts`

---

### integrations (31 skills)
Third-party service integrations: Airtable, Notion, Google Workspace, GitHub, n8n, fal.ai, Spotify, Webflow, Trello, and more.

[Browse integrations skills](skills/integrations/INDEX.md) | [Readme](skills/integrations/README.md)

Highlights: `exa-plus`, `n8n`, `n8n-pro`, `github`, `gog`, `google-drive`, `airtable`, `notion-masterclass`, `fal-ai`, `webflow`, `spotify`

---

### knowledge (22 skills)
LLM fine-tuning (LoRA, GRPO, DPO), quantization (GGUF, llama.cpp), vLLM inference, Whisper STT, DSPy, AudioCraft, and model evaluation.

[Browse knowledge skills](skills/knowledge/INDEX.md) | [Readme](skills/knowledge/README.md)

Highlights: `vllm`, `unsloth`, `axolotl`, `llama-cpp`, `gguf`, `whisper`, `dspy`, `audiocraft`, `lm-evaluation-harness`

---

### meta (8 skills)
Skills about the skill system itself: authoring, registry, planning, QA, and brainstorming.

[Browse meta skills](skills/meta/INDEX.md) | [Readme](skills/meta/README.md)

Highlights: `skill-creator`, `hermes-agent-skill-authoring`, `clawhub`, `clawlist`, `brainstorming`, `dogfood`

---

### ops (16 skills)
Infrastructure management, DevOps, git workflows, tmux, 1Password, fleet health, and system administration.

[Browse ops skills](skills/ops/INDEX.md) | [Readme](skills/ops/README.md)

Highlights: `digital-ocean`, `gitclaw`, `healthcheck`, `tmux`, `1password`, `git-sync`, `appie-self-maintenance`

---

### personal (4 skills)
Personal productivity and lifestyle integrations (primarily macOS).

[Browse personal skills](skills/personal/INDEX.md) | [Readme](skills/personal/README.md)

Highlights: `bear-notes`, `things-mac`, `spotify-player`, `weather`

---

## Master Index

Full skill listing with descriptions: [skills/INDEX.md](skills/INDEX.md)

---

## Installing Skills

```bash
# Copy a single skill (Hermes Agent)
cp -r skills/content/design ~/.hermes/skills/

# Copy an entire category
cp -r skills/knowledge/* ~/.hermes/skills/

# Or use the installer to copy everything
./install.sh /path/to/your/workspace
```

Hermes Agent loads skills from `~/.hermes/skills/` at session start.
OpenClaw loads skills from `~/.openclaw/skills/`.

No restart required if you copy skills while the agent is idle; they are picked up at the start of the next conversation.

---

## Adding a Skill

See [CONTRIBUTING.md](CONTRIBUTING.md) for the SKILL.md frontmatter spec and category guidelines.
