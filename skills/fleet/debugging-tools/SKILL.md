---
name: debugging-tools
description: "Debugging tools for development: pdb, debugpy, and Node.js inspect debugger."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, pdb, debugpy, node-inspect, cdp, breakpoints, dap]
    related_skills: [development-workflow, systematic-debugging]
---

# Debugging Tools

Debugging tools for stepping through code, inspecting state, and diagnosing runtime issues. This umbrella covers the two main ecosystems: Python and Node.js.

## When to Use Debugger Tools

| Tool | When |
|------|------|
| **`breakpoint()` + pdb** | Local, interactive, simplest. Add `breakpoint()` in source, run normally. |
| **`python -m pdb`** | Launch existing script under pdb with no source edits. |
| **`debugpy`** | Remote / headless / attach to already-running process. Talks DAP. |
| **`node inspect`** | Node.js built-in inspector. Zero install, CLI REPL. |
| **`ndb` / CDP** | Scriptable from Node/Python; automate many breakpoints across runs. |

**Start with `breakpoint()` or `node inspect`.** These are the cheapest things that work.

## Don't Use Debugger For
Things `print()` / `console.log` / `pytest -vv --tb=long` solve in under a minute. Breakpoint-driven debugging is heavier; use it when the payoff is real.

## Quick Reference: pdb
Inside any pdb prompt (`(Pdb)`):
```
n(ext)     — Execute next line
s(tep)     — Step into function
c(ontinue) — Continue until breakpoint
l(ist)     — Show source around current line
p <expr>   — Print expression value
pp <expr>  — Pretty-print expression
b <line_no> — Set breakpoint at line
```

## Quick Reference: node inspect
```
n            — Next
s            — Step into
o            — Step out
cont         — Continue
list(n)      — List source around line
repl         — Enter REPL mode to eval expressions
watch('var') — Watch expression across steps
```

## Reference Files
- **references/python-debugpy.md** — Full pdb + debugpy reference (breakpoint(), remote attach, DAP)
- **references/node-inspect-debugger.md** — Full Node.js --inspect reference (CDP, breakpoints, heap snapshots)