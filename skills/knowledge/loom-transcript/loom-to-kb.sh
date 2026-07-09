#!/bin/bash
# loom-to-kb.sh — turn a Loom share link into a clean markdown transcript.
#
# Loom's transcript file lives behind a SIGNED CloudFront URL. We render the page
# in a real browser (agent-browser), capture the signed transcription request from
# the network log, fetch the FULL transcript JSON from it, and assemble clean MD
# with the video's real title + Loom's auto-summary + chapters.
#
# Usage: ./loom-to-kb.sh <loom-share-url> [output-dir]
# Then ingest the .md into the shared KB separately (cognify --tenant fleet ingest).
set +e
URL="${1:?usage: loom-to-kb.sh <loom-url> [outdir]}"
OUTDIR="${2:-$HOME/clawd/knowledge/loom-transcripts}"
mkdir -p "$OUTDIR"
VID=$(echo "$URL" | grep -oE '[a-f0-9]{32}' | head -1)
[ -n "$VID" ] || { echo "bad loom url" >&2; exit 1; }

# 1. Render the page; the browser fetches the signed transcript on load.
agent-browser network requests --clear >/dev/null 2>&1 || true
agent-browser open "$URL" >/dev/null 2>&1
sleep 4
agent-browser click "Transcript" >/dev/null 2>&1 || true
sleep 2

TITLE=$(agent-browser eval "document.title" 2>/dev/null | tr -d '"' | sed 's/ | Loom$//' | head -1)
[ -n "$TITLE" ] || TITLE="Loom $VID"
RAWFILE=$(mktemp /tmp/loom-raw.XXXXXX); agent-browser read 2>/dev/null > "$RAWFILE" || true

# 2. Grab the signed transcription URL and fetch the full transcript JSON.
SIGNED=$(agent-browser network requests --filter "transcription" 2>/dev/null \
  | grep -oE "https://cdn.loom.com/mediametadata/transcription/[^ \"']+" | head -1)
JSONFILE=$(mktemp /tmp/loom-json.XXXXXX)
if [ -n "$SIGNED" ]; then curl -s --max-time 30 -A "Mozilla/5.0" "$SIGNED" -o "$JSONFILE" || true; fi

# 3. Assemble clean markdown.
python3 - "$VID" "$URL" "$OUTDIR" "$TITLE" "$RAWFILE" "$JSONFILE" <<'PY'
import sys,re,os,json
vid,url,outdir,title,rawfile,jsonfile=sys.argv[1:7]
title=title.strip() or f"Loom {vid}"

# full transcript from the signed JSON (phrases[].text)
transcript=""
try:
    d=json.load(open(jsonfile,encoding='utf-8',errors='ignore'))
    phr=d.get('phrases') if isinstance(d,dict) else None
    if phr:
        parts=[]
        for p in phr:
            t=(p.get('text') or p.get('value') or '').strip()
            if t: parts.append(t)
        transcript=" ".join(parts).strip()
        # light sentence wrapping for readability
        transcript=re.sub(r'(?<=[.!?]) (?=[A-Z])','\n',transcript)
except Exception:
    pass

# summary + chapters from the page read (best-effort)
raw=open(rawfile,encoding='utf-8',errors='ignore').read() if os.path.exists(rawfile) else ""
lines=[l.rstrip() for l in raw.splitlines()]
def block(after,stop):
    out=[];grab=False
    for l in lines:
        s=l.strip().lower()
        if not grab and s==after: grab=True; continue
        if grab:
            if any(s.startswith(x) for x in stop): break
            if l.strip(): out.append(l.strip())
    return out
summary=" ".join(block("## summary",["chapters","activity","transcript"]))
chapters=[l for l in block("chapters",["activity","transcript"]) if re.match(r'^\d+:\d\d',l)]

md=[f"# {title}","",f"Source: {url}",f"Loom id: {vid}",""]
if summary: md+=["## Summary","",summary,""]
if chapters: md+=["## Chapters",""]+[f"- {c}" for c in chapters]+[""]
md+=["## Transcript","",transcript or "(transcript not captured)"]
safe=re.sub(r'[^a-zA-Z0-9]+','-',title).strip('-').lower()[:60] or vid
path=os.path.join(outdir,f"{safe}-{vid[:8]}.md")
open(path,"w").write("\n".join(md))
print(path)
print(f"  title: {title}")
print(f"  transcript chars: {len(transcript)}")
PY
