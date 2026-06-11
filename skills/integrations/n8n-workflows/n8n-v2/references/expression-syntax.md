# n8n Expression Syntax Guide

Complete reference for expressions used in n8n workflows. Expressions allow dynamic values in node parameters using `={{ expression }}` syntax.

## Table of Contents

- [Basic Syntax](#basic-syntax)
- [Cross-Node References](#cross-node-references)
- [String Operations](#string-operations)
- [Conditional Expressions](#conditional-expressions)
- [Array Operations](#array-operations)
- [Object Operations](#object-operations)
- [Date/Time Operations](#datetime-operations)
- [Regular Expressions](#regular-expressions)
- [Number Operations](#number-operations)
- [JSON Operations](#json-operations)
- [Input Access Functions](#input-access-functions)
- [Common Patterns](#common-patterns)
- [Expressions in Different Node Types](#expressions-in-different-node-types)
- [Debugging Expressions](#debugging-expressions)

---

## Basic Syntax

### Accessing Current Item

```javascript
{{ $json.fieldName }}          // Get field from current item
{{ $json['field name'] }}      // Field with spaces or special characters
{{ $json.nested.field }}       // Nested field access
{{ $json.array[0] }}           // Array element by index
{{ $json.object.nested.deep }} // Deep nested access
```

### Data Types

All JavaScript data types are supported:

```javascript
{{ $json.stringField }}        // String
{{ $json.numberField }}        // Number
{{ $json.booleanField }}       // Boolean
{{ $json.objectField }}        // Object
{{ $json.arrayField }}         // Array
{{ $json.nullField }}          // null
```

### Expression Prefix

Expressions MUST start with `=` in node configuration:

```javascript
// In node parameter
"value": "={{ $json.field }}"        // Expression (evaluated)
"value": "static text"               // Literal (not evaluated)
"url": "=https://api.com/{{ $json.id }}"  // Expression with text
```

---

## Cross-Node References

### Access Another Node's Output

```javascript
// First item from named node
{{ $('Node Name').item.json.field }}
{{ $('Node Name').first().json.field }}

// All items from named node
{{ $('Node Name').all() }}

// Specific item by index
{{ $('Node Name').item(0).json.field }}
{{ $('Node Name').item(1).json.field }}

// Check if node has data
{{ $('Node Name').itemMatching(0) }}
```

**Real example from workflow:**
```javascript
// Access data prepared before Wait node
const preparedData = $('Prepare Review').first().json;
const stories = preparedData.stories;
```

### Access Node Parameters

```javascript
{{ $parameter.workflowId }}     // Node parameter value
{{ $parameter.fieldName }}      // Any configured parameter
```

### Access Workflow Information

```javascript
{{ $workflow.id }}              // Current workflow ID
{{ $workflow.name }}            // Current workflow name
{{ $workflow.active }}          // Is workflow active
```

---

## String Operations

### Concatenation

```javascript
// Using + operator
{{ "Hello " + $json.name }}

// Using template literals
{{ `${$json.firstName} ${$json.lastName}` }}
{{ `Score: ${$json.score}` }}
```

### String Methods

```javascript
{{ $json.text.toLowerCase() }}
{{ $json.text.toUpperCase() }}
{{ $json.text.trim() }}
{{ $json.text.substring(0, 100) }}
{{ $json.text.slice(0, 100) }}
{{ $json.text.replace('old', 'new') }}
{{ $json.text.split(',') }}
{{ $json.text.includes('keyword') }}
{{ $json.text.startsWith('prefix') }}
{{ $json.text.endsWith('suffix') }}
{{ $json.text.length }}
```

### Template Literals

```javascript
// Dynamic URLs
={{ `https://api.com/item/${$json.id}` }}
={{ `https://example.com/user/${$json.username}/posts` }}

// Formatted strings
={{ `Score: ${$json.score}, Rank: ${$json.rank}` }}
={{ `Posted ${$json.commentsCount} comments` }}
```

### Real Example - URL Construction

```javascript
// Hacker News item URL
={{ $json.url || `https://news.ycombinator.com/item?id=${$json.id}` }}
```

---

## Conditional Expressions

### Ternary Operator

```javascript
// Basic ternary
{{ $json.score > 50 ? 'High' : 'Low' }}

// With computations
{{ $json.points > 100 ? $json.points * 2 : $json.points }}

// Nested ternary
{{ $json.score > 100 ? 'Excellent' : $json.score > 50 ? 'Good' : 'Poor' }}
```

### Logical OR for Defaults

```javascript
// Fallback to default
{{ $json.url || 'https://example.com' }}
{{ $json.title || 'Untitled' }}
{{ $json.score || 0 }}

// Chain multiple fallbacks
{{ $json.description || $json.summary || $json.title || 'No description' }}
```

### Nullish Coalescing

```javascript
// Use ?? for null/undefined only (not empty string or 0)
{{ $json.value ?? 'default' }}
```

### Optional Chaining

```javascript
// Safe property access
{{ $json.user?.email }}
{{ $json.settings?.theme?.color }}

// With fallback
{{ $json.user?.email ?? 'no-email@example.com' }}
```

---

## Array Operations

### Array Methods

```javascript
// Length
{{ $json.items.length }}

// Join
{{ $json.tags.join(', ') }}

// Map
{{ $json.items.map(x => x.name) }}
{{ $json.items.map(x => x.price * 1.1) }}

// Filter
{{ $json.items.filter(x => x.score > 50) }}
{{ $json.items.filter(x => x.active === true) }}

// Find
{{ $json.items.find(x => x.id === 123) }}
{{ $json.items.find(x => x.name === 'target') }}

// Some/Every
{{ $json.items.some(x => x.urgent) }}
{{ $json.items.every(x => x.validated) }}

// Sort
{{ $json.items.sort((a, b) => b.score - a.score) }}

// Slice
{{ $json.items.slice(0, 5) }}  // First 5 items
```

### Real Example - Extract Hashtags

```javascript
// Match all hashtags
{{ $json.text.match(/#\w+/g) }}

// Join as string
{{ $json.text.match(/#\w+/g)?.join(' ') || '' }}
```

---

## Object Operations

### Access Properties

```javascript
// Dot notation
{{ $json.user.email }}
{{ $json.settings.notifications.email }}

// Bracket notation (for special characters)
{{ $json['field-with-dashes'] }}
{{ $json['field with spaces'] }}
{{ $json['2024-data'] }}  // Starts with number
```

### Object Methods

```javascript
// Get keys
{{ Object.keys($json) }}
{{ Object.keys($json.settings) }}

// Get values
{{ Object.values($json) }}

// Get entries
{{ Object.entries($json) }}
```

---

## Date/Time Operations

### Current Time

```javascript
// Current timestamp
{{ new Date().toISOString() }}
{{ Date.now() }}  // Unix timestamp (ms)

// Formatted date
{{ new Date().toLocaleDateString() }}
{{ new Date().toLocaleTimeString() }}
```

### Parse and Format

```javascript
// Parse date string to ISO
{{ new Date($json.timestamp).toISOString() }}

// Convert Unix timestamp (seconds) to ISO
={{ new Date($json.time * 1000).toISOString() }}

// Get timestamp
{{ new Date($json.pubDate).getTime() }}
```

### Date Calculations

```javascript
// Age in hours
{{ (Date.now() - new Date($json.timestamp).getTime()) / (1000 * 60 * 60) }}

// Age in days
{{ (Date.now() - new Date($json.timestamp).getTime()) / (1000 * 60 * 60 * 24) }}

// Add days
{{ new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString() }}
```

### Real Example - Time-based Scoring

```javascript
// Recent = higher score
const ageHours = (Date.now() - new Date($json.timestamp).getTime()) / (1000 * 60 * 60);
const recencyScore = ageHours < 6 ? 3 : ageHours < 24 ? 2 : ageHours < 48 ? 1 : 0;
```

---

## Regular Expressions

### Pattern Matching

```javascript
// In Filter node
"operation": "regex",
"value2": "(?i)(AI|machine learning|automation)"

// In Code node
const match = $json.title.match(/(?i)(AI|ML|automation)/);
if (match) {
  // Keyword found
}

// Test pattern
{{ /pattern/.test($json.field) }}

// Extract matches
{{ $json.text.match(/\d+/g) }}  // All numbers
{{ $json.text.match(/@\w+/g) }}  // All @mentions
```

### Case-Insensitive Flag

```javascript
// (?i) at start of pattern for case-insensitive
"(?i)(keyword1|keyword2)"

// Or use /i flag
/keyword/i.test($json.text)
```

### Real Example - Keyword Filtering

```javascript
// Multiple keywords, case-insensitive
"value2": "(?i)(AI|machine learning|automation|n8n|workflow|API)"
```

---

## Number Operations

### Math Operations

```javascript
// Basic arithmetic
{{ $json.score * 2 }}
{{ $json.price + $json.tax }}
{{ $json.total / $json.count }}
{{ $json.quantity - $json.used }}

// Math functions
{{ Math.round($json.value) }}
{{ Math.floor($json.value) }}
{{ Math.ceil($json.value) }}
{{ Math.max($json.a, $json.b) }}
{{ Math.min($json.a, $json.b) }}
{{ Math.abs($json.value) }}
{{ Math.pow($json.base, 2) }}
{{ Math.sqrt($json.value) }}
```

### Number Formatting

```javascript
// Fixed decimals
{{ $json.price.toFixed(2) }}

// Parse string to number
{{ parseInt($json.stringNumber) }}
{{ parseFloat($json.stringDecimal) }}
{{ Number($json.stringValue) }}
```

---

## JSON Operations

### Parse and Stringify

```javascript
// Parse JSON string
{{ JSON.parse($json.jsonString) }}

// Stringify object
{{ JSON.stringify($json.object) }}

// Stringify with formatting
{{ JSON.stringify($json.object, null, 2) }}
```

### Quote Filter

For embedding strings in JSON bodies:

```json
"jsonBody": "={\n  \"content\": {{ $json.text | quote }}\n}"
```

The `| quote` filter properly escapes strings for JSON.

---

## Input Access Functions

### In Code Nodes

```javascript
// Get all input items
$input.all()
// Returns: [{ json: {...} }, { json: {...} }, ...]

// Get first item
$input.first()
// Returns: { json: {...} }

// Get last item
$input.last()

// Get current item in iteration
$input.item

// Access JSON directly
$input.first().json.field
```

### Return Format Requirement

Code nodes MUST return array of objects with `json` property:

```javascript
// Correct
return [{ json: { result: 'data' } }];

// Multiple items
return [
  { json: { id: 1 } },
  { json: { id: 2 } }
];

// Transform all
return $input.all().map(item => ({
  json: {
    ...item.json,
    processed: true
  }
}));

// Wrong (will fail)
return { result: 'data' };
return 'data';
```

---

## Common Patterns

### URL Normalization

```javascript
// Normalize URL for comparison
const normalizedUrl = $json.url
  .toLowerCase()
  .replace(/^https?:\/\/(www\.)?/, '')
  .replace(/\/$/, '');
```

### Field with Fallback Chain

```javascript
// Try multiple fields
{{ $json.description || $json.summary || $json.title || 'No description' }}
{{ $json.image || $json.thumbnail || $json.icon || '/default.png' }}
```

### Conditional Field Access

```javascript
// Check existence before access
{{ $json.user ? $json.user.email : 'No email' }}

// Optional chaining (safer)
{{ $json.user?.email ?? 'No email' }}
```

### LinkedIn Member URN Format

```javascript
// Convert member ID to URN format
`urn:li:person:${$json.sub}`

// Example: { "sub": "abc123" } → "urn:li:person:abc123"
```

### Extract Domain from URL

```javascript
// In Code node
const domain = new URL($json.url).hostname.replace(/^www\./, '');

// In expression
{{ new URL($json.url).hostname }}
```

### Score Normalization

```javascript
// Normalize different scoring systems to 0-1
const normalized = $json.score / 100;

// Or to 0-10 scale
const scaled = ($json.score / $json.maxScore) * 10;
```

---

## Expressions in Different Node Types

### Set Node

```json
{
  "assignments": {
    "assignments": [
      {
        "name": "title",
        "value": "={{ $json.headline }}",
        "type": "string"
      }
    ]
  }
}
```

### HTTP Request URL

```json
{
  "url": "=https://api.example.com/item/{{ $json.id }}.json"
}
```

### HTTP Request JSON Body

```json
{
  "jsonBody": "={{ JSON.stringify({ query: $json.searchTerm }) }}"
}
```

### Filter Conditions

```json
{
  "conditions": {
    "number": [
      {
        "value1": "={{ $json.score }}",
        "operation": "larger",
        "value2": 20
      }
    ]
  }
}
```

### Wait Node Form Description

Supports markdown:

```json
{
  "formDescription": "## Story Title\n\n{{ $json.title }}\n\n**URL:** {{ $json.url }}\n\n**Score:** {{ $json.score }}"
}
```

Dynamic content from previous node:

```json
{
  "formDescription": "={{ $json.storyList }}"
}
```

### IF Node Conditions

```json
{
  "conditions": {
    "string": [
      {
        "value1": "={{ $json['Action'] }}",
        "operation": "equals",
        "value2": "Approve"
      }
    ]
  }
}
```

### Code Node

NO `={{ }}` needed in Code nodes - write plain JavaScript:

```javascript
// Direct JavaScript
const input = $input.first().json;
const result = input.score * 2;
return [{ json: { doubled: result } }];
```

---

## Debugging Expressions

### View Expression Results

1. Execute the node
2. Click node to view output
3. Check "Output" tab for results
4. Inspect data structure

### Common Errors

**Undefined field:**
```javascript
{{ $json.nonexistent }}  // Returns undefined
```

**Type mismatch:**
```javascript
{{ $json.stringNumber + 5 }}  // May concatenate instead of add
{{ Number($json.stringNumber) + 5 }}  // Correct
```

**Syntax error:**
```javascript
{{ $json.field }}  // Correct
{{ $json.field }  // Wrong - missing closing brace
```

**Cross-node reference before execution:**
```javascript
{{ $('Node Name').item.json.field }}
// Error if "Node Name" hasn't executed yet
```

### Safe Field Access

```javascript
// Use optional chaining
{{ $json.user?.email ?? 'default@example.com' }}

// Or ternary
{{ $json.user ? $json.user.email : 'default@example.com' }}

// Or logical OR (but treats empty string as falsy)
{{ $json.email || 'default@example.com' }}
```

### Type Checking

```javascript
// Check if field exists
{{ $json.field !== undefined }}

// Check type
{{ typeof $json.field === 'string' }}

// Check if array
{{ Array.isArray($json.field) }}
```

---

## Performance Tips

1. **Simple expressions in Set nodes**, complex logic in Code nodes
   - Set node: `={{ $json.field.toUpperCase() }}`
   - Code node: Complex transformations, loops, multiple operations

2. **Avoid repeated cross-node access**
   ```javascript
   // Bad - accesses node 3 times
   {{ $('Node').item.json.a + $('Node').item.json.b + $('Node').item.json.c }}

   // Good - use Code node
   const data = $('Node').first().json;
   const sum = data.a + data.b + data.c;
   ```

3. **Cache computed values**
   ```javascript
   // In Code node, compute once
   const normalized = $input.all().map(item => ({
     json: {
       ...item.json,
       normalizedUrl: normalizeUrl(item.json.url)
     }
   }));
   ```

4. **Use Code nodes for loops** rather than complex array expressions

---

## See Also

- `references/node-library.md` - Node-specific expression usage
- `code-snippets/` - Reusable expression patterns
- `assets/examples/` - Real workflow examples
- [n8n Expression Documentation](https://docs.n8n.io/code-examples/expressions/)
