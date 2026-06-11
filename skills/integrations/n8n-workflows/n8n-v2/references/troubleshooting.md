# n8n Troubleshooting Guide

Common issues and solutions when working with n8n v2.0 workflows.

## Table of Contents

- [Execute Sub-Workflow Issues](#execute-sub-workflow-issues)
- [Authentication Issues](#authentication-issues)
- [Data Issues](#data-issues)
- [Expression Issues](#expression-issues)
- [Workflow Execution Issues](#workflow-execution-issues)
- [Data Quality Issues](#data-quality-issues)
- [API Integration Issues](#api-integration-issues)
- [Performance Issues](#performance-issues)
- [Import/Export Issues](#importexport-issues)
- [Debug Checklist](#debug-checklist)

---

## Execute Sub-Workflow Issues

See [execute-sub-workflow-issues.md](execute-sub-workflow-issues.md) for dedicated documentation.

**Quick summary:**
- **Problem:** "Node out of date" error after import
- **Solution:** Delete old Execute Sub-Workflow nodes, add fresh ones from palette

---

## Authentication Issues

### LinkedIn `unauthorized_scope_error`

**Symptoms:**
- OAuth flow completes successfully
- API calls return 401 or 403 errors
- Error message: "Insufficient permissions" or "unauthorized_scope_error"

**Root cause:** Organization Support or Legacy toggles are enabled in credentials

**Solution:**
1. Open n8n UI > Home > Credentials
2. Find LinkedIn OAuth2 credential
3. Edit credential
4. Turn OFF both toggles: ❌ Organization Support, ❌ Legacy
5. Save and test

---

### API Key Authentication Failing

**Symptoms:**
- 401 Unauthorized or 403 Forbidden errors
- "Invalid API key" messages

**Checklist:**
1. Header name is exact match (case-sensitive): `X-Api-Key` not `x-api-key`
2. Credential type matches node's `nodeCredentialType`
3. API key not expired
4. Not hitting rate limits

---

## Data Issues

### Field is Undefined

**Common causes:**
1. Typo in field name: `$json.titel` vs `$json.title`
2. Wrong node referenced
3. Field doesn't exist in some items

**Solutions:**
```javascript
// Use optional chaining
{{ $json.field?.nestedField ?? 'default' }}

// Fallback chain
{{ $json.field || 'default' }}
```

---

### Data Lost Between Nodes

**Common causes:**
1. Filter node removed all items
2. Code node not returning correct format
3. Connection missing

**Solution - Correct Code node return:**
```javascript
// Correct
return [{ json: { data } }];
return items.map(item => ({ json: item }));

// Wrong
return { data };
return data;
```

---

### Merge Node Not Combining Data

**Checklist:**
1. Mode is `append` for combining lists
2. All inputs connected
3. Upstream nodes executed successfully

---

## Expression Issues

### Expression Not Evaluating

**Solutions:**
1. Check syntax: `={{ expression }}` not `{{ expression }}`
2. Enable expression mode in node parameter (toggle)
3. Escape literal braces if needed

---

### Cross-Node Reference Returns Empty

**Solutions:**
1. Node name exact match (case-sensitive)
2. Node has executed
3. Correct syntax: `$('Node Name').first().json.field`

---

## Workflow Execution Issues

### Wait Node Not Pausing

**Solution:** Use Wait node with `resume: "form"`, NOT respondToWebhook or Set nodes.

See [wait-nodes-guide.md](wait-nodes-guide.md) for details.

---

### Split in Batches Infinite Loop

**Solution:** Ensure downstream nodes connect back to Split in Batches for loop continuation.

---

## Data Quality Issues

### Duplicate Items

**Solution:** Use Code node for deduplication:
```javascript
const items = $input.all();
const seen = new Set();
const unique = [];

for (const item of items) {
  const key = item.json.url.toLowerCase().replace(/\/$/, '');
  if (!seen.has(key)) {
    seen.add(key);
    unique.push(item);
  }
}
return unique;
```

See `code-snippets/deduplication.js`

---

### Date/Time Format Mismatch

**Solution:** Normalize to ISO format:
```javascript
// Set node
"value": "={{ new Date($json.pubDate).toISOString() }}"

// Unix timestamp (seconds)
"value": "={{ new Date($json.time * 1000).toISOString() }}"
```

---

## API Integration Issues

### Rate Limit Errors

**Solutions:**
1. Use Split in Batches to reduce request frequency
2. Add delays between requests
3. Cache responses

---

### LinkedIn Member ID Format Error

**Solution:** Use URN format:
```javascript
// urn:li:person:{id}
={{ `urn:li:person:${$json.sub}` }}
```

See [api-credentials.md](api-credentials.md)

---

## Performance Issues

### Workflow Timeout

**Solutions:**
1. Filter data earlier in workflow
2. Use Split in Batches
3. Optimize Code nodes (avoid nested loops)

---

### Memory Issues

**Solutions:**
1. Process in batches
2. Limit array sizes
3. Keep only essential fields

---

## Import/Export Issues

### Imported Workflow Shows Errors

**Solutions:**
1. Execute Sub-Workflow nodes: delete and recreate
2. Reconfigure credentials
3. Verify all connections

---

## Debug Checklist

1. Execute nodes individually and check output
2. Trace data flow through workflow
3. Verify expressions in isolation
4. Inspect connections visually
5. Review credentials configuration
6. Check n8n logs
7. Test APIs externally (curl/Postman)

---

## See Also

- `references/execute-sub-workflow-issues.md`
- `references/wait-nodes-guide.md`
- `references/api-credentials.md`
- `references/expression-syntax.md`
- `references/node-library.md`
