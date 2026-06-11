# Wait Nodes for Human-in-the-Loop Workflows

## The Right Way: Wait Nodes

For workflows that need human approval or input, use **Wait nodes** with "Resume: On Form Submitted".

### Key Features

- **Actually pauses execution** until the form is submitted
- **Form fields**: dropdowns, text inputs, number inputs, etc.
- **Data access**: Submitted values available in next node via `$json['Field Name']`

### Configuration Structure

```json
{
  "type": "n8n-nodes-base.wait",
  "parameters": {
    "resume": "form",
    "form": {
      "formTitle": "Title shown to user",
      "formDescription": "Instructions (supports markdown)",
      "formFields": {
        "values": [
          {
            "fieldLabel": "Field Name",
            "fieldType": "dropdown",
            "fieldOptions": {
              "values": [
                {"option": "Option 1"},
                {"option": "Option 2"}
              ]
            },
            "requiredField": true
          }
        ]
      }
    }
  }
}
```

### Field Types

- `dropdown` - Select one option from a list
- `text` - Single-line text input
- `textarea` - Multi-line text input
- `number` - Numeric input
- `date` - Date picker

### Accessing Form Data

After the Wait node resumes, access submitted values in the next node:

```javascript
// In a Code node or expression
$json['Field Name']  // Gets the submitted value

// Example: Check approval status
if ($json['Approval Status'] === 'Approved') {
  // Continue with approved workflow
}
```

## Wrong Approaches (Don't Use)

These patterns do NOT pause execution:

❌ **respondToWebhook nodes** - These return a response but don't pause the workflow
❌ **Set nodes with manual notes** - Notes like "MANUAL STEP: Edit this node" don't stop execution
❌ **IF nodes checking fields that were never set** - The workflow continues immediately with empty/null values

## Common Use Cases

### Content Approval

```json
{
  "formTitle": "Review Generated Content",
  "formDescription": "## Generated LinkedIn Post\n\n{{ $json.generated_post }}\n\n**Approve or request edits:**",
  "formFields": {
    "values": [
      {
        "fieldLabel": "Action",
        "fieldType": "dropdown",
        "fieldOptions": {
          "values": [
            {"option": "Approve and Post"},
            {"option": "Edit Content"},
            {"option": "Reject"}
          ]
        },
        "requiredField": true
      },
      {
        "fieldLabel": "Edited Content",
        "fieldType": "textarea",
        "requiredField": false
      }
    ]
  }
}
```

### Data Validation

```json
{
  "formTitle": "Verify Extracted Data",
  "formDescription": "Please verify the extracted information is correct:",
  "formFields": {
    "values": [
      {
        "fieldLabel": "Name",
        "fieldType": "text",
        "requiredField": true
      },
      {
        "fieldLabel": "Email",
        "fieldType": "text",
        "requiredField": true
      },
      {
        "fieldLabel": "Confirmed",
        "fieldType": "dropdown",
        "fieldOptions": {
          "values": [
            {"option": "Yes"},
            {"option": "No, needs correction"}
          ]
        },
        "requiredField": true
      }
    ]
  }
}
```

## All Field Types with Examples

### Dropdown

```json
{
  "fieldLabel": "Priority",
  "fieldType": "dropdown",
  "fieldOptions": {
    "values": [
      {"option": "High"},
      {"option": "Medium"},
      {"option": "Low"}
    ]
  },
  "requiredField": true
}
```

---

### Text (single-line)

```json
{
  "fieldLabel": "Title",
  "fieldType": "text",
  "requiredField": true
}
```

---

### Textarea (multi-line)

```json
{
  "fieldLabel": "Comments",
  "fieldType": "textarea",
  "requiredField": false
}
```

---

### Number

```json
{
  "fieldLabel": "Quantity",
  "fieldType": "number",
  "requiredField": true
}
```

---

### Date

```json
{
  "fieldLabel": "Publish Date",
  "fieldType": "date",
  "requiredField": true
}
```

**Note:** Date field returns ISO 8601 format string (e.g., `2024-01-15T00:00:00.000Z`)

---

## Accessing Form Data in Subsequent Nodes

After Wait node resumes, submitted data is available in `$json`.

### In IF Node

Check submitted values to branch workflow:

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

---

### In Code Node

Process form submission:

```javascript
// Access form data
const action = $json['Action'];
const comments = $json['Comments'];
const editedContent = $json['Edited Content'];

// Example: Use edited content if provided, otherwise use original
const finalContent = editedContent || $json.originalContent;

return [{
  json: {
    action,
    content: finalContent,
    comments,
    approvedAt: new Date().toISOString()
  }
}];
```

---

### In Set Node

Transform form data:

```json
{
  "assignments": {
    "assignments": [
      {
        "name": "approved",
        "value": "={{ $json['Action'] === 'Approve' }}",
        "type": "boolean"
      },
      {
        "name": "userComments",
        "value": "={{ $json['Comments'] }}",
        "type": "string"
      }
    ]
  }
}
```

---

### Retrieving Stored Data After Wait

Common pattern: Store data before Wait node, retrieve after:

**Before Wait node (Code node):**
```javascript
const stories = $input.all().slice(0, 5);

return [{
  json: {
    stories: stories.map(s => s.json),
    formattedList: stories.map((s, i) => `${i+1}. ${s.json.title}`).join('\n')
  }
}];
```

**Wait node:**
```json
{
  "formDescription": "={{ $json.formattedList }}",
  "formFields": {
    "values": [
      {
        "fieldLabel": "Select Story",
        "fieldType": "dropdown",
        "fieldOptions": {
          "values": [
            {"option": "Story 1"},
            {"option": "Story 2"},
            {"option": "Story 3"}
          ]
        },
        "requiredField": true
      }
    ]
  }
}
```

**After Wait node (Code node):**
```javascript
// Retrieve stored data from before Wait node
const storedData = $('Prepare Data').first().json;
const selectedIndex = parseInt($json['Select Story'].replace('Story ', '')) - 1;
const selectedStory = storedData.stories[selectedIndex];

return [{
  json: selectedStory
}];
```

---

## Form Description Markdown Formatting

The `formDescription` field supports markdown for rich formatting.

### Basic Formatting

```json
{
  "formDescription": "## Heading\n\n**Bold text**\n\n*Italic text*\n\n- List item 1\n- List item 2"
}
```

**Renders as:**
```
## Heading

**Bold text**

*Italic text*

- List item 1
- List item 2
```

---

### Dynamic Content

Include data from previous nodes:

```json
{
  "formDescription": "## Review Story\n\n**Title:** {{ $json.title }}\n\n**URL:** {{ $json.url }}\n\n**Score:** {{ $json.score }}\n\n**Summary:**\n{{ $json.summary }}"
}
```

---

### Complex Layouts

```json
{
  "formDescription": "## Approval Required\n\n### Generated Content\n\n{{ $json.generatedPost }}\n\n---\n\n### Metadata\n\n| Field | Value |\n|-------|-------|\n| Source | {{ $json.source }} |\n| Score | {{ $json.score }} |\n| Date | {{ $json.publishedAt }} |\n\n---\n\n**Please approve or reject:**"
}
```

---

### Using Expressions for Full Control

Pass pre-formatted markdown from Code node:

**Code node before Wait:**
```javascript
const items = $input.all();

const formattedDescription = `
## Select a Story to Share

${items.map((item, i) => `
### ${i+1}. ${item.json.title}

**Source:** ${item.json.source}
**Score:** ${item.json.score} points
**URL:** ${item.json.url}

${item.json.summary}

---
`).join('\n')}
`;

return [{
  json: {
    description: formattedDescription,
    items: items.map(i => i.json)
  }
}];
```

**Wait node:**
```json
{
  "formDescription": "={{ $json.description }}"
}
```

---

## Field Validation

n8n provides basic validation through `requiredField` property.

### Required vs Optional

```json
{
  "formFields": {
    "values": [
      {
        "fieldLabel": "Email",
        "fieldType": "text",
        "requiredField": true    // User must fill this
      },
      {
        "fieldLabel": "Comments",
        "fieldType": "textarea",
        "requiredField": false   // Optional field
      }
    ]
  }
}
```

---

### Custom Validation

For advanced validation, use IF node or Code node after Wait:

```javascript
// In Code node after Wait
const email = $json['Email'];
const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

if (!isValidEmail) {
  throw new Error('Invalid email format');
}

return $input.all();
```

---

## Complete Workflow Example

For a full production example with Wait nodes, see:

`assets/examples/news-aggregation-workflow.json` - Includes human review step with Wait node

---

## Documentation

- [Wait Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/)

---

## See Also

- `references/node-library.md` - Complete Wait node documentation
- `references/workflow-patterns.md` - Human-in-the-loop pattern
- `code-snippets/form-data-preparation.js` - Form data formatting helpers
