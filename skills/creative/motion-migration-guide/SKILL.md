---
name: motion-migration-guide
description: "Guide for migrating from framer-motion to Motion (motion/react) v12.42+. Covers the new import paths, animateView API for View Transitions, and breaking changes."
author: Appie-1
tags: [motion, animation, framer-motion, react, vue, migration]
related_skills: [motion-foundations, motion-patterns, motion-ui]
---

# Motion v12.42+ Migration Guide

Framer Motion has been spun out from Framer into an independent open-source project called **Motion**. The library is now at `motion/react` (was `framer-motion`).

## Key Changes

### New Import Paths

```typescript
// OLD (framer-motion)
import { motion, AnimatePresence, useScroll } from "framer-motion";

// NEW (Motion)
import { motion, AnimatePresence, useScroll } from "motion/react";
```

### animateView API (View Transitions)
Introduced in v12.41, moved to main library in v12.42:

```typescript
import { animateView } from "motion/react";

// Basic page transition
animateView(() => {
  // DOM updates happen here
  updatePageContent();
}, {
  // Transition options
  duration: 0.5,
  easing: [0.16, 1, 0.3, 1],
});
```

**Key features:**
- `.add()`, `.new()`, `.old()`, `.layout()`, `.class()` — fine-grained control
- Auto-grouping — layers auto-group to match DOM hierarchy
- `.group(false)` to opt out of auto-grouping
- Auto-crop with border-radius animation (aspect-ratio aware)

### Framework Support
- **React:** `motion/react`
- **Vue 3:** `motion-v` (new!)
- **Vanilla JS:** Works without any framework
- **Solid:** `motion/solid` (community)

## Installation

```bash
npm install motion
# or
pnpm add motion
# or
yarn add motion
```

After installing, remove `framer-motion` from package.json.

## Migration Steps

1. `npm uninstall framer-motion && npm install motion`
2. Replace all imports: `from "framer-motion"` → `from "motion/react"`
3. Update `package.json` references
4. Test AnimatePresence exit animations (bug fixed in v12.42.2)

## Version History (Recent)

| Version | Date | Key Change |
|---------|------|------------|
| v12.41.0 | 2026-06-23 | `animateView` moves from Early Access to main library |
| v12.42.0 | 2026-06-24 | `animateView` layers auto-group, aspect-ratio aware auto-crop |
| v12.42.2 | 2026-06-30 | Bug fixes: AnimatePresence exit, drag constraints, scroll hydration |

## Pitfalls
- `motion/react` is the new canonical path, NOT `motion` (bare import)
- If you still see `framer-motion` in lockfile after migration, run `npm dedupe`
- AnimatePresence exit animation bugs were fixed in v12.42.2 — upgrade if you're on an older v12 release===ME:motion-migration-guide