---
name: motion-animate-view
description: "Motion library's animateView() and AnimateView — View Transition API wrapper with spring animations, interruption handling, and page transitions. Now free in core library (v12.41+). Use when building page transitions, layout animations, or view morphing effects."
author: Appie-1
tags: [motion, animation, view-transitions, react, page-transitions, framer-motion]
---

# Motion animateView — View Transitions

Motion v12.41.0+ (June 23, 2026) graduated `animateView()` from Motion+ Early Access into the free core library. It wraps the browser's native View Transition API with a clean API, spring animations, and interruption handling.

## Why animateView?

The browser's native View Transition API is powerful but painful to use directly. Motion's `animateView()`:
- **Cleaner API** — declarative, chainable builder
- **Spring animations** — native View Transitions only support CSS easing
- **Interruption handling** — queuing so rapid clicks don't break animations
- **Simplified shared element matching** — auto-generates `view-transition-name`
- **Graceful degradation** — DOM updates still run in browsers without View Transition API

## JavaScript API

```js
import { animateView } from "motion";

// Basic usage
await animateView(() => {
  // Update the DOM here
  document.querySelector(".container").innerHTML = newContent;
});

// Shared element morphing
animateView((update) => {
  updateDOM();
})
  .add(".card")           // Select elements to animate
  .new({ opacity: [0, 1] })  // Incoming page
  .old({ opacity: [1, 0] })  // Outgoing page
  .layout({ duration: 0.3 }); // Shared layout transition
```

## React API (AnimateView)

```tsx
import { AnimateView } from "motion/react";

function Page({ show }) {
  return (
    <AnimateView show={show} transition={{ type: "spring", duration: 0.5 }}>
      <div className="content">
        <h1>My Page</h1>
      </div>
    </AnimateView>
  );
}
```

## Key Methods

| Method | Purpose |
|--------|---------|
| `.add(selector)` | Target elements for shared element morphing |
| `.new(values)` | Animate incoming elements |
| `.old(values)` | Animate outgoing elements |
| `.enter(values)` | Elements entering the DOM (no old match) |
| `.exit(values)` | Elements leaving the DOM (no new match) |
| `.layout(options)` | Custom transition for shared layout animation |
| `.class(name)` | Tag elements with `view-transition-class` |
| `.crop(false)` | Disable automatic border-radius cropping |

## Page Transitions

```js
animateView(() => navigate("/about"))
  .new({ opacity: [0, 1], x: [20, 0] })
  .old({ opacity: [1, 0], x: [0, -20] });
```

## Upgrade from framer-motion

```bash
npm uninstall framer-motion
npm install motion
```

```tsx
// Before
import { motion } from "framer-motion";
// After
import { motion } from "motion/react";
```

## When to Use

- **Page transitions** — route changes, full-view swaps (best fit)
- **Shared element morphing** — card expanding to detail view
- **Layout changes** — reordering, toggling between layouts
- **NOT for micro-interactions** — view transitions are non-interruptible; use layout animations for responsive UIs

## Pitfalls

- View transitions are non-interruptible — one at a time, unlike layout animations
- State changes must be wrapped in `startTransition` for React
- Not available in all browsers — degrades gracefully (no animation, DOM still updates)
- `motion` package replaces `framer-motion` — update imports