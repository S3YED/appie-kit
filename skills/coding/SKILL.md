# Coding Skill

*How Appies write code*

## Purpose
Guidelines and prompts for writing high-quality, maintainable code.

---

## Core Principles

### 1. Minimal Invasion
- Change only what's necessary
- Preserve existing patterns
- Don't refactor unless required
- Leave working code alone

### 2. Readability First
```javascript
// ❌ Clever
const x = data.reduce((a,b)=>({...a,[b.k]:b.v}),{});

// ✅ Clear
const result = {};
data.forEach(item => {
  result[item.key] = item.value;
});
```

### 3. Explicit Over Implicit
```javascript
// ❌ Magic
const users = await db.get('users');

// ✅ Clear
const users = await database.users.findAll({ 
  where: { active: true },
  limit: 100 
});
```

### 4. Error Handling
```javascript
// Always handle errors
try {
  const result = await riskyOperation();
  return { ok: true, result };
} catch (error) {
  console.error('Operation failed:', error.message);
  return { ok: false, error: error.message };
}
```

---

## Code Quality Checklist

Before committing code, check:

- [ ] **No hardcoded secrets** - Use env vars
- [ ] **Input validation** - Check all external inputs
- [ ] **Error handling** - Try/catch with meaningful messages
- [ ] **No TODOs** - Fix or document separately
- [ ] **Consistent style** - Match existing code
- [ ] **Clear names** - Variables/functions describe purpose
- [ ] **One thing per function** - Single responsibility
- [ ] **Comments explain WHY** - Not what (code shows what)

---

## Appie Coding Prompt

When writing code, follow this structure:

### 1. Understand Requirements
```
What problem am I solving?
What are the inputs?
What are the outputs?
What are the edge cases?
```

### 2. Check Existing Code
```bash
# Find similar implementations
grep -r "similar_function" .
# Read before reimplementing
```

### 3. Write Simple First
```javascript
// Start with the simplest solution
function processData(data) {
  // Basic happy path
  if (!data) return null;
  return data.map(item => item.value);
}
```

### 4. Add Error Handling
```javascript
function processData(data) {
  if (!data) {
    console.error('processData: data is required');
    return { ok: false, error: 'Data required' };
  }
  
  try {
    const result = data.map(item => {
      if (!item.value) throw new Error('Missing value');
      return item.value;
    });
    return { ok: true, result };
  } catch (error) {
    console.error('processData failed:', error.message);
    return { ok: false, error: error.message };
  }
}
```

### 5. Test Edge Cases
```javascript
// What if...
processData(null);           // null input
processData([]);             // empty array
processData([{value: 1}]);   // valid input
processData([{}]);           // missing value
```

### 6. Document
```javascript
/**
 * Process data array and extract values
 * @param {Array<{value: any}>} data - Array of objects with value property
 * @returns {{ok: boolean, result?: any[], error?: string}}
 */
function processData(data) {
  // ...
}
```

---

## Common Patterns

### API Request Wrapper
```javascript
async function apiRequest(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: { 'Content-Type': 'application/json' },
      ...options
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return { ok: true, data };
  } catch (error) {
    return { ok: false, error: error.message };
  }
}
```

### File Operations
```javascript
const fs = require('fs').promises;

async function readJsonFile(path) {
  try {
    const content = await fs.readFile(path, 'utf8');
    const data = JSON.parse(content);
    return { ok: true, data };
  } catch (error) {
    if (error.code === 'ENOENT') {
      return { ok: false, error: 'File not found' };
    }
    return { ok: false, error: error.message };
  }
}
```

### Retry Logic
```javascript
async function retryOperation(fn, maxRetries = 3, delay = 1000) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, delay * (i + 1)));
    }
  }
}
```

---

## Security Rules

### 1. Never Trust Input
```javascript
// Validate and sanitize
function validateEmail(email) {
  if (typeof email !== 'string') return false;
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email.trim());
}
```

### 2. Use Environment Variables
```javascript
// ❌ Never
const apiKey = 'sk-1234567890';

// ✅ Always
const apiKey = process.env.API_KEY;
if (!apiKey) throw new Error('API_KEY not set');
```

### 3. Sanitize Paths
```javascript
const path = require('path');

function safePath(userInput) {
  // Prevent directory traversal
  const normalized = path.normalize(userInput);
  const base = '/allowed/directory';
  const full = path.join(base, normalized);
  
  if (!full.startsWith(base)) {
    throw new Error('Invalid path');
  }
  
  return full;
}
```

---

## Testing Approach

### Unit Test Template
```javascript
// test.js
const assert = require('assert');

function testProcessData() {
  // Test valid input
  const result1 = processData([{value: 1}, {value: 2}]);
  assert.strictEqual(result1.ok, true);
  assert.deepStrictEqual(result1.result, [1, 2]);
  
  // Test null input
  const result2 = processData(null);
  assert.strictEqual(result2.ok, false);
  
  // Test empty array
  const result3 = processData([]);
  assert.strictEqual(result3.ok, true);
  assert.strictEqual(result3.result.length, 0);
  
  console.log('✅ All tests passed');
}

testProcessData();
```

---

## Debugging Workflow

### 1. Reproduce
```javascript
// Minimal test case
const input = { ... };
const output = buggyFunction(input);
console.log('Expected:', expectedOutput);
console.log('Got:', output);
```

### 2. Isolate
```javascript
// Add logging
function buggyFunction(input) {
  console.log('Input:', JSON.stringify(input, null, 2));
  
  const step1 = processStep1(input);
  console.log('After step1:', step1);
  
  const step2 = processStep2(step1);
  console.log('After step2:', step2);
  
  return step2;
}
```

### 3. Fix Minimally
```javascript
// Change only what's broken
// - const result = buggyLogic(input);
+ const result = fixedLogic(input);
```

### 4. Verify
```bash
# Run tests
node test.js

# Check in real environment
curl http://localhost:3000/api/endpoint
```

---

## Code Review Questions

Before pushing code, ask:

1. **Does it work?** - Tested manually?
2. **Is it readable?** - Would I understand this in 6 months?
3. **Is it safe?** - No security holes?
4. **Is it simple?** - Could it be simpler?
5. **Does it fit?** - Matches existing patterns?

---

## Common Anti-Patterns to Avoid

### Premature Optimization
```javascript
// ❌ Over-engineered
const cache = new LRU({ max: 1000, ttl: 60000 });
function getUser(id) {
  return cache.get(id) || (cache.set(id, db.get(id)), cache.get(id));
}

// ✅ Simple (optimize later if needed)
function getUser(id) {
  return db.get(id);
}
```

### Magic Numbers
```javascript
// ❌ What is 86400000?
setTimeout(cleanup, 86400000);

// ✅ Clear
const ONE_DAY_MS = 24 * 60 * 60 * 1000;
setTimeout(cleanup, ONE_DAY_MS);
```

### Deep Nesting
```javascript
// ❌ Nested hell
if (user) {
  if (user.subscription) {
    if (user.subscription.active) {
      return user.subscription.plan;
    }
  }
}

// ✅ Early returns
if (!user) return null;
if (!user.subscription) return null;
if (!user.subscription.active) return null;
return user.subscription.plan;
```

---

## See Also

- `frameworks/gsd/` - Productivity system
- `SOUL.md` - Code quality principles
- VDF (Vibe Debugging Framework) in SOUL.md

---

*"Good code is boring code."*
