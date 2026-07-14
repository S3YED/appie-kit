# Namecheap JFE030050 Error

## The Misleading Bounce

When Namecheap Private Email receives mail from a domain with no SPF record,
it returns:

```
554 5.1.1 <recipient@domain.com>: Recipient address rejected: undeliverable
address: Mailbox might be disabled, full, or may not exist on the server.
Reason: JFE030050
```

This SAYS "address not found" but the real problem is:
→ The SENDING domain has no SPF record.

## How We Diagnosed This (thrivingrose.com case)

1. **Seyed@weblyfe.nl → info@thrivingrose.com**: Bounced with JFE030050
2. **weblyfenl@gmail.com → info@thrivingrose.com**: Arrived fine
3. **DNS check on weblyfe.nl**: NO SPF record at all (MX on smtp.google.com)
4. **Added SPF**: `v=spf1 include:_spf.google.com ~all`
5. **Verified fix**: Mail delivered after SPF propagation

## Key Insight

Namecheap Private Email treats NO-SPF domains as untrusted and rejects with
a misleading "address not found" error. The mailbox DOES exist. The problem
is the SENDER's authentication, not the RECIPIENT's mailbox.

## Fix Checklist

1. Check SPF on SENDING domain: `dig DOMAIN TXT +short | grep spf`
2. If missing: add `v=spf1 include:_spf.google.com ~all` (Google Workspace)
   or `v=spf1 include:spf.privateemail.com ~all` (Namecheap Private Email)
3. Wait 1-2 hours for DNS propagation
4. Test again