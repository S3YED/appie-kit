# API Credentials Setup Guide

## LinkedIn OAuth2

### App Setup

1. Create app at https://www.linkedin.com/developers/apps
2. Configure OAuth redirect URLs in app settings
3. Required scopes: `openid`, `profile`, `w_member_social`

### n8n Credential Configuration

**Important toggles** (both must be OFF):
- ❌ Turn OFF "Organization Support" toggle
- ❌ Turn OFF "Legacy" toggle

Both toggles cause `unauthorized_scope_error` if enabled.

### Getting Your Member ID

LinkedIn requires your member ID in URN format for posting and profile operations.

**Method: Use LinkedIn UserInfo API**

Create a simple workflow:
1. Manual Trigger
2. HTTP Request to `https://api.linkedin.com/v2/userinfo`
3. Use LinkedIn OAuth2 credentials
4. Extract `sub` field from response

**Configuration:**
```json
{
  "method": "GET",
  "url": "https://api.linkedin.com/v2/userinfo",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "linkedInOAuth2Api"
}
```

**Response:**
```json
{
  "sub": "abc123xyz",  // This is your member ID
  "name": "Your Name",
  "email": "your@email.com"
}
```

**URN Format:**

The member ID must be formatted as a URN for LinkedIn API calls:

```
urn:li:person:{member_id}
```

**Examples:**
- If `sub` is `s7_nIa3ccD`, use `urn:li:person:s7_nIa3ccD`
- If `sub` is `abc123`, use `urn:li:person:abc123`

**In expressions:**
```javascript
// Convert sub to URN
={{ `urn:li:person:${$json.sub}` }}
```

**See also:** `assets/examples/linkedin-member-id-workflow.json` for complete workflow example

## Anthropic API

### Setup

1. Get API key from https://console.anthropic.com/
2. Add as "Header Auth" credential in n8n
3. Header name: `x-api-key`
4. Header value: Your API key

### Common Models

- `claude-3-5-sonnet-20241022` - Best for content generation
- `claude-3-opus-20240229` - Most capable, higher cost
- `claude-3-haiku-20240307` - Fastest, lowest cost

### Recommended Parameters for Content Generation

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "temperature": 0.7,
  "max_tokens": 400
}
```

## NewsAPI

### Setup

1. Get API key from https://newsapi.org/
2. Add as "Header Auth" credential in n8n
3. Header name: `X-Api-Key`
4. Header value: Your API key

### Rate Limits

Free tier: 100 requests/day (sufficient for most use cases)

### Common Endpoints

#### `/v2/everything` - Search All Articles

Search through millions of articles from news sources and blogs.

**URL:** `https://newsapi.org/v2/everything`

**Query Parameters:**
- `q`: Keywords or phrases to search for (required)
- `sources`: Comma-separated news source IDs
- `from`: Earliest date to retrieve (ISO 8601)
- `to`: Latest date to retrieve (ISO 8601)
- `language`: 2-letter ISO-639-1 code (e.g., `en`)
- `sortBy`: `relevancy`, `popularity`, or `publishedAt`
- `pageSize`: Number of results (max 100)

**Example:**
```json
{
  "url": "https://newsapi.org/v2/everything",
  "qs": {
    "q": "AI OR automation",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 50
  }
}
```

---

#### `/v2/top-headlines` - Breaking News

Get breaking news headlines for a country and category.

**URL:** `https://newsapi.org/v2/top-headlines`

**Query Parameters:**
- `country`: 2-letter ISO 3166-1 code (e.g., `us`)
- `category`: `business`, `entertainment`, `general`, `health`, `science`, `sports`, `technology`
- `q`: Keywords to search for
- `pageSize`: Number of results (max 100)

**Example:**
```json
{
  "url": "https://newsapi.org/v2/top-headlines",
  "qs": {
    "country": "us",
    "category": "technology",
    "pageSize": 20
  }
}
```

---

### Response Format

**Article structure:**
```json
{
  "source": {
    "id": "source-id",
    "name": "Source Name"
  },
  "author": "Author Name",
  "title": "Article Title",
  "description": "Article description",
  "url": "https://article-url.com",
  "urlToImage": "https://image-url.com/image.jpg",
  "publishedAt": "2024-01-15T10:30:00Z",
  "content": "Article content..."
}
```

**Important notes:**
- NewsAPI doesn't provide engagement scores (likes, shares, comments)
- For ranking by relevance, implement custom scoring based on keywords, recency, and source
- `publishedAt` is in ISO 8601 format

---

### Data Normalization Example

Normalize NewsAPI response to common schema:

```json
{
  "assignments": {
    "assignments": [
      {
        "name": "title",
        "value": "={{ $json.title }}",
        "type": "string"
      },
      {
        "name": "url",
        "value": "={{ $json.url }}",
        "type": "string"
      },
      {
        "name": "source",
        "value": "={{ $json.source.name }}",
        "type": "string"
      },
      {
        "name": "timestamp",
        "value": "={{ $json.publishedAt }}",
        "type": "string"
      },
      {
        "name": "summary",
        "value": "={{ $json.description }}",
        "type": "string"
      },
      {
        "name": "score",
        "value": 0,
        "type": "number"
      }
    ]
  }
}
```

## General Troubleshooting

### Authentication Errors

- Verify API key is correct and not expired
- Check header names match exactly (case-sensitive)
- Ensure required scopes are granted (OAuth)

### Rate Limiting

- Implement exponential backoff for retries
- Cache responses when possible
- Use webhook triggers instead of polling when available
