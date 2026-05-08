# Appie Kit FAQ

Answers to the questions buyers and evaluators ask most. If your question isn't here, open a GitHub issue or post in the community.

---

## Setup and Installation

**What do I need before I start?**

Three things: an OpenRouter API key (free to create at openrouter.ai), a Telegram bot token (create one via @BotFather in Telegram), and either Hermes Agent or OpenClaw installed on your machine. You do not need to run a server, the agent runs locally.

**Which operating systems are supported?**

macOS and Linux (Ubuntu, Debian, Fedora, and equivalents). Windows via WSL2 works but is not officially tested. Apple Silicon (M1 - M4) works well; see the Hardware section below for notes.

**Can I run this on a VPS or cloud server?**

Yes. Any Linux VPS with 1+ GB RAM works for the base setup. Run `tools/setup-openclaw-vps.sh` for an automated install. For GPU-dependent skills (image/video generation), you need either a local GPU or API access to fal.ai / RunPod.

**The install script fails. What do I check?**

Common causes in order of frequency:
1. Node.js is missing or below v18. Run `node -v` to check.
2. Python 3.9+ not found. Run `python3 --version`.
3. Permissions issue on the workspace directory. Run `chmod 755 /path/to/workspace`.
4. OpenRouter key is invalid. Test with: `curl https://openrouter.ai/api/v1/models -H "Authorization: Bearer YOUR_KEY"`.

**I get "gateway already running" on startup. What now?**

The gateway process from a previous session is still alive. Run `tools/safe-gateway-restart.sh` to cleanly stop and restart it. If that fails, find the PID with `pgrep -f openclaw` or `pgrep -f hermes` and kill it manually.

**Do I need a GPU?**

No. The agent itself runs entirely on CPU. GPU is only relevant for local LLM inference (optional via Ollama) or local image generation (optional via ComfyUI). Most users rely on API-based models, no GPU needed.

---

## Skills

**How do I install a skill?**

Copy the skill folder into your agent's skills directory:

```bash
# Hermes Agent
cp -r skills/content/ui-ux-pro-max ~/.hermes/skills/

# OpenClaw
cp -r skills/content/ui-ux-pro-max ~/.openclaw/skills/
```

Restart the agent (or reload skills with `hermes skills reload`) for the skill to activate.

**How do I write my own skill?**

A skill is a folder containing a `SKILL.md` file with a YAML frontmatter block and a description of what the agent should do. See `skills/meta/skill-authoring/SKILL.md` for the full spec, and `case-studies/skill-development-tdd.md` for a complete walkthrough with examples.

Minimum frontmatter:
```yaml
---
name: my-skill
description: What this skill does and when to use it.
version: 1.0.0
---
```

**Can I sell my own skills?**

Yes. Skills you write are yours. The MIT license on this kit applies to the kit itself, not to skills you create separately. If you bundle and sell a skill pack, no royalties are owed.

**Do skills work with agents other than Hermes and OpenClaw?**

Skills are plain Markdown files. Any agent that reads a system prompt or context file can use them. The YAML frontmatter is consumed by Hermes and OpenClaw for auto-discovery; other agents can ignore it and treat the file as a plain prompt. Many skills in this kit work with Claude Code, Cursor, Windsurf, and Aider with minimal adaptation.

**How do I know which skills are active?**

In Hermes: `hermes skills list`. In OpenClaw: check the `skills/` directory in your workspace and look at gateway logs for skill load confirmations.

**Can I run all 155 skills at once?**

You can install them all, but loading too many into a single context window degrades performance. The recommended pattern is Just-In-Time loading: install all skills, let the agent load only the skills relevant to the current task. AGENTS.md in the workspace/ templates covers this.

---

## Models and Cost

**Is MiniMax M2.7 really $0.01 per 1M tokens?**

The listed price on OpenRouter is approximately $0.01/1M input and $0.03/1M output as of Q2 2026. Prices can change. Check openrouter.ai/models for current pricing before committing to a budget.

**What does a typical month cost for a solo user?**

A solo founder doing email triage, calendar management, and occasional content generation typically spends $5-15/month at MiniMax M2.7 pricing. Heavy content production (daily social posts, video scripts) runs $30-60/month. Compare to $200-400/month for Claude Opus at similar volume.

**Can I run a local model with Ollama?**

Yes. Set your OpenRouter base URL override to your Ollama endpoint, or configure the model directly in your agent config. Recommended local models: Llama 3.1 70B (good reasoning), Mistral 7B (fast, lightweight tasks), or Qwen 2.5 32B (best quality/speed balance if you have the VRAM). Quality will be lower than MiniMax M2.7 on complex tasks.

**What is the difference between Hermes Agent and OpenClaw?**

Hermes Agent is a newer, lighter runtime with better multi-agent support and an active community. OpenClaw is an older runtime with a broader plugin ecosystem including voice calls and some macOS-native integrations. The Appie Kit v4.4 runs on both. Hermes is recommended for new installs.

**What is a good Claude Opus alternative for cost-sensitive setups?**

For coding and reasoning tasks: MiniMax M2.7 at 1/350th the cost with similar quality. For vision tasks: Gemini 1.5 Pro via OpenRouter. For tasks where Claude's safety alignment matters: Claude Haiku (10x cheaper than Opus) handles most day-to-day tasks. Opus is worth it for one-off high-stakes reasoning; it's not worth running 24/7 as the default.

**Will my agent always use the most expensive model?**

Only if you configure it that way. The recommended setup uses MiniMax M2.7 as the default and escalates to stronger models only for specific skills (e.g., code review, complex analysis). See TOOLS.md in the workspace templates for the recommended model fallback chain.

---

## Privacy and Security

**Where do my API keys live?**

In `.env.secrets` at the root of your workspace, chmod 600. The file is `.gitignore`-listed. Keys are never sent anywhere except to the API endpoints you configure. Run `tools/security-scan.sh` at any time to verify no keys are exposed in logs or config files.

**Can I run completely offline?**

With a local Ollama model: yes. The agent loop, skill execution, and memory system all run locally. The only outbound calls are to the LLM endpoint you configure. If that endpoint is local, no data leaves your machine.

**What does the agent send to external APIs?**

Only what you explicitly route to them. If you use OpenRouter, your prompts go to OpenRouter's API (and from there to the model provider). If you use fal.ai for image generation, your prompts go to fal.ai. The agent does not send data to any third party beyond the services you configure.

**Can someone else access my agent?**

Only via channels you open. Telegram: only users you explicitly allow via the access control list. The gateway is bound to localhost by default and never exposed publicly. Run `tools/security-scan.sh` to check for accidental public exposure.

**Is the workspace safe to commit to a public GitHub repo?**

Not as-is. `.env.secrets` is gitignored, but SOUL.md and USER.md contain personal context you may not want public. Before pushing, review those files and replace personal details with placeholders. The workspace/ folder in this kit shows what sanitized templates look like.

---

## Hardware

**Mac or Linux, which is better?**

Both work well. Mac has advantages if you use macOS-specific integrations (iMessage via BlueBubbles, macOS Automator). Linux is better for server deployment, lower cost, and headless operation. Most users run the agent on a Mac Mini or a cheap Hetzner VPS (2 EUR/month).

**Does Apple Silicon (M1 - M4) work?**

Yes, and it is the recommended local setup. Hermes Agent runs natively on ARM. If you run local LLMs via Ollama, M-series chips are highly efficient (Llama 3.1 8B runs at 40+ tokens/sec on M2).

**How much RAM do I need?**

For API-based models (no local LLM): 2 GB is enough. For local LLM inference: 16 GB for 7B models, 32 GB for 30B+ models. For the full fleet setup described in FLEET-GUIDE.md: each agent node needs 1-2 GB for the runtime.

**Do I need a dedicated machine, or can I run it on my laptop?**

You can run it on your laptop, but the agent will go offline when the laptop sleeps. For 24/7 operation, use a Mac Mini, a VPS, or a small dedicated machine. A $5/month Hetzner CX22 handles the base agent comfortably.

---

## Use Cases

**Small business owner (5-person team)**

Best starting point: email triage, calendar management, and customer support via Telegram. Install `gws-gmail-triage` + `gws-calendar` + `telegram` skills. Expected time saving: 1-2 hours per day after the first week of setup. See `case-studies/lead-automation.md` for a concrete example.

**Freelancer**

High-ROI starting point: proposal generation, invoice chasing, and client communication. Install `notion` + `gws-gmail-send` + the content creation skills. One user reported generating and sending 3 custom proposals in 20 minutes instead of 3 hours.

**Marketing agency**

Content pipeline is the highest-ROI use case. See `case-studies/content-pipeline.md` for the full setup. Cost: approximately $12/reel fully AI-generated vs $200-500/reel with a freelance editor.

**Developer / engineering team**

Code review, PR summarization, issue triage. Install `github` + `coding` + `coding-agent` skills. The `claude-code` skill lets you delegate implementation tasks to a background Claude Code session.

**Do I need to know how to code?**

No, but basic command-line comfort helps. If you can open a terminal, run a git clone, and edit a text file, you have enough skill to get started. The GETTING-STARTED.md guide is written for non-developers.

---

## Troubleshooting Top 5

**1. Gateway won't start**

See TROUBLESHOOTING.md for detailed steps. Short version: check that port 3000 (or your configured port) is not in use, verify node version is 18+, and look at `~/.hermes/logs/gateway.log` for the actual error.

**2. Telegram bot is silent**

Most common causes: bot token not set in config, Telegram chat not authorized in access.json, or the gateway is down. Run `tools/health-check.sh` to verify the gateway is running, then check `~/.hermes/logs/` for errors.

**3. OAuth expired (Google Workspace)**

Google tokens expire after 7 days unless refresh tokens are properly configured. Run the auth setup again: `hermes setup google` or the equivalent for your platform. See TROUBLESHOOTING.md for the permanent fix using an Internal OAuth app.

**4. Skill not loading**

Verify the skill folder is in the right location and contains a valid SKILL.md with frontmatter. Check for YAML syntax errors (frontmatter is sensitive to indentation). Run `hermes skills validate <skill-name>` if your version supports it.

**5. Model rate limit**

OpenRouter returns HTTP 429. The agent backs off automatically in most cases. If it persists, check your OpenRouter account limits, add a backup model to the fallback chain in TOOLS.md, or reduce concurrent agent tasks.

---

## Pricing and Support

**Is there a paid version of this kit?**

The kit is free and open source (MIT license). The "Build Your Own 24/7 AI Employee" course at weblyfe.ai/store includes step-by-step video walkthroughs, a private community, and ongoing updates. The kit here is everything you need to run the system, the course accelerates the learning curve.

**Where do I get help?**

1. Check the docs: FAQ (this file), TROUBLESHOOTING.md, GETTING-STARTED.md.
2. Open a GitHub issue for bugs or feature requests.
3. Course buyers get access to the private community for direct support.

**How often is the kit updated?**

The kit tracks the live Weblyfe fleet. Major versions (v4.3, v4.4) are released with the course updates, typically every 2-3 months. Smaller skill additions and bug fixes are pushed continuously.

**Can I use this commercially?**

Yes. MIT license, use it for your own business, build products on top of it, resell services using it. Attribution is appreciated but not required.
