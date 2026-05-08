# communication

Skills for sending and receiving messages across platforms, managing chat sessions, and integrating with messaging APIs. Use these to wire your Appie into Telegram, Discord, Slack, iMessage, email clients, and other channels.

Prerequisite tools: platform-specific tokens/keys (see per-skill docs), `curl` for webhook-based skills, Python for gateway-bridged skills.

## Skills

| Skill | Description | Required env | Compat |
|-------|-------------|-------------|--------|
| [appie-self-maintenance](appie-self-maintenance/) | Protocols for agent self-check, health reporting, and status updates via message | - | Both |
| [bluebubbles](bluebubbles/) | iMessage via BlueBubbles server API. Send, receive, react to messages | BLUEBUBBLES_URL, BLUEBUBBLES_PASSWORD | Hermes |
| [debugging-hermes-tui-commands](debugging-hermes-tui-commands/) | Cheatsheet for Hermes TUI keyboard shortcuts and debug commands | - | Hermes |
| [discord](discord/) | Discord ops via the message tool. Channel posting, reactions, moderation | DISCORD_TOKEN | Both |
| [dspy](dspy/) | DSPy framework integration for structured LLM pipelines and prompt optimization | OPENAI_API_KEY | Both |
| [find-nearby](find-nearby/) | Find nearby places using location services and maps APIs | - | Both |
| [guidance](guidance/) | Microsoft Guidance library for constrained LLM generation | - | Both |
| [gws-chat](gws-chat/) | Google Chat: read spaces, list messages, manage memberships | GOOGLE_OAUTH | Both |
| [gws-chat-send](gws-chat-send/) | Send messages to Google Chat spaces and direct messages | GOOGLE_OAUTH | Both |
| [himalaya](himalaya/) | Email client via himalaya CLI. Read, send, move, flag emails from terminal | - | Hermes |
| [imessage](imessage/) | Send iMessages via macOS AppleScript or osascript. Mac-only | - | Both |
| [imsg](imsg/) | Lightweight iMessage send wrapper for quick message dispatch | - | Both |
| [linear](linear/) | Linear issue tracker: create, update, comment on issues and projects | LINEAR_API_KEY | Both |
| [maps](maps/) | Location search, directions, and place details via mapping APIs | - | Both |
| [modal](modal/) | Modal Labs integration for serverless Python function execution | MODAL_TOKEN | Both |
| [native-mcp](native-mcp/) | Native MCP server communication protocol for direct tool access | - | Both |
| [openclaw-to-hermes](openclaw-to-hermes/) | Migration guide and tooling for moving from OpenClaw to Hermes Agent | - | Both |
| [outlines](outlines/) | Structured generation via Outlines library. JSON schema enforcement | - | Both |
| [session-logs](session-logs/) | Parse and search Hermes session log files for debugging and auditing | - | Hermes |
| [slack](slack/) | Slack messaging: send messages, read channels, manage threads | SLACK_BOT_TOKEN | Both |
| [stable-diffusion](stable-diffusion/) | Stable Diffusion image generation via local or API endpoint | SD_API_URL | Both |
| [voice-call](voice-call/) | Initiate and manage voice calls via supported telephony integrations | - | Both |
| [wacli](wacli/) | WhatsApp CLI integration for sending and receiving messages | WACLI_SESSION | Hermes |
| [webhook-subscriptions](webhook-subscriptions/) | Manage incoming webhooks, register endpoints, route payloads | - | Both |
| [weights-and-biases](weights-and-biases/) | Weights and Biases experiment tracking. Log runs, metrics, artifacts | WANDB_API_KEY | Both |

## Install

```bash
cp -r skills/communication/<skill> ~/.hermes/skills/
# or for OpenClaw:
cp -r skills/communication/<skill> ~/.openclaw/skills/
```
