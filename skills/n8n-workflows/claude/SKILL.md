---
name: claude
description: Claude Code-specific n8n v2.0 workflow reference. Use when building n8n workflows — creating workflow JSON, implementing Wait node approval flows, troubleshooting Execute Sub-Workflow issues, setting up API credentials, building orchestrator patterns, using expressions, or any n8n workflow task.
compatibility: Designed for Claude Code
---

# n8n v2.0 Workflow Development (Claude Code)

This is the Claude Code-specific version of the n8n-v2-workflow skill. References point to the shared `references/` and `../code-snippets/` directories in the parent skill folder.

## Critical: No Execute Command Node

The `n8n-nodes-base.executeCommand` node is **NOT available** in the default n8n container image. Do NOT use it in any workflow.

Instead, use **Code nodes** (JavaScript) with the Node.js `fs` module for all file operations:
- `fs.readdirSync()` instead of `find` / `ls`
- `fs.readFileSync()` instead of `cat`
- `fs.writeFileSync()` instead of `echo >`
- `fs.renameSync()` instead of `mv`
- `fs.existsSync()` instead of `test -f`

## Overview

Comprehensive reference for building n8n workflows using v2.0 patterns and best practices. This skill provides complete documentation for nodes, expressions, patterns, troubleshooting, and production-ready examples.

---

## Quick Start Guide

### 1. Test APIs First
```bash
curl -X GET "https://api.example.com/endpoint" \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Create Workflow JSON
Generate workflow JSON with nodes and connections.

### 3. Import into n8n
n8n UI > Settings > Import from File

### 4. Configure & Fix
- Replace Execute Sub-Workflow nodes (if needed)
- Configure credentials
- Test each node

### 5. Test Execution
Use MCP server `mcp__n8n__execute_workflow` or manual trigger

---

## Core Concepts

### n8n MCP Server Integration

**What it CAN do:**
- ✅ Search workflows
- ✅ View workflow details
- ✅ Execute workflows

**What it CANNOT do:**
- ❌ Create workflows
- ❌ Modify workflows
- ❌ Manage credentials

**Workaround:** Generate JSON files, import via UI

📖 **Deep dive:** [references/mcp-limitations.md](../references/mcp-limitations.md)

---

### Node Library

Complete reference for all n8n nodes:

**Trigger Nodes:** Manual Trigger, Execute Workflow Trigger
**Data Processing:** Code, Set, Merge, Filter, Split in Batches
**Flow Control:** IF, Wait
**Integration:** HTTP Request, RSS Feed Read
**Action:** Execute Workflow, Respond to Webhook

Each node documented with configuration examples, parameters, and patterns.

📖 **Complete reference:** [references/node-library.md](../references/node-library.md)

---

### Expression Syntax

Dynamic values in node parameters using `={{ expression }}`:

```javascript
{{ $json.field }}                      // Current item
{{ $('Node Name').first().json.field }} // Cross-node
{{ $json.url || 'default' }}           // Fallback
{{ new Date().toISOString() }}         // Date/time
`urn:li:person:${$json.sub}`          // Template literal
```

📖 **Complete guide:** [references/expression-syntax.md](../references/expression-syntax.md)

---

## Common Workflows

### Human-in-the-Loop Approval

Use **Wait nodes** with forms (NOT respondToWebhook):

```
Trigger → Generate Content → Wait Node (form) → IF → Action
```

📖 **Complete patterns:** [references/wait-nodes-guide.md](../references/wait-nodes-guide.md)

---

### Multi-Workflow Orchestration

Orchestrator coordinates sub-workflows:

```
Main Orchestrator
├── Trigger
├── Execute Sub-Workflow: Data Fetcher
├── Wait Node: Review
├── Execute Sub-Workflow: Processor
└── Execute Sub-Workflow: Output
```

📖 **All patterns:** [references/workflow-patterns.md](../references/workflow-patterns.md)

---

### News Aggregation

Multi-source data fetch, normalize, merge, deduplicate, rank:

```
Trigger
├── HTTP Request: Source 1 → Normalize
├── HTTP Request: Source 2 → Normalize
└── RSS Feed: Source 3 → Normalize
    → Merge → Deduplicate → Rank
```

📖 **Detailed patterns:** [references/workflow-patterns.md](../references/workflow-patterns.md#news-aggregation-pattern)

---

### AI Content Generation

Sub-workflow pattern for AI content:

```
Execute Workflow Trigger
→ Code: Build Prompt
→ HTTP Request: AI API
→ Code: Extract Response
```

📖 **Implementation:** [references/workflow-patterns.md](../references/workflow-patterns.md#content-generation-with-ai-pattern)

---

## Critical Issues & Solutions

### Execute Sub-Workflow "Out of Date" Error

**Problem:** Imported nodes show error after import

**Solution:**
1. Delete old Execute Sub-Workflow nodes
2. Add fresh nodes from palette
3. Select "Database" and choose workflow

📖 **Detailed troubleshooting:** [references/execute-sub-workflow-issues.md](../references/execute-sub-workflow-issues.md)

---

### Wait Node Not Pausing

❌ **Wrong:** respondToWebhook, Set nodes, IF on unset fields
✅ **Correct:** Wait node with `resume: "form"`

📖 **Complete guide:** [references/wait-nodes-guide.md](../references/wait-nodes-guide.md)

---

### LinkedIn `unauthorized_scope_error`

❌ Turn OFF both: "Organization Support" and "Legacy" toggles

📖 **All auth issues:** [references/api-credentials.md](../references/api-credentials.md)

---

## Templates & Examples

### Basic Templates
