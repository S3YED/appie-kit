/**
 * Form Data Preparation for Wait Nodes
 *
 * Patterns for formatting data to display in Wait node forms.
 * Use in Code node before Wait node to prepare markdown descriptions.
 */

// ============================================================================
// CREATE NUMBERED LIST
// ============================================================================
// Display items as numbered list with key fields

const items = $input.all().slice(0, 5);  // Limit to top 5

const numberedList = items.map((item, idx) => {
  const data = item.json;
  return `${idx + 1}. **${data.title}**
   Source: ${data.source} | Score: ${data.score} | Comments: ${data.comments}
   URL: ${data.url}`;
}).join('\n\n');

return [{
  json: {
    formDescription: numberedList,
    items: items.map(i => i.json)  // Store for later retrieval
  }
}];


// ============================================================================
// CREATE MARKDOWN TABLE
// ============================================================================
// Tabular display of items

const items = $input.all().slice(0, 10);

const tableHeader = '| # | Title | Source | Score |';
const tableDivider = '|---|-------|--------|-------|';
const tableRows = items.map((item, idx) => {
  const data = item.json;
  const title = data.title.substring(0, 50);  // Truncate for table
  return `| ${idx + 1} | ${title} | ${data.source} | ${data.score} |`;
}).join('\n');

const table = [tableHeader, tableDivider, tableRows].join('\n');

return [{
  json: {
    formDescription: table,
    items: items.map(i => i.json)
  }
}];


// ============================================================================
// CREATE SUMMARY CARDS
// ============================================================================
// Rich card-style display with all details

const items = $input.all().slice(0, 3);

const cards = items.map((item, idx) => {
  const data = item.json;
  return `## ${idx + 1}. ${data.title}

**Source:** ${data.source}
**URL:** ${data.url}
**Score:** ${data.score} points | **Comments:** ${data.comments}
**Published:** ${new Date(data.timestamp).toLocaleString()}

### Summary
${data.summary}

---`;
}).join('\n\n');

return [{
  json: {
    formDescription: cards,
    items: items.map(i => i.json)
  }
}];


// ============================================================================
// COMPLETE FORM DATA PREPARATION
// ============================================================================
// Full pattern with dropdown options generation

const items = $input.all();
const topItems = items.slice(0, 5);

// Create formatted list for description
const formattedList = topItems.map((item, idx) => {
  const data = item.json;
  return `### Story ${idx + 1}: ${data.title}

**Source:** ${data.source}
**URL:** ${data.url}
**Score:** ${data.score} | **Comments:** ${data.comments}

${data.summary}

---`;
}).join('\n');

// Create dropdown options (Story 1, Story 2, etc.)
const dropdownOptions = topItems.map((_, idx) => ({
  option: `Story ${idx + 1}`
}));

return [{
  json: {
    // For Wait node formDescription
    storyList: `# Select a Story to Share\n\n${formattedList}`,

    // For Wait node dropdown field
    dropdownOptions: dropdownOptions,

    // Store full data for retrieval after Wait
    stories: topItems.map(i => i.json)
  }
}];


// ============================================================================
// DYNAMIC CONTENT WITH METADATA
// ============================================================================
// Include generated content + metadata for review

const generatedContent = $input.first().json;

const formDescription = `## Review Generated Content

### Generated Post

${generatedContent.text}

---

### Metadata

| Field | Value |
|-------|-------|
| Model | ${generatedContent.model} |
| Tokens Used | ${generatedContent.usage?.total_tokens || 'N/A'} |
| Generated At | ${new Date().toLocaleString()} |

---

**Please approve or request edits:**`;

return [{
  json: {
    formDescription,
    originalContent: generatedContent.text,
    metadata: generatedContent
  }
}];


// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

// Format list with custom fields
function formatList(items, fields) {
  return items.map((item, idx) => {
    const fieldText = fields.map(field => {
      const value = item.json[field];
      return `**${field}:** ${value}`;
    }).join(' | ');

    return `${idx + 1}. ${fieldText}`;
  }).join('\n\n');
}

// Usage:
const formatted = formatList(items, ['title', 'source', 'url', 'score']);


// Create dropdown options with labels
function createDropdownOptions(items, labelField = 'title') {
  return items.map((item, idx) => ({
    option: item.json[labelField].substring(0, 50)  // Truncate long labels
  }));
}

// Usage:
const options = createDropdownOptions(items, 'title');


// Generate summary card
function createCard(item, index) {
  const data = item.json;
  return `## ${index}. ${data.title}

**Source:** ${data.source}
**URL:** ${data.url}
**Score:** ${data.score} | **Comments:** ${data.comments}

${data.summary}

---`;
}

// Usage:
const cards = items.map((item, i) => createCard(item, i + 1)).join('\n');


// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/*
EXAMPLE 1: Simple numbered list

Before Wait node:
- Code node creates numbered list
- Returns formDescription + stored items

Wait node:
- formDescription shows list
- Dropdown with "Story 1", "Story 2", etc.

After Wait node:
- Code node retrieves stored items
- Gets selected item by index
*/

/*
EXAMPLE 2: Rich content review

Before Wait node:
- AI generates content
- Code node formats content + metadata
- Returns formDescription with markdown table

Wait node:
- Shows generated content beautifully formatted
- Dropdowns for Approve/Edit/Reject
- Optional textarea for edits

After Wait node:
- Code node checks approval status
- Uses edited content if provided
*/

/*
EXAMPLE 3: Data validation

Before Wait node:
- Extract data from document
- Format as table for review

Wait node:
- Shows extracted data in table
- Text fields pre-filled with extracted values
- User can correct errors

After Wait node:
- Code node saves corrected data
*/
