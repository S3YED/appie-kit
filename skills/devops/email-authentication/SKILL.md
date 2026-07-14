---
name: email-authentication
description: Diagnose and fix email deliverability with SPF, DKIM, DMARC. Covers Google Workspace, Namecheap Private Email, and general DNS mail record verification.
---

# Email Authentication (SPF / DKIM / DMARC)

Use when diagnosing bounced emails, spam delivery, or setting up mail authentication for a domain.

## Diagnosis workflow

When mail from domain A to domain B bounces but mail from Gmail to B works:

1. Run the verification script (see references/dns-checks.md) on domain A first
2. Missing SPF is the most common cause — fix it before investigating DKIM
3. Namecheap Private Email bounce `JFE030050` ("address not found") is usually SPF rejection in disguise, even when the mailbox exists
4. After fixes, wait 1-2 hours for DNS propagation, then test with a real email

## Provider-specific SPF records

| Provider | SPF record |
|---|---|
| Google Workspace | `v=spf1 include:_spf.google.com ~all` |
| Namecheap Private Email | `v=spf1 include:spf.privateemail.com ~all` |

Host is always `@` (root domain). Type is always TXT.

## DKIM

**Google Workspace**: Enable in Google Admin → Apps → Gmail → Authenticate email. Default selector is `google`, so the record goes at `google._domainkey.<domain>`.

**Namecheap Private Email**: Enable in Namecheap dashboard → Private Email → Manage domain → Email Security → Generate DKIM. Namecheap uses selector `privateemail` (NOT `default`), so the record goes at `privateemail._domainkey.<domain>`. Copy the Host and DNS Record fields from the dashboard — the Public Key field is informational only and already included in the DNS Record.

## DMARC

Start with monitor mode for all new domains:

```
v=DMARC1; p=none; rua=mailto:<report-address>
```

Host is `_dmarc`. After a few weeks of monitoring with no issues, tighten to `p=quarantine` then `p=reject`.

For Weblyfe client domains, use `rua=mailto:info@<client-domain>` unless they have a dedicated DMARC parser.

## Verification

After adding records, verify with `dig` (see references/dns-checks.md). A passing set has:
- SPF TXT record at root domain
- DKIM TXT record at `<selector>._domainkey.<domain>`
- DMARC TXT record at `_dmarc.<domain>`

All three must be present for full authentication. Mail sent with SPF+DKIM+DMARC passing virtually never lands in spam.

## Pitfalls

- **Two SPF records**: a domain must have exactly one SPF TXT record. Merge, don't add a second.
- **Wrong DKIM selector**: Namecheap uses `privateemail`, Google Workspace uses `google`. Guessing `default` gives a false negative.
- **Adding records to the wrong DNS panel**: if nameservers point to Cloudflare/DigitalOcean, Namecheap's Advanced DNS panel is ignored. Always confirm with `dig NS <domain> +short`.