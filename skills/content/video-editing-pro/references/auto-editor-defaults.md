# auto-editor Default Parameters Reference

Source: https://auto-editor.com/ref/edit + https://auto-editor.com/options

## Audio edit method defaults

```
(audio [threshold] [stream])
  threshold: 0.04   (normalized amplitude, NOT dB)
  stream: 'all
```

`threshold=0.04` means: if the loudest sample in a timebase window divided by the max possible sample value is less than 0.04, that window is considered silent.

Approximate dB equivalents:
- 0.04 normalized ≈ -28 dBFS
- 0.05 ≈ -26 dBFS
- 0.09 ≈ -21 dBFS
- For noisy rooms or distant mics, raise threshold to 0.06–0.08

## Margin (padding)

```
--margin 0.2s
```

200ms is added before AND after every "loud" segment. This is the buffer that prevents consonants from being clipped. Never go below 0.1s. For natural speech, 0.3–0.4s feels more conversational.

## Smooth (mincut and minclip)

```
--smooth 0.2s,0.1s
  mincut:  0.2s  — don't cut a silence shorter than 200ms
  minclip: 0.1s  — don't keep a loud clip shorter than 100ms
```

These prevent the Swiss-cheese effect where tiny silences between syllables get cut.

## Motion detection defaults (for B-roll/screen recording edits)

```
(motion [threshold] [stream] [blur] [width])
  threshold: 0.02
  blur: 9
  width: 400
```

## Actions (defaults)

```
--when-normal nil     (keep loud sections unchanged)
--when-silent cut     (cut silent sections)
```

## Practical thresholds for talking-head Dutch/English creator content

| Scenario | Threshold | Margin | Notes |
|---|---|---|---|
| Clean indoor audio (handheld mic) | 0.04 | 0.2s | Default, works fine |
| Slight room noise / iPhone mic | 0.06 | 0.25s | Raise threshold slightly |
| Noisy environment | 0.08–0.10 | 0.3s | May need manual review |
| Aggressive cut (podcast style) | 0.04 | 0.15s | Tighter, review result |

## Source: Discussion #593 (user reporting words being cut)

User reported: "word endings are getting cut." Root cause: threshold too high, cutting mid-syllable.
Fix: lower threshold until silent regions don't overlap waveform, OR increase margin to 0.3s.

This confirms: 200ms margin is the minimum comfortable setting. When in doubt, increase margin rather than threshold.
