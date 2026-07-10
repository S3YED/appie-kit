---
name: n8n-code-tool
description: Write JavaScript or Python for the n8n Custom Code Tool (@n8n/n8n-nodes-langchain.toolCode) — the AI-agent-callable tool, NOT the workflow Code node. Use when building a Code Tool attached to an AI Agent, writing code that an LLM will invoke, parsing the `query` input, returning a string result, defining an input schema for structured arguments (specifyInputSchema, jsonSchemaExample, DynamicStructuredTool), or troubleshooting errors like "Wrong output type returned", "No execution data available", "The response property should be a string, but it is an object", "Cannot assign to read only property 'name'", or an AI agent that refuses to call the tool. Covers the critical differences between Code node and Code Tool: return format (string vs `[{json:{...}}]`), unavailability of `$fromAI`/`$input`/`$helpers` in the Code Tool sandbox, naming rules for AI invocation, and when to use `toolWorkflow`/HTTP Request Tool instead.
---

# n8n Custom Code Tool

Expert guidance for writing code inside `@n8n/n8n-nodes-langchain.toolCode` — the tool an AI Agent can invoke, **not** the regular workflow Code node.

---

## ⚠️ This is NOT the Code node

The Custom Code Tool looks like a Code node in the editor — same JavaScript editor, similar layout — but it is a **completely different node** from a different package with a **different runtime contract**.

| | Code node | Custom Code Tool |
|---|---|---|
| **Node type** | `n8n-nodes-base.code` | `@n8n/n8n-nodes-langchain.toolCode` |
| **Package** | `n8n-nodes-base` | `@n8n/n8n-nodes-langchain` |
| **Invoked by** | Previous node (workflow flow) | AI Agent (LangChain) |
| **Input** | `$input.all()` — item stream | `query` — string or object from LLM |
| **Return** | `[{json: {...}}]` (items array) | **A string** |
| **`$fromAI()`** | N/A | **Not available** (see Errors) |
| **HTTP helper** | `this.helpers.httpRequest` (auth helpers blocked) | Not exposed to the tool sandbox |
| **State** | Per-run execution data | No `getContext`, no `$getWorkflowStaticData` |

**If you treat it like a Code node, it fails.** The rest of this skill covers the Code Tool's actual contract.

---

## Quick Start

### Minimal JavaScript Code Tool

```javascript
// `query` is whatever the AI sent (a string by default)
return `You asked: ${query}`;
```

### Minimal Python Code Tool

```python
# `_query` is whatever the AI sent (a string by default)
return f"You asked: {_query}"
```

### Essential Rules

1. **Return a string.** Numbers are auto-converted. Anything else throws `"The response property should be a string, but it is an object"`.
2. **Input variable is fixed**: `query` (JS), `_query` (Python). You cannot rename it.
3. **Do NOT use `$fromAI()`** inside the Code Tool sandbox — it throws `"No execution data available"`.
4. **Do NOT use `[{json: {...}}]`** return format — that's for Code nodes. Throws `"Wrong output type returned"`.
5. **Use a descriptive tool name** (letters/numbers/underscores, v1.1+). The agent calls the tool by its name.
6. **Write a precise description** — the LLM decides whether to invoke the tool based on it.

---

## The Two Input Modes

The Code Tool has two input shapes, controlled by `specifyInputSchema`:

### Mode 1: Unstructured (default, `specifyInputSchema: false`)

The AI passes **a single string** as `query`. If you need multiple fields, the AI has to stuff them into that one string and you parse them out. In practice, LLMs will happily pass a JSON string if your description tells them to.

```javascript
// Parse a JSON string the AI sent
let params;
try {
  params = typeof query === 'string' ? JSON.parse(query) : query;
} catch (e) {
  throw new Error('Expected a JSON object. Parser said: ' + e.message);
}
const price = Number(params.price);
const months = Number(params.months);
// ...
return JSON.stringify({ monthly_payment: /* ... */ });
```

**Pros**: simplest to set up, one field to describe.
**Cons**: no schema validation — if the LLM forgets a field, the tool throws at runtime.

**Best for**: quick prototypes, tools with one natural input (a question, a URL, a text blob).

### Mode 2: Structured (`specifyInputSchema: true`)

The tool becomes a LangChain `DynamicStructuredTool`. The LLM sees a typed argument schema and passes a **validated object** as `query`. You access fields directly.

```javascript
// query is now an object matching your schema
const price = query.price;
const months = query.months;
const residual_percent = query.residual_percent;

const monthly = computeAnnuity(price, months, residual_percent);
return JSON.stringify({ monthly_payment: monthly });
```

Schema is defined via either:
- `schemaType: "fromJson"` + `jsonSchemaExample` (n8n v≥1.3) — paste an example JSON, n8n infers the schema
- `schemaType: "manual"` + `inputSchema` — write a full JSON Schema yourself

**Pros**: LLM gets type hints, invalid calls rejected before your code runs, cleaner code.
**Cons**: a little more setup; requires n8n version with schema support.

**Best for**: production tools with multiple typed parameters (calculators, API wrappers, anything with numeric fields the LLM tends to stringify).

**See**: [INPUT_SCHEMA.md](INPUT_SCHEMA.md) for complete schema setup.

---

## Return Format

**The return value must be a string.** The LLM reads it as the tool's observation.

```javascript
// ✅ String
return "42";

// ✅ Number (auto-converted to string by n8n)
return 42;

// ✅ JSON-encoded structured result (recommended for rich output)
return JSON.stringify({ result: 42, currency: "SEK" });

// ❌ Raw object → "The response property should be a string, but it is an object"
return { result: 42 };

// ❌ Workflow item format → "Wrong output type returned"
return [{ json: { result: 42 } }];

// ❌ Array → "The response property should be a string, but it is an object"
return [1, 2, 3];
```

### Best practice: JSON-stringify structured results

When your tool has more than a trivial scalar output, return a JSON string:

```javascript
return JSON.stringify({
  monthly_payment_sek: 5405,
  loan_amount: 351920,
  total_cost_of_credit: 63295
});
```

The LLM parses JSON reliably and can pick the fields it needs to present to the user.

### Error handling: the agent reads your failures

Errors don't just stop the workflow — they go back to the LLM, which usually corrects its call and retries. Use that:

```javascript
// Option A: throw — n8n surfaces the message to the agent
if (!isFinite(price)) throw new Error('price must be a number, e.g. 439900');

// Option B: return an error string — agent reads it like any tool result
if (!isFinite(price)) return JSON.stringify({ error: 'price must be a number, e.g. 439900' });
```

Either way, write error messages **for the LLM**: state what was wrong and what a valid call looks like. A bare `throw new Error('invalid input')` wastes the retry; an instructive message usually fixes the next call.

---

## Tool Name and Description

These fields are NOT documentation — they are the **tool contract the LLM sees**. Treat them as prompt engineering.

### Name
- Must match `[A-Za-z0-9_]+` (v1.1+). No spaces, no hyphens, no emoji.
- Use a verb-y descriptive name: `calculate_car_loan`, `get_weather`, `search_orders`.
- The agent calls the tool by this name. `Code Tool` (the default) is useless — the agent won't know when to call it.

### Description
- Explain **when** to use it and **what** to send.
- If unstructured mode, **include an example of the JSON string** the LLM should send.
- If structured mode, the schema speaks for itself — just describe purpose.

**Unstructured example (JSON-in-string pattern):**
```
Deterministiskt beräknar månadskostnad för billån. Anropa med EN JSON-sträng:
{"price":439900,"down_payment":87980,"interest_rate":6.95,"months":36,"residual_percent":50}
Fält: price (SEK), down_payment (SEK), interest_rate (% per år), months, residual_percent (0-99).
```

**Structured example (schema-defined):**
```
Deterministically computes the monthly car-loan payment given price, down payment, 
annual interest rate, term, and residual percent. Use whenever the user asks for 
monthly cost, total credit cost, or loan breakdown.
```

---

## Top Errors and Fixes

### Error 1: `"There was an error: 'Cannot assign to read only property \"name\" of object: Error: No execution data available'"`

**Cause**: you called `$fromAI()` inside the Code Tool sandbox.
