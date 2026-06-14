# ops

Skills for infrastructure management, DevOps workflows, Git operations, and system administration. Use these when your Appie needs to manage servers, automate deployments, handle GitHub operations, or maintain fleet health.

Prerequisite tools: `gh` CLI for GitHub skills, SSH access for remote management, Tailscale for fleet networking, `git` for all git-* skills.

## Skills

| Skill | Description | Required env | Compat |
|-------|-------------|-------------|--------|
| [ashp](ashp/) | ASHP (Appie Shell Protocol): standardized shell command execution and logging | - | Hermes |
| [clawdcursor](clawdcursor/) | Desktop AI agent: control any app via GUI. Screenshots, clicks, forms, cross-app workflows | macOS | OpenClaw |
| [clawhub](clawhub/) | OpenClaw hub management: register, update, and manage skill hubs | - | OpenClaw |
| [clawlist](clawlist/) | List and search installed OpenClaw skills and their metadata | - | OpenClaw |
| [coding](coding/) | Code quality guidelines: immutability, small files, error handling, security patterns | - | Both |
| [agent-fleet-operations](agent-fleet-operations/) | Hermes/Appie fleet provisioning, reachability gates, provider recovery, and refresh workflow | SSH, Tailscale | Hermes |
| [client-bot-security](client-bot-security/) | Audit and harden client Telegram bot deployments, token storage, SSH keys, and lifecycle controls | SSH | Hermes/OpenClaw |
| [digital-ocean](digital-ocean/) | Manage DigitalOcean droplets, domains, and infrastructure via DO API | DO_API_TOKEN | Both |
| [eightctl](eightctl/) | Eightfold infrastructure control: manage resources and deployments | - | Both |
| [fleet-skill-sync](fleet-skill-sync/) | Pull, dedupe, curate, and distribute skills across the Appie fleet | SSH, Tailscale | Hermes/OpenClaw |
| [git-sync](git-sync/) | Two-way git sync for workspace files: push local changes, pull remote updates | GIT_REMOTE | Both |
| [gitclaw](gitclaw/) | Automated workspace backup to GitHub via crontab. Self-install, conflict resolution | GITHUB_TOKEN | Both |
| [github](github/) | GitHub operations via gh CLI: issues, PRs, CI runs, code review, API queries | GH_TOKEN | Both |
| [github-auth](github-auth/) | GitHub authentication: device flow, token management, org access | GH_TOKEN | Both |
| [github-code-review](github-code-review/) | Automated GitHub PR code review with structured feedback | GH_TOKEN | Both |
| [github-issues](github-issues/) | GitHub Issues management: create, label, assign, close, search | GH_TOKEN | Both |
| [github-pr-workflow](github-pr-workflow/) | Full GitHub PR lifecycle: branch, commit, PR, review, merge | GH_TOKEN | Both |
| [github-repo-management](github-repo-management/) | GitHub repo operations: create, configure, archive, manage settings | GH_TOKEN | Both |
| [tmux](tmux/) | tmux session management: create, attach, send commands, manage windows | - | Both |

## Install

```bash
cp -r skills/ops/<skill> ~/.hermes/skills/
# or for OpenClaw:
cp -r skills/ops/<skill> ~/.openclaw/skills/
```
