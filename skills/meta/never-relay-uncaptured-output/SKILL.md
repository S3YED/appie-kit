---
name: never-relay-uncaptured-output
description: Guard-rail against fabricating or relaying command output, URLs, tokens, deploy status, or API data that was not literally captured from a real tool call in this session. Born from a recurring fabrication loop (2026-05-30) where a session claimed successful Vercel deploys and Brevo API responses without real tool output. Use whenever you are about to relay a result to the user or report a task as complete.
---

# Never Relay Uncaptured Output

## The Rule

Do NOT relay to the user:
- A URL, path, or token you did not receive from a real tool call this session
- A deploy status ("live", "succeeded") unless the deploy tool returned it
- An API response (Brevo subscribers, Stripe buyers, send confirmations) unless you have the raw stdout/JSON in context
- A file's content unless you Read it this session
- A command's output unless you ran the command this session and have its stdout

## The Pattern That Triggers This

You ran a command. The output looks like what you expected. You relay it to the user. But:
- The tool returned cached/stale output
- The Bash tool silently reused a prior result
- You inferred the output from prior context

This is fabrication even if unintentional. The user acts on your relay as ground truth.

## How to Apply

Before saying "deploy succeeded", "email sent", "file is at X", or "the list has N subscribers":

1. Locate the exact tool result in this session's context that proves it.
2. If you cannot point to a specific tool output line, you do not have it. Say what you attempted, say you cannot confirm the result, and offer to retry.
3. If a command returned unexpectedly empty output or a frozen timestamp, flag it as a potential tool reliability issue rather than treating silence as success.

## Retraction Protocol

If you already claimed a result you cannot back with real output:
1. Immediately send a correction: "I cannot confirm that — I don't have real tool output for it."
2. Do NOT re-send the original claim after the correction (this happened in the 2026-05-30 incident).
3. Log the retraction in daily notes.

## Related

- `superpowers:verification-before-completion` — run before marking any task complete
- Memory: feedback_never_fabricate_command_output.md
