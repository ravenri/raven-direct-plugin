---
name: "screening-diligence-focus-areas"
description: "Produces a ranked, up-to-10-item list of the most important credit questions to resolve before a deal can be underwritten with conviction, each with a one-sentence credit mechanism and 2-3 specific investigative actions (the document, call, or model run needed to close it). This is not a trimmed version of Diligence Gaps; it draws on both Diligence Gaps' HIGH-priority items and the deal's Merits & Risks record."
when_to_use: "Use when the user asks what to focus on, what the key open questions are, what they need to run down before IC, or wants a prioritized action list rather than a full gaps register. Do not use it for the complete list of every open gap; that is the Diligence Gaps skill."
---

# Diligence Focus Areas

Pulls the Diligence Focus Areas synthesis's already-computed, ranked list directly, combining the
HIGH-priority items from the Diligence Gaps register with the risk cards from the Merits & Risks
record into one prioritized action list.

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

Search the diligence summary analysis for "diligence focus areas key credit questions before
underwriting" (top 5 results).

This search can return both the Open Data Gaps register and the Diligence Focus Areas synthesis,
since both live under the same vault category. **Identify the focus areas content by its structured
header** — it starts with `Focus Area Count: [n]`, distinct from the gaps register's
`Gaps Identified:` header. Use only the focus areas content for this skill.

If no focus areas content is found (synthesis not yet generated for this deal), say so plainly — do
not assemble a substitute list from Diligence Gaps or Merits & Risks directly. Those are the
synthesis's own inputs, not a fallback path for this skill to re-derive the same list itself.

## Render

**[Deal Name] — Diligence Focus Areas**

Numbered list, in the synthesis's own stored rank order — do not re-rank:

```
[N]. [Focus Area] · [Category]
[Credit Mechanism — one sentence, verdict-first, no hedging]
Investigative Actions:
- [action 1]
- [action 2]
- [action 3, if present]
```

At the end, from the synthesis's own structured fields:

```
Focus Area Count: [n]
Company or Industry Items: [n]
Source Mix: [n from Merits & Risks] | [n from Diligence Gaps HIGH-priority items]
```

## Rules

- This is a stored read of the synthesis's own output — never re-derive, re-rank, or invent a focus area.
- Up to 10 items, evidence-determined. A short list (fewer than 10) where the evidence only
  supports a few is correct — never pad toward a target count.
- Each item makes a distinct claim. If two items in the source content overlap, that's a source
  issue to flag, not something to silently merge or dedupe here.
- The Credit Mechanism line stays verdict-first and specific — reproduce it from the source rather
  than softening it into hedged language.
- Never invent an investigative action not present in the source content.

## Delivery

After rendering, ask the user how they want it: export as a Word document, or keep it in chat.

- **Word:** only if this session can create files — build it with the Word document skill and
  present it for download. If it can't, say so and keep it in chat.
- **Chat:** wrap up politely.
