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
