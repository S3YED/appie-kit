# automation

Skills for agent self-management, workflow orchestration, and inter-agent coordination. Use these when you need your Appie to manage its own runtime, sync context across fleet nodes, or delegate work to sub-agents.

Prerequisite tools: Hermes Agent or OpenClaw installed, tmux for persistent sessions, `git` for brain-sync.

## Skills

| Skill | Description | Required env | Compat |
|-------|-------------|-------------|--------|
| [agentic-video-tools](agentic-video-tools/) | Compare and integrate agentic video editing APIs (Vizard, Submagic, Descript). Automation-first ranking | - | Both |
| [brain-sync](brain-sync/) | Sync agent memory and context files across fleet nodes via rsync + git | GIT_REMOTE | Hermes |
| [coding-agent](coding-agent/) | Spawn a focused coding sub-agent for isolated implementation tasks | - | Both |
| [fleet-dream](fleet-dream/) | Nightly consolidation: compress daily notes, update long-term memory, prune stale context | - | Hermes |
| [hermes-agent](hermes-agent/) | Configure, extend, and contribute to Hermes Agent. Setup, profiles, skill authoring, gateway | - | Hermes |
| [hermes-agent-skill-authoring](hermes-agent-skill-authoring/) | Write, test, and publish Hermes skills. Frontmatter spec, SKILL.md format, validation | - | Hermes |
| [hermes-dream-skill](hermes-dream-skill/) | Dream-cycle skill: self-reflection and memory consolidation at end of session | - | Hermes |
| [project-context-sync](project-context-sync/) | Sync project context files (SOUL.md, IDENTITY.md, MEMORY.md) to remote fleet hosts | SSH_KEY | Hermes |

## Install

```bash
cp -r skills/automation/<skill> ~/.hermes/skills/
# or for OpenClaw:
cp -r skills/automation/<skill> ~/.openclaw/skills/
```
