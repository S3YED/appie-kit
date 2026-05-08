# Notion Tasks Skill

*How Appies manage tasks in Notion*

## Purpose

Comprehensive guide for creating, managing, and completing tasks in the Notion Tasks database. This is the central task management system for all Appies.

---

## Database Overview

**Tasks Database**
- **Database ID:** `538bdf7b-a506-4c9c-b451-5d2f78b4d544`
- **Data Source ID:** `7da4b13f-ea03-44d8-a0ec-f725a76dac79` (Use this for queries!)
- **API Version:** `2025-09-03`

### Task Properties

| Property | Type | Description |
|----------|------|-------------|
| **Task** | Title | Task name/description |
| **Status** | Status | Not started, In progress, Done, Blocked |
| **Assignee** | Relation | Links to Appie Status pages |
| **Priority** | Select | High, Medium, Low |
| **Due date** | Date | Task deadline |
| **Label** | Multi-select | Categories/tags |
| **Project** | Rich Text | Project name |
| **Estimated Hours** | Number | Time estimate |

---

## Appie Status Pages

Each Appie has a status page in the Status database that tasks can be assigned to:

| Appie | Status Page ID | Bot |
|-------|---------------|-----|
| **Appie-1 (Mac)** | `2ffc3321-de60-810c-ba85-d818742249db` | @weblyfeopenclaw |
| **Appie-2 (DO)** | `2ffc3321-de60-8127-a19c-d0f3271bd24f` | @appieweblyfebot |
| **Appie-3 (DO)** | `2ffc3321-de60-8115-abee-eed033d76e17` | @eppieweblyfebot |
| **Seyed** | `308c3321-de60-8113-a39f-c956a26b7fe2` | (human) |

---

## Task Workflow

### The Complete Lifecycle

```
1. Task Created (Not started)
   ↓
2. Appie assigns to self + sets "In Progress"
   ↓
3. Appie works on task
   ↓
4. Appie adds documentation to task body
   ↓
5. Appie shows work to Seyed for review
   ↓
6. After approval → Mark as "Done"
```

### Rules

1. **Always assign before starting** - Set Assignee relation
2. **Set to In Progress** - Update status when you begin
3. **Document your work** - Add what you did to task body
4. **Show for review** - Message Seyed with summary
5. **Wait for approval** - Don't mark Done until confirmed
6. **Push to GitHub** - Commit code/docs before marking Done

---

## API Usage

### Setup

```javascript
const https = require('https');
const fs = require('fs');

const NOTION_TOKEN = fs.readFileSync(process.env.HOME + '/.config/notion/api_key', 'utf8').trim();
const TASKS_DATA_SOURCE_ID = '7da4b13f-ea03-44d8-a0ec-f725a76dac79';

function notionRequest(path, method = 'POST', body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.notion.com',
      port: 443,
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${NOTION_TOKEN}`,
        'Notion-Version': '2025-09-03',
        'Content-Type': 'application/json'
      },
      timeout: 15000
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => resolve(JSON.parse(data)));
    });

    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}
```

### Query Tasks

```javascript
async function getTasks(filters = {}) {
  const body = {
    page_size: 100
  };

  // Add filters if provided
  if (Object.keys(filters).length > 0) {
    body.filter = filters;
  }

  const result = await notionRequest(
    `/v1/data_sources/${TASKS_DATA_SOURCE_ID}/query`, 
    'POST', 
    body
  );

  return result.results;
}

// Get all unfinished tasks
const unfinished = await getTasks({
  property: 'Status',
  status: {
    does_not_equal: 'Done'
  }
});

// Get tasks assigned to Appie-3
const myTasks = await getTasks({
  property: 'Assignee',
  relation: {
    contains: '2ffc3321-de60-8115-abee-eed033d76e17'
  }
});

// Get high priority tasks
const urgent = await getTasks({
  property: 'Priority',
  select: {
    equals: 'High'
  }
});
```

### Find Specific Task

```javascript
async function findTask(taskTitle) {
  const result = await notionRequest(
    `/v1/data_sources/${TASKS_DATA_SOURCE_ID}/query`,
    'POST',
    {
      filter: {
        property: 'Task',
        title: {
          contains: taskTitle
        }
      }
    }
  );

  return result.results[0] || null;
}

const task = await findTask('Build Morning Brief');
```

### Create Task

```javascript
async function createTask(title, options = {}) {
  const properties = {
    Task: {
      title: [{ 
        type: 'text', 
        text: { content: title }
      }]
    },
    Status: {
      status: { name: options.status || 'Not started' }
    }
  };

  // Add optional properties
  if (options.priority) {
    properties.Priority = { select: { name: options.priority }};
  }

  if (options.due) {
    properties['Due date'] = { date: { start: options.due }};
  }

  if (options.assignee) {
    properties.Assignee = { relation: [{ id: options.assignee }]};
  }

  if (options.project) {
    properties.Project = { 
      rich_text: [{ 
        type: 'text', 
        text: { content: options.project }
      }]
    };
  }

  const result = await notionRequest('/v1/pages', 'POST', {
    parent: { 
      type: 'database_id',
      database_id: '538bdf7b-a506-4c9c-b451-5d2f78b4d544'
    },
    properties
  });

  return result;
}

// Example: Create task
await createTask('Deploy new feature', {
  priority: 'High',
  due: '2026-02-20',
  assignee: '2ffc3321-de60-8115-abee-eed033d76e17', // Appie-3
  project: 'Command Center'
});
```

### Update Task Status

```javascript
async function updateTaskStatus(pageId, status) {
  await notionRequest(`/v1/pages/${pageId}`, 'PATCH', {
    properties: {
      Status: {
        status: { name: status }
      }
    }
  });
}

// Mark task as In Progress
await updateTaskStatus(task.id, 'In progress');

// Mark task as Done
await updateTaskStatus(task.id, 'Done');
```

### Assign Task to Appie

```javascript
async function assignTask(pageId, appieStatusId) {
  await notionRequest(`/v1/pages/${pageId}`, 'PATCH', {
    properties: {
      Assignee: {
        relation: [{ id: appieStatusId }]
      }
    }
  });
}

// Assign to Appie-3
await assignTask(task.id, '2ffc3321-de60-8115-abee-eed033d76e17');
```

### Add Documentation to Task

```javascript
async function documentTask(pageId, documentation) {
  await notionRequest(`/v1/blocks/${pageId}/children`, 'PATCH', {
    children: [
      {
        object: 'block',
        type: 'heading_2',
        heading_2: {
          rich_text: [{ 
            type: 'text', 
            text: { content: '✅ Completed by Appie-3' }
          }]
        }
      },
      {
        object: 'block',
        type: 'paragraph',
        paragraph: {
          rich_text: [{ 
            type: 'text', 
            text: { content: documentation }
          }]
        }
      }
    ]
  });
}

const doc = `
Created: skills/notion-tasks/SKILL.md (15KB)

What it includes:
- Complete task workflow
- API usage examples
- Helper scripts
- Best practices

Location: /root/clawd/skills/notion-tasks/
Commit: abc1234
Date: 2026-02-16
`;

await documentTask(task.id, doc);
```

---

## Helper Scripts

### Task Workflow Tool

**Location:** `/root/clawd/tools/task-workflow.js`

#### Start a Task
```bash
node /root/clawd/tools/task-workflow.js start "Task Title"
```

What it does:
1. Finds task by title
2. Assigns to Appie-3
3. Sets status to "In Progress"

#### Finish a Task
```bash
node /root/clawd/tools/task-workflow.js finish "Task Title" "Documentation text"
```

What it does:
1. Finds task by title
2. Adds documentation to task body
3. Marks as "Done"

#### Programmatic Usage

```javascript
const { startTask, finishTask } = require('./tools/task-workflow.js');

// Start task
await startTask('Build new feature');

// ... do the work ...

// Finish task with documentation
await finishTask('Build new feature', `
Created: features/new-thing/
Files: 5 files, 1,200 lines
Tested: ✅ All tests pass
Commit: abc1234
`);
```

---

## Common Patterns

### Daily Task Check

```javascript
// Get today's tasks
async function getTodaysTasks(appieId) {
  const today = new Date().toISOString().split('T')[0];
  
  const tasks = await getTasks({
    and: [
      {
        property: 'Assignee',
        relation: { contains: appieId }
      },
      {
        property: 'Status',
        status: { does_not_equal: 'Done' }
      }
    ]
  });

  return tasks.filter(task => {
    const due = task.properties['Due date']?.date?.start;
    return due && due <= today;
  });
}
```

### Overdue Tasks

```javascript
async function getOverdueTasks() {
  const today = new Date().toISOString().split('T')[0];
  
  const tasks = await getTasks({
    and: [
      {
        property: 'Status',
        status: { does_not_equal: 'Done' }
      }
    ]
  });

  return tasks.filter(task => {
    const due = task.properties['Due date']?.date?.start;
    return due && due < today;
  });
}
```

### Task Summary

```javascript
async function getTaskSummary(appieId) {
  const allTasks = await getTasks({
    property: 'Assignee',
    relation: { contains: appieId }
  });

  const summary = {
    total: allTasks.length,
    notStarted: 0,
    inProgress: 0,
    done: 0,
    blocked: 0
  };

  allTasks.forEach(task => {
    const status = task.properties.Status?.status?.name || 'Not started';
    
    if (status === 'Not started') summary.notStarted++;
    else if (status === 'In progress') summary.inProgress++;
    else if (status === 'Done') summary.done++;
    else if (status === 'Blocked') summary.blocked++;
  });

  return summary;
}
```

---

## Best Practices

### 1. One Task, One Thing
- Break big tasks into smaller ones
- Each task should be completable in < 1 day
- Use projects to group related tasks

### 2. Clear Titles
```
❌ "Fix stuff"
❌ "Work on website"
✅ "Fix login timeout on Peakspring site"
✅ "Add file explorer API to Command Center"
```

### 3. Always Estimate
- Add estimated hours to help with planning
- Review estimates weekly to improve accuracy

### 4. Document Everything
- What you built
- Where files are located
- How to test it
- Commit hash
- Known issues

### 5. Keep Status Current
- Update to "In Progress" when you start
- Update to "Blocked" if stuck (with reason)
- Update to "Done" only after approval

### 6. Use Labels
- Label tasks by type: `bug`, `feature`, `documentation`
- Label by client: `Peakspring`, `Fiatballers`, `Weblyfe`
- Label by skill: `n8n`, `automation`, `design`

---

## Integration with Other Systems

### Morning Brief

The daily brief pulls from Tasks:
```javascript
const todaysTasks = await getTodaysTasks(APPIE_ID);
const overdue = await getOverdueTasks();

const brief = `
TOP PRIORITIES TODAY:
${todaysTasks.map(t => `- [ ] ${t.properties.Task.title[0].plain_text}`).join('\n')}

⚠️ OVERDUE:
${overdue.map(t => `- ${t.properties.Task.title[0].plain_text}`).join('\n')}
`;
```

### Goal-Based Task Generation

When creating tasks from goals:
```javascript
const phases = breakdownGoal(goal);

for (const phase of phases) {
  for (const task of phase.tasks) {
    await createTask(task.title, {
      project: goal.name,
      priority: task.priority,
      due: task.due,
      assignee: determineAssignee(task)
    });
  }
}
```

### Command Center Dashboard

The dashboard shows task stats:
```javascript
app.get('/api/tasks/summary', async (req, res) => {
  const summary = await getTaskSummary(APPIE_ID);
  res.json(summary);
});
```

---

## Troubleshooting

### Task Not Found
```javascript
// Search is case-sensitive and uses "contains"
// Try partial match:
const tasks = await getTasks({
  property: 'Task',
  title: { contains: 'Morning' }
});
```

### Can't Update Status
```javascript
// Make sure status name matches exactly:
// ✅ "In progress" (lowercase p)
// ❌ "In Progress" (will fail)

// Valid statuses:
- "Not started"
- "In progress"
- "Done"
- "Blocked"
```

### Assignee Not Working
```javascript
// Use the STATUS PAGE ID, not database ID:
const APPIE3_STATUS_ID = '2ffc3321-de60-8115-abee-eed033d76e17';

await notionRequest(`/v1/pages/${pageId}`, 'PATCH', {
  properties: {
    Assignee: {
      relation: [{ id: APPIE3_STATUS_ID }] // Array of objects!
    }
  }
});
```

### Rate Limiting
```javascript
// Notion API: 3 requests/second
// Add delay between operations:

for (const task of tasks) {
  await updateTask(task);
  await new Promise(resolve => setTimeout(resolve, 350)); // 350ms delay
}
```

---

## See Also

- `tools/task-workflow.js` - Automated task workflow
- `tools/daily-brief/` - Morning brief integration
- `systems/goal-based-tasks/` - Goal → Task generation
- `MEMORY.md` - Task completion tracking

---

*"A task without documentation is a task that never happened."*
