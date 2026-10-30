---
name: "screening-credit-assessment"
description: "Renders a deal's Credit Assessment as a screening-depth read covering the rating and composite scorecard, the preliminary recommendation up top, the eight scored lenses at three to four sentences each with every figure kept, the key-metrics-to-watch lines, and the other-matters deep dives (deal context, rate/FX, risk factors), sourced from Raven's credit_assessment tile. This is the analyst's own rating read that becomes an input to IC, not the full-length assessment. Keeps the tile's own ratings, composite, and recommendation exactly as stated (never re-scores) but tightens the lens narratives rather than reproducing every paragraph. Adds a silent analyst scan surfaced as Analyst Notes, building on the tile's own Coherence Notes."
when_to_use: "Use when the user asks for the credit assessment, credit score, the rating on this deal, the scorecard, the recommendation, or a rated screening read of a deal. Do not use it when the user wants the full-length assessment with every lens narrative reproduced; say the full memo covers that."
---

# Credit Assessment (Screening)

Renders Raven's Credit Assessment tile as a screening-depth read: the rating and scorecard, the
preliminary recommendation up top, the lenses tightened to three to four sentences each, key metrics to
watch, and the other-matters deep dives — plus a silent analyst scan surfaced as Analyst Notes.

This is the analyst's own rating read on a deal, the kind of thing that becomes an **input to IC**,
not the IC-facing document itself. The `credit_assessment` tile is large and already well-built —
it carries a real 1-4 scorecard, a governing rationale, eight scored lenses, a metrics-to-watch
lens, other-matters deep dives, and its own coherence check. The skill's job is to render that
faithfully but at screening length: keep the tile's own verdicts, tighten its prose.

## Scope

Screening depth. This is a rated first read to inform whether to pursue and what to dig into, not
the full-length assessment (the full memo reproduces every lens narrative in full). The distinction
is length and audience, not substance: same assessment, tightened here, reproduced whole in the memo.
The lens narratives are tightened to three to four sentences each rather than reproduced in full.
When the request is for the full-length assessment with every lens narrative reproduced, say that the
full memo covers that and that this skill renders the screening-depth version.

## Language

All output conforms to `references/language-standard.md` (American spelling, credit-desk register,
quantify rather than characterize, no em-dashes, no hype adjectives, house banned-word list). Read
it and apply it; do not restate its rules here. Do not expose platform plumbing (no "the tile,"
"the vault," prompt IDs) — present a rating as the rating, a finding as a finding.

Lens narratives run three to four sentences. The language standard's one-to-three-sentence limit
applies to the other narrative fields.

**This applies to the tile's own prose too, which is the easy trap.** The tile's narrative fields
are frequently written in exactly the register the standard bans — sell-side, inflated, or
hollow. Passing them through verbatim imports that language. Specific phrasings seen live on this
tile that must be rewritten, never rendered as-is: "the credit is sound," "the loan is likely
repaid as structured," "supported by," "reinforced by," "translates to," "gives the revenue base
more durability than," "indicates a business with real competitive position." Rewrite each into a
plain declarative that leads with the fact. The verdict the sentence carries is the tile's; the
words are not.

## Project Resolution

- If the deal is already identified from earlier in this conversation, use it directly.
- Otherwise, if the user named a deal, look it up by name in the user's list of deals. Exactly one match →
  use it. More than one → present as a table and ask the user to confirm. Do not guess.
- If no deal has been named, ask which deal before doing anything else.

**Skip-if-known (strict):** if the analysis status or the Credit Assessment dashboard was already
retrieved earlier in this conversation, do not fetch it again.

## STEP 0 — Analysis Readiness

Check whether the deal's analysis has finished running (skip if already known). "Ready to view!" →
proceed. Anything else → stop, report the status, and say to retry once the analysis completes, or
to start the analysis from within Raven if it shows Not started, Failed, or Aborted. This chat
cannot start it.

## Retrieve

Retrieve the deal's Credit Assessment dashboard in a single call. It does not support
section-scoping; it is always one full call. It returns the scorecard (composite,
band, per-lens scores + drivers), the Call block (rating, repayment read, summary, governing
conditions, preliminary screening view), the lenses (each with rating, narrative, and any blocks),
the key-metrics-to-watch lens, a Coherence Notes field, and Other Matters (deal context, rate/FX,
other risk factors). Read all of it — the condensation happens in the render, not the retrieval.

If the Credit Assessment dashboard is not available for this deal (not yet generated), say so
plainly. Do not assemble an assessment from searches of the deal's analysis.

## STEP 0.5 — Staleness (after Retrieve)

Check the response for a freshness indicator. This is confirmed inconsistent across deals; some
carry it and some don't. If it is present and says the data is stale, surface it as the first
Analyst Note. If it is absent, do not assume either way.

## Render — screening depth: keep the verdicts, rewrite the prose

Render in this order. **Two different disciplines apply, and conflating them is the main failure
mode of this skill:**

- **Verdicts, scores, and numbers — keep exactly as the tile states them.** The rating word, the
  composite, each lens score, the Proceed/Conditional/Pass view, every figure. Never re-score,
  re-derive, or adjust a verdict.
- **All prose — rewrite it to the language standard. Never pass tile prose through verbatim.** The
  tile's own narrative is often loose, sell-side, or AI-inflected ("the credit is sound," "likely
  repaid as structured," "supported by," "translates to"). That phrasing violates
  `references/language-standard.md`. Rewriting the prose to credit-desk register is not optional and
  is not re-scoring — the decision and the numbers are the tile's; the sentences are yours, and they
  must be clean. Lead with the figure, state the position, name the risk, cut the filler. If a
  sentence would embarrass a credit analyst to have written, rewrite it.

This is the resolution of "summarize but never re-score": summarize and rewrite the prose freely;
keep the verdict values fixed.

**[Deal Name] · Credit Assessment**

**Recommendation** — up top, as the headline, before anything else. Render the tile's Preliminary
Screening View: the tranche and the view (Proceed / Proceed Conditional / Pass — kept exactly), with
its Basis **rewritten to the language standard** (not lifted from the tile's Summary or Repayment
Read fields). Lead with the leverage/coverage figures and name what repayment actually turns on. Do
not open with "the credit is sound," "the loan is likely repaid," or any variant — banned. **Do not
render the tile's "Governing Conditions" field — it is internal scaffolding, not reader-facing
output** (like Feeding Lens, Source Labels, and the run IDs). Use the tile's own field names for the
fields that ARE rendered; never invent a friendlier label for one.

**Scorecard** — the composite and the eight (or however many) scored lenses, as a table. This is
the part that "lays it out well," so render it cleanly and completely:

| Lens | Rating | Score | Driver |
|---|---|---|---|

One row per lens, the tile's own rating word and score, and its one-line driver (already short;
keep it close to the tile's wording, but remove em-dashes and any banned phrasing). Put the
composite and band on one line directly above the table (for example, "Composite 3.25 / 4 · Above
Average"), then the table. The composite and band appear only there.

**Lenses** — render each lens close to the tile's own length, cleaned up rather than compressed.
Keep all the specific figures, the main support, and the binding constraint, roughly 3-4 sentences
per lens, trimming only genuine redundancy and sell-side padding, not real content. Each lens's
rating and score sit in the Scorecard table; do not restate the rating word in the lens prose.
This is a screening read so it is tighter than the full IC narrative, but the tile's lenses carry
specific figures (revenue splits, margin levels, concentration percentages, tenure) that are the
substance of the assessment — do not strip them to a two-sentence gist. The job is to clean the
prose and cut padding, not to gut the content. **Keep any block that carries real figures** — the
forecast credit-stats trajectory, the quality-forward metrics, the recovery grid — as compact
tables. Rewrite prose to the language standard; keep the figures and the verdict.

**Key Metrics to Watch** — the metrics-to-watch lens, as a short list: each scored line, its rating
if it has one, and a one-line read. This is what to track post-close, so keep it tight but complete.

**Other Matters** — condense each to its essential point:
- **Deal Context** — 1-2 sentences on the transaction (structure, what's being acquired, any
  defining feature like a carve-out).
- **Rate / FX** — the exposure and the execution question, condensed; keep the quantified
  calibration points (interest sensitivity, non-USD revenue share) since those are the substance.
- **Other Risk Factors** — each named factor as a one-line read, not its full body.

**Analyst Notes** — the silent scan (below), in the house vocabulary. Comes last.

## The silent analyst scan — tidy up, build on the tile's own coherence check

After rendering, silently read across the whole assessment the way an analyst would before passing
it to IC. **Never label or narrate this scan — only its output appears, as Analyst Notes.** Use the
house vocabulary shared with the Raven-powered memo and deal-terms: **Analyst Note** (an internal
inconsistency or a figure that needs reconciling), **Key Credit Concern** (a fact that materially
governs the credit), **Counterargument** (a point cutting against Raven's own framing), **Diligence
Item** (an open question to resolve). In Analyst Notes, refer to "Raven's analysis," never "the tile." Look for:

1. **Staleness** — from STEP 0.5, if present.
2. **The tile's own Coherence Notes.** This tile generates its own coherence check (e.g. flagging
   that the EBITDA bridge shows a seam — one source deriving PF EBITDA differently than another).
   **Do not duplicate it verbatim and do not ignore it** — elevate what it flags into a plain-language
   Analyst Note or Key Credit Concern, since a coherence seam in the EBITDA basis directly affects
   the leverage denominator the whole assessment is struck on. Then look for what the tile's own
   check missed.
3. **A rating that sits oddly against its own narrative.** If a lens's narrative reads more negative
   (or more positive) than the score it carries, flag it as an Analyst Note — not to re-score it
   (the score stays the tile's), but so the reader knows to look.
4. **A recommendation that leans on something unresolved.** If the Proceed view depends on a
   governing condition that is itself a real risk (an unrealized synergy number embedded in the
   EBITDA basis, an execution plan not yet evidenced), name it as a Key Credit Concern — the
   recommendation is only as good as its binding assumption.
5. **A stress the tile admits it didn't model.** Recovery grids and forecasts often flag a case not
   run (an EBITDA-down stress, an un-modeled downside). Surface it as a Diligence Item.

Include a note only when it is real. A genuinely clean assessment can produce few notes; do not
manufacture concerns to fill the section. If nothing flags, omit the Analyst Notes section.

Close with a single "🔗 Open in Raven" link if the assessment carries one, plus a one-line footnote
giving the date it was generated, so the reader knows how current the assessment is. Omit either if
it isn't present; never construct them.

## Rules

- Keep the tile's ratings, composite, scores, and recommendation exactly as stated — never
  re-score, re-derive, or adjust a verdict.
- Rewrite ALL prose to the language standard — never pass tile narrative through verbatim. The
  tile's own language is often loose/sell-side/AI-inflected; cleaning it is mandatory, not optional,
  and is not the same as re-scoring. Keep the numbers and the verdict; rewrite the sentences.
- Governing Conditions and Coherence Notes are read silently as inputs to the analyst scan but not
  rendered as their own blocks. Do not render other internal fields either: Feeding Lens, Source
  Labels, Source Run ID, State.
- Use the tile's own field names verbatim for fields rendered under their own name: Preliminary
  Screening View, Key Metrics to Watch, and so on. The Recommendation heading is the one exception;
  it carries the Preliminary Screening View. Never invent a friendlier label ("depends on") for any
  other field the tile names. Renaming a field is a form of making things up.
- Never open the recommendation (or any section) with "the credit is sound," "the loan is likely
  repaid," "supported by," or similar — lead with the figure and the position.
- Recommendation goes up top, as the headline.
- Render lenses close to the tile's own length — clean the prose and cut padding, keep all the
  figures, the support, and the constraint (~3-4 sentences each). Do not compress to a two-sentence
  gist; that strips real content. Preserve every figure-carrying block (leverage trajectory,
  recovery grid, quality metrics) as a compact table.
- The analyst scan is silent — never render a "scan" or "second review" heading. Only Analyst Notes
  appear, in the house vocabulary.
- Build on the tile's own Coherence Notes rather than duplicating or ignoring them.
- This is screening depth — a rated read to inform IC, tighter than the full-length
  assessment, but not stripped to a gist.
- Zero Analyst Notes on a clean assessment is valid; do not invent concerns.

## Delivery

Render in chat by default. Only produce a document if asked. After rendering, offer one natural
next step: the source page behind a specific figure, the full memo, or a Word export. A Word export
is only possible if this session can create files; if it can't, say so and keep it in chat.
