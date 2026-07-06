# Animated SVG Icons with Framer Motion

When LottieFiles CDN blocks direct downloads (HTTP 403) or you want a lighter alternative to Lottie JSON, use Framer Motion to animate inline SVGs.

## Advantages over Lottie

| Factor | Lottie JSON | Animated SVG |
|--------|-------------|--------------|
| File size | 5-50KB per icon | ~0.5KB per icon |
| Dependencies | `lottie-react` + JSON | Framer Motion (already in stack) |
| Color control | Must edit JSON or use `rendererSettings` | Direct SVG props, Tailwind classes |
| Loading state | Fetch + parse delay | Immediate (inline) |
| CDN dependency | LottieFiles may 403 | Zero external calls |

## Pattern

Each icon is a plain SVG element with Framer Motion `motion.*` wrappers on the parts that animate.

### Basic structure

```tsx
import { motion } from "framer-motion";

export function AnimatedScale({ className = "", size = 24 }: { className?: string; size?: number }) {
  return (
    <svg className={className} width={size} height={size} viewBox="0 0 24 24"
      fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">

      {/* Static parts — plain SVG elements */}
      <path d="M12 3v18M8 21h8M3 7l4 4 4-4M13 17l4-4 4 4" />

      {/* Animated accent line — subtle oscillation */}
      <motion.line
        x1="3" y1="7" x2="13" y2="7"
        animate={{ x2: [13, 12, 13] }}
        transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        stroke="#d4b07a" strokeWidth="1.5"
      />
    </svg>
  );
}
```

### Animation types by icon role

| Icon | Animation | Technique |
|------|-----------|-----------|
| Scale/justice | Gold weighing beam oscillates | `motion.line` `x2` keyframes |
| Heart/pulse | Subtle scale pulse | `motion.path` `scale` keyframes, `transformOrigin: "center"` |
| Building | Windows glow staggered | `motion.rect` `opacity` keyframes with `delay` per window |
| File/document | Lines fade in sequence | `motion.line` `opacity` keyframes with staggered `delay` |
| Shield | Checkmark draws repeatedly | `motion.path` `pathLength` + `opacity` keyframes |
| Phone | Gentle shake/ring | `motion.g` `rotate` keyframes, `transformOrigin: "12px 12px"` |
| Mail | Envelope line fades | `motion.path` `opacity` keyframes |
| Check circle | Circle breathes + check draws | `motion.circle` `scale` + `motion.path` `pathLength` |
| Map pin | Pin bobs + inner circle pulses | `motion.path` `y` keyframes + `motion.circle` `r` keyframes |
| Arrow right | Line extends + arrow slides | `motion.line` `x2` + `motion.polyline` `x` keyframes |
| Briefcase | Drawer line fades | `motion.line` `opacity` keyframes |
| Message | Chat lines appear staggered | `motion.line` `opacity` keyframes with `delay` |

### Performance notes

- Use `opacity` and `scale`/`pathLength` over `d`/`path` for GPU-composited animations
- Keep `repeat: Infinity` durations at 2-4s for subtle ambient motion (not distracting)
- Avoid animating `stroke-dasharray` or complex paths — use `pathLength` instead
- Wrap in `IntersectionObserver` (via `useRef` + `useEffect`) to pause when off-screen if there are many instances on one page
- All icons share the gold accent color via the brand token — make it consistent

### Gold accent discipline

The animated accent color should match the brand's single accent color. For Soleiman/legal sites:
- Gold: `#d4b07a` (champagne — use on animated parts only)
- Navy: `#0f2644` (main color for icon background squares)
- Keep accent to ONE animated line/shape per icon — restraint = premium

### Full collection pattern

Export all icons from a single barrel file:

```tsx
export const iconMap = {
  scale: AnimatedScale,
  heart: AnimatedHeart,
  building: AnimatedBuilding,
  file: AnimatedFile,
  shield: AnimatedShield,
  phone: AnimatedPhone,
  mail: AnimatedMail,
  check: AnimatedCheck,
  pin: AnimatedPin,
  arrow: AnimatedArrow,
  briefcase: AnimatedBriefcase,
  message: AnimatedMessage,
} as const;
export type AnimatedIconName = keyof typeof iconMap;
```

Then import and use like `<AnimatedScale size={20} />` wherever the old `<Scale className="h-5 w-5" />` was used.