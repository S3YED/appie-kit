# n8n Workflow Patterns

## Orchestrator Pattern

Use a main orchestrator workflow to coordinate multiple sub-workflows.

### Benefits

- Separation of concerns
- Reusable sub-workflows
- Easier testing and debugging
- Clear workflow organization

### Structure

```
Main Orchestrator
├── Trigger (Schedule, Webhook, Manual)
├── Execute Sub-Workflow: Data Fetcher
├── Wait Node: Human Review
├── Execute Sub-Workflow: Data Processor
└── Execute Sub-Workflow: Output Handler
```

### Example: Content Generation Pipeline

```
Main Orchestrator
├── Schedule Trigger (daily at 9am)
├── Execute Sub-Workflow: News Fetcher
├── Wait Node: Review News Items
├── Execute Sub-Workflow: Content Generator
├── Wait Node: Approve Content
└── Execute Sub-Workflow: Social Media Poster
```

## Sub-Workflow Pattern

Create focused, single-purpose workflows that can be reused.

### Guidelines

- Each sub-workflow should do one thing well
- Accept inputs via workflow execution
- Return outputs for the parent workflow
- Handle errors gracefully with error workflows

### Input/Output

Sub-workflows receive data from parent workflows:

```javascript
// In sub-workflow, access parent data
$input.all()
```

Return data to parent:

```javascript
// Last node output is returned to parent
return [{
  json: {
    result: "processed data",
    status: "success"
  }
}];
```

## Human-in-the-Loop Pattern

Use Wait nodes to pause workflows for human input.

See [wait-nodes-guide.md](wait-nodes-guide.md) for detailed Wait node configuration.

### Basic Flow

```
Trigger
├── Fetch/Generate Data
├── Wait Node: Review & Approve
├── IF Node: Check Approval
│   ├── Approved → Continue
│   └── Rejected → End or Loop
└── Execute Action
```

## Data Aggregation Pattern

Combine data from multiple sources and deduplicate.

### Example Structure

```
Trigger
├── HTTP Request: Source 1
├── HTTP Request: Source 2
├── HTTP Request: Source 3
├── Merge Node (combine all)
├── Code Node: Deduplicate
└── Code Node: Rank/Score
```

### Deduplication Logic

```javascript
// Deduplicate by URL
const seen = new Set();
const unique = [];

for (const item of items) {
  const normalizedUrl = item.url.toLowerCase().replace(/\/$/, '');
  if (!seen.has(normalizedUrl)) {
    seen.add(normalizedUrl);
    unique.push(item);
  }
}

return unique.map(item => ({ json: item }));
```

## Error Handling Pattern

Handle errors gracefully in workflows.

### Error Workflow

Create a dedicated error workflow:

```
Error Trigger
├── Code Node: Format Error Message
├── Send Notification (Email, Slack, etc.)
└── Log to Database
```

Link error workflow in node settings:
- Settings → Error Workflow → Select your error workflow

## Testing Pattern

Test APIs and data sources before building full workflows.

### Recommended Approach

1. **Test via Bash/curl first**
   ```bash
   curl -X GET "https://api.example.com/endpoint" \
     -H "Authorization: Bearer $TOKEN"
   ```

2. **Verify response format**
   - Check field names
   - Understand data structure
   - Test authentication

3. **Then create workflow JSON**
   - Now you know exactly what fields to use
   - Avoid import → test → fail → fix cycles

## News Aggregation Pattern

Fetch data from multiple sources, normalize to common schema, merge, and deduplicate.

### Complete Flow

```
Trigger
├── HTTP Request: Hacker News API
│   └── Set: Normalize to common schema
├── HTTP Request: NewsAPI
│   └── Set: Normalize to common schema
├── RSS Feed Read: Blog
│   └── Set: Normalize to common schema
└── Merge (append mode)
    ├── Code: Deduplicate by URL
    ├── Code: Rank/Score items
    └── Filter: Top N items
```

### Key Steps

**1. Fetch from multiple sources in parallel**

All HTTP Request and RSS nodes execute simultaneously for faster aggregation.

**2. Normalize each source to common schema**

Each source outputs different field names. Use Set node immediately after each source:

```json
// Common schema
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

**3. Merge all normalized data**

Merge node combines all sources into single array.

**4. Deduplicate**

Use Code node to remove duplicates by normalized URL.

**5. Rank/Score**

Calculate relevance score based on keywords, recency, and engagement.

**See:** `assets/examples/news-aggregation-workflow.json` for complete implementation

---

## Content Generation with AI Pattern

Generate content using AI API (Anthropic, OpenAI, etc.) within workflow.

### Structure

```
Execute Workflow Trigger (receives input data)
├── Code: Build prompt from input
├── HTTP Request: Call AI API
├── Code: Extract and format response
└── Return result to parent
```

### Implementation Details

**1. Build prompt dynamically**

```javascript
// In Code node
const input = $input.first().json;

const prompt = `Create a LinkedIn post about: ${input.title}

URL: ${input.url}
Summary: ${input.summary}

Requirements:
- Professional tone
- 2-3 paragraphs
- Include relevant hashtags`;

return [{
  json: {
    prompt,
    title: input.title
  }
}];
```

**2. Call AI API**

```json
{
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
  "jsonBody": "={{ JSON.stringify({\n  model: 'claude-3-5-sonnet-20241022',\n  max_tokens: 400,\n  temperature: 0.7,\n  messages: [{\n    role: 'user',\n    content: $json.prompt\n  }]\n}) }}"
}
```

**3. Extract response**

```javascript
// In Code node
const response = $input.first().json;
const generatedText = response.content[0].text;

return [{
  json: {
    generatedContent: generatedText,
    model: response.model,
    usage: response.usage
  }
}];
```

**See:** `assets/examples/content-generation-workflow.json`

---

## Scoring and Ranking Pattern

Calculate relevance scores and rank items.

### Multi-Factor Ranking

Combine multiple factors with weighted scores:

```javascript
// In Code node
const items = $input.all().map(item => item.json);

// Configuration
const config = {
  highValueKeywords: ['ai', 'automation', 'n8n'],
  mediumValueKeywords: ['technology', 'workflow', 'integration'],
  weights: {
    relevance: 0.5,
    recency: 0.3,
    engagement: 0.2
  }
};

// Score each item
const scoredItems = items.map(item => {
  let relevanceScore = 0;
  let recencyScore = 0;
  let engagementScore = 0;

  // Relevance scoring (keyword matching)
  const text = (item.title + ' ' + item.summary).toLowerCase();
  config.highValueKeywords.forEach(keyword => {
    if (text.includes(keyword)) relevanceScore += 3;
  });
  config.mediumValueKeywords.forEach(keyword => {
    if (text.includes(keyword)) relevanceScore += 1;
  });

  // Recency scoring (time-based)
  const ageHours = (Date.now() - new Date(item.timestamp).getTime()) / (1000 * 60 * 60);
  if (ageHours < 6) recencyScore = 3;
  else if (ageHours < 24) recencyScore = 2;
  else if (ageHours < 48) recencyScore = 1;

  // Engagement scoring
  const score = item.score || 0;
  if (score > 100) engagementScore = 3;
  else if (score > 50) engagementScore = 2;
  else if (score > 20) engagementScore = 1;

  // Calculate weighted final score
  const finalScore =
    (relevanceScore * config.weights.relevance) +
    (recencyScore * config.weights.recency) +
    (engagementScore * config.weights.engagement);

  return {
    ...item,
    finalScore,
    relevanceScore,
    recencyScore,
    engagementScore
  };
});

// Sort by score (descending)
const ranked = scoredItems.sort((a, b) => b.finalScore - a.finalScore);

return ranked.map(item => ({ json: item }));
```

**See:** `code-snippets/ranking-algorithms.js` for reusable implementation

---

## Connection Patterns

How nodes connect in workflows.

### Sequential Pattern

Linear flow, one node after another:

```
Node A → Node B → Node C → Node D
```

**JSON structure:**
```json
{
  "connections": {
    "Node A": {
      "main": [[{"node": "Node B", "type": "main", "index": 0}]]
    },
    "Node B": {
      "main": [[{"node": "Node C", "type": "main", "index": 0}]]
    }
  }
}
```

---

### Parallel Pattern

Multiple nodes execute simultaneously:

```
           ┌→ Node B
Trigger ───┼→ Node C → Merge
           └→ Node D
```

**JSON structure:**
```json
{
  "connections": {
    "Trigger": {
      "main": [[
        {"node": "Node B", "type": "main", "index": 0},
        {"node": "Node C", "type": "main", "index": 0},
        {"node": "Node D", "type": "main", "index": 0}
      ]]
    },
    "Node B": {
      "main": [[{"node": "Merge", "type": "main", "index": 0}]]
    },
    "Node C": {
      "main": [[{"node": "Merge", "type": "main", "index": 1}]]
    },
    "Node D": {
      "main": [[{"node": "Merge", "type": "main", "index": 2}]]
    }
  }
}
```

**Benefits:**
- Faster execution (simultaneous)
- Independent operations
- Merge combines results

---

### Conditional Branching Pattern

IF node creates true/false paths:

```
               ┌→ True Path → Action A
IF Node ───────┤
               └→ False Path → Action B
```

**JSON structure:**
```json
{
  "connections": {
    "IF Node": {
      "main": [
        [{"node": "Action A", "type": "main", "index": 0}],  // True (index 0)
        [{"node": "Action B", "type": "main", "index": 0}]   // False (index 1)
      ]
    }
  }
}
```

---

### Loop Pattern

Split in Batches creates loop:

```
Split in Batches → Process Item → HTTP Request ─┐
       ↑                                         │
       └─────────────────────────────────────────┘
       ↓ (after all batches)
Continue Workflow
```

**Use case:** Process large arrays in smaller chunks

---

## Complete Workflow Examples

Comprehensive, production-ready workflow JSONs:

- `assets/examples/news-aggregation-workflow.json` - Multi-source aggregation with deduplication
- `assets/examples/content-generation-workflow.json` - AI content generation sub-workflow
- `assets/examples/multi-source-deduplication-workflow.json` - Focused deduplication example
- `assets/examples/linkedin-member-id-workflow.json` - LinkedIn member ID retrieval

---

## Documentation References

- [Execute Sub-Workflow Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/)
- [Sub-workflows Guide](https://docs.n8n.io/flow-logic/subworkflows/)
- [Wait Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/)

---

## See Also

- `code-snippets/deduplication.js` - Reusable deduplication code
- `code-snippets/ranking-algorithms.js` - Scoring and ranking implementations
- `code-snippets/data-normalization.js` - Common normalization patterns
- `references/node-library.md` - Individual node documentation
- `references/expression-syntax.md` - Expression patterns used in workflows
