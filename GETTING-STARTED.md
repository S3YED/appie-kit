# Getting Started

From zero to first response in about 20 minutes.

This guide assumes you've never run an AI agent before. If you've done this before, skip to the step that's relevant.

---

## Pre-flight (5 minutes)

You need three things before cloning:

### 1. OpenRouter API key

Go to [openrouter.ai](https://openrouter.ai), create a free account, and generate an API key. Copy it somewhere safe.

The default model is **MiniMax M2.7**: approximately $0.01/1M tokens. For context, a busy day of messages, emails, and tasks typically costs under $0.05. Add $5 in credits to start, it'll last weeks.

### 2. Telegram bot token

Open Telegram and message [@BotFather](https://t.me/botfather). Send `/newbot`, give it a name and username, and copy the token it gives you. It looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`.

### 3. Install Hermes Agent

Hermes Agent is the runtime that powers your agent. Install it with:

```bash
npm install -g @nousresearch/hermes-agent
hermes --version # confirm it's installed
```

Alternatively, use [OpenClaw](https://github.com/openclaw/openclaw) if you prefer. All commands below have OpenClaw equivalents in the README.

---

## Step 1: Clone the kit (1 minute)

```bash
git clone https://github.com/S3YED/appie-kit.git
cd appie-kit
```

---

## Step 2: Set your environment variables (2 minutes)

```bash
cp .env.example .env.secrets
chmod 600 .env.secrets
```

Open `.env.secrets` in a text editor and fill in your keys:

```bash
OPENROUTER_API_KEY=sk-or-... # your OpenRouter key
TELEGRAM_BOT_TOKEN=123456789:... # your Telegram bot token
```

Leave the other fields empty for now. You can add them as you expand.

---

## Step 3: Customize SOUL.md (5 minutes)

This file defines your agent's personality. Open `workspace/SOUL.md` and replace the placeholders:

```bash
nano workspace/SOUL.md
```

Key fields to fill in:

```yaml
You are **<your-agent-name>**, an autonomous AI assistant.

## Your Human
- **Name:** <your-name>
- **Timezone:** <your-timezone> # e.g., America/New_York
- **Company:** <your-company>
- **Voice:** <how you want it to communicate>
```

Example:
```yaml
You are **Maya**, an autonomous AI assistant built on Hermes Agent.

## Your Human
- **Name:** Alex
- **Timezone:** Europe/Amsterdam
- **Company:** Acme Consulting
- **Voice:** Direct, professional, no corporate jargon. Concise answers.
```

The personality section is worth spending time on. An agent that matches your communication style feels dramatically better to use day-to-day.

---

## Step 4: Customize USER.md (3 minutes)

USER.md tells the agent about you. Open `workspace/USER.md`:

```bash
nano workspace/USER.md
```

Fill in:
- Your name and preferred name
- Timezone and language
- Your company and what you do
- Communication style preferences

Example:
```
- **Name:** Alex Johnson
- **What to call them:** Alex
- **Timezone:** America/New_York
- **Language preference:** English
- **Email:** alex@acmeconsulting.com

## Company / Business
- **Company:** Acme Consulting
- **Website:** acmeconsulting.com
- **Industry:** IT consulting
- **What you do:** Help small businesses implement cloud infrastructure
- **Stack:** Airtable, Google Workspace, Vercel, Stripe

## Communication Style
Direct and technical. I prefer bullet points over paragraphs.
```

---

## Step 5: Install your starter skill pack (5 minutes)

155 skills are included. Start with five that cover the basics:

```bash
# Google Calendar: schedule, check, add events
cp -r skills/integrations/gws-calendar ~/.hermes/skills/

# Telegram: read and send messages
cp -r skills/communication/discord ~/.hermes/skills/ # swap for your preferred channel

# n8n: trigger and manage automations
cp -r skills/integrations/n8n ~/.hermes/skills/

# Browser automation: web research, form filling
cp -r skills/automation/playwright ~/.hermes/skills/

# Coding help: code review, debugging, generation
cp -r skills/automation/coding ~/.hermes/skills/
```

Or install an entire category at once:

```bash
cp -r skills/integrations/* ~/.hermes/skills/
cp -r skills/content/* ~/.hermes/skills/
```

---

## Step 6: Copy workspace files to Hermes (1 minute)

```bash
cp workspace/SOUL.md ~/.hermes/SOUL.md
cp workspace/USER.md ~/.hermes/USER.md
cp workspace/AGENTS.md ~/.hermes/AGENTS.md
cp workspace/TOOLS.md ~/.hermes/TOOLS.md
```

---

## Step 7: Start the agent (1 minute)

```bash
hermes start
```

You should see output like:
```
Hermes Agent v1.x.x
Gateway running on http://localhost:3000
Telegram bot connected: @yourbotname
Loaded 5 skills
Ready.
```

Now open Telegram and send your bot a message.

---

## Step 8: First conversation (1 minute)

Send this to your Telegram bot:

```
What skills do you have loaded? What can you help me with today?
```

Your agent should respond with a summary of its loaded skills and a few suggestions based on your USER.md context.

Try a real task:

```
Check my Google Calendar for tomorrow and tell me what I have scheduled.
```

or:

```
Search the web for the latest news about [your industry].
```

---

## What to do next

Now that the agent responds, the real work is personalization:

**Add more skills.** Browse `skills/` by category. Each skill folder has a SKILL.md explaining what it does. Install what's relevant to your work.

**Extend TOOLS.md.** Add your Airtable base ID, Notion workspace, or any other service you want the agent to access. The more context it has, the more useful it becomes.

**Set up recurring checks.** Edit `workspace/HEARTBEAT.md` to configure what the agent checks proactively (email, calendar, server health). This turns it from a chatbot into an employee that works while you sleep.

**Read the case studies.** `case-studies/` contains real-world implementations with concrete numbers. The content pipeline and lead automation examples are directly applicable to most small businesses.

**Questions?** Check FAQ.md for common questions, TROUBLESHOOTING.md for error symptoms, and open a GitHub issue if you're stuck.
