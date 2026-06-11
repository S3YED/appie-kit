/**
 * Data Normalization Patterns for n8n Code Nodes
 *
 * Common transformations to unify data from different sources.
 * Use these in Set nodes or Code nodes after fetching from APIs.
 */

// ============================================================================
// COMPLETE NORMALIZATION EXAMPLE
// ============================================================================
// Normalize multiple data sources to common schema

const items = $input.all();

const normalized = items.map(item => {
  const data = item.json;

  return {
    json: {
      // Standardized fields
      title: cleanText(data.title || data.headline || 'Untitled', 200),
      url: normalizeUrl(data.url || data.link),
      source: data.source || data.sourceName || 'Unknown',
      timestamp: normalizeTimestamp(data.timestamp || data.pubDate || data.created_at),
      summary: cleanText(data.summary || data.description || data.excerpt || '', 500),

      // Normalized metrics
      score: data.score || data.points || 0,
      comments: data.comments || data.descendants || 0,

      // Computed fields
      domain: extractDomain(data.url || data.link),
      ageHours: getAgeInHours(data.timestamp || data.pubDate),

      // Original data (for debugging)
      _original: data
    }
  };
});

return normalized;

// Helper functions
function normalizeUrl(url) {
  if (!url) return '';
  return url
    .trim()
    .toLowerCase()
    .replace(/^https?:\/\/(www\.)?/, 'https://')
    .replace(/\/$/, '');
}

function normalizeTimestamp(timestamp) {
  if (!timestamp) return new Date().toISOString();
  const date = new Date(timestamp);
  return isNaN(date.getTime()) ? new Date().toISOString() : date.toISOString();
}

function cleanText(text, maxLength = 500) {
  return text
    .trim()
    .replace(/\s+/g, ' ')
    .substring(0, maxLength);
}

function extractDomain(url) {
  if (!url) return 'unknown';
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch (e) {
    return 'unknown';
  }
}

function getAgeInHours(timestamp) {
  if (!timestamp) return 0;
  const age = Date.now() - new Date(timestamp).getTime();
  return Math.round(age / (1000 * 60 * 60));
}


// ============================================================================
// INDIVIDUAL NORMALIZATION FUNCTIONS
// ============================================================================

// URL Normalization
function normalizeUrl(url) {
  return url
    .toLowerCase()
    .replace(/^https?:\/\/(www\.)?/, '')
    .replace(/\/$/, '');
}

// Timestamp to ISO
function toISO(timestamp) {
  // Handle Unix timestamps (seconds)
  if (typeof timestamp === 'number' && timestamp < 10000000000) {
    return new Date(timestamp * 1000).toISOString();
  }
  // Handle Unix timestamps (milliseconds) or ISO strings
  return new Date(timestamp).toISOString();
}

// Extract domain
function getDomain(url) {
  try {
    const domain = new URL(url).hostname;
    return domain.replace(/^www\./, '');
  } catch (e) {
    return null;
  }
}

// Normalize score/engagement metrics
function normalizeMetrics(data) {
  return {
    score: data.score || data.points || data.upvotes || 0,
    comments: data.comments || data.numComments || data.descendants || 0,
    likes: data.likes || data.reactions || data.favorites || 0,
    shares: data.shares || data.retweets || 0
  };
}

// Clean and truncate text
function cleanText(text, maxLength = 500) {
  if (!text) return '';
  return text
    .trim()
    .replace(/\s+/g, ' ')  // Normalize whitespace
    .replace(/\n+/g, ' ')  // Remove line breaks
    .substring(0, maxLength);
}


// ============================================================================
// SOURCE-SPECIFIC NORMALIZATION
// ============================================================================

// Hacker News normalization
function normalizeHackerNews(item) {
  return {
    json: {
      title: item.json.title,
      url: item.json.url || `https://news.ycombinator.com/item?id=${item.json.id}`,
      source: 'Hacker News',
      score: item.json.score || 0,
      comments: item.json.descendants || 0,
      timestamp: new Date(item.json.time * 1000).toISOString(),
      summary: item.json.title
    }
  };
}

// NewsAPI normalization
function normalizeNewsAPI(item) {
  return {
    json: {
      title: item.json.title,
      url: item.json.url,
      source: item.json.source.name,
      score: 0,
      comments: 0,
      timestamp: item.json.publishedAt,
      summary: item.json.description || item.json.title
    }
  };
}

// RSS Feed normalization
function normalizeRSS(item) {
  return {
    json: {
      title: item.json.title,
      url: item.json.link,
      source: item.json.creator || 'RSS Feed',
      score: 0,
      comments: 0,
      timestamp: item.json.pubDate,
      summary: item.json.contentSnippet || item.json.title
    }
  };
}


// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/*
EXAMPLE 1: Normalize Hacker News data

Input:
{
  "id": 123456,
  "title": "Show HN: My Project",
  "url": "https://example.com",
  "score": 150,
  "descendants": 42,
  "time": 1704067200
}

Output:
{
  "title": "Show HN: My Project",
  "url": "https://example.com",
  "source": "Hacker News",
  "score": 150,
  "comments": 42,
  "timestamp": "2024-01-01T00:00:00.000Z",
  "summary": "Show HN: My Project",
  "domain": "example.com"
}
*/

/*
EXAMPLE 2: Normalize multiple sources

Before Normalization:
- HN: { title, url, score, descendants, time }
- NewsAPI: { title, url, source.name, publishedAt, description }
- RSS: { title, link, creator, pubDate, contentSnippet }

After Normalization (all sources):
{
  title: "string",
  url: "string",
  source: "string",
  score: number,
  comments: number,
  timestamp: "ISO string",
  summary: "string"
}
*/
