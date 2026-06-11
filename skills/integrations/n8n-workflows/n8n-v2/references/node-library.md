# n8n Node Library Reference

Complete reference for nodes used in n8n v2.0 workflows. Each node includes configuration examples, parameters, use cases, and patterns extracted from production workflows.

## Table of Contents

- [Trigger Nodes](#trigger-nodes)
- [Data Processing Nodes](#data-processing-nodes)
- [Flow Control Nodes](#flow-control-nodes)
- [Integration Nodes](#integration-nodes)
- [Action Nodes](#action-nodes)
- [Node Versioning](#node-versioning)
- [Node Positioning](#node-positioning)

---

## Trigger Nodes

### Manual Trigger

**Type:** `n8n-nodes-base.manualTrigger` (v1)

Starts workflow manually from the n8n UI.

**Use cases:**
- Testing workflows during development
- On-demand execution
- Debugging workflow logic

**Configuration:**
```json
{
  "parameters": {},
  "name": "Manual Trigger",
  "type": "n8n-nodes-base.manualTrigger",
  "typeVersion": 1,
  "position": [240, 400]
}
```

**Parameters:** None required

**Output:** Empty object `{}`

**Common pattern:** Use as starting point for workflows during development, then replace with appropriate trigger (Schedule, Webhook, etc.) for production.

---

### Execute Workflow Trigger

**Type:** `n8n-nodes-base.executeWorkflowTrigger` (v1)

Receives input from parent workflow when this workflow is called as a sub-workflow.

**Use cases:**
- Sub-workflows called by orchestrators
- Reusable workflow components
- Modular workflow architecture

**Configuration:**
```json
{
  "parameters": {},
  "name": "Execute Workflow Trigger",
  "type": "n8n-nodes-base.executeWorkflowTrigger",
  "typeVersion": 1,
  "position": [240, 300]
}
```

**Parameters:** None required

**Accessing parent data:**
```javascript
// In Code node after this trigger
$input.all()          // Get all items from parent
$input.first().json   // Get first item data
```

**Output:** Passes through data from parent workflow

**Pattern:** Sub-workflows that process data and return results to orchestrator.

---

## Data Processing Nodes

### Code Node

**Type:** `n8n-nodes-base.code` (v2)

Execute JavaScript to transform, filter, or process data.

**Use cases:**
- Complex data transformation
- Deduplication logic
- Ranking and scoring algorithms
- Custom business logic
- Array manipulation

**Configuration:**
```json
{
  "parameters": {
    "jsCode": "// Your JavaScript code\nreturn $input.all();"
  },
  "name": "Process Data",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [460, 300]
}
```

**Key parameters:**
- `jsCode`: JavaScript code to execute (string)

**Available variables:**
```javascript
$input.all()                    // Array of all input items
$input.first()                  // First input item
$input.last()                   // Last input item
$input.item                     // Current item in iteration
$json                          // Current item's JSON data
$('Node Name').first().json    // Reference another node
$('Node Name').all()           // All items from another node
```

**Return format:**
Must return array of objects with `json` property:
```javascript
return [
  { json: { field: 'value1' } },
  { json: { field: 'value2' } }
];

// Single item
return [{ json: resultObject }];

// Transform all items
return $input.all().map(item => ({
  json: {
    ...item.json,
    newField: 'computed value'
  }
}));
```

**Example - Deduplication:**
```javascript
const items = $input.all();
const seen = new Set();
const unique = [];

for (const item of items) {
  const key = item.json.url.toLowerCase();
  if (!seen.has(key)) {
    seen.add(key);
    unique.push(item);
  }
}

return unique;
```

**Example - Data extraction:**
```javascript
// Extract specific fields
const items = $input.all();
return items.map(item => ({
  json: {
    title: item.json.title,
    url: item.json.url,
    score: item.json.score || 0
  }
}));
```

**See also:** `code-snippets/` for reusable patterns

---

### Set Node

**Type:** `n8n-nodes-base.set` (v3.3)

Create or modify fields in data items. Primary tool for data normalization.

**Use cases:**
- Normalizing data from different sources to common schema
- Adding computed fields
- Renaming fields
- Setting constant values
- Type conversion

**Configuration:**
```json
{
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "id": "title",
          "name": "title",
          "value": "={{ $json.headline }}",
          "type": "string"
        },
        {
          "id": "score",
          "name": "score",
          "value": "={{ $json.points }}",
          "type": "number"
        },
        {
          "id": "source",
          "name": "source",
          "value": "Hacker News",
          "type": "string"
        }
      ]
    },
    "options": {}
  },
  "name": "Normalize Data",
  "type": "n8n-nodes-base.set",
  "typeVersion": 3.3,
  "position": [680, 300]
}
```

**Key parameters:**
- `assignments.assignments`: Array of field mappings
  - `id`: Internal identifier
  - `name`: Output field name
  - `value`: Expression or literal value
  - `type`: Data type (string, number, boolean, object, array)

**Expression patterns:**
```javascript
// Static value
"value": "Hacker News"

// Map from existing field
"value": "={{ $json.title }}"

// With fallback
"value": "={{ $json.url || 'https://example.com' }}"

// Computed
"value": "={{ $json.score * 2 }}"

// Type conversion
"value": "={{ new Date($json.time * 1000).toISOString() }}"
```

**Common pattern - Data normalization:**

When aggregating from multiple sources, normalize each source to common schema:

```
HN API → Set Node (normalize to common schema)
NewsAPI → Set Node (normalize to common schema)
RSS Feed → Set Node (normalize to common schema)
           ↓
      Merge Node
```

Common schema example:
```json
{
  "title": "string",
  "url": "string",
  "source": "string",
  "score": "number",
  "comments": "number",
  "timestamp": "ISO date string",
  "summary": "string"
}
```

---

### Merge Node

**Type:** `n8n-nodes-base.merge` (v2.1)

Combine data from multiple inputs into single output.

**Use cases:**
- Aggregating data from multiple sources
- Combining parallel processing branches
- Joining related data

**Modes:**
- `append`: Combine all items into one list (most common)
- `combine`: Pair items from input 1 and 2
- `choose`: Pick one input or the other
- `multiplex`: Create cartesian product

**Configuration (append mode):**
```json
{
  "parameters": {
    "mode": "append"
  },
  "name": "Merge All Sources",
  "type": "n8n-nodes-base.merge",
  "typeVersion": 2.1,
  "position": [1560, 400]
}
```

**Connection pattern:**

Multiple nodes connect to Merge as inputs:
```
Source 1 ──┐
Source 2 ──┼─→ Merge Node → Combined Output
Source 3 ──┘
```

Input indices (0, 1, 2...) increment automatically for each connection.

**Common pattern - Multi-source aggregation:**
```
HTTP Request (HN) ──┐
HTTP Request (API) ──┼─→ Merge (append) → Deduplicate → Process
RSS Feed Read ───────┘
```

---

### Filter Node

**Type:** `n8n-nodes-base.filter` (v2)

Keep only items that match specified conditions.

**Use cases:**
- Filtering by field values
- Removing invalid/incomplete data
- Keyword matching
- Quality control
- Threshold filtering

**Configuration:**
```json
{
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{ $json.title }}",
          "operation": "regex",
          "value2": "(?i)(AI|machine learning|automation)"
        }
      ],
      "number": [
        {
          "value1": "={{ $json.score }}",
          "operation": "larger",
          "value2": 20
        }
      ]
    }
  },
  "name": "Filter Stories",
  "type": "n8n-nodes-base.filter",
  "typeVersion": 2,
  "position": [1120, 240]
}
```

**Condition types:**

**String operations:**
- `contains`: Substring match
- `equals`: Exact match
- `notEquals`: Not equal
- `regex`: Regular expression
- `startsWith`: Begins with
- `endsWith`: Ends with

**Number operations:**
- `equals`, `notEquals`
- `larger`, `largerEqual`
- `smaller`, `smallerEqual`

**Boolean operations:**
- `equals`, `notEquals`

**DateTime operations:**
- `after`, `before`, `between`

**Regex example:**
```javascript
// Case-insensitive keyword matching
"value2": "(?i)(AI|ML|automation|n8n)"

// URL pattern
"value2": "^https://.*\\.com$"
```

**Multiple conditions:** All conditions must match (AND logic). For OR logic, use multiple Filter nodes in parallel or use Code node.

---

### Split in Batches Node

**Type:** `n8n-nodes-base.splitInBatches` (v3)

Process large arrays in smaller chunks, creating a loop.

**Use cases:**
- API rate limiting (process N items at a time)
- Memory management for large datasets
- Batch API requests
- Progressive processing

**Configuration:**
```json
{
  "parameters": {
    "batchSize": 30,
    "options": {}
  },
  "name": "Batch Process Items",
  "type": "n8n-nodes-base.splitInBatches",
  "typeVersion": 3,
  "position": [680, 240]
}
```

**Key parameters:**
- `batchSize`: Number of items per batch (e.g., 10, 30, 50)

**How it works:**

1. Splits input array into batches
2. Processes first batch
3. Loop continues for next batch
4. When all batches complete, workflow proceeds

**Loop structure:**
```
Split in Batches → Process Batch → HTTP Request ─┐
       ↑                                          │
       └──────────────────────────────────────────┘
```

Downstream nodes must connect back to Split in Batches for loop continuation.

**Common pattern - Rate-limited API calls:**
```
Get IDs (100 items) → Split in Batches (10) → HTTP Request → Process
```
Processes 10 items at a time instead of overwhelming API with 100 requests.

---

## Flow Control Nodes

### IF Node

**Type:** `n8n-nodes-base.if` (v2)

Branch workflow based on conditions.

**Use cases:**
- Approval/rejection flows
- Conditional processing
- Error handling
- Data routing
- Status checking

**Configuration:**
```json
{
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{ $json['Action'] }}",
          "operation": "equals",
          "value2": "Approve"
        }
      ]
    }
  },
  "name": "Check Approval",
  "type": "n8n-nodes-base.if",
  "typeVersion": 2,
  "position": [1560, 400]
}
```

**Outputs:**
- Output 0 (true branch): Condition matched
- Output 1 (false branch): Condition not matched

**Connection structure:**
```json
"connections": {
  "IF Node": {
    "main": [
      [{ "node": "Approved Action", "type": "main", "index": 0 }],
      [{ "node": "Rejected Action", "type": "main", "index": 0 }]
    ]
  }
}
```

**Accessing Wait node form data:**
```javascript
// Check dropdown selection
"value1": "={{ $json['Approval Status'] }}"

// Check text input
"value1": "={{ $json['Comments'] }}"
```

**Multiple conditions:** Supports string, number, boolean, dateTime conditions. All must match (AND logic).

**Common pattern - Human approval:**
```
Wait Node (form) → IF Node → True: Post to API
                           → False: Send notification
```

---

### Wait Node

**Type:** `n8n-nodes-base.wait` (v1.1)

Pause workflow execution until resume condition is met.

**Use cases:**
- Human approval workflows
- Form submissions
- Manual review gates
- Scheduled delays
- Webhook callbacks

**Resume modes:**
- `form`: Human fills out form (most common)
- `webhook`: External system sends webhook
- `after`: Time-based delay

**Configuration (form mode):**
```json
{
  "parameters": {
    "resume": "form",
    "form": {
      "formTitle": "Review Content",
      "formDescription": "Please review and approve:",
      "formFields": {
        "values": [
          {
            "fieldLabel": "Action",
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
  },
  "name": "Wait for Approval",
  "type": "n8n-nodes-base.wait",
  "typeVersion": 1.1,
  "position": [900, 400]
}
```

**Field types:**
- `dropdown`: Select from options
- `text`: Single-line text input
- `textarea`: Multi-line text input
- `number`: Numeric input
- `date`: Date picker

**Accessing form data:**

After Wait node resumes, access submitted values in next node:
```javascript
// In expression
{{ $json['Action'] }}
{{ $json['Comments'] }}

// In Code node
const action = $json['Action'];
const comments = $json['Comments'];
```

**IMPORTANT:** Wait node actually pauses execution. Do NOT use:
- respondToWebhook (doesn't pause)
- Set nodes with manual notes (doesn't pause)
- IF nodes checking fields that were never set (doesn't pause)

**See:** `references/wait-nodes-guide.md` for complete documentation

---

## Integration Nodes

### HTTP Request Node

**Type:** `n8n-nodes-base.httpRequest` (v4.2)

Make HTTP API calls to any REST endpoint.

**Use cases:**
- Fetching data from APIs
- Posting data to external systems
- Webhook calls
- Any HTTP-based integration

**Configuration (GET request):**
```json
{
  "parameters": {
    "url": "https://api.example.com/data",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "httpHeaderAuth",
    "options": {}
  },
  "name": "Fetch Data",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [460, 400]
}
```

**Configuration (POST with JSON body):**
```json
{
  "parameters": {
    "method": "POST",
    "url": "https://api.anthropic.com/v1/messages",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "anthropicApi",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "anthropic-version",
          "value": "2023-06-01"
        }
      ]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify($json.requestData) }}",
    "options": {}
  },
  "name": "Call Anthropic API",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [680, 300]
}
```

**Key parameters:**
- `method`: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- `url`: Can use expressions for dynamic URLs
- `authentication`: none, predefinedCredentialType, genericCredentialType
- `nodeCredentialType`: Type of credential (httpHeaderAuth, oAuth2Api, etc.)
- `sendHeaders`: true to add custom headers
- `headerParameters`: Array of header name/value pairs
- `sendBody`: true for POST/PUT/PATCH
- `specifyBody`: json, form, raw
- `jsonBody`: JSON body as string or expression

**Dynamic URL:**
```javascript
"url": "=https://api.example.com/item/{{ $json.id }}.json"
```

**Authentication types:**
- Header Auth: API keys in headers
- OAuth2: For LinkedIn, Google, etc.
- Basic Auth: Username/password
- None: For public APIs

**Response access:**
```javascript
{{ $json.responseField }}      // API response data
{{ $statusCode }}              // HTTP status code (200, 201, etc.)
```

**Common pattern - Check status:**
```
HTTP Request → IF Node (check $statusCode === 201) → Success/Failure branches
```

**See:** `references/api-credentials.md` for credential setup

---

### RSS Feed Read Node

**Type:** `n8n-nodes-base.rssFeedRead` (v1)

Fetch and parse RSS/Atom feeds.

**Use cases:**
- Blog aggregation
- News monitoring
- Content curation
- Feed-based workflows

**Configuration:**
```json
{
  "parameters": {
    "url": "https://blog.n8n.io/rss/",
    "options": {}
  },
  "name": "Read Blog Feed",
  "type": "n8n-nodes-base.rssFeedRead",
  "typeVersion": 1,
  "position": [460, 560]
}
```

**Key parameters:**
- `url`: RSS feed URL

**Output fields:**
- `title`: Article title
- `link`: Article URL
- `pubDate`: Publication date
- `contentSnippet`: Text excerpt
- `content`: Full content (HTML)
- `creator`: Author name
- `categories`: Article categories/tags

**Common pattern - Normalize after read:**
```
RSS Feed Read → Set Node (normalize to common schema) → Merge with other sources
```

Example normalization:
```json
{
  "name": "title",
  "value": "={{ $json.title }}",
  "type": "string"
},
{
  "name": "url",
  "value": "={{ $json.link }}",
  "type": "string"
},
{
  "name": "timestamp",
  "value": "={{ $json.pubDate }}",
  "type": "string"
},
{
  "name": "source",
  "value": "Blog RSS",
  "type": "string"
}
```

---

## Action Nodes

### Execute Workflow Node

**Type:** `n8n-nodes-base.executeWorkflow` (v1)

**UI Label:** "Execute Sub-Workflow" (in node palette)

**Important:** In n8n v2.0+, this node is labeled "Execute Sub-Workflow" in the UI, but the node type in JSON remains `n8n-nodes-base.executeWorkflow`. This is normal and correct.

Call another workflow as a sub-workflow.

**Use cases:**
- Orchestrator patterns
- Workflow reuse
- Modular workflow architecture
- Breaking complex workflows into manageable pieces

**Configuration:**
```json
{
  "parameters": {
    "workflowId": "={{ $parameter.workflowId }}",
    "options": {}
  },
  "name": "Execute Sub-Workflow",
  "type": "n8n-nodes-base.executeWorkflow",
  "typeVersion": 1,
  "position": [680, 400]
}
```

**Source selection:**
- `database`: Select workflow from dropdown (recommended for production)
- `localFile`: Use workflow file
- `parameter`: Dynamic workflow ID via expression

**Import Issue:** When importing workflow JSON, Execute Workflow nodes **sometimes** show "out of date" error after import.

**When this happens:**
- The node appears with a red error indicator after importing
- Error message: "This node is out of date. Please upgrade by removing it and adding a new one"
- This does NOT mean the JSON is wrong - the node type `executeWorkflow` is correct

**Workaround if you see the error:**
1. Import workflow JSON
2. Delete Execute Workflow nodes showing errors (not all of them, only ones with errors)
3. Add fresh "Execute Sub-Workflow" nodes from palette (same type, just recreated)
4. Select "Database" as source
5. Choose target workflow from dropdown

**Best practice:** 
- Include Execute Workflow nodes normally in your JSON - they usually import fine
- If you frequently have import issues, consider omitting these nodes and adding manually

**Data flow:**
```
Orchestrator: Execute Workflow Node (passes data)
                      ↓
Sub-workflow: Execute Workflow Trigger (receives data)
                      ↓
              Process data
                      ↓
              Return result (last node output)
                      ↓
Orchestrator: Receives result from Execute Workflow Node
```

**See:** `references/execute-sub-workflow-issues.md` for detailed troubleshooting

---

### Respond to Webhook Node

**Type:** `n8n-nodes-base.respondToWebhook` (v1)

Send HTTP response back to webhook caller.

**Use cases:**
- Webhook-based workflows
- API endpoints
- Synchronous responses to HTTP requests

**Configuration:**
```json
{
  "parameters": {
    "respondWith": "json",
    "responseBody": "={{ $json }}",
    "options": {}
  },
  "name": "Respond to Webhook",
  "type": "n8n-nodes-base.respondToWebhook",
  "typeVersion": 1,
  "position": [900, 400]
}
```

**Key parameters:**
- `respondWith`: json, text, html
- `responseBody`: Data to return
- `responseCode`: HTTP status code (default 200)

**IMPORTANT:** This node does NOT pause workflow execution. It returns a response immediately while the workflow continues.

**For human input, use Wait nodes instead.**

**Anti-pattern:**
```
❌ Webhook Trigger → Respond to Webhook (asking for input)
```
This returns immediately - user never gets to provide input.

**Correct pattern:**
```
✅ Webhook Trigger → Wait Node (form) → Process → Respond to Webhook
```

---

## Node Versioning

Nodes have `typeVersion` indicating schema version:

**Common versions:**
- manualTrigger: v1
- executeWorkflowTrigger: v1
- httpRequest: v4.2
- code: v2
- set: v3.3
- merge: v2.1
- filter: v2
- if: v2
- wait: v1.1
- splitInBatches: v3
- rssFeedRead: v1
- executeWorkflow: v1

**Version compatibility:**

When importing workflows, n8n usually auto-upgrades node versions. Exception: Execute Workflow nodes often require manual recreation.

**Check version:** Look at `typeVersion` in node configuration.

---

## Node Positioning

Nodes are positioned on 2D canvas using `[x, y]` coordinates (pixels).

**Conventions:**
- **Horizontal flow:** Increase x by ~220 per node
- **Parallel branches:** Vary y coordinate
- **Grid alignment:** Use multiples of 20

**Example positions:**
```
Trigger:        [240, 400]
Process:        [460, 400]
Decision (IF):  [680, 400]
  ├─ True:      [900, 300]
  └─ False:     [900, 500]
Continue:       [1120, 400]
```

**Visual layout:**
```
Start → Process → Decision ┬→ Branch A → Merge
                           └→ Branch B ──┘
```

Positioning doesn't affect execution - it's purely for visual organization.

---

## See Also

- `references/expression-syntax.md` - Using expressions in node parameters
- `references/workflow-patterns.md` - How nodes connect in common patterns
- `code-snippets/` - Reusable Code node implementations
- `assets/examples/` - Complete workflow examples
- `references/wait-nodes-guide.md` - Detailed Wait node documentation
- `references/execute-sub-workflow-issues.md` - Troubleshooting Execute Workflow
- `references/api-credentials.md` - Setting up authentication
