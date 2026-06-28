---
name: security-scanning
title: Daily Security Scanning & Fleet Health Automation (v2)
description: Design, build, and maintain automated daily security scans for a multi-machine CTO fleet. Covers scan architecture, macOS-specific scripting quirks, SSL cert checking, supply-chain auditing, and CVE monitoring.
trigger: User asks for security scan, daily briefing, fleet health check, fleet exploration, tailnet reconnaissance, 'scan the fleet', 'check certificates', 'build a security cron job', 'daily security suggestions', 'governance pattern', 'secure all client bots', 'can you access all bots', 'check bot health', 'check client bots', 'youtube deeds', 'explore tailnet', 'inventory fleet', 'improve security scripts', 'daily research', or any request to automate security monitoring, discover fleet topology, or continuously harden the fleet based on research.
---

# Daily Security Scanning & Fleet Health Automation (v2)

## When to Use

Build or maintain a daily security scan when:
- User requests a "security scan" or "daily security briefing"
- Setting up cron jobs for CTO oversight
- Automating fleet health monitoring
- Checking SSL cert expiry, CVE feeds, supply chain vulns
- Any recurring security audit workflow

## Scan Architecture (v2 — 9 Layers)

The canonical script lives at the workspace path `~/clawd/tools/appie-3-daily-security-scan.sh`. The actual runnable copy is at `~/.hermes/scripts/appie-3-daily-security-scan.sh` (or the profile-specific scripts dir, e.g. `~/.hermes-appie3/scripts/` on some setups). Every layer maps to a function.

### Layer 1: Local Machine Health

```bash
- Disk usage (df -h /)
- Memory: vm_stat — use grep, NOT awk /pattern/
  * WRONG: vm_stat | awk '/pages active/ {print $NF}'  → empty!
  * RIGHT: vm_stat | grep 'pages active' | awk '{print $NF}'
  * On macOS vm_stat output starts with uppercase "Pages", awk /pages/ doesn't match
  * If >90% active: dump top 5 processes by RSS + swap info
- Load averages (sysctl vm.loadavg / uptime)
- Hermes agent count (pgrep -f hermes_cli | wc -l)
- Failed logins in 24h (log show --predicate)
```

### Layer 2: Fleet Health (SSH via Tailscale)

Uses **4 category arrays** (all indexed, pipe-separated — bash 3.x compat):

| Array | Emoji | Condition | Check Type |
|-------|-------|-----------|------------|
| `FLEET` | 🟢/🔴 | SSH key works | Full SSH health (disk, load, Hermes, updates) |
| `BROKEN_KEYS` | 🟡 | Online, port 22 open, key rejected | `nc -zv` port check (<1s) |
| `TAILNET_ONLINE` | ⚪ | Online, no SSH daemon | Tailnet status only |
| `GHOSTS` | 💤 | Offline >7d | Archived, no active check |

Entry format: `"name|user@tailscale_ip|ssh_key_path|description"`
SSH: `-o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no`
Results cached to FLEET_CACHE file (pipe-separated: `name|status|desc`)

**Key v2 fix**: FLEET_CACHE is shared between markdown report and Telegram output. NO separate SSH loop for Telegram. This eliminates the v1 Telegram divergence bug.

**Tailnet-only entries** (BROKEN_KEYS, TAILNET_ONLINE, GHOSTS) also write to FLEET_CACHE so the Telegram output can render all 4 groups in sequence from a single cache read. This is critical for completeness — the Telegram scan should show ALL tailnet nodes, not just SSH-reachable ones.

### Layer 3: Local Open Ports

```bash
lsof -iTCP -sTCP:LISTEN -P -n | awk 'NR>1 && !seen[$1,$9]++'
```
Flags unexpected dev services on unprivileged ports. Expected: bun on 37701 (Hermes internal).

### Layer 4: Supply Chain Security

```bash
# npm audit (high+ only)
npm audit --audit-level=high

# Python safety check
safety check --short

# Gitleaks secret scan — CRITICAL: always use --no-git with .gitleaks.toml
gitleaks detect --source $CLAWD_DIR --no-git --config .gitleaks.toml --verbose
```
- **ALWAYS --no-git**: git mode scans 2369 commits (487MB) → 35k false positives
- **ALWAYS .gitleaks.toml**: suppress example keys, lockfile hashes, test data
- **ALWAYS timeout 60**: gitleaks --no-git can CPU-spike to 975%
- Extract leak count from "leaks found: N" line, not grep -c

### Layer 5: SSL/TLS Certificates

```bash
# Use brew OpenSSL — system LibreSSL can't parse x509 output
ossl="/opt/homebrew/bin/openssl"
cert_raw=$(echo "" | "$ossl" s_client -servername "$domain" -connect "$domain":443 2>&1)
enddate=$(echo "$cert_raw" | "$ossl" x509 -noout -enddate 2>/dev/null | cut -d= -f2)
```
- NO 2>/dev/null on s_client (kills output in subshell)
- NO timeout wrapper (kills mid-handshake)
- Flag <7d 🔴, <30d ⚠️

### Layer 6: Security Headers

```bash
curl -sI --max-time 5 "https://$domain"
# Check for: HSTS, CSP, X-Frame-Options, X-Content-Type-Options
```
All 4 required. Score: 4/4 🟢, 2-3 ⚠️, 0-1 🔴.
Caveat: follow redirects with `-L` if domain uses Cloudflare/redirect chains.

### Layer 7: Pending Updates (fleet SSH)

```bash
ssh <node> "apt list --upgradable | grep -v 'Listing...' | wc -l"
ssh <node> "apt list --upgradable | grep -i security | wc -l"
```
- Security count via `grep -i security` (not `-security` — varies by distro)
- 0 updates ✅, 1-20 ⚠️, 20+ or any security 🔴

### Layer 8: Tailscale Network

```bash
tailscale status --json | python3 -c "import sys,json; ..."
```
Counts peers, finds offline nodes, shows last-seen timestamps.

### Layer 9: CVE Watch (v2 — no NVD)

**PRIMARY: GitHub Advisory API** (no auth, no rate limit issues)
```
GET https://api.github.com/advisories?type=reviewed&severity=critical&per_page=8
```
- Returns GHSA advisories sorted by `published_at` desc
- Use HTTP status code check (curl -w %{http_code}) — don't rely on python successfully parsing
- Filter by published_at within 48h via Python datetime comparison
- Also fetch high severity for awareness

**SECONDARY: OSV.dev** (per-package, always works)
```
POST https://api.osv.dev/v1/query
{"package": {"name": "openssl", "ecosystem": "PyPI"}}
```
- Query key packages: openssl, node, curl
- Also query agent frameworks via `agent-framework-cve-scan.py` (see `references/agent-framework-cve-scan.md`)
- Filter by published date within 90d
- No auth needed, no rate limits observed

**TERTIARY: Agent Framework & Go Ecosystem CVE Scanner** (standalone Python script)
  - Covers 20 packages: 17 Python agent frameworks (LangChain, CrewAI, Semantic Kernel, AutoGen, LlamaIndex, LiteLLM, guardrails-ai, giskard, etc.) + 3 Go infra packages (golang.org/x/crypto, github.com/go-chi/chi, github.com/sigstore/rekor)
  - Checks `pip list` locally + OSV.dev API per package
  - Go packages added 2026-06-26 n.a.v. 7 critical SSH crypto CVEs published 2026-06-25
- Run: `python3 ~/clawd/tools/agent-framework-cve-scan.py`
- See `references/agent-framework-cve-scan.md`

NVD API v2.0 is NOT used — requires API key to avoid 5 req/30s limit. Free key tier exists but is unavailable from this environment.

### Layer 10: Bot & Client Health Check (ad-hoc, not in daily scan)

Run periodically (weekly or on demand) — check all active Telegram bots and web live services for basic health:

```bash
# 1. List deployed bots from project config
# 2. For each bot endpoint, check:
#    - curl -m 5 <bot_url>/health (or /) — returns 200?
#    - curl -m 5 <bot_url> | grep -i "ok\|alive\|running"
# 3. For Telegram bots, check response via bot API:
#    curl -m 5 "https://api.telegram.org/bot<TOKEN>/getMe"
# 4. For YouTube / media bots, check if deploy is still live on platform
```

Not automated as a daily cron (too many client-specific endpoints, rate-limit risk on Telegram API). Run as an ad-hoc CTO audit.

### Layer 11: Continuous Improvement — Research → Scripts

Seyed's standing directive: **use the daily AI briefing research to improve the security scripts.** After each daily briefing, scan the research output for:

| Signal | Action |
|--------|--------|
| New CVE class or attack vector | Add a check layer or tool to the scan |
| New tool or best practice | Add install command + verification to the scan or host-init |
| Configuration hardening advice | Add to the security suggestion pipeline |
| Client bot platform deprecation | Flag in bot health check layer |
| New scanning methodology | Replace or augment an existing scan layer |

Implementation checklist after each daily briefing:
1. Read the research output (`~/clawd/appie-brain/knowledge/research/daily-research/YYYY-MM-DD/README.md`)
2. Cross-reference against existing scan layers — what's missing?
3. For any gap: add a new function to the scan script or update existing logic, **or create a standalone script** for cross-platform use
4. Test the change: run the affected layers manually
5. If the improvement is structural (new layer, new tool), update this SKILL.md — add a reference file if the new tool has its own docs
6. Log to Mission Control: `mc-log-task.py "Security script improvement: <summary>" --agent Appie-3`

**Do not batch up improvements.** Make them as you discover them. A one-line regex addition or a new cert check costs nothing; deferring it until "next Monday" means it never happens.

**Examples of recent improvements from research:**
- `agent-framework-cve-scan.py` — created from 2026-06-20 briefing which found CVE-2026-26030 (Semantic Kernel RCE), GHSA-gr75-jv2w-4656 (LangChain path traversal). Expanded 2026-06-25 +3 (litellm, guardrails-ai, giskard). Expanded 2026-06-26 +3 Go infra packages (golang.org/x/crypto after 7 critical SSH CVEs, go-chi/chi IP spoofing, sigstore/rekor OOM). See `references/agent-framework-cve-scan.md`.
- `headroom-ai` v0.26.0 — installed after 2026-06-20 briefing flagged Headroom (60-95% token compression). Has MCP server, pure Python, Apache-2.0.
- SkillsGuard evaluated — TypeScript/Node.js project (not installable on Python stack), cloud API available at `https://skillsguard.apiskillsguard.workers.dev/scan`.

### Tailnet Reconnaissance — Full Fleet Exploration Pattern

A standalone workflow for when you need a **complete picture of every machine on Tailscale**: what's online, what ports are open, what services run, and whether SSH keys work. Use this before setting up scans, deploying keys, or auditing fleet security posture.

#### Workflow

Step-by-step exploration, run each command and compile results:

**Step 1: List all machines**

```bash
tailscale status
# Full listing with IP, name, OS, online/offline status
tailscale status | grep -v offline  # only online machines
tailscale status --json             # programmatic access
```

**Step 2: Ping all online machines**

```bash
for ip in <all_online_tailscale_ips>; do
  result=$(ping -c 2 -W 3 $ip 2>&1 | tail -1)
  echo "$ip -> $result"
done
```

Helps identify reachability and latency. Machines behind DERP relays show higher RTT (100-400ms). Local DERP-free machines show 1-5ms.

**Step 3: Port-scan per machine**

Use `nc -zv` for fast TCP port checks. Common ports to probe:

```bash
# Linux servers
for port in 22 80 443 3000 5000 8000 8080 8443 9090 2375 2376 6443 7860 8888; do
  nc -zv -w 2 $ip $port 2>&1 | grep -v "Connection refused"
done
```

Additional macOS-specific ports: 5900 (VNC), 7000 (AirPlay), 5353 (mDNS).

Key port signatures:
- `22` → SSH (verify key auth next)
- `443` → HTTPS web service
- `80` → HTTP (redirect to HTTPS or legacy)
- `3000` → Common dev/Next.js default port
- `5000` → Flask/Express/development
- `5900` → VNC/Screen Sharing (macOS)
- `8443` → Alternative HTTPS

**Step 4: Identify web services**

For every open HTTP/HTTPS port, curl the root path to identify the service:

```bash
# HTTPS
curl -sk https://$ip/ | head -c 200
curl -sk https://$ip/ 2>&1 | grep -i "<title>"

# HTTP on alternate ports
curl -sk http://$ip:$port/ | head -c 200
```

Look for:
- `<title>` tag — identifies the site/app
- Server headers: `curl -sI https://$ip/ | grep -i server`
- Framework fingerprints (Next.js, WordPress, Flask, etc.)
- JSON responses if it's an API
- Empty response may indicate TLS SNI filtering — try `-H "Host: example.com"`

### Step 5: Test SSH Connectivity & Diagnose Failures

When SSH fails, methodically diagnose *why* — the remediation differs by failure mode.

#### 5a. Basic Auth Test

```bash
ssh -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no \
  -i ~/.ssh/id_ed25519 <user>@<ip> "hostname && uname -a"
```

**Outcomes by error message:**

| Error | Meaning | Next step |
|---|---|---|
| `Permission denied (publickey)` | Port open, SSH running, key **not accepted** | Deploy the key (see refs) |
| `Connection refused` | Port 22 closed, no SSH daemon | Go to 5b below |
| `Connection timed out` / hangs | Firewall dropping or host unreachable | Check network (ping) |
| `unexpected HTTP response: 502 Bad Gateway` via `tailscale ssh` | Tailscale SSH not configured on remote | Go to 5b below |

Also test alternative keys: `id_ed25519_github`, `id_ed25519_spark`, etc.

#### 5b. Port-Closed Diagnosis (SSH daemon not running)

When port 22 is closed, use this systematic flow:

```bash
# 1) Verify basic network reachability
ping -c 2 -W 3 <IP>

# 2) Check if the host is on Tailscale and its state
tailscale status | grep <IP-or-name>
# Look for: "active" → reachable, "offline" → unreachable

# 3) Check the remote peer's Tailscale SSH capabilities
tailscale status --json | python3 -c "
import sys, json
d = json.load(sys.stdin)
for pid, p in d.get('Peer', {}).items():
    if '<IP>' in str(p.get('TailscaleIPs', [])):
        print('OS:', p.get('OS'))
        print('Online:', p.get('Online'))
        print('Capabilities:', p.get('Capabilities'))
        print('CapMap:', p.get('CapMap'))
"
```

**Interpretation:**
- `Capabilities: null` / `CapMap: null` → **Tailscale SSH is NOT enabled** on the remote node. SSH won't work via `tailscale ssh` either.
- `"https://tailscale.com/cap/ssh": null` in CapMap → Tailscale SSH IS enabled. If it fails with 502, check the Tailscale admin console.
- Node is `active` with direct connection → reachable (even if SSH is closed).

```bash
# 4) Port scan common services to see if ANY ports are open
for port in 22 443 5900 8080 8443 3000 5000; do
  nc -zv -w 3 <IP> $port 2>&1 | grep -v "Connection refused"
done
```

**Remediation by failure mode:**

| Failure | Fix |
|---|---|
| Port 22 closed, macOS | On the Mac: **System Settings → General → Sharing → Remote Login**. Or in **Tailscale Admin Console** → approve node for Tailscale SSH. |
| Port 22 closed, Linux | `sudo systemctl enable --now sshd` or `sudo apt install openssh-server` |
| Port 22 open, `Permission denied` | Deploy SSH public key to remote `~/.ssh/authorized_keys` (see `references/ssh-key-deployment.md` / `references/mac-mini-coding-harness-recovery.md`) |
| Tailscale SSH 502, port 22 works fine | Retry direct `ssh` via Tailscale IP. The 502 is a Tailscale relay issue, not an SSH error. |
| No ports open at all (22, 443, 5900, etc. all refused) | Machine may be asleep, on a restricted network, or fully locked down. macOS: no services enabled in Sharing prefs. |

For detailed session walkthrough with real error transcripts, see `references/ssh-connectivity-diagnostics.md`.

**macOS coding-harness recovery pattern**: if a Mac mini is online, port `22` is open, but common users reject Appie-3's key, stop guessing users/passwords. Ask the local operator or another authorized agent on the box to add Appie-3's public key to the active macOS user's `~/.ssh/authorized_keys`, enable Remote Login, and report the actual username. Then verify harness state (`~/clawd`, `~/.hermes`, `~/.codex`, `~/.claude`, and `ps` for `hermes|claude|codex|copilot|node|python`) before changing anything. Full recipe: `references/mac-mini-coding-harness-recovery.md`.

**Step 6: Check local authorized_keys**

```bash
cat ~/.ssh/authorized_keys
cat ~/.ssh/id_ed25519.pub  # your own public key
```

This tells you:
- Who can SSH into *you* (the keys in authorized_keys)
- Who *you* claim to be (the pubkey comment field)
- Whether cross-fleet SSH is unidirectional only

**Step 7: Compile and present**

Present findings as a compact table:

```
| Machine | IP | OS | Ping | Open ports | Services |
|---------|----|----|------|------------|---------|
| machine | 100.x.x.x | Linux | Xms | 22, 443, 3000 | SSH, web (app name) |
```

Include:
- Online/offline status per machine
- Reachable services and what they are
- SSH key acceptance status
- The user's own pubkey (ready to copy-paste for deployment)

#### Common Findings

- **SSH key not deployed**: New VPS/machine provisioning — pubkey needs to be added to authorized_keys. Common pattern: Appie-3's key isn't on any fleet machine, but other agents' keys already are.
- **VNC open**: macOS machines with Screen Sharing enabled. Port 5900 open means anyone on tailnet could attempt authentication. Verify VNC is password-protected.
- **Web service on alternate port**: Next.js dev server (3000), Flask/Express (5000), alternative HTTPS (8443) — may be development/staging environments not meant for production.
- **Offline nodes >30d**: Move to GHOSTS array in scan script. Their Tailscale IPs may change on reconnection.
- **Multi-OS tailnet**: macOS machines have VNC (5900), AirPlay (7000), and different SSH configuration paths. Linux servers are more consistent.

### Multi-Agent Cron Inventory — Fleet-Wide Schedule Audit

A systematic method for auditing ALL cron jobs across a multi-agent fleet. Use when Seyed asks for a comprehensive schedule review, "make all cron jobs aesthetic", or before any fleet-wide cron reformatting.

#### Workflow

**Step 1: Enumerate all accessible machines**

```bash
# SSH key test across ALL tailnet hosts
for host in "root@100.x.x.x" "appie@100.x.x.x" "eva@100.x.x.x" "root@100.x.x.x"; do
  result=$(ssh -o ConnectTimeout=3 -o BatchMode=yes -o StrictHostKeyChecking=no \
    -i ~/.ssh/id_ed25519 "$host" "hostname" 2>&1)
  echo "$host → $result"
done
```

Note: SSH user varies by machine — try `root`, `appie`, the user's name (`eva`, `harry`). Don't assume one user works everywhere.

**Step 2: For each reachable machine, identify the runtime**

```bash
# Hermes cron
hermes cron list

# OpenClaw cron (legacy)
ls ~/.openclaw/cron/ 2>/dev/null

# launchd plists (macOS)
ls ~/Library/LaunchAgents/ | grep -v 'com\.google\|homebrew'
```

Key signals for runtime detection via `ps aux`:
- `hermes_cli.main gateway run` → Hermes agent
- `openclaw` in process name → OpenClaw agent
- `claude` or `codex` in process name → Claude Code / Codex CLI

**Step 3: Check cron managers**

| Runtime | Cron Manager | Command |
|---------|-------------|---------|
| Hermes | `hermes cron` | `hermes cron list` |
| OpenClaw (legacy) | cron files | `ls ~/.openclaw/cron/` |
| macOS (legacy) | launchd plists | `launchctl list \| grep com.weblyfe` |
| System crontab | system cron | `crontab -l` |

**Step 4: Document per-job health**

For each job, note:
- Name and schedule
- Last run status (ok/error/failed delivery)
- Delivery target (telegram/origin/none)
- If job is broken: capture the exact error message

**Step 5: Identify aesthetic/styling improvements**

Check for:
- **Naming convention**: consistent prefix per agent (`appie3-`, `appie2-`), no mixed case
- **Output formatting**: Markdown + emoji headers vs plain text
- **Delivery target**: all jobs deliver to Telegram (or all to origin — be consistent)
- **Timing deconfliction**: no overlapping runs on the same agent
- **Broken jobs**: provider errors, expired credits, delivery failures — all need fixing

#### Fleet Topology Map (2026-06-24)

| Machine | IP | Runtime | Cron | Notes |
|---------|----|---------|------|-------|
| appie-3-hermes | 100.69.131.51 | Hermes | `hermes cron` (6 jobs) | ✅ stable |
| appie-2 | 100.118.143.10 | Hermes | `hermes cron` (13 jobs) | 🟡 7 broken |
| appie-1 | 100.101.29.56 | OpenClaw | launchd (40+ plists) | 🟢 |
| eva | 100.99.64.92 | Hermes + OpenClaw | launchd | 🟢 |
| eugi | 100.110.58.73 | Hermes | 0 cron jobs | schone lei |
| Deadpool | ? (off-tailnet) | ? | ? | Aparte Hetzner VPS voor Roslan + EKO |

Zie `references/fleet-inventory.md` voor de complete actuele inventaris.

### Tailnet Discovery

**Not all fleet machines are on Tailscale.** Deadpool (Hetzner VPS voor Roslan + EKO) is NOT on the tailnet and has no SSH config entry. When checking "all machines", distinguish between tailnet-connected and off-tailnet infrastructure.

```bash
# Full peer list with online status
tailscale status

# JSON output for programmatic use (Self vs Peer distinction is CRITICAL)
tailscale status --json
```

The local machine appears in `Self`, ALL other nodes in `Peer` dict:

```python
d = json.load(sys.stdin)
self = d.get('Self', {})
self_online = self.get('Online', False)               # local machine
peer_online = any(p.get('Online', False)
                  for p in d.get('Peer', {}).values()) # others
```

**WRONG**: Looping over `Peer` to find "appie-1" → always returns offline.
**RIGHT**: Check `Self` for the local machine, `Peer` for all others.

This matters for watchdog scripts that check local node tailnet health. The `tailscale status` CLI output shows the local node without a status column (making it look unknown), but JSON `Self.Online` is always `True` for the running machine.

### Connectivity Checks

```bash
tailscale ping -c 1 --timeout 3s <IP>          # cross-platform
ssh -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no <user>@<ip> <cmd>
```

**Key**: Never use direct Hetzner IPs — they change on reprovision. Always use Tailscale IPs (`100.x.x.x`). SSH key timeout: `ConnectTimeout=5` is required; `ConnectTimeout=3` gives false positives on DERP relay nodes.

### Cross-Machine File Retrieval

When you need to find and retrieve a file from a fleet machine:

1. **Know where canonical assets live** — common locations per machine:
   - **appie-1** (Mac Mini): `~/clawd/projects/openclaw-guide/canonical/` (Build-Your-Own-Appie PDFs), `~/clawd/assets/agent-avatars/` (Telegram bot avatars)
   - **appie-2** (Hetzner VPS): `/root/appie-brain/`, `/root/.hermes/`
   - **eugi** (Hetzner VPS): `/root/.openclaw/`, `/root/.hermes/`

2. **Search remotely** — use `find` with name globs:
   ```bash
   ssh <user>@<tailscale-host> "find <path> -iname '*pattern*v4*' -o -iname '*pdf*' 2>/dev/null"
   ```
   - Always use `find` (not `ls -R`) — scales to large directories
   - Quote paths with spaces: `"/Users/appie/clawd/projects/openclaw-guide/"`
   - Use wildcards for version numbers: `*v4.5*`

3. **SCP back** — file to local `/tmp/`:
   ```bash
   scp <user>@<tailscale-host>:"<remote-path>" /tmp/<local-name>
   ```
   - `scp` via Tailscale IP/hostname works without extra flags
   - Use `/tmp/` for ephemeral copies; move to `~/clawd/` for permanent storage

4. **Deliver the file**:
   - **Telegram**: include `MEDIA:/tmp/<file>` in response — sends as native attachment
   - **Email**: NOT set up on this VPS (no himalaya, mailtools, or SMTP creds). Ask Seyed for creds or an alternative
   - **Public URL**: upload somewhere if Seyed needs to share the link

5. **Clean up** — remove from `/tmp/` when no longer needed:
   ```bash
   rm /tmp/<local-name>
   ```

**Pitfall**: macOS paths start with `/Users/`, not `/root/`. Check remote OS before constructing search paths.

## SSH Key Inventory

Keys stored in `~/.ssh/`. SSH config (`~/.ssh/config`) has host aliases for fleet machines.  
**Current reality (2026-06-24):** `appie-2`, `eugi`, `appie-1`, and `eva` all accept Appie-3's key. All other fleet nodes reject it or have no SSH daemon. Deploying the key to remaining BROKEN_KEYS nodes is the next step for fleet-wide SSH management.

| File | Purpose | Status | Last Verified |
|------|---------|--------|---------------|
| `~/.ssh/id_ed25519` | Default key (`appie-3-hermes@tailnet`) | 🟢 appie-2, eugi, appie-1, eva / 🔴 others | 2026-06-24 |
| `~/.ssh/id_ed25519_github` | GitHub-only key | 🟢 Works | — |
| `~/.ssh/id_ed25519_spark` | Spark Atlas key | 🔴 Stale (node offline) | 2026-06-11 |

### Fleet SSH Access Map (2026-06-23)

| Device | OS | Port 22 | SSH Key | Category | Remedy |
|--------|----|---------|---------|----------|--------|
| appie-2 | Linux | ✅ Open | ✅ Root accepted | FLEET 🟢 | — |
| eugi | Linux | ✅ Open | ✅ Root accepted | FLEET 🟢 | — |
| appie-1 | macOS | ✅ Open | ✅ `appie@100.101.29.56` | FLEET 🟢 | User `appie`, discovered 2026-06-24 |
| eva | macOS | ✅ Open | ✅ `eva@100.99.64.92` | FLEET 🟢 | User `eva`, discovered 2026-06-24 |
| appie-mc-1 | Linux | ✅ Open | ❌ Key rejected | BROKEN_KEYS 🟡 | Deploy pubkey to `root@100.107.179.3` |
| harry (mac-mini-van-harry) | macOS | ✅ Open | ❌ Key rejected | BROKEN_KEYS 🟡 | Add pubkey to macOS user's authorized_keys |
| rabi (mac-mini-van-rabi) | macOS | ❌ Closed | N/A | TAILNET_ONLINE ⚪ | Enable Remote Login in Sharing prefs |
| techwiz-mbp | macOS | ❌ Closed | N/A | TAILNET_ONLINE ⚪ | Enable Remote Login in Sharing prefs |
| ipad-pro | iOS | N/A | N/A | TAILNET_ONLINE ⚪ | No SSH possible |
| spark-atlas | Linux | ❌ Offline | N/A | GHOSTS 💤 | Wait for node to come online |
| artemis | macOS | ❌ Offline | N/A | GHOSTS 💤 | Wait for node to come online |
| mac-studio-luminaire | macOS | ❌ Offline | N/A | GHOSTS 💤 | Wait for node to come online |
| iphone181 | iOS | ❌ Offline | N/A | GHOSTS 💤 | No SSH possible |
| macbook-air-lorenzo | macOS | ❌ Offline | N/A | GHOSTS 💤 | Wait for node to come online |
| wolf-diddy | macOS | ❌ Offline | N/A | GHOSTS 💤 | External peer, no access |

**Key SSH failure patterns (2026-06-19 audit):**
- **macOS with port 22 open**: SSH server running but `appie-3-hermes@tailnet` key not in any macOS user's `~/.ssh/authorized_keys`. Remedy: deploy the key to the actual macOS user.
- **Linux with port closed**: SSH daemon not installed/started (`systemctl enable --now sshd` + `apt install openssh-server` if needed).
- **Linux with `Connection refused` after initial `Permission denied`**: fail2ban likely blocked the source IP (eugi pattern).
- **macOS with all ports closed**: Remote Login + Screen Sharing both disabled in System Sharing prefs.

See `references/ssh-connectivity-diagnostics.md` for detailed error transcripts and step-by-step per-failure diagnosis.

### Fleet Node Authorized Keys Audit

Check how many authorized keys exist per node and who they belong to:

```bash
for host in "root@100.118.143.10" "root@100.110.58.73"; do
  echo "=== $host ==="
  ssh -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no \
    -i "$HOME/.ssh/id_ed25519" "$host" \
    "cat /root/.ssh/authorized_keys | awk '{print \$3}'"
done
```

| Node | Keys | Identities |
|------|------|------------|
| appie-2 | 4 | appie@weblyfe-ocean, appie@weblyfe, seyed@Techwiz-MacBook-Pro-8, mc@appie-mc-1 |
| eugi | 2 | appie@weblyfe, Appie-2@appie-brain |

Document any unexpected keys. The comment field (3rd column) identifies the key owner. Stale keys (old hostnames, decommissioned users) should be removed.

### Fleet Node Deploy Keys

Fleet nodes may carry per-service deploy keys for CI/CD:

```bash
ssh <host> "ls -la /root/.ssh/ | grep -v authorized_keys | grep -v known_hosts"
```

Example from appie-2:
```
privanotify_admin_deploy     → PrivaNotify admin
privanotify_deploy           → PrivaNotify
weblyfe_ai_deploy            → Weblyfe AI
weblyfe_ai_deploy_new        → Weblyfe AI (new)
github_do_appie              → GitHub Actions deploy
```

Document the purpose of each key. Remove stale ones.

### SSH Config Audit

```bash
ssh <host> "cat /root/.ssh/config"
```

Check for:
- `PasswordAuthentication no`
- `PubkeyAuthentication yes`
- No wildcard `Host *` patterns that expose sensitive hosts

SSH config aliases can drift over time as Tailscale IPs change during reprovisioning. Periodically run `tailscale status` and update SSH config.

### Hermes Agent Detection

```bash
ssh <host> "ps aux | grep -iE '(hermes|claude|python.*bot|node.*bot|discord|telegram)' | grep -v grep"
```

The process looks like:
```
/usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace
```

Hermes proc count on a healthy node: 2-5 (gateway + workers). Count of 0-1 is a warning.

### Appie-Brain Locations

| Machine | Path |
|---------|------|
| appie-3-hermes (deze VPS) | `/root/clawd/appie-brain/` |
| appie-2 (Hetzner) | `/root/appie-brain/` |
| appie-1 (Mac Mini) | `~/clawd/appie-brain/` |

### Fleet Reality-Check (Periodic Inventory Refresh)

Fleet node status changes over time — offline nodes come back, new nodes join, nodes get decommissioned. All 4 arrays in the scan script drift from reality.

**Run this check monthly** to verify the script's arrays match real Tailscale status:

```bash
# 1. Get actual Tailscale online state
tailscale status | grep -v '^$' | awk '{print $1, $2, $(NF)}'

# 2. Compare against script's FLEET array
grep -A20 '^FLEET=(' ~/clawd/tools/appie-3-daily-security-scan.sh

# 3. Check BROKEN_KEYS — are they still online?
grep -A15 '^BROKEN_KEYS=(' ~/clawd/tools/appie-3-daily-security-scan.sh

# 4. Check TAILNET_ONLINE — still no SSH?
grep -A10 '^TAILNET_ONLINE=(' ~/clawd/tools/appie-3-daily-security-scan.sh

# 5. Check GHOSTS — any back online?
grep -A15 '^GHOSTS=(' ~/clawd/tools/appie-3-daily-security-scan.sh
```

**When to move a node between arrays**:
- Ghost comes online → move to FLEET (with current SSH key and Tailscale IP)
- Active node offline >30d → move to GHOSTS
- Node decommissioned → remove from both arrays

**2026-06-02 update**: `spark-atlas` and `mac-mini-van-eva` both returned online after 51+ days offline. Move from GHOSTS back to FLEET. Verify SSH keys still work before re-adding.

### Fleet Status Categories

15 tailnet nodes (2026-06-23) grouped into 4 arrays:

#### FLEET — SSH-reachable (daily full health check)
```bash
FLEET=(       # dagelijks SSH health → 🟢 (full data) / 🔴 (failed)
    "appie-2|root@100.118.143.10|$HOME/.ssh/id_ed25519|Weblyfe VPS"
    "eugi|root@100.110.58.73|$HOME/.ssh/id_ed25519|Ubuntu VPS (FSN)"
    "appie-1|appie@100.101.29.56|$HOME/.ssh/id_ed25519|Mac Mini Weblyfe (macOS)"
    "eva|eva@100.99.64.92|$HOME/.ssh/id_ed25519|Mac Mini Naoufal (macOS)"
)
```

#### BROKEN_KEYS — online, port 22 open, key rejected
```bash
BROKEN_KEYS=( # daily nc port check only → 🟡
    "appie-mc-1|root@100.107.179.3|$HOME/.ssh/id_ed25519|Mission Control v1 (Linux) — key rejected"
    "harry|100.79.180.56|none|Mac Mini Harry (macOS) — key rejected"
)
```

#### TAILNET_ONLINE — online, no SSH daemon at all
```bash
TAILNET_ONLINE=( # tailnet status only → ⚪
    "rabi|100.67.184.25|macOS|Mac Mini Rabi — Remote Login off"
    "techwiz-mbp|100.87.99.11|macOS|Techwiz MacBook Pro — Remote Login off"
    "ipad-pro|100.105.56.2|iOS|iPad Pro — no SSH"
)
```

#### GHOSTS — offline >7d (logged but no active check)
```bash
GHOSTS=(      # archived → 💤
    "spark-atlas|100.69.197.43|linux|DGX Spark — offline 9d"
    "artemis|100.95.165.116|macOS|Artemis — offline 11d"
    "mac-studio-luminaire|100.126.237.96|macOS|Studio Luminaire — offline 11d"
    "iphone181|100.98.117.8|iOS|iPhone S3YED — offline 4d"
    "macbook-air-lorenzo|100.112.169.28|macOS|Book Air Lorenzo — offline 74d"
    "wolf-diddy|100.102.181.116|macOS|Wolf Diddy — offline 32d"
)
```

**Transition rules:**
- Ghost comes online → move to BROKEN_KEYS or TAILNET_ONLINE (test SSH first)
- BROKEN_KEYS node gets SSH key deployed → move to FLEET
- Online node offline >7d → move to GHOSTS
- Node decommissioned → remove from all arrays
- iOS/iPad nodes belong in TAILNET_ONLINE or GHOSTS — never in FLEET (no SSH)

Voorkomt: valse 🔴 elke dag, 5s SSH timeouts per ghost, ruis in CTO notes.

**CRITICAL**: Maintener de arrays actief. Wanneer een ghost node terug online komt (check via `tailscale status`), verplaats hem direct terug naar BROKEN_KEYS of TAILNET_ONLINE. De SSH key en Tailscale IP kunnen veranderd zijn sinds de node offline ging.

Periodic refresh: zie "Fleet Reality-Check" sectie hierboven.

### Fleet Health Report Template

```markdown
🌐 Weblyfe Tailnet — [DATE]

### ✅ Actieve Bots
appie-1 | 100.101.29.56 | macOS | ✅
appie-2 | 100.118.143.10 | Linux | ✅

### 💤 Gearchiveerd
spark-atlas — offline >30d
eva — offline >30d

### 🔴 Offline (overige nodes)
macbook-air-van-lorenzo — last seen 2026-04-10
```

### Quick Fleet Scan Pattern (Telegram / on-demand)

When Seyed asks for a quick fleet analysis, keep it fast and operational rather than running the full daily scan:

1. **Local health first**: `hostname`, `date -Is`, `uptime`, `df -h /`, `free -m`, Hermes gateway service status, failed SSH logins in 24h, pending apt update count.
2. **Tailnet state via JSON**: parse `tailscale status --json`; include `Self` and `Peer` separately. Summarize online/offline, OS, Tailscale IP, and last-seen age.
3. **Expected-offline context matters**: if Seyed says a device is physically offline/in suitcase, mark it `expected/no action`, not an incident. Still include last-seen time.
4. **Reachability probes**: for online/core nodes, run `tailscale ping` and quick TCP checks for `22,80,443,3000,5000,8000,8080,8443,5900`.
5. **SSH auth check**: test key-based SSH separately from port reachability. Report `port 22 open but key rejected` as an access/remediation issue, not node downtime.
6. **Service fingerprints**: for open HTTP(S) ports, use `curl -skI` and a short body/title probe. On macOS, `5000` often fingerprints as AirTunes and `5900` is Screen Sharing/VNC, both tailnet-accessible rather than internet-facing.
7. **Report concise risk classes**: `healthy`, `expected offline`, `access issue`, `tailnet-exposed service`, `ghost/offline >30d`. End with the next 1-3 recommended actions.

Avoid over-escalating offline personal devices, iOS nodes, or user-declared travel/suitcase devices. The security signal is unexpected offline core infrastructure, key rejection on nodes that should be manageable, public DNS/service failure, or exposed services that should not be tailnet-wide.

### Telegram Fleet Output — Grouped by Status Category

The daily scan Telegram output groups all fleet nodes by their connectivity status for at-a-glance readability. Implemented via `FLEET_CACHE` pipe-separated file and a `case` statement that tracks group transitions:

```
*Fleet*
  SSH ✅
    🟢 appie-2
    🟢 eugi

  SSH key rejected
    🟡 appie-mc-1
    🟡 appie-1
    🟡 eva
    🟡 harry

  Online (geen SSH)
    ⚪ rabi
    ⚪ techwiz-mbp
    ⚪ ipad-pro

  Offline
    💤 spark-atlas
    💤 artemis
    ...
```

**Implementation pattern** in the script's Telegram generation block:

```bash
current_group=""
while IFS="|" read -r name status desc; do
    case "$status" in
        "🟢") group="SSH ✅" ;;
        "🔴") group="SSH ❌" ;;
        "🟡") group="SSH key rejected" ;;
        "⚪") group="Online (geen SSH)" ;;
        "💤") group="Offline" ;;
        *) group="" ;;
    esac
    if [ "$group" != "$current_group" ] && [ -n "$group" ]; then
        [ -n "$current_group" ] && tg_echo ""
        tg_echo "  $group"
        current_group="$group"
    fi
    tg_echo "    $status $name"
done < "$FLEET_CACHE"
```

**Key constraint**: ALL 4 array types (FLEET, BROKEN_KEYS, TAILNET_ONLINE, GHOSTS) must write to the same FLEET_CACHE in array order. The Telegram block reads once sequentially. This guarantees the Telegram output matches the report and no nodes are missed.

**Cache format** (pipe-separated, no JSON):
```
appie-2|🟢|Weblyfe VPS (Hetzner)
eugi|🟢|Ubuntu VPS (FSN)
appie-mc-1|🟡|Mission Control v1 — key rejected
rabi|⚪|Mac Mini Rabi — Remote Login off
spark-atlas|💤|DGX Spark — offline 9d
```

## Watchdog Architecture (separate cron jobs, no_agent=True)

These run independently from the daily scan to catch problems early. Script-only mode: zero LLM tokens per tick, silent when healthy.

| Watchdog | Schedule | Script | Trigger |
|----------|----------|--------|---------|
| Disk | Every 4h | `disk-watchdog.sh` | >80% ⚠️, >90% 🔴 on any fleet node |
| Tailscale | Every 30min | `tailscale-watchdog.sh` | Core node (appie-1, appie-2, eugi) goes offline |
| SSH key audit | 1st of month | `ssh-key-audit.sh` | Monthly authorized_keys review per node |
| Failed login trend | In daily scan | `failed-login-trend.sh` | Spike >5x yesterday or >10/day |
| Agent framework CVEs (Python + Go) | Daily 06:30 UTC | `agent-framework-cve-scan.py` (via LLM cron job `c503abd02155`) | Any CVE reported in last 90d for 20 packages (17 Python agent + 3 Go infra). Uses `[SILENT]` when clean. |

Cron job setup:
```bash
# Scripts must be at ~/.hermes/scripts/ (or the profile-specific scripts dir)
# Symlinks may be blocked by the cron scheduler — use real files
cronjob action=create name="disk-watchdog" schedule="0 */4 * * *" \
  no_agent=True script="disk-watchdog.sh" deliver="telegram:1817919454"
```

## Security Governance & Suggestion Pipeline

A multi-agent governance pattern for human-in-the-loop security improvements. Appie-3 (CTO specialist) creates the suggestion plan, Appie-Opus (orchestrator) presents suggestions to Seyed, Seyed approves before execution.

### When to Use

- After the daily security scan finds issues that need remediation
- User asks for "daily security suggestions", "action plan for opus", "suggestions to present to seyed"
- Setting up a security governance workflow where changes require human approval
- Any recurring task where the CTO recommends but the user decides

### Architecture

```
Appie-3 (CTO)                Appie-Opus (orchestrator)    Seyed (human)
      │                              │                        │
      │  Creates plan ──────────────►│                        │
      │  DAILY-SECURITY-             │                        │
      │  SUGGESTIONS.md              │                        │
      │                              │  Presents S001-S00X ──►│
      │                              │  "Wat, waarom,         │
      │                              │   risico, revert"      │
      │                              │◄─────── 👍 / 👎 ──────│
      │                              │                        │
      │  (Appie-3 only acts          │  Executes approved     │
      │   when directly asked)       │  suggestions           │
```

### Suggestion Format

Each suggestion MUST include four fields:

| Field | Description |
|-------|-------------|
| **Wat** | What the check/change is (1-2 zinnen) |
| **Waarom** | Why it matters (1 zin) |
| **Risico** | Risk level: Geen / Laag / Medium |
| **Revert** | Exact command to undo the change |

### Safety Rules (for Appie-Opus)

1. **Read-only or reversible only** — no `rm -rf`, `chmod -R`, `iptables -F`
2. **STOP on error** — report to Seyed, do not self-fix
3. **No lockouts** — always test key-based login before disabling password auth
4. **No service restarts** without explicit Seyed approval
5. **Every suggestion has a revert step** — if missing, do not execute

### Suggestion Count

S001-S027 exist (expanded 2026-06-20 met S021-S027: agent framework CVE scan, Headroom install/verify/MCP, SkillsGuard cloud API, CVE-2026-2256 check, MCP cutover check, SSH key deployment plan).

### Daily Rotation

27 suggestions exist (S001-S027), rotated by day:

| Dag | Category | Sample Suggestions |
|-----|----------|-------------------|
| Maandag | Access audit | authorized_keys check (appie-2 + eugi), tailnet status, S027 (SSH key plan) |
| Dinsdag | Config check | .env perms, open ports on fleet, S025 (CVE-2026-2256 check) |
| Woensdag | Dependency scan | gitleaks, npm audit, S021 (agent framework CVE scan), S026 (MCP cutover) |
| Donderdag | Web security | SSL certs, security headers, failed logins, S024 (SkillsGuard) |
| Vrijdag | System health | disk, pending updates, S022-S023 (Headroom check/MCP) |
| Weekend | Fleet check | tailnet status, spark-atlas SSH, gateway uptime |

### Plan Location

Canonical plan: `~/clawd/appie-3-cto/DAILY-SECURITY-SUGGESTIONS.md`

Zie `references/security-suggestions.md` voor de volledige, actuele suggestielijst.

## Backup Sync (optional, needs approval)

`backup-sync.sh` — rsyncs appie-brain, Hermes config, SSH config, and secrets to appie-2.
Not active by default. Script exists at `~/.hermes-appie3/scripts/backup-sync.sh`.

## Cross-Platform Detection (macOS vs Linux)

The daily scan script may run on macOS (Mac Mini) or Linux (Hetzner VPS). Use an `uname` check at the top to branch OS-specific commands:

```bash
OS="$(uname -s)"
case "$OS" in
  Darwin) IS_MACOS=true; IS_LINUX=false ;;
  Linux)  IS_MACOS=false; IS_LINUX=true  ;;
esac
```

### Command Equivalents

| macOS Command | Linux Alternative | When to Use |
|---|---|---|
| `vm_stat` | `free` or `/proc/meminfo` | Memory check |
| `sysctl -n vm.loadavg` | `cat /proc/loadavg` | Load averages |
| `log show --predicate ... --last 24h` | `journalctl --since "24 hours ago" \| grep -c "Failed password"` | Failed login count |
| `date -j -f "%b %d %H:%M:%S %Y %Z" "$date" +%s` | `date -d "$date" +%s` | Date parsing (SSL cert expiry) |
| `date -v-1d +%Y-%m-%d` | `date -d "yesterday" +%Y-%m-%d` | Date arithmetic |
| `/opt/homebrew/bin/openssl` | `/usr/bin/openssl` | SSL cert check |
| `pgrep -f "hermes_cli"` | `pgrep -f "hermes gateway"` | Hermes process detection |
| `ping` | `ping` (exists on both, but macOS has stricter permissions) | Connectivity check |
| `trash` | `rm -i` or `/usr/bin/trash-cli` | Safe delete |

### Branch Template

```bash
if [ "$IS_MACOS" = true ]; then
    mem_active=$(vm_stat | grep 'pages active' | awk '{print $NF}' | tr -d '.')
    mem_free=$(vm_stat | grep 'pages free' | awk '{print $NF}' | tr -d '.')
    load=$(sysctl -n vm.loadavg | tr -d '{}')
    failed_logins=$(log show --predicate 'eventMessage contains "Failed to authenticate"' --last 24h --style compact 2>/dev/null | wc -l | tr -d ' ')
    ossl="/opt/homebrew/bin/openssl"
    hermes_pat="hermes_cli"
    date_parse() { date -j -f "%b %d %H:%M:%S %Y %Z" "$1" +%s 2>/dev/null; }
    date_prev() { date -v-1d '+%Y-%m-%dT00:00:00.000' 2>/dev/null; }
else
    mem_active=$(awk '/Active/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)
    mem_free=$(awk '/MemAvailable/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)
    load=$(cat /proc/loadavg | cut -d' ' -f1-3)
    failed_logins=$(journalctl --since "24 hours ago" 2>/dev/null | grep -c "Failed password" || echo 0)
    ossl="/usr/bin/openssl"
    hermes_pat="hermes gateway"
    date_parse() { date -d "$1" +%s 2>/dev/null; }
    date_prev() { date -d "yesterday" '+%Y-%m-%dT00:00:00.000' 2>/dev/null; }
fi
```

### Key Pitfall: Memory Calculation Mismatch

`vm_stat` outputs **pages** (4096 bytes each on macOS ARM) while `/proc/meminfo` outputs **kB** on Linux. The percentage calculation may differ. If you only need percentage, use platform-specific thresholds or normalise to MB first.

On Linux:
```bash
mem_total_kb=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
mem_active_kb=$(awk '/Active/ {print $2}' /proc/meminfo)
mem_pct=$(( mem_active_kb * 100 / mem_total_kb ))
```

On macOS:
```bash
page_size=$(vm_stat | grep 'page size' | awk '{print $8}')
mem_active=$(vm_stat | grep 'pages active' | awk '{print $NF}' | tr -d '.')
mem_active_mb=$(( mem_active * page_size / 1048576 ))
```

### Hermes Process Detection

The binary path varies between machines. Instead of matching a specific process name, detect Hermes generically:

```bash
hermes_count=$(pgrep -f "$hermes_pat" | wc -l | tr -d ' ')
# Also try the canonical install path
if [ "$hermes_count" -eq 0 ]; then
    hermes_count=$(pgrep -af "/usr/local/lib/hermes-agent" | wc -l | tr -d ' ')
fi
```

## macOS-Specific Scripting Quirks

All discovered through trial and error. Encode these in every script.

### Bash 3.x — No Associative Arrays, `local` Only in Functions
- macOS bash 3.x: `local -A` (associative arrays) fails silently
- `local` keyword ONLY inside function bodies. Brace blocks `{ }` are NOT functions.
- The Telegram generation block (brace group at script bottom) must NOT use `local`
- Use indexed arrays with pipe-separated fields:
```bash
local fleet=(
    "appie-2|root@100.118.143.10|$HOME/.ssh/id_ed25519"
)
for entry in "${fleet[@]}"; do
    name=$(echo "$entry" | cut -d'|' -f1)
    ssh_target=$(echo "$entry" | cut -d'|' -f2)
done
```

### vm_stat Parsing — Case-Sensitive grep Required (macOS only; irrelevant on Linux)
macOS vm_stat outputs uppercase field names:
```
Pages free:                               96480.
Pages active:                            296328.
```
```bash
# WRONG — awk /pages active/ doesn't match (case)
mem_active=$(vm_stat | awk '/pages active/ {print $NF}')
# RIGHT
mem_active=$(vm_stat | grep 'pages active' | awk '{print $NF}' | tr -d '.')
```
This applies to ALL vm_stat fields. The `-i` flag on grep works too.

### LibreSSL vs OpenSSL (macOS only)
`/usr/bin/openssl` is LibreSSL 3.3.6 — silently fails on `x509 -noout -enddate`.
Always use brew: `/opt/homebrew/bin/openssl` (OpenSSL 3.x). On Linux `/usr/bin/openssl` works fine.

### No `2>/dev/null` With openssl in Subshells
```bash
# DON'T: cert=$(openssl ... 2>/dev/null)  ← kills cert output!
# DO:    cert=$(openssl ... 2>&1)
```

### No `timeout` With openssl
`timeout 5 openssl s_client` kills the process mid-TLS-handshake. Don't wrap openssl in timeout (it exits naturally after DONE).

### No `ping` Binary (macOS only)
Use `tailscale ping` instead. On Linux, `ping` is available.

### No `/dev/tcp` (macOS only)
Bash's virtual filesystem `/dev/tcp` doesn't exist on macOS.

### SSH Key Timeout for Relay Nodes
Nodes behind Tailscale DERP relays take 3-5s per SSH connection. Always use `ConnectTimeout=5`. `ConnectTimeout=3` gives false positives.

### No SSH Private Keys on Linux VPS
On the Hetzner VPS where Appie-3 runs, `~/.ssh/` typically only has `authorized_keys` — no `id_*` private keys. Fleet SSH checks that rely on SSH keys will fail. Use the local machine as the SSH client (Mac Mini appie-1) or deploy keys to the VPS if fleet checks must run from there.

## Client Site Reconnaissance & Deployment Inspection

A recurring CTO task: user says "check out [client site]" and you need to identify the platform, find the deployment, and inspect the build.

### 1. Platform Identification

When visiting an unknown client site, determine what platform it's built on:

| Signal | Platform | How to Check |
|--------|----------|-------------|
| Scripts from `cdn.prod.website-files.com` | **Webflow** | `document.querySelectorAll('script[src*=\"website-files\"]')` via browser_console |
| `server: Netlify` in HTTP headers | **Netlify** | `curl -sI https://example.com \| grep -i server` |
| `X-NF-Request-Id` / `Netlify Edge` in cache-status | **Netlify** | `curl -sI \| grep -i 'x-nf\|netlify'` |
| `server: cloudflare` only | **Cloudflare proxy** (platform unknown) | `curl -sI \| grep -i server` — need to dig deeper |
| WordPress paths (`/wp-content/`, `/wp-admin/`) | **WordPress** | Check page source or paths |
| `meta[name="generator"]` content | Various | `document.querySelector('meta[name=\"generator\"]')?.content` |
| Nameservers | Hosting provider | `dig example.com NS +short` |

**Pattern**: always check multiple signals — a single header can be misleading (Cloudflare proxies many platforms).

### 2. Codebase Search for Non-Resolving Subdomains

When user gives a subdomain that doesn't resolve (DNS error), search the workspace:

```bash
# The domain is likely stored somewhere in project configs
search_files(path="~/clawd", pattern="booking.example*", target="content")
search_files(path="~/clawd/projects", pattern="example*", target="files")
```

Common hiding places in the Weblyfe workspace:
- `projects/weblyfe-ai-standalone/screenshot-tool.js` — `url` keys in the array
- `projects/*/netlify.toml` — custom domain configs
- `projects/*/fleet-config.ts` — agent/client domain inventory
- `docs/openclaw_clients*.csv` — client domain lists

### 3. Netlify Deployment Inspection

Requires: `NETLIFY_AUTH_TOKEN` in `~/.weblyfe-secrets/.env`.

```bash
# Source the token
source ~/.weblyfe-secrets/.env

# List all sites and find the target
curl -s -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
  "https://api.netlify.com/api/v1/sites?page=1&per_page=100" | \
  python3 -c "import sys,json; [print(s['name'], s.get('custom_domain','')) for s in json.load(sys.stdin)]"

# Get site details — includes build_settings (cmd, dir, repo_url, repo_branch)
SITE_ID=$(curl -s -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
  "https://api.netlify.com/api/v1/sites?page=1&per_page=100" | \
  python3 -c "import sys,json; [print(s['id']) for s in json.load(sys.stdin) if 'example' in s['name'].lower()]")

# Check deploys (last 5)
curl -s -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
  "https://api.netlify.com/api/v1/sites/$SITE_ID/deploys?page=1&per_page=5"
```

**Key fields from deploy:**
- `state`: `ready` / `error` — build success
- `created_at`: deploy timestamp
- `deploy_time`: seconds
- `commit_ref`: git commit SHA (first 10 chars for display)
- `commit_url`: link to GitHub commit
- `published`: `true` = live version (`None` = not published)
- `error_message`: build failure reason

**Key fields from build_settings** (in site detail):
- `cmd`: build command (e.g. `npm run build`)
- `dir`: publish directory (e.g. `dist`)
- `repo_url`: linked GitHub repo
- `repo_branch`: branch for auto-deploys
- `provider`: git provider (`github`)
- `allowed_branches`: which branches trigger deploys

### 4. DNS & Nameserver Checks

```bash
# Check A record
dig example.com A +short

# Check nameservers (identify hosting provider)
dig example.com NS +short

# Check if subdomain exists
dig sub.example.com A +short

# Check HTTP headers (platform identification)
curl -sI https://example.com | grep -iE 'server|x-powered-by|x-served-by'
```

### 5. GitHub Repo Inspection (if token works)

Source from `~/.weblyfe-secrets/.env` and use:
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO"
```

If the token returns `401 Bad credentials`, note it and proceed without — the build settings from Netlify usually have enough info.

### 6. Site Reconnaissance Results Template

Report findings in a compact table for Telegram:

```markdown
**🌐 Site:** `https://example.com` — description
**Platform:** Webflow / Netlify / WordPress

**Netlify:** naam | ✅ Live | laatst: datum (Xs)
**Repo:** `owner/repo` (branch: main)
**Build:** `npm run build` → `dist/`

**App details:**
- Multi-step wizard: Step 1 → Step 2 → ...
- Key features: feature list
- Footer: credits, links
```

## Post-Scan Steps

After the scan script finishes:

### 0. Log to Mission Control

Log task lifecycle to the fleet orchestrator dashboard:

```bash
python3 ~/clawd/tools/mc-log-task.py "Daily security scan" --agent Appie-3 --status done
```

Zie `references/mission-control-integration.md` voor de standing directive, tool setup, en endpoint details.

### 1. Update INDEX.md
Append one line to `~/clawd/appie-brain/knowledge/research/daily-research/INDEX.md`:
```
| YYYY-MM-DD | 🟢/🔴 Security Scan — key findings | [Report](./YYYY-MM-DD/security-scan.md) |
```
Use `patch` to append after the last table row — never `write_file` (would overwrite index).

### 2. Add CTO Action Items
For every 🔴/⚠️ finding, append a `## CTO Action Items` section:
```
## CTO Action Items
  🔴 **finding** — context
  ├─ Check: command
  └─ Priority: High/Medium/Low
```

### 3. Verify Report
Read file at `~/clawd/appie-brain/knowledge/research/daily-research/YYYY-MM-DD/security-scan.md` before delivering.

## Timing

v2 scan takes ~120-180s (down from 180-300s in v1):
- SSH fleet: 5-15s
- SSL certs: 10-15s (4 domains)
- Gitleaks --no-git: 10-60s
- Security headers: 10-20s (4 domains)
- Pending updates: 5-10s (SSH)
- CVE APIs: 5-15s
- npm audit: 30-60s

## Pitfalls

### Pending Updates Scorecard Bug — SSH Fail Falsely Reports ✅ (FIXED 2026-06-12)

The `scan_updates()` function had a logic flaw: when SSH fails (`$updates = "?"`), the if-condition fell through to `else` which reported `"✅ $name — up-to-date"`. Fixed by adding an explicit `?` check that reports `"🔴 $name — unreachable"` instead. See `references/linux-cross-platform-notes.md` for the cross-platform equivalents used during the port.

**Old behavior**: SSH unreachable → falsely reported as "up-to-date"
**Current behavior**: SSH unreachable → "🔴 $name — unreachable"
- **vm_stat awk bug**: `awk '/pages active/'` returns empty on macOS. Always use `grep`.
- **Gitleaks git mode**: 35,399 false positives from history. Always `--no-git` with `.gitleaks.toml`.
### Cron Workdir Must Exist on the Host

Each cron job can have a `workdir` that Hermes `cd`s into before running the script. If the workdir path doesn't exist on the host (e.g. macOS path `/Users/appie/clawd` on a Linux VPS), the job may fail silently or produce no delivery.

**Best practice**: either omit `workdir` (uses default), or set it to an absolute path that exists on the current host. Check with `ls -d /path/to/workdir` before scheduling.

### `no_agent` Script Location

Scripts must be at `~/.hermes/scripts/<name>` (or the active profile's scripts directory). Hermes resolves no_agent script names from this directory — do not include a path prefix in the cron `script` field, just the filename.
- **FLEET_CACHE format**: Use pipe-separated, not JSON. JSON escaping of emoji statuses (🟢🔴) and descriptions with parentheses causes parse failures.
- **`[]` in fleet cache**: Initialize with `: > "$FLEET_CACHE"` (empty file), not `echo "[]" > "$FLEET_CACHE"`. The Telegram section reads all lines and `[]` appears as garbage output.
- **Security headers via curl**: Cloudflare/redirect chains may show intermediate headers. Use `-L` or check the final URL separately.
- **Pending updates security count**: Use `grep -i security` not `-security` — the dash-prefix format varies by Ubuntu version.

### v1 → v2 What Changed
- **Telegram/report divergence**: FIXED. v1 had separate SSH loops for report and Telegram with different ConnectTimeout values. v2 uses shared FLEET_CACHE.
- **CVE feed**: NVD (rate-limited) → GitHub Advisory API (no auth) + OSV.dev (no auth).
- **Ghost nodes**: spark-atlas, eva removed from active scan → "Archived Nodes" section.
- **Duplicate macOS quirks**: Removed from bottom of SKILL.md. Now only in the macOS section.
- **Watchdogs**: Not part of daily scan. Separate cron jobs with no_agent=True.

### v4 — New (2026-06-23)
- **4-category fleet model**: Added TAILNET_ONLINE array for online nodes without SSH (iOS, Remote Login off). BROKEN_KEYS refactored for port-22-open/key-rejected nodes. GHOSTS expanded to ALL offline nodes, not just >30d.
- **Comprehensive fleet coverage**: Scan now covers all 15 tailnet nodes instead of just 2-3 reachable ones. Telegram output groups by status category.
- **Grouped Telegram output**: New `case`-based group-tracking pattern for organized fleet display. All 4 array types write to shared FLEET_CACHE.
- **Fleet SSH Access Map**: Updated from 7 to 15 nodes with category column.
- **Fleet Reality-Check**: Expanded from 2 arrays to all 4.

## Docker Web Service Hardening

A recurring CTO task: a client-facing web service (often n8n, but the pattern applies to any Docker-based service) that's exposed to the internet via reverse proxy. This section captures the systematic hardening sequence, applied during the 2026-06-15 n8n-weblyfe upgrade.

### Hardening Sequence (ordered by risk)

| Step | Action | Risk if skipped | Revert |
|------|--------|-----------------|--------|
| 1 | **Pin Docker images** — never `latest` tag. Use exact semver (e.g. `n8n:2.26.3`, `caddy:2`) | Unpredictable updates break workflows | `docker compose up -d` with old tag |
| 2 | **Bind internal ports to 127.0.0.1 only** — `127.0.0.1:5678:5678` instead of `5678:5678`. The reverse proxy (Caddy) reaches it via the Docker network, not host interface | Direct HTTP access bypasses TLS/HTTPS | Revert port mapping in compose |
| 3 | **Persist encryption keys in .env** — extract from container config (e.g. n8n's `/home/node/.n8n/config` encryptionKey), add to `.env`, reference in compose as `N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}` | On volume rebuild, all encrypted credentials become unrecoverable | Remove env var, config falls back to auto-generated key |
| 4 | **UFW firewall** — `deny incoming`, allow only 22, 80, 443. Docker's DOCKER-USER chain runs before UFW, so container-networking (Caddy→n8n) stays intact | Exposed SSH + direct service ports | `ufw disable` |
| 5 | **Fail2ban for SSH** — `maxretry=3`, `bantime=86400` on sshd jail. Pre-installed on many Ubuntu images but often not enabled | Unlimited brute-force attempts | `fail2ban-client stop sshd` |
| 6 | **SSH key-only** — `PermitRootLogin prohibit-password`, `PasswordAuthentication no`. Verify with `sshd -t && systemctl reload ssh` before disconnecting. **Exception:** Digital Ocean web console requires password login — set `PermitRootLogin yes` + `PasswordAuthentication yes` if DO console access is needed | Password-based attacks | Revert sshd_config changes |
| 7 | **System updates + reboot** — `apt update && DEBIAN_FRONTEND=noninteractive apt upgrade -y` then reboot for kernel. **Use `systemctl reboot`** — `reboot`/`shutdown -r now` may be blocked by agent security. May leave SSH session in background during long upgrades | Unpatched kernel + CVE-exploitable packages | Rollback via apt snapshots (rarely needed) |
| 8 | **Clean up old Docker images** — `docker image prune -f`, remove old tags (`docker rmi <old-tag>`). Reclaim 2-4GB on small droplets | Disk fills up, service degrades | Images can be re-pulled by tag |

### Docker Compose Pitfalls (n8n-specific, but apply generally)

**Docker Compose v2:** Remove the `version:` top-level key. Compose v2 emits `version must be a string` validation errors and ignores it entirely. Use raw services block.

**`.env` variable expansion:** Docker Compose auto-loads `.env` from the compose project directory. But when `docker compose config` shows unresolved paths (e.g. `${DATA_FOLDER}/x`), switch to **absolute paths** in the compose file to guarantee reliability regardless of env loading order.

**Image registry divergence:** The n8n 1-Click Droplet had two n8n images — `n8nio/n8n:latest` (Docker Hub) and `docker.n8n.io/n8nio/n8n:latest` (official n8n registry). Only one is used by the compose file; the other is orphaned waste. After pinning a specific version, clean up the orphan with `docker rmi`.

**n8n deprecation handling:** After upgrade, check container logs (`docker logs <container> --tail 20`). Common deprecations to action:
- `N8N_RUNNERS_ENABLED` → Remove from environment; no longer needed (task runners auto-register)
- `storage directory rename` → Set `N8N_MIGRATE_FS_STORAGE_PATH=true` to migrate binaryData→storage for n8n v3
- `pdf-lib not installed` in task runner → Install via Dockerfile or remove from NODE_FUNCTION_ALLOW_EXTERNAL if not used

### n8n-Specific Hardening (see reference)

See `references/n8n-droplet-hardening.md` for the full session transcript including version gap (2.13.2 → 2.26.3 = 12+ minor versions), n8n config structure, and the exact docker-compose.yml changes applied.

### Original v1 Pitfalls (still relevant)
- SSH timeout consistency: all sections must use same ConnectTimeout.
- Hermes agent count >1 is normal (gateway + workers).
- macOS load includes disk I/O, expect slightly higher readings vs Linux.

## Reference Files
### Seyed Communication Pattern — Short Blocker Lists

Seyed responds best to **executive blocker summaries** — not detailed reports. When reporting fleet security status:

- Lead with a **3-6 item checklist** of blockers (🔴 = blocks me, 🟡 = needs his input, ✅ = already working)
- Each blocker: 1 line description + 1 line remedy
- End with what's already running without his help
- Example pattern from 2026-06-20: "🔴 Blocker 1 — eugi SSH" → Seyed forwarded the key within minutes
- Do NOT bury the blocker in prose. Use a compact table or bullet list with urgency emoji

This pattern is preferred over full scan reports for daily/standup comms. Save the full report for when he asks "run the scan" or for cron deliveries.

## Reference Files

- `references/daily-security-scan-script.md` — annotated v2 script reference (output structure, key implementation details, normal ranges)
- `references/mission-control-integration.md` — Mission Control task-logging setup, standing directive, fleet config reference
- `references/fleet-snapshot-v2.md` — fleet state after 2026-06-02 update (spark-atlas/eva back online, current node inventory)
- `references/fleet-inventory.md` — SSH key inventory, active/ghost node map, latency, and per-machine notes
- `references/security-suggestions.md` — daily security suggestion pipeline (S001-S020) voor multi-agent governance, dagrotatie, en veilige/reversible acties
- `references/cron-log-self-audit.md` — systematic procedure for auditing cron job health, log anomalies, and script config drift against real Tailscale state
- `references/ssh-key-deployment.md` — batch deploy Appie-3's SSH public key to the fleet: deploy script template, idempotent key check, non-Tailscale server pattern (public IP / Digital Ocean), post-deployment verification
- `references/tailscale-device-cleanup.md` — identify and remove stale/duplicate Tailscale devices via dashboard/Admin API, including StableID verification and post-key-deploy SSH probes
- `references/new-host-init.md` — procedure for initializing the CTO agent on a fresh host: cron validation, platform-specific patching, tool installation, pending-items documentation
- `references/new-host-init.md` — procedure for initializing the CTO agent on a fresh host: cron validation, platform-specific patching, tool installation, pending-items documentation
- `references/mac-mini-coding-harness-recovery.md` — recover access to an online macOS Mini / coding harness over Tailscale when SSH is listening but Appie-3's key is not authorized.
- `references/new-host-init.md` — procedure for initializing the CTO agent on a fresh host: cron validation, platform-specific patching, tool installation, pending-items documentation

## Scripts (in `~/.hermes/scripts/`, or profile-specific scripts dir)

- `disk-watchdog.sh` — disk threshold check, silent when healthy
- `tailscale-watchdog.sh` — core node connectivity, silent when healthy
- `ssh-key-audit.sh` — monthly authorized_keys review per fleet node
- `failed-login-trend.sh` — CSV-based daily count with spike detection
- `backup-sync.sh` — rsync to appie-2 (optional, needs approval)
- `file-integrity-check.sh` — sha256 baseline for critical system files
- `appie-3-daily-security-scan.sh` — daily security scan (covers 9 layers)