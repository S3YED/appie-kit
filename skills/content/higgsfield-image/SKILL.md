---
name: higgsfield-image
description: Generate images using Higgsfield's Nano Banana Pro (nano_banana_2) via the mcporter MCP server. Use for product photos, character-consistent fashion photography, and creative assets. Primary image generation tool for TracyToronto e-commerce content.
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires": { "tools": ["mcporter"] },
        "install": [],
      },
  }
---

# Higgsfield Image Generation

## Auth System (CRITICAL — two separate auth mechanisms)

Higgsfield has TWO auth systems. `generate_image` requires **OAuth tokens**, NOT the API key.

| Credential | Type | Used For | Location |
|---|---|---|---|
| `HIGGSFIELD_API_KEY_ID` + `HIGGSFIELD_API_KEY_SECRET` | API Key pair | `tools/list`, `balance` (read-only) | `~/.openclaw/workspace/config/mcporter.json` under `higgsfield.env` |
| OAuth Bearer token (from Clerk) | OAuth session | `generate_image`, `generate_video`, `show_characters` (write ops) | `~/.mcporter/credentials.json` under `higgsfield\|fb7b405dd99c24b1` |

**The API key pair does NOT work for `generate_image`.** That tool requires a valid Clerk OAuth access token.

## Quick Reference

**Tool:** `mcporter call higgsfield.generate_image`
**Model:** `nano_banana_2` (Nano Banana Pro, 4K quality)
**Auth:** OAuth Bearer token from mcporter credentials

## Generate an Image

```bash
mcporter call higgsfield.generate_image params='{"model":"nano_banana_2","prompt":"YOUR PROMPT","aspect_ratio":"4:5"}'
```

## With Reference Image (Character Consistency)

```bash
mcporter call higgsfield.generate_image params='{"model":"nano_banana_2","prompt":"YOUR PROMPT...same woman as reference...","aspect_ratio":"4:5","medias":[{"value":"https://URL-TO-REFERENCE-IMAGE.PNG","role":"image"}]}'
```

**IMPORTANT:** Use `value` (not `url`) for the media reference.

## OAuth Token Refresh

If `generate_image` returns "Invalid or expired token", the OAuth session has expired:

```bash
mcporter auth higgsfield --reset
```

This opens a browser for Clerk OAuth login and stores new tokens in `~/.mcporter/credentials.json`.

**Token status check:**
```bash
cat ~/.mcporter/credentials.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
e=d['entries'].get('higgsfield|fb7b405dd99c24b1',{})
print('Has tokens:', 'tokens' in e and bool(e.get('tokens')))
print('Updated:', e.get('updatedAt'))
"
```

## Check Generation Status

```bash
mcporter call higgsfield.show_generations type="image" size=5
```

Poll every ~30 seconds. 4K images take 30-50 seconds to generate.

## Models Available

| Model ID | Name | Best For |
|---|---|---|
| `nano_banana_2` | Nano Banana Pro | Top quality 4K, text/diagrams, fashion |
| `nano_banana_flash` | Nano Banana 2 | Fast 4K, high-volume work |
| `soul_2` | Soul 2 | Character/avatar consistency |
| `marketing_studio_image` | Marketing Studio | Product ads with avatars |

## Aspect Ratios

- `1:1` — Square (Instagram post, thumbnail)
- `4:5` — Portrait (Instagram post, fashion)
- `2:3` — Portrait tall (fashion editorial)
- `3:4` — Portrait (standard)
- `9:16` — Story/Reel vertical
- `16:9` — Landscape (YouTube, banner)
- `21:9` — Ultrawide (banner)

## Resolution Options

- `1k` — 1024px (fast draft)
- `2k` — 2048px (standard)
- `4k` — 4096px (premium, default for nano_banana_2)

## Character Photo System Prompt

Always include for realistic fashion photography:

```
The image must look like it was captured with a high-end DSLR fashion camera using an 85mm lens, with natural depth of field, realistic light diffusion, and authentic photographic detail. The result must be extremely photorealistic, studio-quality fashion photography in ultra 4K resolution, indistinguishable from a real camera photograph, with no AI artifacts or synthetic appearance. Maintain true-to-life skin texture, natural wrinkles, pores, and realistic lighting reflections. No beauty filters, no artificial smoothing.
```

## Complete Workflow Example

### 1. Generate product photo with character

```bash
# Start generation
RESULT=$(mcporter call higgsfield.generate_image params='{"model":"nano_banana_2","prompt":"Full-length studio fashion photograph of a mature woman (47 years old, Franco-Canadian, elegant professional style, same face as reference) wearing a cozy plaid fleece jacket in rich autumn colors. She stands confidently in a clean white studio setting, full body visible, natural depth of field, 85mm lens photography, ultra realistic fashion editorial, authentic photographic detail, no AI artifacts.","aspect_ratio":"2:3","medias":[{"value":"https://d8j0ntlcm91z4.cloudfront.net/user_3AFZ6u2cNdsIdJPF7lWsctX8zrH/hf_20260418_172507_97ef24b2-a658-4cd9-acb8-00429c66948d.png","role":"image"}]}')
JOB_ID=$(echo $RESULT | python3 -c "import json,sys; print(json.load(sys.stdin)['results'][0]['id'])")
echo "Job ID: $JOB_ID"

# Wait and check
sleep 40
mcporter call higgsfield.show_generations type="image" size=5 | python3 -c "
import json, sys
data = json.load(sys.stdin)
for g in data.get('items', []):
    if g.get('id') == '$JOB_ID':
        print('STATUS:', g.get('status'))
        if g.get('status') == 'completed':
            print('URL:', g.get('results', {}).get('rawUrl'))
"
```

### 2. Download generated image

```bash
curl -s "IMAGE_URL" -o ./generated_image.png
```

## Quality Notes

- **nano_banana_2** produces 8/10 fashion photography — excellent skin textures, realistic lighting
- 4K generation takes 30-50 seconds
- Reference images must be accessible HTTPS URLs (no local files in MCP context)
- For Margot character: use `margot_APPROVED.jpg` as reference

## Troubleshooting

**"Invalid or expired token":** OAuth session expired. Run `mcporter auth higgsfield --reset` on the Mac Mini.

**"Model not found":** Check model ID is correct — use `nano_banana_2` not `nano-banana-pro`

**"Invalid arguments: expected string, received undefined":** The `medias` field requires `{value: string, role: string}`, not `{url: ..., roles: [...]}`

**Generation pending forever:** Poll `show_generations` with size=5 to find your job ID

## Credentials Locations

| File | Content |
|---|---|
| `~/.mcporter/credentials.json` → `entries.higgsfield\|fb7b405dd99c24b1` | OAuth PKCE data + tokens (state, codeVerifier, access_token, refresh_token) |
| `~/.openclaw/workspace/config/mcporter.json` → `higgsfield.env` | `HIGGSFIELD_API_KEY_ID` + `HIGGSFIELD_API_KEY_SECRET` (API key pair — does NOT auth generate_image) |

The API key pair and OAuth tokens are TWO DIFFERENT things. mcporter.json's API key only works for read-only tools like `tools/list`.