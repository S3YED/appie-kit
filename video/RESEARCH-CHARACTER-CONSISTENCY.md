# Character Consistency in AI Video — Research Notes

**Date:** 2026-03-27
**Purpose:** Best tools & methods for keeping Appie consistent across 6-scene origin story video
**Sources:** Exa deep search, multiple production guides, creator workflows

---

## Tier 1 Tools (Ranked by Character Consistency Score)

### 1. Kling 3.0 Elements — Score: 9/10 ⭐ OUR PICK
- **Platform:** fal.ai (API), klingai.com (web UI)
- **How it works:** Upload reference images as "Elements". Tag in prompt as `@Element1`.
- **API endpoint:** `fal-ai/kling-video/v3/standard/reference-to-video`
- **Input:** Array of `KlingV3ComboElementInput` objects:
  - `reference_image_urls`: array of side/pose images
  - `frontal_image_url`: front-facing headshot
- **Prompt syntax:** `"@Element1 wizard walks through..."` (1-based index)
- **Supports:** Up to 5 reference images per element
- **Multi-shot:** Up to 15 seconds, multiple shots in single generation
- **Cost:** ~$0.029/sec (Pro mode ~$3-4 per 10s clip)
- **Why #1:** Highest consistency score in independent benchmarks. "Elements" system locks identity across angles, lighting, expressions.
- **Source:** noelcabral.com deep dive, digitaljournal.com review, Medium analysis

### 2. Seedance 2.0 — Score: 8.5/10
- **Platform:** WaveSpeedAI, Dreamina (CapCut), SeaArt, Atlas Cloud
- **How it works:** "Universal Reference" system with `@Image1` / `@Video1` tags
- **Input:** Up to 12 assets (9 images, 3 videos, 3 audio)
- **Best practice:**
  - Prepare 1-4 reference images (front, 3/4, profile views)
  - Neutral pose/expression, same lighting, 2K+ resolution
  - Prompt: `"@Image1 for exact face/character identity, maintain throughout"`
  - Use `consistency_level: high`
  - Negative prompts: `"blurry, distorted faces"`
- **Strength:** Multi-shot cinematic narratives with native subject consistency
- **NOT on fal.ai** (separate platforms needed)
- **Source:** programminginsider.com, spacecoastdaily.com

### 3. Veo 3.1 (Google) — Score: 8/10
- **Best cinematic quality overall**
- **Much more expensive:** ~$0.75/sec vs Kling's $0.029
- **Reference-driven consistency, native audio**
- **Good for final hero shots, not for iterating**

### 4. Runway Gen-4.5 — Score: 7.5/10
- Reference conditioning
- Better for style consistency than identity consistency

---

## The Production Workflow (From Creators Earning $5K-30K/mo on YouTube)

### Phase 1: Character Bible (CRITICAL)
1. Generate/collect high-quality reference images from MULTIPLE ANGLES:
   - **Front face** (headshot)
   - **3/4 angle face**
   - **Profile (side view)**
   - **Full body front**
   - **Full body 3/4**
   - **Action pose**
2. All same style, same lighting, same outfit
3. Resolution: 2K+ minimum
4. This is the SINGLE MOST IMPORTANT STEP

### Phase 2: Shot Planning
1. Write shot list with camera directions per scene
2. Batch similar shots (same angle, same lighting conditions)
3. Don't generate chronologically — batch by similarity

### Phase 3: Generation
1. Upload character bible images as Elements/References
2. Use image-to-video with approved stills as starting frames
3. Generate in batches of similar shots
4. QA each clip for identity drift (face, hair, outfit, eyes)

### Phase 4: Assembly
1. FFmpeg or DaVinci Resolve for stitching
2. Add voiceover (ElevenLabs)
3. Music + sound design
4. Export per platform (9:16, 16:9)

---

## Key Insights

### Why Image-to-Video Helps But Doesn't Fully Solve It
- Model must infer how 2D reference looks from different angles
- Still introduces variation in jaw shape, hair shade, eye spacing
- Over 40-60 clips, small variations compound into obvious inconsistency
- **Solution:** Reinforce with Element references + consistent prompting

### The "90% Control" Formula (Pro Tip from Filmmaker)
> "Use Element Library to lock your character, then Custom Multi-Shot for angles.
> This gives you roughly 90% control over narrative flow."

### What We Need That We DON'T Have Yet ⚠️
- **Full body shots** (we only have headshots!)
- **Side/profile views**
- **Action poses**
- **Different angles of same outfit/cloak**
- Without these, Kling Elements will struggle with body consistency
- The model will hallucinate the body differently each time

### Recommended Reference Image Set (Minimum)
| View | Purpose | Status |
|------|---------|--------|
| Front face headshot | Identity anchor | ✅ Have (all 4 ages) |
| 3/4 angle face | Angle consistency | ❌ NEED |
| Profile (side) | Side shot consistency | ❌ NEED |
| Full body front | Body/outfit lock | ❌ NEED |
| Full body 3/4 | Walking/action shots | ❌ NEED |
| Action pose | Dynamic scenes | ❌ NEED |

---

## Cost Comparison

| Tool | Cost/sec | 10s clip | 60s video (6 clips) |
|------|----------|----------|----------------------|
| Kling 3.0 Standard | $0.029 | $0.29 | $1.74 |
| Kling 3.0 Pro | ~$0.35 | $3.50 | $21.00 |
| Seedance 2.0 | Varies | $2-5 | $12-30 |
| Veo 3.1 | $0.75 | $7.50 | $45.00 |
| Sora 2 | ~$0.50 | $5.00 | $30.00 |

---

## Sources
- https://www.aimagicx.com/blog/long-form-ai-video-character-consistency-guide-2026
- https://noelcabral.com/kling-ai-3-0-deep-dive
- https://www.digitaljournal.com/pr/news/vehement-media/kling-ai-3-0-review-1-1759575677.html
- https://medium.com/@vik_agny/kling-3-0-the-new-king-of-ai-video-control-c8e7f5e39260
- https://programminginsider.com/seedance-2-and-the-breakthrough-in-visual-consistency/
- https://spacecoastdaily.com/2026/02/character-consistency-solved-maintaining-identity-across-scenes-in-seedance-2-0/
- http://ulazai.com/ai-video-models-guide-2025/
- https://kling3.video/
- https://seedance-ai.com/

*Last updated: 2026-03-27*
