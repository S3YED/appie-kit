# DNS mail record verification commands

Run these to audit any domain's email authentication status.

## Quick audit (single domain)

```bash
echo "=== SPF ===" && dig $DOMAIN TXT +short | grep spf
echo "=== DKIM ===" && for sel in google default privateemail ncpe ncpe1; do
  result=$(dig +short $sel._domainkey.$DOMAIN TXT)
  [ -n "$result" ] && echo "$sel: found" && break
done
echo "=== DMARC ===" && dig _dmarc.$DOMAIN TXT +short
```

## Manual step-by-step

### SPF
```bash
dig <domain> TXT +short
```
Expected: `"v=spf1 include:<provider-spf> ~all"`

### DKIM
```bash
# Google Workspace
dig google._domainkey.<domain> TXT +short
# Namecheap Private Email
dig privateemail._domainkey.<domain> TXT +short
```
Expected: `"v=DKIM1; k=rsa; p=<long-base64-key>"`

### DMARC
```bash
dig _dmarc.<domain> TXT +short
```
Expected: `"v=DMARC1; p=none; rua=mailto:..."`

## Reference: weblyfe.nl (Google Workspace)

```
SPF:   v=spf1 include:_spf.google.com ~all
DKIM:  google._domainkey.weblyfe.nl (RSA key)
DMARC: v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com
```

## Reference: thrivingrose.com (Namecheap Private Email)

```
SPF:   v=spf1 include:spf.privateemail.com ~all
DKIM:  privateemail._domainkey.thrivingrose.com (RSA key)
DMARC: v=DMARC1; p=none; rua=mailto:info@thrivingrose.com
```