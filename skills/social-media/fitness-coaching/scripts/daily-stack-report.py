#!/usr/bin/env python3
"""Daily stack report for a fitness coaching business.
Template: copy this, customise IDs/tokens, and use as a cron script with no_agent=True.

Expects tokens in /tmp/:
  - /tmp/ghl_token.txt  (GoHighLevel Private Integration token)
  - /tmp/tf_token.txt   (Typeform API key, optional)
  - /tmp/slack_token.txt (Slack bot token, optional)
"""

import json, subprocess, urllib.request, os, datetime

REPORT = []
date_str = datetime.datetime.now().strftime("%b %d, %Y — %H:%M DUBAI")
LOCATION_ID = "zW3bdqnEq35lXOivvJoz"  # CHANGE to your client's location ID

# ── 1. System Health ──
try:
    load = os.getloadavg()
    uptime_raw = subprocess.run(["uptime", "-p"], capture_output=True, text=True).stdout.strip()
    uptime = uptime_raw.replace("up ", "", 1) if uptime_raw.startswith("up") else uptime_raw
    REPORT.append(f"📟 **System** | Load: {load[0]:.1f} {load[1]:.1f} {load[2]:.1f} | {uptime}")

    disk = subprocess.run(["df", "-h", "/"], capture_output=True, text=True).stdout.splitlines()
    for line in disk:
        if line.startswith("/dev"):
            parts = line.split()
            free_pct = parts[4].replace("Use", "").replace("%","")
            free_num = int(free_pct) if free_pct.isdigit() else 0
            emoji = "🟢" if free_num < 80 else ("🟡" if free_num < 90 else "🔴")
            REPORT.append(f"{emoji} **Disk**: {parts[3]} free ({parts[4]} used)")

    mem_raw = subprocess.run(["free", "-m"], capture_output=True, text=True).stdout.splitlines()
    for line in mem_raw:
        if line.startswith("Mem:"):
            parts = line.split()
            mem_pct = int(parts[2]) / int(parts[1]) * 100
            emoji = "🟢" if mem_pct < 70 else ("🟡" if mem_pct < 85 else "🔴")
            REPORT.append(f"{emoji} **RAM**: {parts[2]}MB/{parts[1]}MB ({mem_pct:.0f}%)")
except Exception as e:
    REPORT.append(f"⚠️ System: {str(e)[:50]}")

# ── 2. Website ──
try:
    req = urllib.request.Request("https://ibrahim-one-gilt.vercel.app/",
        headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=10)
    size = len(resp.read())
    REPORT.append(f"🌐 **Site** | ✅ {resp.status} | {size//1024}KB")
except Exception as e:
    REPORT.append("🌐 **Site** | 🔴 UNREACHABLE")

# ── 3. GoHighLevel ──
token_path = "/tmp/ghl_token.txt"
if os.path.exists(token_path):
    ghl_token = open(token_path).read().strip()
    try:
        headers = {"Authorization": f"Bearer {ghl_token}",
                   "Version": "2021-07-28", "User-Agent": "Mozilla/5.0"}
        loc = LOCATION_ID

        # Pipeline overview
        url = f"https://services.leadconnectorhq.com/opportunities/pipelines?locationId={loc}"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        pipelines = json.loads(resp.read()).get("pipelines", [])
        if pipelines:
            REPORT.append("## **PIPELINES**")
            for pipe in pipelines:
                stages = pipe.get("stages", [])
                s = " → ".join(s["name"] for s in stages[:4])
                if len(stages) > 4:
                    s += f" +{len(stages)-4} more"
                REPORT.append(f"🏷️ **{pipe['name']}** — {s[:80]}")

        # Contact count
        url = f"https://services.leadconnectorhq.com/contacts/?locationId={loc}&limit=1"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        contacts = json.loads(resp.read())
        total = contacts.get("total", contacts.get("meta", {}).get("total", "?"))
        REPORT.append(f"👤 **Contacts**: {total}")

        # Calendar list
        url = f"https://services.leadconnectorhq.com/calendars/?locationId={loc}"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        calendars = json.loads(resp.read()).get("calendars", [])
        if calendars:
            cal_names = ", ".join(c["name"] for c in calendars[:5])
            REPORT.append(f"📅 **Calendars**: {cal_names}")
            if len(calendars) > 5:
                REPORT[-1] += f" +{len(calendars)-5} more"
    except Exception as e:
        REPORT.append(f"📊 **GHL**: {str(e)[:60]}")
else:
    REPORT.append("📊 **GHL**: No token")

# ── 4. Typeform (optional) ──
tf_path = "/tmp/tf_token.txt"
if os.path.exists(tf_path):
    try:
        tf_token = open(tf_path).read().strip()
        req = urllib.request.Request("https://api.typeform.com/forms",
            headers={"Authorization": f"Bearer {tf_token}"})
        resp = urllib.request.urlopen(req, timeout=10)
        forms = json.loads(resp.read()).get("items", [])
        REPORT.append(f"📝 **Typeform**: {len(forms)} forms")
    except:
        pass

# ── 5. Slack (optional) ──
slack_path = "/tmp/slack_token.txt"
if os.path.exists(slack_path):
    try:
        token = open(slack_path).read().strip()
        req = urllib.request.Request(
            "https://slack.com/api/conversations.list?types=public_channel,private_channel&limit=10",
            headers={"Authorization": f"Bearer {token}"})
        resp = urllib.request.urlopen(req, timeout=10)
        channels = json.loads(resp.read()).get("channels", [])
        REPORT.append(f"💬 **Slack**: {len(channels)} channels")
    except:
        pass

# ── OUTPUT ──
header = f"🏋️ **DAILY REPORT** — {date_str}"
sep = "━━━━━━━━━━━━━━━━━━"
footer = sep + "\nReply to give me an order."

print(f"{header}\n{sep}\n" + "\n".join(REPORT) + f"\n{footer}")