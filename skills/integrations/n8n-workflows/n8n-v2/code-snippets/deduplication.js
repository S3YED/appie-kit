/**
 * Deduplication Patterns for n8n Code Nodes
 *
 * Reusable JavaScript functions for removing duplicate items from arrays.
 * Use these in Code nodes after Merge nodes or when aggregating data.
 */

// ============================================================================
// PATTERN 1: Deduplicate by URL
// ============================================================================
// Most common pattern for news/content aggregation
// Normalizes URLs to catch variations (http vs https, www vs non-www, trailing slash)

const items = $input.all();
const seen = new Set();
const unique = [];

for (const item of items) {
  // Normalize URL for comparison
  const url = item.json.url || '';
  const normalizedUrl = url
    .toLowerCase()
    .replace(/^https?:\/\/(www\.)?/, '')  // Remove protocol and www
    .replace(/\/$/, '');                   // Remove trailing slash

  if (!seen.has(normalizedUrl)) {
    seen.add(normalizedUrl);
    unique.push({
      json: {
        ...item.json,
        normalizedUrl,  // Store for debugging
        fetchedAt: new Date().toISOString()
      }
    });
  }
}

return unique;


// ============================================================================
// PATTERN 2: Deduplicate by Title
// ============================================================================
// Useful when URLs might differ but content is the same

const items = $input.all();
const seen = new Set();
const unique = [];

for (const item of items) {
  const title = (item.json.title || '').toLowerCase().trim();

  if (title && !seen.has(title)) {
    seen.add(title);
    unique.push(item);
  }
}

return unique;


// ============================================================================
// PATTERN 3: Deduplicate by ID
// ============================================================================
// When items have unique IDs from APIs

const items = $input.all();
const seen = new Set();
const unique = [];

for (const item of items) {
  const id = item.json.id;

  if (id && !seen.has(id)) {
    seen.add(id);
    unique.push(item);
  }
}

return unique;


// ============================================================================
// PATTERN 4: Deduplicate by Multiple Fields
// ============================================================================
// Composite key deduplication (e.g., title + source)

const items = $input.all();
const seen = new Set();
const unique = [];

for (const item of items) {
  // Create composite key
  const key = `${item.json.title}|${item.json.source}`.toLowerCase();

  if (!seen.has(key)) {
    seen.add(key);
    unique.push(item);
  }
}

return unique;


// ============================================================================
// PATTERN 5: Deduplicate with Priority
// ============================================================================
// Keep item with highest score when duplicates found

const items = $input.all();
const byUrl = new Map();

// Group by normalized URL, keeping highest score
for (const item of items) {
  const url = (item.json.url || '')
    .toLowerCase()
    .replace(/^https?:\/\/(www\.)?/, '')
    .replace(/\/$/, '');

  const existing = byUrl.get(url);
  const currentScore = item.json.score || 0;
  const existingScore = existing?.json.score || 0;

  if (!existing || currentScore > existingScore) {
    byUrl.set(url, item);
  }
}

// Convert Map to array
return Array.from(byUrl.values());


// ============================================================================
// PATTERN 6: Deduplicate and Track Duplicates
// ============================================================================
// Keep track of how many duplicates were found

const items = $input.all();
const seen = new Map();
const unique = [];

for (const item of items) {
  const url = (item.json.url || '')
    .toLowerCase()
    .replace(/^https?:\/\/(www\.)?/, '')
    .replace(/\/$/, '');

  if (!seen.has(url)) {
    seen.set(url, 1);
    unique.push({
      json: {
        ...item.json,
        duplicateCount: 1
      }
    });
  } else {
    seen.set(url, seen.get(url) + 1);
    // Update duplicate count on existing item
    const existingItem = unique.find(u =>
      u.json.url?.toLowerCase().replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, '') === url
    );
    if (existingItem) {
      existingItem.json.duplicateCount = seen.get(url);
    }
  }
}

return unique;


// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/*
EXAMPLE 1: Basic URL deduplication after Merge node

Previous nodes:
- HTTP Request: Hacker News
- HTTP Request: NewsAPI
- RSS Feed Read: Blog
- Merge (append mode)
- Code (this deduplication code)

Result: Removes duplicate URLs across all sources
*/

/*
EXAMPLE 2: Deduplicate with normalization

Input data:
[
  { url: "https://www.example.com/article" },
  { url: "http://example.com/article/" },
  { url: "https://example.com/article" }
]

Output after deduplication:
[
  { url: "https://www.example.com/article", normalizedUrl: "example.com/article" }
]

All three variations recognized as duplicates
*/

/*
EXAMPLE 3: Priority-based deduplication

Input data:
[
  { url: "https://example.com/post", score: 50 },
  { url: "https://example.com/post", score: 100 },  // Kept (higher score)
  { url: "https://example.com/post", score: 75 }
]

Output:
[
  { url: "https://example.com/post", score: 100 }
]

Keeps the version with highest score
*/
