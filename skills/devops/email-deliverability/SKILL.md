---
name: email-deliverability
description: "Diagnose and fix SPF/DKIM/DMARC for Weblyfe client domains. Covers Namecheap Private Email, Google Workspace, and common DNS misconfigurations."
version: 1.0.0
---

# Email Deliverability

Diagnose and fix email authentication (SPF/DKIM/DMARC) for Weblyfe client domains. Most common scenario: Namecheap Private Email receiving or Google Workspace sending.

## Triggers

- "Email gaat naar spam"
- "Mail komt niet aan bij [client]"
- "Address not found" bounce van Namecheap
- Nieuwe domein mail setup

## Quick Diagnostic

```bash
# Check all three for any domain
dig DOMAIN TXT +short | grep spf    # SPF
dig SELECTOR._domainkey.DOMAIN TXT +short  # DKIM
dig _dmarc.DOMAIN TXT +short        # DMARC
```

## Common Patterns

### Google Workspace Sending → Namecheap Private Email Receiving

**Symptom:** `554 5.1.1 Recipient address rejected: undeliverable address (JFE030050)`

**Root cause:** Namecheap is strict on SPF. If the sending domain has no SPF, Namecheap bounces with "address not found" even though the mailbox exists.

**Fix:** Add SPF to sending domain:
```
v=spf1 include:_spf.google.com ~all
```

### Namecheap Private Email Sending → Anywhere

**SPF:** Auto-configured when you activate Private Email:
```
v=spf1 include:spf.privateemail.com ~all
```

**DKIM:** Must be manually enabled in Namecheap dashboard:
1. Private Email → Manage → Email Security → DKIM → Generate
2. Copy Host + DNS Record values
3. Add as TXT record in DNS
4. Selector is `privateemail` (NOT `default`)

**DMARC:** Add TXT record:
```
Host: _dmarc
Value: v=DMARC1; p=none; rua=mailto:info@DOMAIN
```

## DNSSEC Warning

Namecheap defaults to DNSSEC on. If DNS is managed elsewhere (Cloudflare, DO), DNSSEC must be disabled at Namecheap or records won't resolve.

## Verification

After setup, send a test email and check headers for:
- `spf=pass`
- `dkim=pass`
- `dmarc=pass`

## Pitfalls

- **Namecheap DKIM selector is `privateemail`**, not `default`. Dig for `privateemail._domainkey.DOMAIN`.
- **Missing SPF causes "address not found"** on Namecheap, not "SPF failed". The error is misleading.
- **DMARC `p=none`** is monitor-only. Start here, verify for 2 weeks, then tighten.
- **DKIM record contains the public key** — no separate public key upload needed.
- **Only ONE SPF record per domain.** Multiple TXT records starting with `v=spf1` breaks validation.

## References

- `references/namecheap-jfe030050.md` — the misleading "address not found" error