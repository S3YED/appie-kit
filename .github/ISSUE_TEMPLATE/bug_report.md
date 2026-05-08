---
name: Bug report
about: Something is broken or behaving unexpectedly
title: "[BUG] "
labels: bug
assignees: ''
---

## Environment

- OS: (e.g., macOS 14, Ubuntu 22.04)
- Agent runtime: (Hermes Agent / OpenClaw)
- Agent version: (`hermes --version` or `openclaw --version`)
- Node.js version: (`node -v`)
- Python version: (`python3 --version`)
- Kit version / commit: (`git rev-parse --short HEAD`)

## Steps to reproduce

1. ...
2. ...
3. ...

## Expected behavior

What should have happened.

## Actual behavior

What actually happened. Include error messages verbatim.

## Logs

Paste relevant log output (sanitize API keys first):

```
paste logs here
```

Run `tools/health-check.sh` and include the output.
Run `tools/security-scan.sh` before pasting to verify no keys are exposed.

## Additional context

Any other information that might be relevant.
