/**
 * Cross-Node Data Access Patterns for n8n Code Nodes
 *
 * How to reference data from other nodes in your workflow.
 * These patterns work in Code nodes to access data from named nodes.
 */

// ============================================================================
// BASIC PATTERNS
// ============================================================================

// Access data from named node (first item)
const previousData = $('Previous Node Name').first().json;
const specificField = previousData.fieldName;

// Access all items from named node
const allItems = $('Node Name').all();
const allTitles = allItems.map(item => item.json.title);

// Access specific item by index
const firstItem = $('Node Name').item(0).json;
const secondItem = $('Node Name').item(1).json;

// Get current node's input
const currentInput = $input.first().json;
const allInputs = $input.all();


// ============================================================================
// EXTRACT FORM SUBMISSION FROM WAIT NODE
// ============================================================================

// After Wait node, get form data
const formData = $input.first().json;
const selectedOption = formData['Dropdown Field Name'];
const textInput = formData['Text Field Name'];
const comments = formData['Comments'];

// Use form data
if (selectedOption === 'Approve') {
  // Continue with approval
}


// ============================================================================
// RETRIEVE STORED DATA AFTER WAIT NODE
// ============================================================================

// Common pattern: Data prepared before Wait, retrieved after

// Get data from node before Wait
const preparedData = $('Prepare Data').first().json;

// Get user selection from Wait
const selection = $input.first().json['Select Story'];

// Extract selected item
const selectedIndex = parseInt(selection.replace('Story ', '')) - 1;
const selectedItem = preparedData.stories[selectedIndex];

return [{
  json: selectedItem
}];


// ============================================================================
// COMBINE DATA FROM MULTIPLE NODES
// ============================================================================

// Merge data from different parts of workflow
const dataFromFetch = $('Fetch News').first().json;
const dataFromGenerate = $('Generate Content').first().json;
const dataFromForm = $input.first().json;

const combined = {
  // From fetch
  title: dataFromFetch.title,
  url: dataFromFetch.url,

  // From generation
  generatedContent: dataFromGenerate.text,

  // From form
  userApproval: dataFromForm['Action'],
  userComments: dataFromForm['Comments'],

  // Computed
  processedAt: new Date().toISOString()
};

return [{ json: combined }];


// ============================================================================
// ACCESS NODE PARAMETERS
// ============================================================================

// Access workflow configuration
const workflowId = $parameter.workflowId;
const customParam = $parameter.customFieldName;


// ============================================================================
// SAFE ACCESS WITH FALLBACKS
// ============================================================================

// Check if node exists and has data
const safeData = $('Node Name').itemMatching(0);
if (safeData) {
  const field = safeData.json.field;
}

// With fallback value
const value = $('Node Name').first()?.json?.field || 'default';

// Optional chaining for nested data
const nested = $('Node Name').first()?.json?.user?.email ?? 'no-email@example.com';


// ============================================================================
// LOOP THROUGH NODE DATA
// ============================================================================

// Process all items from previous node
const items = $('Previous Node').all();

const processed = items.map(item => {
  const data = item.json;
  return {
    json: {
      ...data,
      processed: true,
      processedAt: new Date().toISOString()
    }
  };
});

return processed;


// ============================================================================
// COMPLETE EXAMPLE: POST-WAIT PROCESSING
// ============================================================================

// Workflow context:
// 1. "Fetch News" node fetches 10 stories
// 2. "Prepare Review" node formats top 5 for display
// 3. "Wait for Selection" shows stories, user picks one
// 4. This Code node gets selected story and user's comments

// Get original fetched data (before Wait)
const preparedData = $('Prepare Review').first().json;
const allStories = preparedData.stories;

// Get user selection (from Wait node)
const userInput = $input.first().json;
const selection = userInput['Select Story'];  // e.g., "Story 3"
const userComments = userInput['Comments'] || '';

// Extract selected story
const storyNumber = parseInt(selection.replace('Story ', ''));
const selectedStory = allStories[storyNumber - 1];

// Combine with additional context
const result = {
  ...selectedStory,
  selectedBy: 'user',
  selectionTime: new Date().toISOString(),
  userComments: userComments,
  storyNumber: storyNumber
};

return [{ json: result }];


// ============================================================================
// ADVANCED: CONDITIONAL DATA ACCESS
// ============================================================================

// Check multiple nodes, use first available
let data;
if ($('Primary Source').itemMatching(0)) {
  data = $('Primary Source').first().json;
} else if ($('Backup Source').itemMatching(0)) {
  data = $('Backup Source').first().json;
} else {
  data = { error: 'No data available' };
}

return [{ json: data }];


// ============================================================================
// AGGREGATE DATA FROM PARALLEL BRANCHES
// ============================================================================

// After parallel processing, combine results
const branch1Data = $('Branch 1 Process').all();
const branch2Data = $('Branch 2 Process').all();
const branch3Data = $('Branch 3 Process').all();

const allData = [
  ...branch1Data.map(item => item.json),
  ...branch2Data.map(item => item.json),
  ...branch3Data.map(item => item.json)
];

return allData.map(item => ({ json: item }));


// ============================================================================
// ACCESS EXECUTION METADATA
// ============================================================================

// Get execution information
const executionId = $executionId;
const workflowId = $workflow.id;
const workflowName = $workflow.name;
const isWorkflowActive = $workflow.active;

// Add to output
return [{
  json: {
    ...currentInput,
    metadata: {
      executionId,
      workflowId,
      workflowName,
      executedAt: new Date().toISOString()
    }
  }
}];


// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/*
EXAMPLE 1: Simple cross-node access

Node "Fetch Data" returns: { title: "Hello", score: 100 }

In next Code node:
const title = $('Fetch Data').first().json.title;
// Result: "Hello"
*/

/*
EXAMPLE 2: After Wait node

Node "Prepare" returns: { stories: [{ id: 1 }, { id: 2 }] }
Wait node: User selects "Story 2"

In Code node after Wait:
const selected = parseInt($json['Select Story'].replace('Story ', '')) - 1;
const story = $('Prepare').first().json.stories[selected];
// Result: { id: 2 }
*/

/*
EXAMPLE 3: Combine multiple sources

const title = $('Fetch').first().json.title;
const content = $('Generate').first().json.text;
const approved = $json['Action'] === 'Approve';

return [{ json: { title, content, approved } }];
*/
