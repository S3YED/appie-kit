# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Appie Kit, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please use one of these private channels:

1. **GitHub Security Advisories**: https://github.com/S3YED/appie-kit/security/advisories/new (preferred)
2. **Contact form**: https://weblyfe.ai (mark the subject "SECURITY")

Please include:

- A description of the vulnerability
- Steps to reproduce
- Affected files or components
- Potential impact
- Suggested fix (if you have one)

We aim to respond within 72 hours.

## Scope

In scope:
- Hardcoded secrets in committed code
- Insecure default configurations in install scripts or templates
- Skills that expose credentials, allow command injection, or escalate privileges
- Path traversal or arbitrary file access in tools

Out of scope:
- Vulnerabilities in upstream dependencies (Hermes Agent, OpenClaw, MiniMax, etc.). Report those to the upstream project.
- Self-inflicted issues (e.g., user committed their own .env file). Do report a missing .gitignore entry.
- Social engineering of repo maintainers.

## Reporting Other People's Secrets

If you find a hardcoded API key, token, or other secret in this repo, report it via the channels above as a CRITICAL issue. Do NOT open a public PR with the redaction in the diff. Instead, ask us to coordinate the rotation, history rewrite, and force-push.

## Hardening Recommendations for Users

Before going live with your own Appie:

1. **Never commit secrets.** Use `.env.secrets` and add it to `.gitignore`.
2. **Use Tailscale or a VPN for fleet management**, never expose SSH publicly.
3. **Run `tools/security-scan.sh`** after first install to validate file permissions.
4. **Rotate API keys quarterly**, especially if your repo has ever been pushed publicly.
5. **Review `workspace/SOUL.md` and `workspace/USER.md`** for any personal information before committing them anywhere.
6. **Set file permissions correctly**: `chmod 600 .env.secrets`.
7. **Keep fleet access private**: copy `configs/fleet-access.example.yml` to `fleet-access.local.yml` and never commit the filled file.

## Disclosure Policy

After a vulnerability is reported and fixed:

1. We patch the issue.
2. We credit the reporter in the changelog (with permission).
3. We publish a security advisory describing the issue and fix.
4. We notify users via the GitHub repo and Weblyfe community channels.

Thank you for helping keep Appie Kit and its users safe.
