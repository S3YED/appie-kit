---
name: stripe-operations
description: "Operate Stripe safely from an agent or VPS: verify access, install/use Stripe CLI, inspect products/prices/customers/subscriptions/checkout sessions/webhooks, and perform guarded payment operations. Use when the user asks about Stripe access, Stripe CLI setup, billing audits, products/prices, subscriptions, checkout, webhooks, refunds, coupons, or payment configuration."
---

# Stripe Operations

Use this skill for Stripe account access checks, CLI setup, read-only billing inspection, and carefully gated mutations.

## Safety rules

- Never print Stripe secret keys, publishable keys, webhook secrets, restricted keys, OAuth tokens, or connection strings.
- Redact any value matching `sk_live_`, `sk_test_`, `pk_live_`, `pk_test_`, `rk_live_`, `rk_test_`, or `whsec_` before reporting.
- Default to read-only operations: list/retrieve products, prices, customers, subscriptions, checkout sessions, invoices, payment links, events, and webhooks.
- Ask for explicit confirmation before any mutation: creating/updating products or prices, archiving, coupons/promotion codes, refunds, cancellations, webhook endpoint changes, payment links, customer portal changes, or live/test mode switching.
- State clearly whether the key/account is live or test mode.

## Access discovery

1. Check whether Stripe CLI exists:

   ```bash
   command -v stripe && stripe --version
   ```

2. Check env files without printing values:

   ```bash
   python3 - <<'PY'
   from pathlib import Path
   for p in [Path('/root/.hermes/.env'), Path('.env'), Path('.env.local')]:
       if not p.exists():
           continue
       keys=[]
       for line in p.read_text(errors='ignore').splitlines():
           if '=' in line and line.split('=',1)[0].strip().startswith(('STRIPE_', 'NEXT_PUBLIC_STRIPE_')):
               keys.append(line.split('=',1)[0].strip())
       if keys:
           print(str(p) + ': ' + ', '.join(sorted(keys)))
   PY
   ```

3. Verify API access with a read-only account call. Do not echo the key:

   ```bash
   python3 - <<'PY'
   import base64, json, urllib.request, urllib.error
   from pathlib import Path

   key = ''
   for line in Path('/root/.hermes/.env').read_text(errors='ignore').splitlines():
       if line.startswith('STRIPE_SECRET_KEY='):
           key = line.split('=',1)[1].strip().strip('"').strip("'")
           break
   if not key or key.startswith('***') or key == '[REDACTED]':
       print('stripe_secret_status=missing_or_redacted')
       raise SystemExit
   print('stripe_secret_status=present_' + ('live' if key.startswith('sk_live_') else 'test' if key.startswith('sk_test_') else 'unknown_mode'))
   req = urllib.request.Request('https://api.stripe.com/v1/account')
   req.add_header('Authorization', 'Basic ' + base64.b64encode((key + ':').encode()).decode())
   try:
       with urllib.request.urlopen(req, timeout=15) as r:
           data = json.loads(r.read().decode())
       safe = {k: data.get(k) for k in ['id','country','default_currency','business_type','charges_enabled','payouts_enabled','details_submitted']}
       print(json.dumps(safe, sort_keys=True))
   except urllib.error.HTTPError as e:
       print('stripe_api_http_error=' + str(e.code))
   PY
   ```

## Stripe CLI install pattern

- Prefer official package-manager instructions when system directories are writable.
- On constrained agents/VPSes where `/usr/share/keyrings`, `/usr/local/bin`, or APT sources are read-only, install the official GitHub release binary under `/root/.local/bin` and verify SHA256.
- See `references/stripe-cli-install.md` for the user-local, checksum-verified install recipe.

## CLI usage patterns

For read-only CLI commands, pass `STRIPE_API_KEY` from the env without printing it:

```bash
STRIPE_API_KEY="$STRIPE_SECRET_KEY" stripe products list --limit 5
STRIPE_API_KEY="$STRIPE_SECRET_KEY" stripe prices list --limit 5
STRIPE_API_KEY="$STRIPE_SECRET_KEY" stripe customers list --limit 5
STRIPE_API_KEY="$STRIPE_SECRET_KEY" stripe subscriptions list --limit 5
```

Notes:

- Some Stripe CLI versions do not support a global `--format json` flag. If `unknown flag: --format` appears, rerun without it. Many API list commands still print JSON-like output by default.
- If parsing output for reports, capture stdout/stderr to temp files and redact secrets before displaying.
- `stripe login` is optional when a valid API key is available for server-side read-only checks.

## Reporting format

Report concise, non-secret facts:

- CLI installed: yes/no and path
- CLI version
- Key mode: live/test/unknown
- API check: ok/error
- Account ID, country, default currency, business type, charges/payouts/details flags
- Next step and whether it is read-only or requires confirmation

Avoid dumping raw customer, payment, invoice, or subscription data unless the user explicitly asks and the output is minimized/redacted.
