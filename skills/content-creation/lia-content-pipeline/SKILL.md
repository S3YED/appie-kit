---
name: lia-content-pipeline
description: Canonical Lia Smeraldi content generation pipeline running on Spark Atlas DGX. Use when the task is to generate, regenerate, batch, inpaint, upscale, or QA any Lia content (Tier 0 SFW, Tier 1 suggestive, Tier 2 explicit). Enforces bible identity lock + ReActor face-swap + Lia LoRA + ADetailer + iPhone aesthetic post-process.
version: 2.0.0
created: 2026-05-26
license: private
metadata:
  openclaw:
    emoji: "🌸"
    requires:
      bins: [curl, python3, ssh, tmux]
      services: [spark-comfyui]
---

# Lia Content Pipeline

## Single source of truth

The canonical Lia Smeraldi identity lives in the bible:
- **On Diddy host**: `/Users/diddywolf888/.hermes/workspace-diddy/assets/lia/LIA_CHARACTER_BIBLE.md`
- **On Spark mirror**: `/home/admin/lia-training/LIA_CHARACTER_BIBLE.md`

Active source images (18 originals, 2026-05-25 delivery):
- **On Diddy**: `/Users/diddywolf888/.hermes/workspace-diddy/assets/lia/original_source_20260525/`
- **On Spark**: `/home/admin/lia-training/originals/`

The **canonical headshot** used by ReActor face-lock is `lia_original_source_18.jpg`. On Spark this is mirrored at:
```
/home/admin/ComfyUI/input/lia_refs/lia_canonical_2026_05_25.jpg
```

The **previous left-side/bad image** from old face-lock sheet is RETIRED. Do not use it for any new generation, training, or QA.

## Pipeline stack on Spark Atlas

| Layer | Model / file | Purpose |
|---|---|---|
| Base checkpoint | `ponyRealism_V22MainVAE.safetensors` | NSFW-realism SDXL fine-tune, anatomy-strong |
| Lia LoRA | `lia_v2.safetensors` (or `lia_v1.safetensors`) | Bible-trained identity LoRA, 218MB |
| Film grain LoRA | `Analog-Diffusion/` (when stacked) | Adds 35mm grain texture |
| ControlNet | `openpose-sdxl` (xinsir) | Pose lock from reference photo |
| ControlNet | `canny-sdxl` (xinsir) | Composition lock from reference |
| ADetailer | `face_yolov8n.pt` + `hand_yolov8n.pt` | Auto face + hand fix |
| ReActor | `inswapper_128.onnx` + `codeformer.pth` | Face-swap with canonical headshot, visibility 1.0, codeformer 0.85 |
| Upscaler | `4x-UltraSharp.pth` + `RealESRGAN_x4plus.pth` | Post-generation sharpening |
| IP-Adapter | `ip-adapter-faceid-plusv2_sdxl.bin` | Optional identity conditioning during generation |

## Identity blocks (use verbatim)

### Positive identity block
```
Lia Smeraldi, same adult woman from the active Lia source images,
olive tan skin, light hazel green eyes, thick dark natural eyebrows,
shoulder-length dark brown curly hair with defined loose curls,
soft oval heart-shaped face, natural freckles across nose and cheeks,
full soft pink lips, athletic feminine body, toned waist and legs,
natural medium bust, realistic iPhone photo texture,
private camera-roll realism, confident mature feminine energy
```

### Negative identity block
```
different woman, straight hair, blonde hair, blue eyes, dark brown eyes,
plastic skin, doll face, anime face, teenage look, childlike,
over-smoothed, fake glamour model, exaggerated breast size,
distorted hands, distorted feet, broken anatomy, melted limbs,
bad teeth, warped eyes, changed nose, changed jaw, generic influencer face
```

### Pony quality prefix
```
score_9, score_8_up, score_7_up, source_photo, rating_explicit,
amateur iPhone snapshot, 35mm film grain, Kodak Portra 400,
warm tungsten 3200K, low-light film photography
```

## iPhone aesthetic boosters

Always include in positive prompt:
- `(amateur iPhone snapshot:1.3)`
- `(heavy 35mm film grain:1.25)`
- `(Kodak Portra 400 grain:1.15)`
- `(low-light film photography:1.15)`
- `(slight motion blur natural hand-held:1.1)`
- `(warm tungsten 3200K:1.15)`
- `(high ISO 1600 noise:1.1)`

Always exclude (high-weight negatives):
- `(studio lighting:1.3)`
- `(professional model pose:1.3)`
- `sharp clean polished`
- `instagram filter`

## Settings (production-validated)

```
checkpoint:        ponyRealism_V22MainVAE.safetensors
LoRA stack:
  - lia_v2.safetensors at strength 0.85
  - Analog-Diffusion at strength 0.35 (optional, for grain)
resolution:        896x1344 (iPhone portrait 2:3 aspect)
steps:             45
cfg:               7.5
sampler:           dpmpp_2m_sde + karras
ADetailer:         face_yolov8n (0.5 denoise) + hand_yolov8n (0.4 denoise)
Upscale:           2x via 4x-UltraSharp + downscale, denoise 0.25
ReActor:
  swap_model:                inswapper_128.onnx
  facedetection:             retinaface_resnet50
  face_restore_model:        codeformer.pth
  face_restore_visibility:   1.0
  codeformer_weight:         0.85
  source:                    lia_refs/lia_canonical_2026_05_25.jpg
```

## Production rule (per bible §"Current production rule")

1. **Use this bible first.**
2. Use active source images as identity truth.
3. **Do ONE test render first** before any batch.
4. **QA against the face lock sheet** before sending or batching:
   - `/home/admin/lia-training/character_lock/lia_face_lock_sheet_new_sources_delivery.jpg`
5. **If the face drifts, STOP. Do not batch.** Adjust prompt + retry.
6. Tier 2 outputs require Seyed approval before posting (review queue).

## Bible reject conditions (auto-regenerate triggers)

If any of these happen in output, REJECT + REGENERATE:
- Hair becomes straight, blonde, long glam waves, or generic model hair
- Eyes become dark brown/blue or lose hazel-green look
- Face becomes too young, anime, doll-like, or overly airbrushed
- Jaw too sharp/masculine or nose changes heavily
- Freckles/skin texture disappear completely
- Body/face looks like a different influencer
- Bust oversized/fake-looking
- Pose physically impossible
- Hands/feet melted, duplicated, or broken

## Public vs private content tiers (per bible)

| Tier | Where | What's allowed |
|---|---|---|
| 0 SFW | Public/social teaser | clothed, teasing, no explicit nipples/genitals |
| 1 Suggestive | Fanvue/Fansly feed | lingerie, robe, thong, implied nude |
| 2 Explicit | PPV/private | revealing, still QA face/body lock hard |

## Wardrobe anchors (per bible §"Wardrobe/style lock")

Recurring Lia wardrobe:
- Black long-sleeve bodysuit / black fitted top
- Pink ribbed one-piece / soft feminine loungewear
- White ribbed top / white crop top
- Navy/dark fitness set
- Casual hoodie/car selfie look
- Heart pajamas/private bedroom look
- Red polka-dot thong/panty (private-feed/paid lane only)
- Sheer tops (adult/private-feed only)

## Generation scripts

Canonical script (works on any host with ssh access to Spark):
```
/Users/appie/clawd/projects/wolf-diddy/scripts/lia-v5-canonical.py
```

Diddy mirror:
```
/Users/diddywolf888/.hermes/workspace-diddy/scripts/lia-v5-canonical.py
```

Run examples:
```bash
# Tier 2 explicit batch (4 nude scenes)
python3 lia-v5-canonical.py --tier 2

# Tier 1 suggestive batch (lingerie/robe)
python3 lia-v5-canonical.py --tier 1

# Custom output dir
python3 lia-v5-canonical.py --outdir /path/to/queue/
```

## ComfyUI endpoints (Spark)

```
host: http://100.69.197.43:8188
POST /prompt                            # submit workflow JSON, returns prompt_id
GET  /history/{prompt_id}               # status + outputs
GET  /view?filename=...&type=output     # fetch output PNG
GET  /system_stats                      # GPU + RAM health
```

## Safety floor (NON-NEGOTIABLE)

- Real-person photo nudify = NEE (NL Strafrecht 139h, EU AI Act §50)
- All Lia outputs MUST face-match canonical headshot (cosine >0.85)
- Stage 1 visible age <25 = auto-reject
- Tier 2 outputs gated by Seyed approval before posting
- C2PA stamp `synthetic=true` on all outputs (TODO)

## Higgsfield fallback (if Spark unreachable)

```bash
higgsfield generate create text2image_soul_v2 \
  --prompt "<bible identity block + scene>" \
  --aspect_ratio 2:3 \
  --quality 2k \
  --custom_reference_id 28420527-0cdc-4bdd-927e-81574162b123 \
  --wait --wait-timeout 8m
```

## Operational checklist (run before every batch)

- [ ] ComfyUI alive: `curl http://100.69.197.43:8188/system_stats`
- [ ] Canonical headshot present: `ssh spark "ls /home/admin/ComfyUI/input/lia_refs/lia_canonical_2026_05_25.jpg"`
- [ ] Lia LoRA installed: `ssh spark "ls /home/admin/ComfyUI/models/loras/lia_v2.safetensors"`
- [ ] ponyRealism checkpoint available
- [ ] One test render passes face-lock QA
- [ ] Tier 2 outputs gated by Seyed approval

## Caption voice (per bible §"Caption voice")

- Controlled, private access, not needy, seductive but classy
- Short lines, no em dashes
- Examples: "Quick mirror check. You were not supposed to see this much." / "Private room. No audience." / "Not polished. Private. Mine."
