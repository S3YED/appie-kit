---
name: agentic-webdesign-agent-elements
description: Use 21st.dev Agent Elements — 25 shadcn/ui components purpose-built for AI agent UIs. Tool cards (Bash, Edit, Search, Plan, Subagent, MCP), chat, input, streaming. Open source, shadcn-registry install, no runtime lock-in.
tags: [agentic-webdesign, agent-ui, shadcn, 21st-dev, tool-cards]
---

# Agent Elements — 21st.dev Agent UI Components

## What it is

25 open-source shadcn/ui components designed for building AI agent interfaces. Tool cards render agent actions (bash, file edits, searches, plans, sub-agents) as rich UI cards with streaming, diffs, and approval flows — not just plain text.

**GitHub:** https://github.com/21st-dev/agent-elements
**Docs:** https://agent-elements.21st.dev
**Stack:** React 19, Tailwind v4, Base UI, Motion, shadcn/ui

## When to use

Use Agent Elements when building:
- Agent chat interfaces (coding agents, assistants, chatbots that use tools)
- Any UI where an AI agent executes bash commands, edits files, searches, plans, spawns sub-agents
- Approval-based workflows (diff review, plan confirmation)

Do NOT use for simple chat-only interfaces — plain shadcn/ui chat components suffice.

## Components

### Chat surface
- `AgentChat` — drop-in chat shell with MessageList + InputBar, tool dispatch, empty state
- `MessageList` — streaming-aware, scroll-anchored, keyboard-friendly
- `Markdown` — safe streaming markdown rendering

### Input
- `InputBar` — composer with mode/model selection, attachments, send
- `ModeSelector` — toggle plan/build/ask modes
- `ModelPicker` — per-turn model selection
- `AttachmentButton`, `FileAttachment` — drag-and-drop files

### Tool cards (the main value)
- `BashTool` — streams stdout as it arrives, shows exit code
- `EditTool` — real unified diff with approve/reject affordances (Claude Code pattern)
- `SearchTool` — renders search results
- `TodoTool` — renders task lists
- `PlanTool` — structured plan with accept/redirect
- `SubagentTool` — visualises nested agent delegation
- `McpTool` — MCP server tool invocations
- `ThinkingTool` — renders thinking/reasoning output
- `QuestionTool` — clarifying questions (single/multi/free-text)
- `ToolGroup` — groups related tool calls
- `GenericTool` — fallback for custom tools

### Streaming indicators
- `TextShimmer` — animated "generating" text
- `SpiralLoader` — spinner

## Installation

```bash
# Full chat surface (installs all transitive dependencies)
npx shadcn@latest add https://agent-elements.21st.dev/r/agent-chat.json

# Individual tool cards
npx shadcn@latest add https://agent-elements.21st.dev/r/edit-tool.json
npx shadcn@latest add https://agent-elements.21st.dev/r/bash-tool.json
npx shadcn@latest add https://agent-elements.21st.dev/r/plan-tool.json

# Teach your coding agent to use Agent Elements
npx skills add 21st-dev/agent-elements
```

Files land in `components/agent-elements/`. You own the code — no npm package, no runtime dependency on 21st.dev.

## Usage with Vercel AI SDK

```tsx
"use client";
import { AgentChat } from "@/components/agent-elements/agent-chat";
import { BashTool } from "@/components/agent-elements/tools/bash-tool";
import { EditTool } from "@/components/agent-elements/tools/edit-tool";
import { SearchTool } from "@/components/agent-elements/tools/search-tool";
import { useChat } from "@ai-sdk/react";

export default function Chat() {
  const { messages, status, sendMessage, stop } = useChat();

  return (
    <AgentChat
      messages={messages}
      status={status}
      onSend={({ content }) => sendMessage({ text: content })}
      onStop={stop}
      toolRenderers={{
        Bash: BashTool,
        Edit: EditTool,
        Write: EditTool,
        Search: SearchTool,
      }}
    />
  );
}
```

## Architecture pattern

The key insight: map your agent's tool calls to tool card renderers via a `toolRenderers` map. Each renderer receives the tool's `input`/`args`, `output`/`result`, and `state` (call, partial-call, result). Renderers handle their own loading, streaming, and completion states.

## Pitfalls

- Not an npm package — installs via shadcn CLI into your project. You own and maintain the code.
- Requires Tailwind v4 and shadcn/ui already set up.
- Tool cards expect the Vercel AI SDK `UIMessage` shape or compatible adapter.
- The agent-elements skill (`npx skills add 21st-dev/agent-elements`) must be installed for coding agents to use the components correctly — otherwise they hallucinate props.

## Quality

Production-ready. MIT licensed. 77+ GitHub stars. Built by the 21st.dev team (@Ibelick, @serafimcloud). Part of the 21st.dev Agent SDK ecosystem. Computer-use card (screenshot + click sequences) is in development.
