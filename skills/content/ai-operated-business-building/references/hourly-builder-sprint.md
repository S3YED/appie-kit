# Hourly Builder Sprint pattern

Use when Seyed asks the agent to keep building a side-income/business project continuously, e.g. “elk uur werken” or “we gaan nu een ronde doen en zoveel mogelijk afmaken”.

## Pattern

1. Create or update a recurring cron job that runs every hour with a self-contained prompt.
2. Pin the workdir to the project directory or its parent.
3. Enable only needed toolsets: `web`, `terminal`, `file`, `skills`.
4. In the prompt, require tangible file output every run. Never allow “planning only”.
5. Keep external-action guardrails explicit: no outreach, public posts, ads, contracts, or client commitments without approval.
6. Deliver short Dutch updates with:
   - what was built
   - file paths
   - next best step
   - approvals/access needed

## Immediate manual sprint mode

When Seyed says to do a “ronde” and continue as far as possible:

- Load this skill.
- Inspect the project map quickly.
- Use todo for 4-6 concrete work blocks.
- Produce assets in files, not only chat output.
- Prioritize launch assets in this order:
  1. offer/landing copy
  2. intake form
  3. sales script and objections
  4. prospect CRM batch
  5. mini-audits
  6. content calendar/posts
  7. lead magnet
  8. outreach drafts for approval
  9. approval pack

## Good cron prompt ingredients

- Business goal and offer context.
- Exact project path.
- Clear list of allowed work.
- Explicit external-action restrictions.
- “Always write or improve a file” requirement.
- Short reporting format.
- Skill attachment: `ai-operated-business-building`.

## Pitfalls

- Do not scatter into new business ideas during execution. Build the selected wedge.
- Do not spam hourly updates with vague progress. Each update needs paths and concrete output.
- Do not send external outreach just because drafts are ready. Approval first.
- Do not let cron runs fight each other. Repeat hourly, not every few minutes, and keep each run bounded.
