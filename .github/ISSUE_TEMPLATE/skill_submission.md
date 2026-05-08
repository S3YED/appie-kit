---
name: Skill submission
about: Submit a new skill for review and inclusion in the kit
title: "[SKILL] skill-name"
labels: skill-submission
assignees: ''
---

## Skill summary

- **Name:** (hyphen-case, matches `name` in SKILL.md frontmatter)
- **Category:** (automation / communication / content / integrations / knowledge / meta / ops / personal)
- **Description:** One sentence: what it does and when to use it.

## What it does

Describe the skill's behavior in 2-5 sentences. Include what APIs or tools it uses.

## Checklist

- [ ] SKILL.md has valid YAML frontmatter (`name`, `description`, `version`)
- [ ] All required env vars are listed in `prerequisites.env_vars`
- [ ] At least one usage example in the skill body
- [ ] No hardcoded secrets, personal data, or internal hostnames
- [ ] Supporting scripts (if any) have tests in a `tests/` subfolder
- [ ] Tested on Hermes Agent and/or OpenClaw
- [ ] PR is against the `master` branch

## Agent compatibility

- [ ] Hermes Agent
- [ ] OpenClaw
- [ ] Other: ___

## Notes for reviewers

Anything the reviewer should know: known limitations, edge cases handled, APIs it won't work with, etc.
