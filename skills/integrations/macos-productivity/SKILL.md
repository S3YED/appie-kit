---
name: macos-productivity
description: "macOS productivity tools: Apple Notes (memo CLI), Reminders (remindctl), iMessage (imsg), Find My devices/AirTags, and macOS computer-use. Umbrella for all Apple ecosystem agent tools."
version: 1.0.0
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [macOS, Apple, Notes, Reminders, iMessage, FindMy, Productivity]
    related_skills: []
---

# macOS Productivity Tools

Umbrella covering Apple ecosystem CLI tools for agent use. Each tool has a dedicated reference file.

**Note:** These tools are macOS-only. On Linux, each section will skip gracefully.

## Contents

1. [Apple Notes (memo CLI)](#1-apple-notes)
2. [Apple Reminders (remindctl)](#2-apple-reminders)
3. [iMessage (imsg CLI)](#3-imessage)
4. [Find My (FindMy.app via AppleScript)](#4-find-my)
5. [macOS Computer Use](#5-macos-computer-use)

---

## 1. Apple Notes

**Full reference:** `references/apple-notes.md`

Use `memo` CLI to manage Apple Notes from the terminal.

### Quick Start

```bash
# List notes
memo list

# Create a note
memo create "Note Title" --body "Content here"

# Search
memo search "keyword"

# View
memo view <note-id>
```

---

## 2. Apple Reminders

**Full reference:** `references/apple-reminders.md`

Use `remindctl` CLI to manage Apple Reminders.

### Quick Start

```bash
# List reminders
remindctl list

# Add reminder
remindctl add "Buy groceries" --due "tomorrow" --list "Errands"

# Complete
remindctl complete <id>

# Delete
remindctl delete <id>
```

---

## 3. iMessage

**Full reference:** `references/imessage.md`

Use `imsg` CLI to send and receive iMessages/SMS via macOS Messages.app.

### Quick Start

```bash
# Send message
imsg send "Hello!" --to "+1234567890"

# List conversations
imsg list

# Read recent messages
imsg read --limit 10
```

---

## 4. Find My

**Full reference:** `references/findmy.md`

Track Apple devices and AirTags via FindMy.app using AppleScript and screen capture.

### Quick Start

Uses AppleScript to open FindMy.app and screen capture to read locations. No direct CLI available.

```bash
# Open FindMy
osascript -e 'tell application "FindMy" to activate'

# Capture device list (screen capture + OCR)
screencapture -x /tmp/findmy.png
```

---

## 5. macOS Computer Use

**Full reference:** `references/macos-computer-use.md`

Automate macOS UI interactions for agent-driven desktop operations.