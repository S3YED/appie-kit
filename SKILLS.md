# Appie Kit - Skill Discovery

557 public skills, 9 categories. Sourced from a sanitized agent-fleet library plus imported ECC engineering/agentic-ops skills.

Each skill is a directory with a `SKILL.md` file. Drop any skill folder into `~/.hermes/skills/` or `~/.openclaw/skills/` and it is available in your next session.

---

## Categories

### automation (27 skills)
Agent self-management, workflow orchestration, browser automation, coding agents, and inter-agent coordination.

[Browse automation skills](skills/automation/INDEX.md) | [Readme](skills/automation/README.md)

Highlights: `clawflow`, `kanban-orchestrator`, `brain-sync`, `memory-search`, `coding-agent`, `web-scraping-javascript-sites`

---

### communication (7 skills)
Messaging, email, voice, and chat-platform integrations.

[Browse communication skills](skills/communication/INDEX.md) | [Readme](skills/communication/README.md)

Highlights: `discord`, `bluebubbles`, `himalaya`, `wacli`, `voice-call`

---

### content (65 skills)
Design, frontend, media, SEO, copywriting, image/video/audio generation, and creative workflows.

[Browse content skills](skills/content/INDEX.md) | [Readme](skills/content/README.md)

Highlights: `frontend-design`, `ui-ux-pro-max`, `higgsfield-generate`, `higgsfield-product-photoshoot`, `viral-shorts-course`, `video-editing-pro`, `web-design-pipeline`, `seo-checklist`

---

### ecc (250 skills)
Imported ECC engineering and agentic-ops skills: language/framework patterns, testing, security, agents, and ops.

[Browse ecc skills](skills/ecc/INDEX.md) | [Readme](skills/ecc/README.md)

Highlights: `agent-harness-construction`, `autonomous-loops`, `continuous-learning-v2`, `cost-aware-llm-pipeline`, `api-design`, `browser-qa`, `security-review`, `tdd-workflow`

---

### integrations (109 skills)
Third-party service integrations: Google Workspace, Notion, GitHub, n8n, fal.ai, Webflow, Spotify, Trello, and more.

[Browse integrations skills](skills/integrations/INDEX.md) | [Readme](skills/integrations/README.md)

Highlights: `exa-plus`, `n8n`, `github`, `gog`, `airtable`, `notion-masterclass`, `fal-ai`, `webflow`, `spotify`, `spark-comfy`

---

### knowledge (33 skills)
Model, ML, research, fine-tuning, quantization, inference, evaluation, and technical reference skills.

[Browse knowledge skills](skills/knowledge/INDEX.md) | [Readme](skills/knowledge/README.md)

Highlights: `serving-llms-vllm`, `unsloth`, `axolotl`, `llama-cpp`, `gguf-quantization`, `whisper`, `dspy`

---

### meta (11 skills)
Skills about skills: authoring, planning, QA, dogfooding, and agent workflow meta-processes.

[Browse meta skills](skills/meta/INDEX.md) | [Readme](skills/meta/README.md)

Highlights: `skill-creator`, `hermes-agent-skill-authoring`, `clawhub`, `clawlist`, `brainstorming`, `dogfood`

---

### ops (30 skills)
Infrastructure, DevOps, git, fleet operations, security hardening, deployment, and maintenance.

[Browse ops skills](skills/ops/INDEX.md) | [Readme](skills/ops/README.md)

Highlights: `agent-fleet-operations`, `fleet-skill-sync`, `fleet-infra-fixes`, `client-bot-security`, `digital-ocean`, `gitclaw`, `healthcheck`, `tmux`, `1password`

---

### personal (25 skills)
Personal productivity, smart-home, lifestyle, and macOS-centered helper skills.

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

No restart required if you copy skills while the agent is idle. They are picked up at the start of the next conversation.

---

## Adding a Skill

See [CONTRIBUTING.md](CONTRIBUTING.md) for the SKILL.md frontmatter spec and category guidelines.
