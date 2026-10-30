---
name: "screening-diligence-gaps"
description: "Produces the full, structured register of every open data gap in a deal's diligence materials, organized into five fixed categories (Company, Industry, Financial, Collateral & Liquidity, Structural), each gap rated HIGH/MEDIUM/LOW with a specific diligence ask. Reads the vault's own already-computed gap register rather than re-deriving gaps from fresh searches."
when_to_use: "Use when the user asks for diligence gaps, open data gaps, what's missing, what we still need, or a completeness check before IC. Use this instead of an ad hoc search of the deal's analysis. Do not use it for a short prioritized list of what to resolve first; that is the Diligence Focus Areas skill."
---

# Diligence Gaps

Pulls the Open Data Gaps register's already-computed, structured gap list directly — this is a
compile-and-render skill, not a fresh-analysis one.

## Language

Write all output in American English (color, behavior, favorable, organize, analyze) — never
British spellings.

## Project Resolution

- If the deal is already identified from earlier in this conversation, use it directly.
- Otherwise, if the user named a deal, look it up by name in the user's list of deals. Exactly one match →
  use it. More than one → present as a table and ask the user to confirm. Do not guess.
- If no deal has been named, ask which deal before doing anything else.

## STEP 0 — Vault Readiness

Check whether the deal's analysis has finished running (skip if already known).
- "Ready to view!" → proceed.
- Anything else → stop. Tell the user the analysis isn't ready and to retry in 15-30 minutes, or to
  start the analysis from within Raven if it shows Not started, Failed, or Aborted. This chat
  cannot start it.

## Retrieve

Search the diligence summary analysis for "open data gaps missing information credit analysis"
(top 5 results).

This search can return both the Open Data Gaps register and Diligence Focus Areas content in the
same result set, since both live under the same vault category. **Identify the gaps register by its
structured header** — it starts with `Gaps Identified: [n]`, `Gaps By Priority:`, and
`Gaps By Category:` fields, distinct from the Focus Areas header `Focus Area Count:`. Use only the
gaps register content for this skill; if Focus Areas content also surfaces, ignore it here (that's
a different skill).

If no gaps register content is found (register not yet generated for this deal), say so plainly — do not
fall back to assembling gaps from a fresh, unstructured search.

## Render

**[Deal Name] — Diligence Gaps**

Header block, from the register's own structured fields — reproduce these counts exactly, don't recompute:

```
Gaps Identified: [n]
Gaps By Priority: HIGH [n] | MEDIUM [n] | LOW [n]
Gaps By Category: Company [n] | Industry [n] | Financial [n] | Collateral & Liquidity [n] | Structural [n]
Section Prompts Reporting No Gaps: [as the register states it, or "None"]
```

Then, **grouped by category in this fixed order — Company, Industry, Financial, Collateral &
Liquidity, Structural** — regardless of which categories have entries. If a category has zero
gaps, render it anyway with: *"No material gaps outstanding in this section."* An empty category
is a real finding, not something to hide by omitting the heading.

Within each category, preserve the register's own ordering — it's already ranked by credit materiality
within that category. Do not re-sort, and do not compare or rank across categories.

For each gap, one block:

```
[PRIORITY] · [Topic]
Source: [source reference exactly as the register states it]
[Description — one sentence, what's missing and why it matters]
Diligence Ask: [one sentence — the specific document, call, or model run that closes this gap]
```

## Rules

- This is a stored read of the register's own output — never re-derive, re-rank, or invent a gap.
  If the register didn't flag it, it doesn't appear here.
- Priority is exactly as the register states it — HIGH, MEDIUM, or LOW only. Never introduce another label
  (no "Material," "Critical," etc.) and never leave a gap unrated.
- Do not cap the list or drop LOW items to make the output feel tighter — this is the full-deal
  open-gaps record. If the user wants a shorter, prioritized version, that's Diligence Focus Areas,
  a different skill — point them there rather than trimming this one.
- Never invent a diligence ask that isn't in the source content.

## Delivery

After rendering, ask the user how they want it: export as a Word document, or keep it in chat.

- **Word:** only if this session can create files — build it with the Word document skill and
  present it for download. If it can't, say so and keep it in chat.
- **Chat:** wrap up politely.
