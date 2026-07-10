---
name: n8n-agents
description: Design n8n AI agents the right way. Use when building or editing any @n8n/n8n-nodes-langchain.* AI node — an AI Agent, LLM chain, Text Classifier, or Information Extractor — and whenever the user mentions AI agents, LLM with tools, tool calling, $fromAI, system prompts, agent memory, sessionId, structured/JSON output, output parser, RAG, vector store, a chat assistant/bot, or human-in-the-loop review. Covers Agent-vs-chain-vs-classifier choice, the model/memory/tools/outputParser slots, tool names/descriptions as prompt, structured output with autoFix, memory, RAG, human review, and chat topologies.
---

# n8n Agents

The n8n AI Agent node (`@n8n/n8n-nodes-langchain.agent`) is a multi-turn LLM driver with sub-nodes for the model, memory, tools, and an optional output parser. This skill is the **deep** guide to designing agents and the LangChain family around them. For the high-level "where an agent fits in a workflow" picture, see **n8n-workflow-patterns** `ai_agent_workflow.md` — this skill goes one level down into *how to build it well*.

For node-type formats: in workflow JSON the LangChain nodes use the long `@n8n/n8n-nodes-langchain.*` form (`.agent`, `.lmChatOpenAi`, `.memoryBufferWindow`, `.outputParserStructured`, `.toolWorkflow`, `.toolHttpRequest`, `.toolCode`). When you call `get_node` / `validate_node`, use the **short** form (`nodes-langchain.agent`). See **n8n-mcp-tools-expert** for the format rules.

---

## Pick the right node first

Reaching for an Agent when the task is one-shot classification or extraction is the most common over-build. Decide before you wire anything:

| You need to… | Use | Why |
|---|---|---|
| Call tools, reason over multiple turns, or hold memory | **AI Agent** (`.agent`) | The full loop: model + tools + memory + optional parser. Also a fine default when you'd rather standardize. |
| One-shot text in → text out, no tools | **Basic LLM Chain** (`.chainLlm`) | No agent loop, easier to debug. Still accepts an `outputParserStructured` sub-node. |
| Route a natural-language input to one of **N branches** | **Text Classifier** (`.textClassifier`) | ONE node, N output handles, downstream wires directly into each. Not Agent + Switch. |
| Pull structured fields out of free text | **Information Extractor** (`.informationExtractor`) | Purpose-built field extraction with a schema. |
| 3-way positive/neutral/negative split | **Sentiment Analysis** (`.sentimentAnalysis`) | Built-in branch outputs. |
| Condense a long document | **Summarization Chain** (`.chainSummarization`) | Map-reduce summarization built in. |
| Generate an image / audio / video | **The provider's native single-call node** (OpenAI, Gemini, ElevenLabs…) | NEVER wrap media generation in an Agent — see "Binary and the agent boundary". |

**Text Classifier detail (the Agent + Switch anti-pattern):** every category needs both a **name AND a description**. The model routes against the *description*, not the name — a category with no description gets picked by coin-flip. Set `options.enableAutoFixing: true` for robustness on edge inputs. One node, N branches, done. Reaching for an Agent that "decides" then a Switch that "routes" is two nodes plus prompt boilerplate for what Text Classifier does natively.

Chat-model nodes (`.lmChatOpenAi`, `.lmChatAnthropic`, `.lmChatOpenRouter`, …) are **sub-nodes** — they don't run standalone. They wire into a chain, agent, classifier, or extractor via the `ai_languageModel` connection.

---

## The sub-node pattern

The Agent has a **main input** (the prompt / user message) and up to four **sub-node slots**, each wired by its own `ai_*` connection type:

| Slot | Connection type | Required? | Node example |
|---|---|---|---|
| **model** | `ai_languageModel` | Yes | `.lmChatOpenAi`, `.lmChatAnthropic`, `.lmChatOpenRouter` |
| **memory** | `ai_memory` | Optional | `.memoryBufferWindow`, `.memoryPostgresChat` |
| **tools** | `ai_tool` | Optional (but the point of an agent) | `slackTool`, `.toolWorkflow`, `.toolHttpRequest`, `.toolCode` |
| **outputParser** | `ai_outputParser` | Optional | `.outputParserStructured` |

A sub-node connects FROM itself TO the agent. In workflow JSON the connection lives on the **sub-node**, keyed by the `ai_*` type:

```json
"Main LLM": {
  "ai_languageModel": [[{ "node": "AI Agent", "type": "ai_languageModel", "index": 0 }]]
},
"Simple Memory": {
  "ai_memory": [[{ "node": "AI Agent", "type": "ai_memory", "index": 0 }]]
},
"Search customer DB": {
  "ai_tool": [[{ "node": "AI Agent", "type": "ai_tool", "index": 0 }]]
}
```

Multiple tools all connect into the same `ai_tool` index 0 — they stack, they don't fan into separate indices. With `n8n_update_partial_workflow` you wire each with an `addConnection` op using `sourceOutput: "ai_tool"`. The agent puts its final answer in **`$json.output`** (not `.text`, not `.response`) — downstream nodes read `{{ $json.output }}`.

See **EXAMPLES.md** for a complete stateless agent-core node-object snippet.

---

## Two non-negotiables

1. **Tool names and descriptions ARE part of the prompt.** The model picks a tool by reading its name and description — nothing else. A tool named `tool1` with an empty description is invisible to the model: it skips it, mis-selects it, or hallucinates parameters. There's usually no error — just an agent that "won't use my tool". Treat both like API design. → **TOOLS.md**
2. **Structured output must parse AND autoFix.** An `outputParserStructured` with `autoFix: true` and a **coding-capable fixer model** is the production pattern. Without autoFix, one malformed JSON response halts the whole workflow. → **STRUCTURED_OUTPUT.md**

---

## Strong defaults

- **Per-tool usage goes in the tool description, not the system prompt.** Anything about *how to call this specific tool* belongs with the tool, so it travels across agents and keeps the system prompt focused. → **SYSTEM_PROMPT.md**
- **Sub-workflow tools (`.toolWorkflow`) for anything multi-step.** Any workflow becomes a tool with typed `$fromAI()` inputs, and composes with branching, error handling, and reuse. Default here when in doubt. → **SUBWORKFLOW_AS_TOOL.md** and **n8n-subworkflows**.
- **Wrap tools with user-visible side effects in human review.** Sends, payments, refunds, account changes get gated behind an approval node so a human signs off before the tool fires. → **HUMAN_REVIEW.md**
- **Raise `maxIterations`.** The default tool-call cap is **low** (single digits on most versions) — fine for a one-tool agent, far too low for a multi-tool agent that chains several calls per turn. It surfaces as "max iterations reached" or empty output. Set `options.maxIterations` to a realistic ceiling (15 for a focused sub-agent, 50-200 for a broad orchestrator).
- **Put the current date in the system prompt** via `{{ $now }}` (or `{{ $now.format('DDDD') }}`). A hardcoded date is stale immediately.

---

## The four tool types

Pick the lightest option that covers the job:

| Tool type | Node | Use when |
|---|---|---|
| **Native tool node** | `slackTool`, `gmailTool`, `toolCalculator`, … | The capability maps to one existing node + one operation. Lowest overhead. |
| **Sub-workflow as tool** | `.toolWorkflow` | More than one node, reusable logic, or you want independent testability. The canonical n8n way — **default when in doubt**. |
| **HTTP Request Tool** | `.toolHttpRequest` | A single external HTTP API the agent should orchestrate directly. Reuse the service's predefined credential to cover operations a native node doesn't expose. |
| **MCP Client Tool** | `.mcpClientTool` | A maintained MCP server already covers it, or you want one published workflow to serve many agents. |

There is also a **Custom Code Tool** (`.toolCode`) for pure inline computation — but its runtime contract (string in / string out, no `$fromAI`, no `$helpers`) is owned by the **n8n-code-tool** skill. Read that before writing one. Rule of thumb: if you find yourself reaching for `$fromAI()` inside the code, you want `.toolWorkflow` instead.

### `$fromAI()`: how the agent fills tool parameters

Tool parameters the agent should decide are wrapped in `$fromAI()`. It is a **real n8n expression helper**, used inside a tool node's parameter expressions:

```
={{ $fromAI('paramName', 'what to put here — be specific: format, range, example', 'string') }}
```

- **paramName** — the name the model uses internally (snake_case or camelCase, be consistent).
- **description** — tells the model what value to produce. **It is part of the prompt** — write it like JSDoc.
- **type** (optional) — `'string'` (default), `'number'`, `'boolean'`, `'json'`. A wrong-typed value fails the call.
- **defaultValue** (optional) — used when the model omits it.

`$fromAI()` carries JSON only — it **cannot carry binary** (no base64, no file bytes). And not every parameter has to be `$fromAI`: plumb identity, authority limits, and correlation IDs (`userId`, refund caps, `sessionId`) deterministically from workflow context so the agent can't get them wrong or even see them. → **TOOLS.md** for the full anatomy and the "give the agent a button, not a steering wheel" pattern.

---

## System prompt vs tool description

| Belongs in the **system prompt** | Belongs in the **tool's description** |
|---|---|
| Persona, role, voice | What this specific tool does |
| Global output/format rules ("respond in markdown") | When to use it vs other tools |
| Refusal / safety behavior | What each parameter means and its shape |
| Display protocols (`![]()` for images) | Examples of good vs bad invocations |
| Universal context (current date via `$now`, user role) | Tool-specific gotchas (rate limits, edge cases) |
| Inter-tool flow ("after generating, always display") | Tool-specific input transformations |

Why split it: a well-described tool works in **any** agent that drops it in, tool details only "load" when the model considers that tool (token efficiency), and you update one tool description instead of a paragraph buried in a 5000-token prompt. → **SYSTEM_PROMPT.md**

---

## Structured output: when and how

Add an `outputParserStructured` sub-node (wired `ai_outputParser`) when downstream needs strict JSON, not free-form text. Two rules:

1. **Use `schemaType: 'manual'` with a real JSON Schema, not `jsonSchemaExample`.** An example can't express required-vs-optional, enums, numeric ranges, or array constraints — you outgrow it the first time the shape gets non-trivial. Reach for `fromJson` + an example only for throwaway shapes.
2. **`autoFix: true` with a coding-capable fixer model.** Wire a *second* model into the parser's `ai_languageModel` slot. Reconciling broken JSON against a schema is a coding task — a weak fixer just produces another malformed retry and burns tokens.

→ **STRUCTURED_OUTPUT.md** for the schema patterns, the load-bearing "DO NOT wrap in markdown" retry line, and the parse-failure cookbook.

---

## Memory: brief mental model

Memory is a sub-node (`ai_memory`). Without it, every call is stateless — correct for one-shot tasks (classify, summarize). With it, the agent holds a conversation, keyed by whatever expression you bind to `sessionKey`.

- **`memoryBufferWindow`** — keeps the last N exchanges per key and persists across executions via n8n's store. The default for chat. **`contextWindowLength` defaults to 5, which is very low** — 50 is a saner starting point. Messages past the window are gone entirely.
- **`memoryPostgresChat` / `memoryRedisChat`** — only when memory must be read *outside* the agent (your own UI, analytics, cross-system). Not needed just to survive restarts; BufferWindow already does that.

**Plumb a stable key from the trigger to memory consistently.** Chat triggers fill `sessionId` automatically; for other surfaces derive one (Slack `thread_ts`, a webhook conversation ID). Never hardcode `sessionId: 'default'` and never put `sessionId` behind `$fromAI` (the model will fabricate a UUID). → **MEMORY.md**

---

## Binary and the agent boundary

This is the seam that trips people up:

- **The model CAN see uploaded images** (vision) via `options.passthroughBinaryImages: true` on the agent.
- **Tools CANNOT receive binary.** `$fromAI()` is JSON-only — no base64, no bytes, even through non-AI bindings.
- **The agent's output is text-shaped** (or structured-text with a parser). When a model returns image/audio/video bytes, the Agent doesn't surface them at all — there's nothing to recover downstream.

**Workaround:** pre-stage uploads to storage before the agent runs, inject the storage keys into the system prompt, and let tools accept the key as a string parameter and re-fetch internally. For one-shot media generation, skip the agent and call the provider's native single-call node directly.

The binary mechanics (which storage, how to stage, how to re-fetch) are owned by **n8n-binary-and-data** — see its agent-tool binary reference. This skill only marks the boundary; don't re-derive the mechanics here.

---

## Human review (gate destructive tools)

When a tool's effect needs human sign-off before execution (sends, payments, refunds, account changes), wrap it with a review tool node — `slackHitlTool`, `discordHitlTool`, `telegramHitlTool`, `gmailHitlTool`, etc. (n8n names these "Hitl" / human-in-the-loop). The review node sits **between** the wrapped tool and the agent on the `ai_tool` connection: wrapped tool → review node → Agent.

Whether sign-off is needed is a product/policy call — **surface the question to the user**, recommend based on blast radius, and let them decide.

**The critical rule: show the actual parameters the wrapped tool will receive.** Use the literal `{{ $tool.parameters.<name> }}` in the approval message, never a `$fromAI()` paraphrase — otherwise the human approves text the model made up, not the call about to fire. → **HUMAN_REVIEW.md**

---

## Chat agents (Slack, Discord, Teams, Telegram)

**The one non-negotiable, regardless of complexity:** any chat-triggered workflow that posts a reply MUST **filter out the bot's own user ID**, or its own replies re-trigger it in an infinite loop that burns runs and tokens. Prefer trigger-level filtering when available (Slack Trigger's `options.userIds` is an **exclusion list** — put the bot ID there); otherwise filter `$json.user !== '<BOT_USER_ID>'` in the first node after the trigger.

Beyond the filter, a simple bot (trigger → agent → reply) lives fine in one workflow. Split into **shell + core + sub-agents** only once you need loading UX, sub-agents, multi-surface reuse, or robust error handling:

- **Shell** — trigger, anti-loop filter, event-type Switch, loading/error UX, renders the reply. No LLM.
- **Core** — stateless agent, `chatInput` + `threadId` inputs, memory keyed on `threadId`, tools and sub-agents.
- **Sub-agents** — one narrow domain each, called via `.toolWorkflow`, **stateless** (full context in `chatInput`).

→ **CHAT_AGENT_PATTERNS.md** for per-surface semantics, threading-as-session, and the full topology.

---

## RAG (retrieval augmented generation)

n8n ships the LangChain RAG primitives (document loaders, splitters, embeddings, vector stores, retrievers). Two opinions worth stating up front:

1. **Rule out cheaper lookups first.** Exact lookups → a database or Data Table query, not RAG. Freshness → a live search tool. A small/structured doc set → give the agent list/fetch tools. Reach for a vector store only when there are too many docs to list and queries are semantic.
2. **Wire the vector store as a retrieval tool** (`mode: 'retrieve-as-tool'`, `ai_tool`) so the agent decides when retrieval is relevant and can phrase the query itself. Embed query and documents with the **same** model.

→ **RAG.md** (intentionally thin — defaults depend on data shape and scale).

---

## Reference files

| File | Read when |
