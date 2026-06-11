# Execute Workflow Node Issues

## Node Naming Clarification

**Important:** In n8n v2.0+, the Execute Workflow node:
- **Node type in JSON**: Still `n8n-nodes-base.executeWorkflow` (unchanged)
- **UI label**: Changed to "Execute Sub-Workflow" in the node palette
- **Functionality**: Same as before - executes other workflows

**This is NOT an error:** Having `"type": "n8n-nodes-base.executeWorkflow"` in your JSON is correct for v2.0.

## The Problem

When importing workflows via JSON, Execute Workflow nodes **sometimes** show an error after import.

**Error message**: "This node is out of date. Please upgrade by removing it and adding a new one"

**When this happens:**
- After importing a workflow JSON file into n8n
- The node appears in the workflow with an error indicator
- The workflow cannot execute until the node is fixed

**When this does NOT happen:**
- When reviewing JSON files (the JSON itself is fine)
- When the node type is `n8n-nodes-base.executeWorkflow` (this is correct)

## Why This Happens

The Execute Workflow node configuration structure can become incompatible during import/export cycles, especially:
- When importing workflows exported from different n8n versions
- When node internal structure has changed between versions
- When workflow references become stale

## Solution

**If you see the "out of date" error after importing:**

1. Import the workflow JSON (Execute Workflow nodes may show errors)
2. Delete the old Execute Workflow nodes showing errors
3. Add fresh "Execute Sub-Workflow" nodes from the node palette (they use the same `executeWorkflow` type)
4. Select "Database" as source
5. Choose the target workflow from the dropdown

## Best Practice

When creating workflow JSON files for import:
- **Option 1**: Include Execute Workflow nodes normally - they usually import fine
- **Option 2**: If you experience import issues, omit these nodes and add them manually after import
- **Option 3**: Document which nodes might need recreation after import

## Identifying Execute Workflow Nodes in JSON

**Correct node structure in v2.0:**

```json
{
  "parameters": {
    "source": "database",
    "workflowId": "={{ $('Select Workflow').item.json.workflowId }}"
  },
  "name": "Execute Sub-Workflow",
  "type": "n8n-nodes-base.executeWorkflow",
  "typeVersion": 1,
  "position": [820, 300]
}
```

**Key points:**
- `"type": "n8n-nodes-base.executeWorkflow"` is correct (not "executeSubWorkflow")
- `"name"` can be anything (commonly "Execute Sub-Workflow" or "Execute Workflow")
- UI shows this as "Execute Sub-Workflow" in the palette, but JSON type is unchanged

## When to Recreate These Nodes

**Recreate only if:**
- ✅ You see "This node is out of date" error after importing
- ✅ The node shows a red error indicator in the workflow
- ✅ The workflow execution fails with this node

**Do NOT recreate if:**
- ❌ You only see `executeWorkflow` in the JSON (this is normal)
- ❌ The node is working fine after import
- ❌ You're just reviewing the JSON file before importing

## See Also

- `references/node-library.md` - Complete Execute Workflow node documentation
- `references/workflow-patterns.md` - Orchestrator patterns using Execute Workflow nodes
