/**
 * Ranking and Scoring Algorithms for n8n Code Nodes
 *
 * Reusable patterns for calculating relevance scores and ranking items.
 * Use after deduplication to prioritize the most relevant items.
 */

// ============================================================================
// MULTI-FACTOR RANKING
// ============================================================================
// Combines relevance, recency, and engagement into weighted score

const items = $input.all().map(item => item.json);

// Configuration
const config = {
  highValueKeywords: ['ai', 'automation', 'machine learning', 'n8n', 'workflow'],
  mediumValueKeywords: ['technology', 'innovation', 'digital', 'api', 'integration'],
  lowValueKeywords: ['software', 'development', 'programming', 'data'],
  weights: {
    relevance: 0.5,  // 50% - keyword matching
    recency: 0.3,    // 30% - how recent
    engagement: 0.2   // 20% - likes/comments/score
  },
  recencyHours: {
    veryRecent: 6,   // < 6 hours = 3 points
    recent: 24,      // < 24 hours = 2 points
    moderate: 48     // < 48 hours = 1 point
  }
};

// Score each item
const scoredItems = items.map(item => {
  let relevanceScore = 0;
  let recencyScore = 0;
  let engagementScore = 0;

  // Relevance scoring (keyword matching)
  const text = ((item.title || '') + ' ' + (item.summary || '')).toLowerCase();

  config.highValueKeywords.forEach(keyword => {
    if (text.includes(keyword.toLowerCase())) relevanceScore += 3;
  });

  config.mediumValueKeywords.forEach(keyword => {
    if (text.includes(keyword.toLowerCase())) relevanceScore += 2;
  });

  config.lowValueKeywords.forEach(keyword => {
    if (text.includes(keyword.toLowerCase())) relevanceScore += 1;
  });

  // Recency scoring (time-based)
  const ageHours = (Date.now() - new Date(item.timestamp).getTime()) / (1000 * 60 * 60);
  if (ageHours < config.recencyHours.veryRecent) recencyScore = 3;
  else if (ageHours < config.recencyHours.recent) recencyScore = 2;
  else if (ageHours < config.recencyHours.moderate) recencyScore = 1;

  // Engagement scoring
  const score = item.score || 0;
  if (score > 100) engagementScore = 3;
  else if (score > 50) engagementScore = 2;
  else if (score > 20) engagementScore = 1;

  // Calculate weighted final score
  const finalScore =
    (relevanceScore * config.weights.relevance) +
    (recencyScore * config.weights.recency) +
    (engagementScore * config.weights.engagement);

  return {
    ...item,
    finalScore,
    relevanceScore,
    recencyScore,
    engagementScore
  };
});

// Sort by final score (descending)
const ranked = scoredItems.sort((a, b) => b.finalScore - a.finalScore);

// Return all or top N
const topN = ranked.slice(0, 10);  // Adjust as needed
return topN.map(item => ({ json: item }));


// ============================================================================
// SIMPLE KEYWORD SCORING
// ============================================================================
// Basic relevance based on keyword presence

const items = $input.all();
const keywords = ['ai', 'automation', 'workflow', 'n8n'];

const scored = items.map(item => {
  const text = (item.json.title + ' ' + item.json.summary).toLowerCase();
  let score = 0;

  keywords.forEach(keyword => {
    if (text.includes(keyword)) score += 1;
  });

  return {
    json: {
      ...item.json,
      keywordScore: score
    }
  };
});

// Sort by keyword score
const sorted = scored.sort((a, b) => b.json.keywordScore - a.json.keywordScore);
return sorted;


// ============================================================================
// TIME DECAY SCORING
// ============================================================================
// Exponential decay based on age

const items = $input.all();
const halfLife = 24; // Hours for score to decay by half

const scored = items.map(item => {
  const ageHours = (Date.now() - new Date(item.json.timestamp).getTime()) / (1000 * 60 * 60);
  const baseScore = item.json.score || 0;

  // Exponential decay formula: score * (0.5 ^ (age / halfLife))
  const decayedScore = baseScore * Math.pow(0.5, ageHours / halfLife);

  return {
    json: {
      ...item.json,
      originalScore: baseScore,
      ageHours: Math.round(ageHours),
      decayedScore: Math.round(decayedScore)
    }
  };
});

const sorted = scored.sort((a, b) => b.json.decayedScore - a.json.decayedScore);
return sorted;


// ============================================================================
// BAYESIAN RANKING
// ============================================================================
// Handles items with few votes/ratings (similar to Reddit's "Best" algorithm)

const items = $input.all();

const scored = items.map(item => {
  const upvotes = item.json.upvotes || 0;
  const downvotes = item.json.downvotes || 0;
  const total = upvotes + downvotes;

  if (total === 0) {
    return { json: { ...item.json, bayesianScore: 0 } };
  }

  // Wilson score confidence interval
  const z = 1.96; // 95% confidence
  const phat = upvotes / total;
  const score = (phat + z*z/(2*total) - z * Math.sqrt((phat*(1-phat)+z*z/(4*total))/total))/(1+z*z/total);

  return {
    json: {
      ...item.json,
      bayesianScore: score
    }
  };
});

const sorted = scored.sort((a, b) => b.json.bayesianScore - a.json.bayesianScore);
return sorted;


// ============================================================================
// USAGE NOTES
// ============================================================================

/*
CUSTOMIZING MULTI-FACTOR RANKING:

1. Update keywords to match your domain
   highValueKeywords: ['your', 'important', 'keywords']

2. Adjust weights based on priorities
   weights: { relevance: 0.6, recency: 0.2, engagement: 0.2 }

3. Modify recency thresholds
   recencyHours: { veryRecent: 12, recent: 48, moderate: 168 }

4. Change top N limit
   const topN = ranked.slice(0, 5);  // Return top 5

5. Add custom scoring factors
   const customScore = item.hasImage ? 2 : 0;
   finalScore += customScore * 0.1;  // 10% weight
*/
