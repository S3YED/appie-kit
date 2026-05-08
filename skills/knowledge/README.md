# knowledge

Skills for research, search, web scraping, email triage workflows, memory management, and documentation reference. Use these when your Appie needs to find information, process inbound content, or maintain a knowledge base.

Prerequisite tools: `EXA_API_KEY` for exa-plus, Google OAuth for gws-gmail-* skills, Python + playwright for browser-based scraping.

## Skills

| Skill | Description | Required env | Compat |
|-------|-------------|-------------|--------|
| [anthropics-frontend-design](anthropics-frontend-design/) | Anthropic design system reference for building Anthropic-style UI components | - | Both |
| [audiocraft](audiocraft/) | Meta AudioCraft for AI music and audio generation (MusicGen, AudioGen) | Python, GPU | Both |
| [blucli](blucli/) | Bluetooth CLI device management and pairing automation | macOS/Linux | Both |
| [browser-use](browser-use/) | Web scraping, screenshots, form filling, Google/YT/TikTok image/video download with Playwright | Python | Both |
| [claude-code](claude-code/) | Claude Code (Claude Code CLI) reference: commands, tool use, slash commands, MCP | - | Both |
| [clawflow](clawflow/) | OpenClaw workflow engine for defining and running multi-step agent pipelines | - | OpenClaw |
| [clawflow-inbox-triage](clawflow-inbox-triage/) | Automated email inbox triage workflow using OpenClaw flow engine | GOOGLE_OAUTH | OpenClaw |
| [codex](codex/) | OpenAI Codex CLI reference and best practices for code generation | OPENAI_API_KEY | Both |
| [content-creation](content-creation/) | Structured content creation: outlines, drafts, SEO, distribution checklist | - | Both |
| [exa-plus](exa-plus/) | Neural web search via Exa AI. People, companies, news, research, code. Deep search, date/domain filters | EXA_API_KEY | Both |
| [gemini](gemini/) | Google Gemini API reference: models, multimodal, grounding, code execution | GOOGLE_API_KEY | Both |
| [gws-events-renew](gws-events-renew/) | Renew Google Workspace Event subscriptions before they expire | GOOGLE_OAUTH | Both |
| [gws-gmail-forward](gws-gmail-forward/) | Forward Gmail messages to addresses or lists with optional transformation | GOOGLE_OAUTH | Both |
| [gws-gmail-reply](gws-gmail-reply/) | Compose and send Gmail replies with threading and signature handling | GOOGLE_OAUTH | Both |
| [gws-gmail-reply-all](gws-gmail-reply-all/) | Reply-all to Gmail threads with smart recipient deduplication | GOOGLE_OAUTH | Both |
| [gws-gmail-triage](gws-gmail-triage/) | Automated Gmail triage: label, archive, prioritize, draft responses | GOOGLE_OAUTH | Both |
| [gws-gmail-watch](gws-gmail-watch/) | Set up Gmail push notifications for real-time message processing | GOOGLE_OAUTH | Both |
| [gws-modelarmor-create-template](gws-modelarmor-create-template/) | Create Model Armor sanitization templates via Google Cloud API | GOOGLE_CLOUD_PROJECT | Both |
| [gws-modelarmor-sanitize-prompt](gws-modelarmor-sanitize-prompt/) | Sanitize user prompts through Model Armor before LLM submission | GOOGLE_CLOUD_PROJECT | Both |
| [gws-modelarmor-sanitize-response](gws-modelarmor-sanitize-response/) | Sanitize LLM responses through Model Armor before delivery | GOOGLE_CLOUD_PROJECT | Both |
| [gws-workflow-email-to-task](gws-workflow-email-to-task/) | Convert Gmail messages to tasks in Google Tasks or Notion | GOOGLE_OAUTH | Both |
| [gws-workflow-file-announce](gws-workflow-file-announce/) | Announce new Drive files to team channels automatically | GOOGLE_OAUTH | Both |
| [gws-workflow-meeting-prep](gws-workflow-meeting-prep/) | Auto-prepare meeting briefs from calendar events and Drive docs | GOOGLE_OAUTH | Both |
| [gws-workflow-standup-report](gws-workflow-standup-report/) | Generate daily standup reports from task and calendar data | GOOGLE_OAUTH | Both |
| [gws-workflow-weekly-digest](gws-workflow-weekly-digest/) | Compile and send weekly activity digest from Workspace activity | GOOGLE_OAUTH | Both |
| [healthcheck](healthcheck/) | Agent health monitoring: check service status, report anomalies | - | Both |
| [heartmula](heartmula/) | Heartbeat + mula (money) monitoring: track revenue metrics and uptime | - | Both |
| [manim-video](manim-video/) | Generate animated math/concept explainer videos using Manim | Python | Both |
| [memory-search](memory-search/) | Search Hermes agent memory across sessions for past context | - | Hermes |
| [minecraft-modpack-server](minecraft-modpack-server/) | Set up and manage Minecraft modpack servers (for fun / client use) | Java | Both |
| [node-connect](node-connect/) | Node.js debugger connection via CDP for live inspection | Node.js | Both |
| [node-inspect-debugger](node-inspect-debugger/) | Node.js inspect-mode debugger integration for runtime debugging | Node.js | Both |
| [obsidian](obsidian/) | Obsidian vault operations: read notes, create entries, search graph | - | Both |
| [ocr-and-documents](ocr-and-documents/) | OCR extraction from images and PDFs, document parsing workflows | Python | Both |
| [opencode](opencode/) | OpenCode CLI reference: commands, configuration, provider setup | - | Both |
| [openhue](openhue/) | Philips Hue smart light control via openhue CLI | OPENHUE_TOKEN | Both |
| [ordercli](ordercli/) | E-commerce order management CLI for tracking and fulfillment | - | Both |
| [peekaboo](peekaboo/) | macOS screenshot and screen observation tool for vision-based agent tasks | macOS | OpenClaw |
| [persona-researcher](persona-researcher/) | Research persona: organize references, notes, source validation, collaboration | - | Both |
| [plan](plan/) | Structured planning skill: break goals into phases, tasks, and dependencies | - | Both |
| [playwright](playwright/) | Playwright browser automation: navigation, interaction, scraping, testing | Python/Node.js | Both |
| [read-github](read-github/) | Read GitHub repos via gitmcp.io. Semantic search, smart code navigation | GH_TOKEN | Both |
| [recipe-create-gmail-filter](recipe-create-gmail-filter/) | Create Gmail filters for automatic labeling and archiving | GOOGLE_OAUTH | Both |
| [recipe-draft-email-from-doc](recipe-draft-email-from-doc/) | Draft Gmail message from a Google Doc template | GOOGLE_OAUTH | Both |
| [recipe-email-drive-link](recipe-email-drive-link/) | Email a Google Drive file link to recipients | GOOGLE_OAUTH | Both |
| [recipe-label-and-archive-emails](recipe-label-and-archive-emails/) | Bulk label and archive emails matching criteria | GOOGLE_OAUTH | Both |
| [recipe-save-email-attachments](recipe-save-email-attachments/) | Save Gmail attachments to specified Google Drive folder | GOOGLE_OAUTH | Both |
| [remotion-best-practices](remotion-best-practices/) | Remotion video-in-React patterns: composition, rendering, lambda deploy | Node.js | Both |
| [research-paper-writing](research-paper-writing/) | Academic research paper structure, citation management, LaTeX workflow | - | Both |
| [seo-backlinks](seo-backlinks/) | Backlink research and link-building strategy workflow | EXA_API_KEY | Both |
| [seo-bezoekersmagneet](seo-bezoekersmagneet/) | Dutch-language SEO content framework for attracting organic traffic | - | Both |
| [seo-keyword-strategie](seo-keyword-strategie/) | Keyword research: long-tail focus, placement rules, search volume validation | - | Both |
| [seo-smart-content](seo-smart-content/) | AI-assisted SEO content writing with keyword integration | - | Both |
| [seo-technische-seo](seo-technische-seo/) | Technical SEO audit: Core Web Vitals, crawlability, structured data | - | Both |
| [songwriting-and-ai-music](songwriting-and-ai-music/) | Songwriting frameworks and AI music generation (Suno, Udio, AudioCraft) | - | Both |
| [summarize](summarize/) | Summarize long documents, transcripts, or web pages into structured bullets | - | Both |
| [web-scraping-javascript-sites](web-scraping-javascript-sites/) | Scrape SPA/TypeScript sites. urllib-first strategy, Playwright fallback, stealth mode | Python | Both |
| [yuanbao](yuanbao/) | Yuanbao (Tencent AI) API integration reference | YUANBAO_API_KEY | Both |

## Install

```bash
cp -r skills/knowledge/<skill> ~/.hermes/skills/
# or for OpenClaw:
cp -r skills/knowledge/<skill> ~/.openclaw/skills/
```
