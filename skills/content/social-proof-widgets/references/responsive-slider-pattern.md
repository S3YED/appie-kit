# Responsive Google Reviews Slider — Component Template

Complete Next.js client component for a branded Google reviews carousel.

## Dependencies
- `framer-motion` (motion primitives)
- `lucide-react` (Star icon)
- `next/image` (profile photos)
- Tailwind CSS with the site's design tokens

## Component Structure

```
src/app/<page>/GoogleReviewsSlider.tsx  — the slider component
src/app/<page>/data/google-reviews.ts  — typed review data from Places API
```

## Data File Type (`data/google-reviews.ts`)

```ts
export interface GoogleReview {
  author: string;
  rating: number;
  text: string;
  time: string;
  photo: string;  // Google CDN profile_photo_url
}

export const GOOGLE_RATING = 5.0;       // from API
export const GOOGLE_REVIEW_COUNT = 59;   // from API user_ratings_total
export const GOOGLE_PLACE_URL = "https://maps.google.com/?cid=<CID>";

export const GOOGLE_REVIEWS: GoogleReview[] = [
  // 4-5 reviews from the Places API
];
```

## Responsive Size Table

| Element | Mobile (<640px) | Tablet+ (md:) |
|---------|----------------|---------------|
| Section padding | `py-16` | `md:py-24` |
| Container padding | `px-4` | `md:px-6` |
| Title | `text-xs` | `md:text-sm` |
| Heading | `text-3xl` | `md:text-5xl` |
| Google badge padding | `px-3 py-2` | `md:px-5 md:py-2.5` |
| Google badge gap | `gap-2` | `md:gap-3` |
| Google G icon | `w-4 h-4` | `md:w-5 md:h-5` |
| Star icon | `w-3 h-3` | `md:w-4 md:h-4` |
| Badge text | `text-xs` | `md:text-sm` |
| Card padding | `p-5` | `md:p-10` |
| Card rounding | `round-2xl` | `md:round-3xl` |
| Review text | `text-base` | `md:text-lg` |
| Arrow buttons | `w-8 h-8` | `md:w-10 md:h-10` |
| Arrow SVG | `w-4 h-4` | `md:w-5 md:h-5` |
| Arrow offset | `-translate-x-1` | `md:-translate-x-2` |
| Profile photo | `w-9 h-9` | `md:w-11 md:h-11` |
| Author name | `text-xs` | `md:text-sm` |
| Author time | `text-[10px]` | `md:text-xs` |
| Card overflow px | `px-6` | `md:px-8` |

## Key Patterns

1. **Auto-advance**: `useEffect(() => { const t = setInterval(next, 5000); return () => clearInterval(t); }, [next])`
2. **Track changes**: `useEffect(() => { if (current >= total) setCurrent(0) }, [current, total])`
3. **Filter empties**: `GOOGLE_REVIEWS.filter(r => r.text)` — skip reviews with no text
4. **Key-based remount**: `key={current}` on the motion.div forces re-animation on slide change
5. **Google brand colors**: Star fill: `#FBBC05`, Card: `bg-white/10 backdrop-blur-md`, Nav arrows: `bg-[#0E3D31]/60`

## Integration Hook

In the page component:
```tsx
import GoogleReviewsSlider from './GoogleReviewsSlider';

// Insert between pricing and FAQ:
<GoogleReviewsSlider />
```

## Stats Bar Mobile Fix

For hero stats that overflow on 375px:
```tsx
className="grid grid-cols-2 sm:flex sm:flex-wrap items-center justify-center gap-3 sm:gap-6"
// Hide pipe separators on mobile:
className="hidden sm:inline text-[#F6FEFC]/20"
```