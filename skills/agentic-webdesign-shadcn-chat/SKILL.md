---
name: agentic-webdesign-shadcn-chat
description: Use shadcn/ui chat interface components — MessageScroller, Message, Bubble, Attachment, Marker. Composable primitives for building streaming chat UIs. Use when building AI chat interfaces, support inboxes, or any conversation UI with shadcn/ui.
metadata:
  created: 2026-07-13
  source: shadcn/ui June 2026 changelog (shadcn@4.12.0)
  tags: [shadcn, chat, streaming, message, ui, ai]
---

# shadcn/ui Chat Interface Components

A set of composable primitives for building streaming chat UIs. The scroll behavior, accessibility, and streaming edge cases are handled for you. You bring the content.

## Install

```bash
npx shadcn@latest add message-scroller message bubble attachment marker
```

## Component Overview

### MessageScroller
The scroll container for a conversation. Handles:
- **Anchored turns** — pin a user message near the top
- **Streamed replies** — auto-scroll only when user is at the bottom
- **Thread restore** — saved scroll position on navigation
- **Prepend history** — preserve position when history loads above
- **Jump-to-message** and scroll controls
- **Visibility tracking**

Headless version available: `@shadcn/react/message-scroller`

Structure:
```
MessageScrollerProvider
  └── MessageScroller
       └── MessageScrollerViewport
            └── MessageScrollerContent (role="log", aria-relevant="additions")
```

### Message
Row layout with avatar, alignment, header, content, footer, and grouped messages.

### Bubble
Message surface with variants, alignment, reactions, links, buttons, and collapsible content.

### Attachment
Files and images with media, metadata, upload state, actions, and full-card trigger.

### Marker
Status updates, system notes, bordered rows, labeled separators — streaming state, tool activity, date breaks.

## CSS Utilities (included with shadcn/tailwind.css)

### scroll-fade
Scroll-aware edge fades. No overlays or JS listeners.

```tsx
<div className="h-72 scroll-fade scrollbar-none overflow-y-auto">
  {...items}
</div>
```

### shimmer
Text shimmer animation for live status:

```tsx
<p className="shimmer text-sm text-muted-foreground">
  Generating response…
</p>
```

## AI Agent Integration

Works with Vercel AI SDK:

```tsx
import { useChat } from '@ai-sdk/react'

const { messages, sendMessage, isLoading } = useChat({
  transport: chat.transport({ chunkDelayMs: 20 })
})
```

## Why This Helps AI Agents

1. **Scroll behavior lives in code** — agents don't need to handle anchor logic in prompts
2. **Small, single-purpose** — each component does one thing, reducing composition errors
3. **Accessibility built-in** — `role="log"`, `aria-relevant`, `aria-busy`, screen reader announcements
4. **Headless option** — `@shadcn/react` decouples behavior from style
5. **Streaming-aware** — auto-scroll only when pinned to bottom, respects user scroll position

## Pitfalls

- MessageScroller owns scroll behavior but NOT your messages, AI state, transport, or persistence
- Use `scrollAnchor` on user messages for anchored turns
- For streaming, set `aria-busy` during active generation
- The `scroll-fade` and `shimmer` utilities only work with projects initialized via `npx shadcn@latest init`