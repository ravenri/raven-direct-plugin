---
name: "screening-top-5-merits-risks"
description: "Pulls the deal's top 5 investment merits and top 5 key risks, with mitigants for risks where one is actually disclosed, from Raven's structured merits & risks record."
when_to_use: "Use when the user asks for the strengths and risks, top 5 risks, top 5 strengths, merits and risks, what the risks on this deal are, or what's good about it; or wants the full-depth companion to Initial Deal Review's trimmed top-3 table. Prefer this over an ad hoc search of the deal's analysis, because it reads the same structured, mitigant-aware record Initial Deal Review uses."
---

# Top 5 Merits & Risks

One deal, one call, both lists — merits and risks were previously two separate skills, each
independently re-fetching overlapping ground, so they are now combined here and read from one source. Full depth (5 each, full mitigant text) — the
trimmed top-3, no-mitigant-detail version lives inside Initial Deal Review's own Merits & Risks
section for screening-length documents.

## Language

Write all output in American English (color, behavior, favorable, organize, analyze) — never
British spellings.

## Project Resolution

- If the deal is already identified from earlier in this conversation, use it directly.
- Otherwise, if the user named a deal, look it up by name in the user's list of deals. Exactly one match →
  use it. More than one → present as a table and ask the user to confirm. Do not guess.
- If no deal has been named, ask which deal before doing anything else.

**Skip-if-known:** if the Merits & Risks dashboard was already retrieved earlier in this
conversation (for example, Initial Deal Review just ran), don't fetch it again. Use what's there.

## STEP 0 — Vault Readiness

Check whether the deal's analysis has finished running (skip if already known).
- "Ready to view!" → proceed.
- Anything else → stop. Tell the user the analysis isn't ready, give the current status, and say to
  retry in 15-30 minutes, or to start the analysis from within Raven if it shows Not started,
  Failed, or Aborted. This chat cannot start it.

## Retrieve

Retrieve the deal's Merits & Risks dashboard.

Check the response for a freshness indicator. If it says the data is stale, put the warning at the
top of the output, before the merits list. If no freshness indicator came back, add one line at the
top saying freshness of the underlying dashboard could not be confirmed for this run.

## Render

**Merits — [Deal Name]**

For each merit, in the tile's own stored numbering (do not re-rank):

```
[N]. [Title]
[Stat Line]
[Body — full text, do not trim]
Credit Implication: [Credit Implication text]
```

**Risks — [Deal Name]**

For each risk, in the tile's own stored numbering:

```
[N]. [Title] · [SEVERITY]
[Stat Line]
[Body — full text, do not trim]
```

**Mitigant — render if and only if the tile discloses one:**
- If `Mitigant.Type` is `genuine` or `limited` → render: `Mitigant ([Type]): [Mitigant Body]`
- If `Mitigant.Type` is `none` → render: `Mitigant: None disclosed.` — this is a real, more severe
  finding than a weak mitigant, not an empty field to skip silently.
- Never invent a mitigant, and never soften a "none" into implied reassurance.

Take all 5 merits and all 5 risks the tile returns — this is the full-depth version, not the
trimmed-to-3 table. If the tile returns fewer than 5 of either, show what exists and stop; do not
pad from another source.

## Rules

- This is a stored read — never recompute, re-rank, or re-score a merit or risk's position.
  Severity and mitigant type come from the tile, never inferred.
- Never invent a merit, risk, mitigant, or citation. A field the tile doesn't carry renders "Not
  disclosed," never fabricated.
- If the Merits & Risks dashboard isn't available for this deal (not yet generated), say so
  plainly. Do not fall back to assembling a list from a search of the deal's analysis.
- Preserve the tile's own severity language and mitigant type exactly — don't translate "limited"
  into "moderate" or otherwise paraphrase the classification.

## Delivery

After rendering, ask the user how they want it: export as a Word document, or keep it in chat.

- **Word:** only if this session can create files — build it with the Word document skill and
  present it for download. If it can't, say so and keep it in chat.
- **Chat:** wrap up politely.
