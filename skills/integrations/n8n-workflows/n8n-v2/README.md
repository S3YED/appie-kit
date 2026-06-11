# n8n v2.0 Workflow Skill for Claude Code

> **Comprehensive n8n 2.0 workflow development reference for Claude Code**

[![n8n Version](https://img.shields.io/badge/n8n-v2.0-orange?style=for-the-badge)](https://n8n.io/)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blueviolet?style=for-the-badge)](https://claude.com/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

## What is This?

This is a **production-ready skill for Claude Code** that provides complete n8n 2.0 workflow development expertise. Use this when building n8n workflows with Claude Code to get comprehensive guidance, working examples, and reusable code patterns.

### Why "v2.0"?

n8n 2.0 introduced **significant breaking changes** from pre-2.0 versions:
- New node versioning system
- Redesigned Execute Workflow node (now "Execute Sub-Workflow")
- Updated expression syntax and variable access
- New Wait node capabilities for human-in-the-loop workflows
- Changed credential handling

**This skill is specifically designed for n8n v2.0+** and includes solutions to v2.0-specific challenges.

---

## Features

### Comprehensive Documentation
- **Node Library** - Complete reference for all n8n v2.0 nodes with configuration examples
- **Expression Syntax Guide** - Master n8n's `{{ expression }}` patterns and cross-node data access
- **Workflow Patterns** - Proven architectures: orchestrator, sub-workflows, human-in-the-loop, data aggregation
- **API Credentials Setup** - LinkedIn OAuth2, Anthropic API, NewsAPI, and more
- **Troubleshooting Guide** - Solutions to common n8n v2.0 issues

### Production-Ready Examples
- **News Aggregation Workflow** - Multi-source fetch, normalize, merge, deduplicate, rank
- **AI Content Generation** - Sub-workflow pattern with Anthropic Claude API integration
- **LinkedIn Member ID Retrieval** - Get your LinkedIn URN for API calls
- **Multi-Source Deduplication** - Merge and deduplicate data from multiple sources

### Reusable Code Library
JavaScript snippets for n8n Code nodes:
- **Deduplication** - By URL, title, ID, or multiple fields
- **Ranking Algorithms** - Multi-factor scoring (relevance, recency, engagement)
- **Data Normalization** - Unify data from different API sources
- **Form Data Preparation** - Format data for Wait node forms
- **Cross-Node Data Access** - Reference data from other nodes safely

### Critical Issue Solutions
- **Execute Sub-Workflow "Out of Date" Error** - Complete fix procedure
- **Wait Nodes Not Pausing** - Correct human-in-the-loop patterns
- **MCP Server Limitations** - What the n8n MCP server can/cannot do
- **LinkedIn `unauthorized_scope_error`** - Credential configuration fixes

---

## Installation

### For Claude Code Users

1. **Install the skill:**
   ```bash
   # Clone this repository
   git clone https://github.com/splinesreticulating/n8n-v2-workflow-skill.git

   # Copy to your Claude skills directory
   cp -r n8n-v2-workflow-skill ~/.claude/skills/n8n-v2
   ```

2. **Use the skill:**
   The skill activates automatically when you ask Claude Code to help with n8n workflows. Trigger phrases include:
   - "Create an n8n workflow that..."
   - "Help me build an n8n workflow for..."
   - "How do I use Wait nodes in n8n?"
   - "Fix my Execute Sub-Workflow node error"

3. **Browse the documentation:**
   Start with [`SKILL.md`](SKILL.md) for the complete reference guide.

---

## Quick Start

### 1. Test Your API First
Before creating workflows, test endpoints:
```bash
curl -X GET "https://api.example.com/endpoint" \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Create Workflow JSON
Use Claude Code to generate workflow JSON with proper n8n v2.0 node structures.

### 3. Import into n8n
- Open n8n UI
- Settings > Import from File
- Select your workflow JSON

### 4. Configure & Fix
- Replace Execute Sub-Workflow nodes (known v2.0 issue)
- Configure credentials
- Test each node

### 5. Execute
Use the n8n MCP server or manual trigger to run your workflow.

---

## What's Included

### Documentation (`/references`)
- `node-library.md` - All n8n v2.0 nodes documented
- `expression-syntax.md` - Complete expression guide
- `workflow-patterns.md` - Common architectures
- `wait-nodes-guide.md` - Human-in-the-loop patterns
- `api-credentials.md` - Authentication setup
- `mcp-limitations.md` - MCP server constraints
- `execute-sub-workflow-issues.md` - Sub-workflow troubleshooting
- `troubleshooting.md` - Common issues and solutions

### Code Snippets (`/code-snippets`)
Reusable JavaScript for Code nodes:
- `deduplication.js` - Remove duplicates by various fields
- `ranking-algorithms.js` - Multi-factor ranking
- `data-normalization.js` - Unify data from different sources
- `form-data-preparation.js` - Format data for Wait node forms
- `cross-node-data-access.js` - Reference data from other nodes

### Workflow Examples (`/assets`)

**Templates** (`/assets/templates`) - Basic structures:
- `wait-node-approval-template.json` - Human-in-the-loop starter
- `orchestrator-template.json` - Multi-workflow coordinator
- `sub-workflow-template.json` - Reusable sub-workflow

**Complete Examples** (`/assets/examples`) - Production-ready:
- `news-aggregation-workflow.json` - Multi-source aggregation with ranking
- `content-generation-workflow.json` - AI content generation sub-workflow
- `linkedin-member-id-workflow.json` - Get LinkedIn member URN
- `multi-source-deduplication-workflow.json` - Merge and deduplicate pattern

---

## n8n v2.0 Breaking Changes Addressed

This skill specifically handles n8n v2.0 changes:

### Execute Sub-Workflow Nodes
**Problem:** Imported Execute Sub-Workflow nodes show "out of date" errors in v2.0

**Solution:** Documented replacement procedure in `references/execute-sub-workflow-issues.md`

### Wait Node Forms
**Problem:** Pre-2.0 patterns (respondToWebhook, Set nodes) don't pause execution in v2.0

**Solution:** Complete Wait node form patterns in `references/wait-nodes-guide.md`

### Expression Syntax
**Problem:** Some pre-2.0 expression patterns don't work in v2.0

**Solution:** Comprehensive v2.0 expression guide in `references/expression-syntax.md`

### Node Versioning
**Problem:** Node type versions changed in v2.0

**Solution:** All examples use correct v2.0 node versions (documented in `references/node-library.md`)

---

## Use Cases

This skill excels at:

1. **Creating workflow JSON files** for import into n8n v2.0
2. **Implementing human-in-the-loop workflows** with Wait nodes and forms
3. **Troubleshooting Execute Sub-Workflow** "out of date" errors
4. **Setting up API credentials** (LinkedIn OAuth2, Anthropic, NewsAPI)
5. **Building orchestrator patterns** with sub-workflows
6. **Writing expressions** for dynamic node parameters
7. **Understanding MCP server limitations** and workarounds
8. **Any n8n v2.0 workflow development task**

---

## MCP Server Integration

If you have the n8n MCP server configured with Claude Code:

**What it CAN do:**
- ✅ Search workflows
- ✅ View workflow details
- ✅ Execute workflows

**What it CANNOT do:**
- ❌ Create workflows
- ❌ Modify workflows
- ❌ Manage credentials

**Workaround:** Generate JSON files with Claude Code, import via n8n UI.

See [`references/mcp-limitations.md`](references/mcp-limitations.md) for details.

---

## Examples

### Quick Example: Human-in-the-Loop Approval

```javascript
// Wait node configuration (v2.0 pattern)
{
  "type": "n8n-nodes-base.wait",
  "parameters": {
    "resume": "form",
    "form": {
      "formTitle": "Approve Content",
      "formDescription": "Review the generated content",
      "formFields": {
        "values": [
          {
            "fieldLabel": "Approval",
            "fieldType": "dropdown",
            "fieldOptions": {
              "values": [
                {"option": "Approve"},
                {"option": "Reject"}
              ]
            },
            "requiredField": true
          }
        ]
      }
    }
  }
}

// Access form data in next node
const approval = $json['Approval'];  // "Approve" or "Reject"
```

### Quick Example: Deduplication

```javascript
// Remove duplicates by normalized URL
const items = $input.all();
const seen = new Set();
const unique = [];

for (const item of items) {
  const url = item.json.url
    .toLowerCase()
    .replace(/^https?:\/\/(www\.)?/, '')
    .replace(/\/$/, '');

  if (!seen.has(url)) {
    seen.add(url);
    unique.push(item);
  }
}

return unique;
```

---

## Contributing

Contributions are welcome! Please:

1. **Focus on n8n v2.0+** - This skill is specifically for v2.0 and later
2. **Test your workflows** - Ensure examples work in current n8n versions
3. **Document thoroughly** - Include clear explanations and comments
4. **Follow the structure** - Keep the progressive disclosure pattern

### Areas for Contribution
- Additional workflow examples
- More code snippets for common operations
- Troubleshooting solutions for new issues
- Documentation improvements
- Support for newer n8n v2.x features

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Resources

### Official n8n Documentation
- [n8n Documentation](https://docs.n8n.io/)
- [Execute Sub-Workflow Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/)
- [Sub-workflows Guide](https://docs.n8n.io/flow-logic/subworkflows/)
- [Wait Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/)

### This Skill's Documentation
Start here: [`SKILL.md`](SKILL.md)

---

## FAQ

**Q: Will this work with n8n pre-2.0?**
A: No, this skill is specifically designed for n8n v2.0+. Pre-2.0 has different node structures and patterns.

**Q: Do I need the n8n MCP server?**
A: No, the MCP server is optional. This skill helps generate workflow JSON files that you import via the n8n UI.

**Q: Can Claude Code create workflows directly in my n8n instance?**
A: Not yet - the n8n MCP server can only view and execute workflows, not create or modify them. Claude Code generates JSON files that you import manually.

**Q: What if my Execute Sub-Workflow nodes show errors after import?**
A: This is a known v2.0 issue. See [`references/execute-sub-workflow-issues.md`](references/execute-sub-workflow-issues.md) for the fix procedure.

**Q: Are these workflow examples production-ready?**
A: Yes! All examples in `/assets/examples/` are complete, tested workflows that you can import and use immediately (after configuring credentials).

---

**Made with Claude Code** | **n8n v2.0+** | **MIT Licensed**
