# meta

Skills about the skill system itself and agent self-improvement. Use these when you're building new skills, testing skill behavior, or running the agent in dogfood mode to evaluate its own capabilities.

Prerequisite tools: none beyond the base Hermes or OpenClaw install.

## Skills

| Skill | Description | Required env | Compat |
|-------|-------------|-------------|--------|
| [brainstorming](brainstorming/) | Structured ideation protocol: diverge, converge, prioritize, refine | - | Both |
| [dogfood](dogfood/) | Run the agent against itself to test skill behavior and surface edge cases | - | Both |

## Install

```bash
cp -r skills/meta/<skill> ~/.hermes/skills/
# or for OpenClaw:
cp -r skills/meta/<skill> ~/.openclaw/skills/
```
