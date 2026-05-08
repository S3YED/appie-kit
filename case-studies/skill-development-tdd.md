# Case Study: Writing and Testing a New Skill

How to take an idea for a new agent behavior, build it as a proper skill, test it, and optionally share it back to the kit.

---

## What is a Skill?

A skill is a folder containing at minimum one file: `SKILL.md`. This file tells the agent what behavior to exhibit in a specific context. It is loaded into the agent's context when the skill is active.

Skills are not code plugins. They are structured prompts with metadata. The `SKILL.md` frontmatter declares the skill's identity; the body is the instruction set.

The simplest possible skill:

```
skills/my-skill/
 SKILL.md
```

More complete skills include supporting scripts, config examples, and tests:

```
skills/my-skill/
 SKILL.md
 scripts/
 main.py
 tests/
 test_main.py
 examples/
 example-output.md
```

---

## The SKILL.md Spec

Every SKILL.md starts with YAML frontmatter (the block between `---` markers):

```yaml
---
name: skill-name # machine-readable, hyphen-case, no spaces
description: > # what this skill does; 1-2 sentences max
 One or two sentences describing when the agent should use this skill.
version: 1.0.0 # semantic versioning
author: your-name # optional
license: MIT # default for public skills
prerequisites:
 env_vars: [API_KEY_NAME] # required env vars (names only, not values)
 commands: [curl, python3] # required CLI tools
 python_packages: [] # optional Python dependencies
metadata:
 hermes:
 tags: [Category, Tag]
---
```

After the frontmatter comes the body, the actual prompt content the agent reads. Keep it focused: what the skill does, how to use it, pitfalls to avoid, and examples.

---

## Example: Building a "Stripe Revenue Check" Skill

This example walks through building a skill that lets the agent check Stripe monthly revenue on demand.

### Step 1: Define what the skill does

Before writing anything, answer three questions:

1. What task does this skill help with?
 - "Check current month's Stripe gross revenue and MRR"

2. When should the agent use it?
 - "When the user asks about revenue, sales numbers, or monthly performance"

3. What does it need to work?
 - Stripe API key (`STRIPE_SECRET_KEY`)
 - `curl` or the Stripe Python SDK

### Step 2: Write the test first

Create a test that verifies the skill's supporting script returns correct output before writing the script:

```python
# skills/integrations/stripe-revenue/tests/test_revenue.py
import subprocess
import json
import os

def test_revenue_check_returns_valid_structure():
 """Script should return JSON with gross_revenue and mrr fields."""
 result = subprocess.run(
 ["python3", "scripts/revenue.py", "--month", "current"],
 capture_output=True, text=True, env={**os.environ}
 )
 assert result.returncode == 0, f"Script failed: {result.stderr}"
 
 data = json.loads(result.stdout)
 assert "gross_revenue" in data, "Missing gross_revenue"
 assert "mrr" in data, "Missing mrr"
 assert "currency" in data, "Missing currency"
 assert isinstance(data["gross_revenue"], (int, float))

def test_revenue_check_handles_missing_key():
 """Script should exit with code 1 and message if STRIPE_SECRET_KEY missing."""
 env = {k: v for k, v in os.environ.items() if k != "STRIPE_SECRET_KEY"}
 result = subprocess.run(
 ["python3", "scripts/revenue.py"],
 capture_output=True, text=True, env=env
 )
 assert result.returncode == 1
 assert "STRIPE_SECRET_KEY" in result.stderr
```

Run the tests: they fail (RED). That's expected. Now write the implementation.

### Step 3: Write the implementation

```python
# skills/integrations/stripe-revenue/scripts/revenue.py
"""
Fetch current month gross revenue and estimated MRR from Stripe.
Requires: STRIPE_SECRET_KEY env var
"""
import json
import sys
import os
import subprocess
from datetime import datetime, timezone

def main():
 key = os.environ.get("STRIPE_SECRET_KEY")
 if not key:
 print("Error: STRIPE_SECRET_KEY not set", file=sys.stderr)
 sys.exit(1)
 
 # Get start of current month as Unix timestamp
 now = datetime.now(timezone.utc)
 month_start = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
 ts_start = int(month_start.timestamp())
 
 # Fetch charges created this month
 result = subprocess.run([
 "curl", "-s",
 "-H", f"Authorization: Bearer {key}",
 f"https://api.stripe.com/v1/charges?created[gte]={ts_start}&limit=100"
 ], capture_output=True, text=True)
 
 if result.returncode != 0:
 print(f"curl failed: {result.stderr}", file=sys.stderr)
 sys.exit(1)
 
 data = json.loads(result.stdout)
 
 if "error" in data:
 print(f"Stripe error: {data['error']['message']}", file=sys.stderr)
 sys.exit(1)
 
 charges = data.get("data", [])
 currency = charges[0]["currency"].upper() if charges else "USD"
 
 # Sum succeeded charges (amounts are in cents)
 gross = sum(
 c["amount"] for c in charges
 if c["status"] == "succeeded" and not c.get("refunded")
 ) / 100
 
 output = {
 "gross_revenue": gross,
 "mrr": gross, # rough estimate for non-subscription businesses
 "currency": currency,
 "charge_count": len([c for c in charges if c["status"] == "succeeded"]),
 "period": f"{now.strftime('%B %Y')}"
 }
 
 print(json.dumps(output, indent=2))

if __name__ == "__main__":
 main()
```

Run the tests again: `python3 -m pytest tests/`. They should pass (GREEN).

### Step 4: Write the SKILL.md

```markdown
---
name: stripe-revenue
description: >
 Check Stripe gross revenue, charge count, and estimated MRR for the current
 month. Use when asked about revenue, sales numbers, or monthly performance.
version: 1.0.0
author: your-name
license: MIT
prerequisites:
 env_vars: [STRIPE_SECRET_KEY]
 commands: [curl, python3]
---

# Stripe Revenue

Check current month's Stripe revenue on demand.

## When to use

When the user asks: "How much have we made this month?", "What's our revenue?",
"Check Stripe", or similar.

## Usage

```bash
python3 {{SKILL_DIR}}/scripts/revenue.py
```

Returns JSON:
- `gross_revenue`: total revenue in account currency
- `mrr`: rough MRR estimate (same as gross for non-subscription setups)
- `currency`: currency code (USD, EUR, etc.)
- `charge_count`: number of successful charges
- `period`: human-readable month name

## Example

```bash
$ python3 scripts/revenue.py
{
 "gross_revenue": 8450.00,
 "mrr": 8450.00,
 "currency": "EUR",
 "charge_count": 23,
 "period": "April 2026"
}
```

## Required env vars

- `STRIPE_SECRET_KEY`: found at dashboard.stripe.com/apikeys

## Notes

- Restricted keys work; need at least `charges:read` scope
- Amounts are converted from cents automatically
- For subscription MRR, use the Stripe subscriptions endpoint instead
```

### Step 5: Refactor and edge-case test

After the basic tests pass, add edge cases:

```python
def test_revenue_handles_empty_month():
 """Should return zero revenue for a month with no charges."""
 # Patch with a future month start date
 ...

def test_revenue_handles_refunded_charges():
 """Refunded charges should be excluded from gross revenue."""
 ...
```

This is the IMPROVE phase of TDD. Add edge cases, refactor for clarity, verify coverage.

---

## Folder Structure Best Practices

```
skills/integrations/stripe-revenue/
 SKILL.md # required: frontmatter + agent instructions
 scripts/
 revenue.py # supporting script(s)
 tests/
 test_revenue.py # pytest tests for scripts
 examples/
 example-output.json # optional: sample output for documentation
 README.md # optional: human-readable docs beyond SKILL.md
```

Keep files small. A skill with a 500-line Python script should be split into modules. A skill that requires 10 supporting files may be better as a mini-package.

---

## Testing Without an API Key

For skills that call external APIs, use environment variable mocking or fixture files:

```python
# tests/conftest.py
import pytest
import json
import os

@pytest.fixture(autouse=True)
def mock_stripe_response(monkeypatch, tmp_path):
 """Patch curl to return fixture data instead of hitting Stripe."""
 fixture = {
 "object": "list",
 "data": [
 {"amount": 9900, "currency": "eur", "status": "succeeded",
 "refunded": False}
 ]
 }
 fixture_file = tmp_path / "stripe_response.json"
 fixture_file.write_text(json.dumps(fixture))
 
 # Monkeypatch subprocess.run to return fixture
 original_run = __import__("subprocess").run
 def fake_run(cmd, **kwargs):
 if "api.stripe.com" in " ".join(cmd):
 class FakeResult:
 returncode = 0
 stdout = fixture_file.read_text()
 stderr = ""
 return FakeResult()
 return original_run(cmd, **kwargs)
 
 monkeypatch.setattr("subprocess.run", fake_run)
```

---

## Sharing a Skill Back

To contribute a skill to the kit:

1. Fork the repo on GitHub.
2. Add your skill folder to the appropriate category under `skills/`.
3. Verify the SKILL.md has valid frontmatter (YAML linter: `python3 -c "import yaml; yaml.safe_load(open('SKILL.md'))"`).
4. Include at least one test or example.
5. Open a PR using the skill submission template (`.github/ISSUE_TEMPLATE/skill_submission.md`).

Skills are reviewed for:
- Working frontmatter with all required fields
- Clear usage instructions
- No hardcoded secrets or personal data
- At least one concrete usage example

---

## Skill Quality Checklist

Before marking a skill done:

- [ ] Frontmatter is valid YAML with `name`, `description`, `version`
- [ ] All required env vars are listed in `prerequisites.env_vars`
- [ ] At least one usage example in the body
- [ ] No personal data, internal hostnames, or account IDs
- [ ] Supporting scripts have tests
- [ ] Edge cases covered (missing key, empty response, API error)
- [ ] File is under 400 lines (split if larger)
