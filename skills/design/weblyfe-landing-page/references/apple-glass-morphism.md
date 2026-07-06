# Apple Glass Morphism — Dark Background Card Pattern

For dark-themed websites (like weblyfe.ai), DON'T use pure white boxes (`bg-white`) — they're "te fel" (too harsh). Use translucent glass:

```
bg-white/30 backdrop-blur-md border border-white/30
```

This creates an Apple iOS frosted glass effect:
- **30% white opacity** — lets the dark background show through subtly
- **backdrop-blur-md** — blurs content behind the card for depth
- **border-white/30** — subtle glass edge, not harsh green border

## Text Colors on Glass

| Element | Class |
|---------|-------|
| Headings | `text-[#0E3D31]` (dark green) |
| Body text | `text-[#0E3D31]/80` (dark green, slightly muted) |
| Labels/muted | `text-[#0E3D31]/70` |
| Gold accents | `text-[#DFB771]` (keep gold for stars, CTAs) |

## Hover State

```
hover:bg-white/80 hover:border-white/50
```

## Where This Applies

- Stat/metric boxes (500+, 5+, 24/7)
- Tech stack pills (WhatsApp, Telegram, Voice Notes, etc.)
- Testimonial cards
- Process/How It Works cards
- Category badges
- Any card on a dark green (#031D16 / #0E3D31) background

## Contrast vs Old Approach

| Before | After |
|--------|-------|
| `bg-[#0E3D31]/50 border-[#247459]/20` | `bg-white/30 backdrop-blur-md border-white/30` |
| Dark green on dark green — muddy, low contrast | Light glass on dark — crisp, modern |
| Gold text on dark green | Dark green text on glass — readable |

## Seyed's Feedback

- "Wit is te fel" — full opacity white is too harsh
- "translucent apple design glass transparant met witte tint" — wants Apple-style frosted glass
- "niet zo veel contrast" — the glass should blend, not jump out
