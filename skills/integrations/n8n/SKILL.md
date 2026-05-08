# n8n Automation Skill

## Purpose
Interact with n8n workflows - list, trigger, monitor, and manage automations.

## Capabilities
- List all workflows (active/inactive)
- Trigger workflows via webhooks
- Get execution history
- Activate/deactivate workflows
- Create workflows from templates

## Configuration Required

### Environment Variables
```bash
N8N_API_URL=https://app.n8n.weblyfe.nl/api/v1
N8N_API_KEY=your-api-key-here
```

### Getting Your API Key
1. Go to n8n Settings → API
2. Create a new API key
3. Store in environment or config

## Usage Examples

### List Active Workflows
```bash
n8n list --active
```

### Trigger a Workflow
```bash
n8n trigger <workflow-id> --data '{"key": "value"}'
```

### Get Execution Status
```bash
n8n executions <workflow-id>
```

### Activate Workflow
```bash
n8n activate <workflow-id>
```

## API Wrapper

### `api/n8n.js`
```javascript
const n8n = require('./api/n8n.js');

// List workflows
const workflows = await n8n.listWorkflows();

// Trigger workflow
const result = await n8n.trigger(workflowId, { data });

// Get executions
const executions = await n8n.getExecutions(workflowId);
```

## Integration with Appie

### Trigger from Chat
```
User: "Run the morning brief workflow"
Appie: → n8n.trigger('morning-brief-id', { user: 'Seyed' })
```

### Notify on Completion
```javascript
// After Appie task completes
await n8n.trigger('notification-workflow', {
    message: 'Task completed',
    appie: 'Appie-1'
});
```

## Common Workflows to Create

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| Morning Brief | 7:00 AM | Generate daily brief |
| Notification | Webhook | Alert Seyed of events |
| Backup | Hourly | Backup important data |
| Sync | On-change | Sync with external services |

## Error Handling

- **401**: Invalid API key - check N8N_API_KEY
- **404**: Workflow not found - verify workflow-id
- **429**: Rate limit - wait and retry
- **500**: n8n server error - check n8n logs

## See Also
- [n8n Documentation](https://docs.n8n.io/)
- `skills/clawdhub/` - For publishing skills
