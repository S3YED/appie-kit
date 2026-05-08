# personal

Skills for personal productivity, task management, and lifestyle integrations. These are primarily macOS-specific. Use them to wire your Appie into your personal workflow: notes, reminders, to-do apps, music, and smart home.

Prerequisite tools: most skills require macOS with the corresponding app installed. Spotify skills require `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`.

## Skills

| Skill | Description | Required env | Compat |
|-------|-------------|-------------|--------|
| [apple-notes](apple-notes/) | Read and create Apple Notes via AppleScript | macOS | OpenClaw |
| [apple-reminders](apple-reminders/) | Manage Apple Reminders: add, complete, list via AppleScript | macOS | OpenClaw |
| [bear-notes](bear-notes/) | Bear note-taking app: create, search, tag notes via Bear URL scheme | macOS | Both |
| [gws-tasks](gws-tasks/) | Google Tasks: create, complete, list task items across task lists | GOOGLE_OAUTH | Both |
| [kanban-orchestrator](kanban-orchestrator/) | Orchestrate a kanban board across multiple agent workers | - | Hermes |
| [kanban-worker](kanban-worker/) | Kanban worker agent: pick tasks from board, execute, update status | - | Hermes |
| [sonoscli](sonoscli/) | Sonos speaker control via CLI: play, pause, volume, grouping | - | Both |
| [spotify-player](spotify-player/) | Spotify playback control: play, pause, skip, search, queue | SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET | Both |
| [things-mac](things-mac/) | Things 3 task manager: create tasks, projects, and areas via URL scheme | macOS | OpenClaw |
| [weather](weather/) | Current weather and forecasts via wttr.in or Open-Meteo. No API key needed | - | Both |

## Install

```bash
cp -r skills/personal/<skill> ~/.hermes/skills/
# or for OpenClaw:
cp -r skills/personal/<skill> ~/.openclaw/skills/
```
