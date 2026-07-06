# Video Streaming Debug: When Videos Don't Play

## Symptoms
- Video files return 200 from server but don't play in browser
- Video card click opens modal (dark overlay) but no video appears
- Video buffers forever or shows only first frame then freezes
- Console errors: no specific error, just silence after `.play()` call

## Root Cause Checklist (check in order)

### 1. Missing Faststart (moov atom at end of file) — MOST COMMON
The browser needs the moov atom (video header/playback info) to start playing. ffmpeg by default puts it at the end. Files > 1-2 MB without faststart won't stream.

**Fix:** Re-encode with faststart:
```bash
ffmpeg -i input.mp4 -vcodec libx264 -crf 30 -preset fast \
  -acodec aac -b:a 64k -movflags +faststart -vf "scale=-2:720" output.mp4 -y
```

**Verify:**
```python
with open('video.mp4','rb') as f:
    data = f.read(10000)
moov_pos = data.find(b'moov')
print(f'moov at pos {moov_pos} — {"OK" if moov_pos < 2000 else "FAIL: no faststart"}')
```

### 2. Inline onclick vs Event Delegation
`onclick="openVideo('name')"` requires `window.openVideo` to exist. Inside an IIFE, you must explicitly assign to `window.openVideo`. Even then, some browser contexts block inline handlers.

**Fix:** Replace inline onclick with `data-video` attribute + event delegation:
```javascript
document.querySelector('.testimonial-grid').addEventListener('click', function(e) {
  var card = e.target.closest('.testimonial-card');
  if (!card) return;
  var name = card.getAttribute('data-video');
  if (!name) return;
  // ... play logic
});
```

### 3. Missing `.load()` before `.play()`
Setting `modalVideo.src = path` does NOT begin loading the video. The browser queues the source assignment but doesn't fetch bytes until the next render cycle or a `.load()` call.

**Fix:** Always call `.load()` after setting `.src` and before `.play()`:
```javascript
modalVideo.src = vidPath;
modalVideo.load();
modalVideo.play().catch(function(err) { /* handle */ });
```

### 4. `src = ''` doesn't unload — use `removeAttribute()`
Setting `src = ''` creates a new empty media request but the browser may keep the old video buffered in memory. This causes memory bloat and prevents clean reinitialisation.

**Fix:**
```javascript
modalVideo.pause();
modalVideo.removeAttribute('src');
modalVideo.load(); // actually unloads
```

### 5. Content-Type missing or wrong
Vercel serves `.mp4` as `video/mp4` automatically. Check with:
```bash
curl -sI https://site.com/videos/test.mp4 | grep content-type
# Expected: content-type: video/mp4
```

### 6. File too large for network
Large files (>20 MB) may time out on slow connections. Check file size:
```bash
ls -lh public/videos/*.mp4
```
Compress aggressively: CRF 30-32 with scale=-2:720 typically yields 1-4 MB per minute of talking-head video, down from 15-30 MB.

## Quick Fix Script

Run this to re-encode a single video with all fixes:
```bash
ffmpeg -y -i "$1" \
  -vcodec libx264 -crf 30 -preset fast \
  -acodec aac -b:a 64k \
  -movflags +faststart \
  -vf "scale=-2:720" \
  "${1%.*}_fixed.mp4"
```

## Google Drive Download via Python (NOT shell curl)

Shell curl breaks on auth tokens with special characters (hyphens, slashes). Always use Python:
```python
with open("/root/.config/gws/tokens.json") as f:
    token = json.load(f)["access_token"]
url = f"https://www.googleapis.com/drive/v3/files/{FILE_ID}?alt=media"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
with urllib.request.urlopen(req) as resp:
    with open("output.mp4", "wb") as f:
        f.write(resp.read())
```