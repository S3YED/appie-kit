# Contributing to Appie Kit

Thank you for contributing. This guide covers how to add skills, follow code style, and submit pull requests.

---

## How to Add a Skill

Each skill is a directory inside the appropriate category under `skills/`. The directory must contain a `SKILL.md` file.

### Directory structure

```
skills/<category>/<skill-name>/
    SKILL.md            # Required: skill definition
    README.md           # Optional: extended docs
    *.sh / *.py / *.js  # Optional: helper scripts
```

### SKILL.md frontmatter spec

Every SKILL.md must start with a YAML frontmatter block:

```markdown
---
name: my-skill-name
description: "One sentence: what this skill does and when to invoke it."
version: 1.0.0
category: content
prerequisites:
  env_vars:
    - MY_API_KEY
  tools:
    - curl
  platforms:
    - any         # or: macos, linux, hermes, openclaw
metadata:
  hermes:
    tags: [search, research, web]
---

# My Skill Name

Short intro paragraph. What it is, what problem it solves.

## When to use this skill

- Specific trigger condition 1
- Specific trigger condition 2

## Usage

Describe invocation patterns, arguments, and expected outputs.

## Prerequisites

List any setup steps beyond what's in the frontmatter.
```

Required frontmatter fields:
- `name`: matches the directory name, lowercase, hyphen-separated
- `description`: one sentence, starts with a verb ("Search...", "Generate...", "Manage...")
- `version`: semver starting at 1.0.0
- `category`: one of automation, communication, content, integrations, knowledge, meta, ops, personal

Optional but recommended:
- `prerequisites.env_vars`: list of required environment variable names
- `prerequisites.tools`: CLI tools that must be installed
- `prerequisites.platforms`: platform restrictions if any
- `metadata.hermes.tags`: searchable tags for the ClawHub registry

### Choosing a category

| Category | What belongs here |
|---|---|
| automation | Agent self-management, workflow orchestration, fleet coordination |
| communication | Messaging platforms, bots, notifications |
| content | Design, media generation, SEO, copywriting, frontend |
| integrations | Third-party APIs, SaaS connectors, platform SDKs |
| knowledge | Research, search, web scraping, ML/fine-tuning |
| meta | Skill authoring, planning, agent self-evaluation |
| ops | Infrastructure, DevOps, git, system administration |
| personal | Productivity apps, lifestyle integrations (mostly macOS) |

If a skill clearly belongs to two categories, pick the primary use case.

---

## How to Test a Skill

1. Copy your skill directory to your agent's skills folder:
   ```bash
   cp -r skills/<category>/<skill-name>/ ~/.hermes/skills/
   ```

2. Start a fresh Hermes session and verify the skill loads without errors:
   ```bash
   hermes start
   ```

3. Invoke the skill and confirm it behaves as documented.

4. Run the security scan to verify no secrets are included:
   ```bash
   ./tools/security-scan.sh
   ```

---

## Code Style

This kit follows these principles for any helper scripts bundled with skills:

- Small files, high cohesion. Extract utilities rather than growing a single file.
- No mutation. Functions return new values; they don't modify inputs in place.
- Comprehensive error handling. Check return codes. Fail fast with clear messages. Never swallow errors silently.
- No hardcoded secrets. API keys, tokens, and credentials belong in environment variables.
- Validate inputs at boundaries. Never trust user input or API responses without validation.

For shell scripts:
- Always `set -e` at the top.
- Quote all variables: `"$VARNAME"`.
- Use `#!/usr/bin/env bash` not `#!/bin/bash` for portability.

For Python helpers:
- Target Python 3.10+.
- Use type hints.
- Handle exceptions explicitly; no bare `except:`.

---

## PR Template

When opening a pull request, include:

```
## What

Brief description of what this PR adds or changes.

## Why

The problem it solves or the use case it enables.

## Skills added / changed

- `skills/<category>/<name>`: one-line description

## Testing

- [ ] SKILL.md frontmatter validates (name, description, version, category present)
- [ ] Skill loads in Hermes Agent without errors
- [ ] Skill loads in OpenClaw without errors (if applicable)
- [ ] security-scan.sh passes (no secrets committed)
- [ ] No em-dashes (--) used in skill content

## Notes

Any caveats, known limitations, or follow-up work.
```

---

## Reporting Bugs

Open an issue at [github.com/S3YED/appie-kit/issues](https://github.com/S3YED/appie-kit/issues).

Include:
- Your agent framework and version (Hermes / OpenClaw)
- The skill name and category
- What you expected vs. what happened
- Relevant error output (sanitize any API keys before pasting)

---

## Questions

- GitHub Issues: [github.com/S3YED/appie-kit/issues](https://github.com/S3YED/appie-kit/issues)
- Guide and community: [weblyfe.ai/store](https://weblyfe.ai/store)
