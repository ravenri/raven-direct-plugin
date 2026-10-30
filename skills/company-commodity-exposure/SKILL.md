---
name: "company-commodity-exposure"
description: "Assesses a deal's commodity and input-cost exposure from Raven's other_risk_factors vault tile — the Commodity / Input Cost deep section: the headline, the credit synthesis, and the demand-side energy exposure, cost-side inputs and supply chain (with a supplier / spend-concentration table where present), and pass-through blocks. Commodity only — never currency / FX, which is a separate read. Faithful stored-read: renders the tile's headline, synthesis, narratives, and table, dated and sourced, with the read brought back to the borrower as a credit point; never recomputes or invents a figure. Pulls the full tile (section-scoping does not work) and extracts the Commodity section, ignoring the risk-factor cards and the Cyclicality section (its own skill, same tile). Mandatory silent second read and final review. Where commodity exposure is minimal, says so rather than filling in. Word or chat. Use for \"commodity exposure,\" \"input-cost risk,\" \"raw-material exposure,\" or \"pass-through.\""
when_to_use: "Use for \"commodity exposure,\" \"input-cost risk,\" \"raw-material exposure,\" or \"pass-through.\" Do not use for currency exposure (FX Exposure), cyclicality, or the full supplier read (Suppliers & Supply Chain)."
---

# Commodity Exposure

Produces the read on the borrower's exposure to commodity and input-cost risk: how much of the cost base
is exposed, whether input inflation gets passed through, and what residual risk to margin and liquidity
that leaves. A focused single-topic read.

**Commodity only.** Do not discuss currency or FX exposure anywhere in this read, even where the source
surfaces FX-adjacent content (a foreign-currency hedging program, translation risk). FX is a separate
read. The one FX-adjacent point that stays is a plain "no commodity hedging is disclosed," rendered as a
commodity finding, not an FX one.

**Commodity exposure has two sides, and the read covers both.** The expense side is commodity prices in the company's own input costs, and whether they pass through (the Cost-side inputs & supply chain and Pass-through blocks). The revenue side is commodity- or energy-linked end-market demand, where a commodity move changes what customers buy (the Demand-side energy exposure block). The tile renders both and the skill mirrors both. Where the tile is thin on one side, say so as a gap; do not present a one-sided read as a complete one.

**This is a stored-read, not an analysis pass.** Raven's Other Risk Factors analysis has already
synthesized the commodity read. This skill renders it in the house voice and never recomputes, re-scores,
or invents a headline, figure, or table cell.

**Two sources, two jobs. Built to the workbook prompt; data from the dashboard and vault.** The Commodity Risk prompt (workbook 1301) is the spec: it defines the structure and the coverage this read must have. The `other_risk_factors` dashboard tile and the vault supply the figures to populate it. Read the tile (extract only the Commodity / Input Cost deep section; ignore the risk-factor Cards and the Cyclicality deep section, which is its own skill off the same tile) and the vault behind it. Where the tile is thin or lags the workbook version, render 1301's structure and flag the missing piece as a gap; do not shrink the read to whatever a weak tile happens to emit.

## Tone and rules

Also apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a specific source field or note; where a tile disagrees with the vault, the vault governs and the conflict is reported, never silently resolved; a tile's own internal inconsistency is evidence against that tile, not a tiebreaker.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives, banned-word list, bold key figures, no platform plumbing). The tile's synthesis is already the borrower read; render it faithfully, rewritten to the standard (`references/language-standard.md`), keeping the substance and figures. Do not layer a second synthesis on top or re-derive the read.

**The Credit Synthesis field is where the tile writes loosest, and passing it through is the trap.** It arrives in characterizing, metaphorical prose (seen live: "the impairment path is a sharp move in metals, freight, or component costs that reaches the plants before customer recovery catches up"). Rewrite that into a plain declarative that leads with the mechanism and the figure ("the trigger is input-cost inflation in metals, freight, or components that hits cost of sales before the negotiated OEM price recovery, which lags"). Never render the synthesis field verbatim.


**Self-check the AI-speak tells before delivering. These keep slipping through:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period. This is a find, not a read.
- Do not pass the tile's synthesis or narrative prose through verbatim; it is written loose. Rewrite to a plain declarative that leads with the mechanism and the figure.
- Headings name content, never function. "The read," "Overview," "Assessment," "The take" are defects.
- No verdict-then-hedge ("manageable but relevant," "sound, but only if Y"). State the finding, then the constraint as its own sentence.
- No X-not-Y and no hype ("well-positioned," "poised to," "robust," "compelling," "sharp move"). Lead with the fact.
- A finding is a statement carrying a figure, not a question and not a characterization where a number exists.
## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, if the user named a deal, `deal_list` to resolve. One match → use it. More than one →
  present as a table (Deal, Company, Sponsor, Status, Created — no internal IDs) and ask. Do not guess.
- If no deal is named, ask which deal first.

**Skip-if-known (strict):** if `analysis_get_status` or `dashboard_get(other_risk_factors)` is already
available from earlier in this conversation (e.g. a Cyclicality run — same tile), reuse it, do not re-call.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, suggest retrying or `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`dashboard_get` is deferred; if not loaded this conversation, `tool_search` it first. The second read uses
`research_search_documents_by_type` and `get_source_page` — load those when you reach them.

## Retrieve

`dashboard_get(project_id, tile="other_risk_factors")` — a single full-tile call. Section-scoping does not
work for this tile (both `commodity` and `cyclicality` return empty placeholders), so always pull the full
tile and extract the **Commodity / Input Cost** deep section client-side. Read the data-confidence level
and generated date first.

If the Commodity / Input Cost section is missing or sparse for the deal — a business with genuinely
minimal commodity exposure, or a tile that does not cover the angle — say so plainly. Do not fill in from
another section or fall back to a vault search.

## Render — built to workbook prompt 1301, figures from the dashboard and vault

1301 is the structure-and-coverage spec. Render it in this order, pulling the figures from the tile and
vault. Where a field is not in the tile, source it from the vault or mark it a gap; never omit a spec
element because the tile was thin. Rewrite all prose to `references/language-standard.md`.

**Header:** **Commodity Exposure — [Deal Name]**, with a meta line (company, sponsor, data-confidence
level).

**Structured fields** (a short header strip):
- Applicable: Yes / No
- Sized magnitude: $ and % of anchor EBITDA, or "not quantified"
- Exposure type: deterministic cash drain / contingent or acceleration risk / not material

**1. Net input-cost exposure (expense side).** Lead with the residual, not the gross input list: the key
commodity / input exposures and their share of cost of sales, then the margin effect of an adverse move
AFTER realistic pass-through. The credit point is the residual once pass-through is accounted for.

**2. Demand-side exposure (revenue side).** Where an end-market's demand is commodity- or energy-linked,
size it ($ and % of revenue) and state the price-to-demand mechanism. Reference the Cyclicality read for
the energy-demand story rather than repeat it.

**3. The trigger and credit synthesis.** The specific price or supply event that materially impairs
EBITDA, its approximate magnitude, and the net exposure after pass-through and any hedging. Conclude with
how it nets for coverage, and name what is not quantified.

**Residual sized-exposure table** — one row per sized exposure: the exposure, whether it is an input or an
end-market, its $ or % of cost of sales or revenue, and the net-of-pass-through effect. Every number is a
real disclosed value; do not render an all-empty table, state the gap instead.

Both sides always appear: the expense side (own input costs and pass-through) and the revenue side
(commodity- or energy-linked demand). Where the tile carries only one, render it and flag the other as a
gap. Every sized figure carries its source and period. Close with the tile's `web_url` as a single
"🔗 Open in Raven" link.

## Second read (mandatory, INTERNAL — a separate pass after the full render, never shown)

Silent, findings woven in as substance. After the render:
1. **Verify the sized figures against the documents** — the cost base and cost-of-sales percentage, any
   disruption drag, the energy-linked revenue — via `research_search_documents_by_type` or
   `get_source_page` on a cited leaf. A tile figure is a claim to verify.
2. **Confirm the pass-through characterization** against the source: historical practice vs. a contractual
   escalator is the crux, and the tile's own wording should support it.
3. **Confirm the diligence gaps** the tile lists are genuinely absent from the documents, not just missing
   from this section.
Findings weave in: a corrected figure appears in place, a confirmed gap strengthens the read. No process
block, no "verified against filings" language. The test that it ran is a changed, more accurate artifact.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled read)

Read the finished piece once more and fix: **tone** (findings not directives; no X-not-Y, no verdict-then-
hedge, credit-desk register); **coherence** (headline, the read, and the blocks tell one story);
**consistency** (a figure matches everywhere); **commodity-only** (no FX content slipped in); **headings**
(every heading names the CONTENT, never the analytical function — no "The read," "The take," "Overview,"
"Assessment," or other meta labels; a heading describing what a paragraph IS rather than what it SAYS is a
defect; the opening synthesis carries no heading at all); and a **literal proofread** (read every heading
and figure as text, not just layout). Then scan literally for the em-dash character (the long dash): language-standard bans it, so replace every one with a comma, semicolon, or period. This is a character search, not a judgment; a prose proofread keeps missing it, so run it as a find, not a read. Silent; its only evidence is a cleaner read.

## Rules

- Commodity only. No FX or currency content in any section.
- Cover both sides: the expense side (own input costs and pass-through) and the revenue side (commodity- or
  energy-linked end-market demand). Where the tile is thin on one side, flag the gap rather than present a
  one-sided read as complete.
- Faithful stored-read. Never compute, re-score, or invent a headline, figure, or table cell. "Not
  disclosed" renders as such.
- Build to workbook prompt 1301's structure (structured fields, net-input-cost-exposure-first, demand-
  side, trigger and synthesis, residual sized-exposure table). Pull figures from the dashboard tile and
  vault. Where the tile is thin or lags the workbook, render the spec and flag the gap; do not shrink to
  the weak tile. Do not invent figures; rewrite prose to `language-standard.md`.
- Every sized figure carries its source and period; render the supplier table's "Not disclosed" cells
  plainly.
- Where commodity exposure is genuinely minimal or uncovered, say so; never fill in from another section.
- Second read and final review are mandatory, separate, and SILENT.
- Scope: commodity / input-cost. Cyclicality is its own skill (same tile); FX is a separate read.

## Delivery

A focused read, so chat is the default. Offer a Word document when a shareable deliverable is wanted
(docx skill, Arial, navy headers, US Letter; validate-and-render before delivering). After delivering,
offer one next step: the source page behind a figure, the Cyclicality read off the same tile, or a Word
export.
