#!/usr/bin/env node
/**
 * n8n API Wrapper
 * Direct HTTP calls to n8n instance
 * 
 * Usage:
 *   node api.js list [--active]
 *   node api.js get <workflowId>
 *   node api.js activate <workflowId>
 *   node api.js deactivate <workflowId>
 *   node api.js executions <workflowId> [--limit N]
 *   node api.js trigger <workflowId> [--data '{"key":"value"}']
 */

const https = require('https');

// Configuration - reads from env
const N8N_BASE_URL = (process.env.N8N_BASE_URL || 'n8n.example.com').trim().replace(/^https?:\/\//, '');
const N8N_API_KEY = (process.env.N8N_API_KEY || '').trim();

if (!N8N_API_KEY) {
  console.error('Error: N8N_API_KEY environment variable required');
  console.error('Set it in your shell or your agent config env vars');
  process.exit(1);
}

function request(path, method = 'GET', body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(`https://${N8N_BASE_URL}/api/v1${path}`);
    
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method,
      headers: {
        'X-N8N-API-KEY': N8N_API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      timeout: 15000,
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed);
        } catch {
          reject(new Error(`Invalid JSON: ${data.substring(0, 200)}`));
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => reject(new Error('Request timeout')));

    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// Commands
async function listWorkflows(activeOnly = false) {
  const result = await request('/workflows');
  let workflows = result.data || [];
  
  if (activeOnly) {
    workflows = workflows.filter(w => w.active);
  }
  
  console.log('ID | Name | Active');
  console.log('-'.repeat(60));
  workflows.forEach(w => {
    console.log(`${w.id} | ${w.name} | ${w.active ? '✅' : '❌'}`);
  });
  
  return workflows;
}

async function getWorkflow(workflowId) {
  const result = await request(`/workflows/${workflowId}`);
  console.log(JSON.stringify(result, null, 2));
  return result;
}

async function activateWorkflow(workflowId) {
  const result = await request(`/workflows/${workflowId}/activate`, 'POST');
  console.log(`✅ Workflow ${workflowId} activated`);
  return result;
}

async function deactivateWorkflow(workflowId) {
  const result = await request(`/workflows/${workflowId}/deactivate`, 'POST');
  console.log(`❌ Workflow ${workflowId} deactivated`);
  return result;
}

async function getExecutions(workflowId, limit = 10) {
  const result = await request(`/executions?workflowId=${workflowId}&limit=${limit}`);
  const executions = result.data || [];
  
  console.log('ID | Status | Started | Finished');
  console.log('-'.repeat(70));
  executions.forEach(e => {
    const started = e.startedAt ? new Date(e.startedAt).toLocaleString() : '-';
    const finished = e.stoppedAt ? new Date(e.stoppedAt).toLocaleString() : '-';
    console.log(`${e.id} | ${e.status} | ${started} | ${finished}`);
  });
  
  return executions;
}

async function triggerWorkflow(workflowId, data = {}) {
  // First get the workflow to find webhook URL
  const workflow = await request(`/workflows/${workflowId}`);
  
  // Check if it has a webhook trigger
  const webhookNode = workflow.nodes?.find(n => 
    n.type === 'n8n-nodes-base.webhook' || 
    n.type.includes('webhook')
  );
  
  if (webhookNode) {
    // Trigger via webhook
    const webhookPath = webhookNode.parameters?.path || workflowId;
    console.log(`Triggering via webhook: /webhook/${webhookPath}`);
    
    const result = await request(`/webhook/${webhookPath}`, 'POST', data);
    console.log('Result:', JSON.stringify(result, null, 2));
    return result;
  } else {
    // Execute via API
    const result = await request(`/workflows/${workflowId}/run`, 'POST', { data });
    console.log('Execution started:', result);
    return result;
  }
}

async function createWorkflow(name, nodes = [], connections = {}) {
  const workflow = {
    name,
    nodes: nodes,
    connections: connections,
    settings: {
      saveManualExecutions: true,
      callerPolicy: 'any',
    },
  };
  
  const result = await request('/workflows', 'POST', workflow);
  console.log(`✅ Workflow created: ${result.id}`);
  console.log(`   Name: ${name}`);
  return result;
}

async function deleteWorkflow(workflowId) {
  const result = await request(`/workflows/${workflowId}`, 'DELETE');
  console.log(`🗑️  Workflow ${workflowId} deleted`);
  return result;
}

async function getWorkflowsWithTriggers() {
  const result = await request('/workflows');
  const workflows = result.data || [];
  
  const withTriggers = await Promise.all(
    workflows.map(async (w) => {
      try {
        const full = await request(`/workflows/${w.id}`);
        const hasWebhook = full.nodes?.some(n => 
          n.type === 'n8n-nodes-base.webhook' || 
          n.type.includes('webhook')
        );
        const hasSchedule = full.settings?.cronExpression;
        return { ...w, hasWebhook, hasSchedule };
      } catch {
        return { ...w, hasWebhook: false, hasSchedule: false };
      }
    })
  );
  
  console.log('ID | Name | Webhook | Schedule | Active');
  console.log('-'.repeat(70));
  withTriggers.forEach(w => {
    console.log(`${w.id} | ${w.name.substring(0, 25).padEnd(25)} | ${w.hasWebhook ? '✅' : '❌'} | ${w.hasSchedule ? '✅' : '❌'} | ${w.active ? '✅' : '❌'}`);
  });
  
  return withTriggers;
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  try {
    switch (command) {
      case 'list':
      case 'ls':
        await listWorkflows(args.includes('--active'));
        break;
        
      case 'list-triggers':
        await getWorkflowsWithTriggers();
        break;
        
      case 'get':
        if (!args[1]) throw new Error('Usage: get <workflowId>');
        await getWorkflow(args[1]);
        break;
        
      case 'activate':
        if (!args[1]) throw new Error('Usage: activate <workflowId>');
        await activateWorkflow(args[1]);
        break;
        
      case 'deactivate':
        if (!args[1]) throw new Error('Usage: deactivate <workflowId>');
        await deactivateWorkflow(args[1]);
        break;
        
      case 'delete':
      case 'rm':
        if (!args[1]) throw new Error('Usage: delete <workflowId>');
        await deleteWorkflow(args[1]);
        break;
        
      case 'executions':
        if (!args[1]) throw new Error('Usage: executions <workflowId> [--limit N]');
        const limitIdx = args.indexOf('--limit');
        const limit = limitIdx > -1 ? parseInt(args[limitIdx + 1]) : 10;
        await getExecutions(args[1], limit);
        break;
        
      case 'trigger':
        if (!args[1]) throw new Error('Usage: trigger <workflowId> [--data JSON]');
        const dataIdx = args.indexOf('--data');
        const data = dataIdx > -1 ? JSON.parse(args[dataIdx + 1]) : {};
        await triggerWorkflow(args[1], data);
        break;
        
      case 'create':
        if (!args[1]) throw new Error('Usage: create <name>');
        const nodesIdx = args.indexOf('--nodes');
        const nodes = nodesIdx > -1 ? JSON.parse(args[nodesIdx + 1]) : [];
        await createWorkflow(args[1], nodes);
        break;
        
      default:
        console.log(`
n8n API Wrapper for Appie

Commands:
  list [--active]              List all workflows
  list-triggers                List workflows with webhook/schedule triggers
  get <workflowId>             Get workflow details
  create <name> [--nodes JSON] Create a new workflow
  activate <workflowId>        Activate a workflow
  deactivate <workflowId>      Deactivate a workflow
  delete <workflowId>          Delete a workflow
  executions <id> [--limit N]  Get execution history
  trigger <id> [--data JSON]   Trigger a workflow
        `);
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
