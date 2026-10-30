---
name: "company-cyclicality"
description: "The company-specific cyclicality read, built to workbook prompt Q636 (Earnings Cyclicality) with figures from the other_risk_factors dashboard tile and the vault: the structured fields (peak and trough Adjusted EBITDA over the most recent cycle, the peak-to-trough decline, and the downturn-resilient revenue share), plus end-market exposure by segment, the recurring-vs-cyclical mix, and historical downturn and forward visibility (drawdown, recovery pace, mechanism, current-vs-peak, contract coverage). Uses the company's own history, not its industry classification; sector cyclicality is Industry Overview (Q418), and commodity is its own skill off the same tile. Rewrites the tile's prose to the standard, never passes the synthesis field through, and flags gaps where cycle data is undisclosed. Tone-and-rules section, silent second read and final review. Word or chat. Use for \"cyclicality,\" \"earnings cyclicality,\" \"peak-to-trough,\" or \"how resilient is this credit in a downturn.\""
when_to_use: "Use for \"cyclicality,\" \"earnings cyclicality,\" \"peak to trough,\" or \"how resilient is this credit in a downturn.\" Do not use for sector-level cyclicality (Industry Overview) or commodity exposure."
---

# Cyclicality

Produces the company-specific cyclicality read: how far earnings fall in a downturn, how fast they
recover, what holds up, and how today's earnings sit against the cycle. The company's own history, not a
sector label.

**This is a company read, not the sector one.** Earnings cyclicality (this skill, workbook Q636) uses the
company's own peak-to-trough record. Sector cyclicality (Q418) is Industry Overview's. Do not drift into
industry sizing or growth (Industry Overview) or full business-model detail (Business Overview). Commodity
/ input-cost is its own skill off the same tile.

**Two sources, two jobs. Built to the workbook prompt; figures from the dashboard and vault.** Workbook
Q636 (Earnings Cyclicality) is the spec: it defines the structure and coverage. The `other_risk_factors`
dashboard tile (its Cyclicality deep section) and the vault supply the figures. Read the tile (extract
only the Cyclicality deep section; ignore the risk-factor Cards and the Commodity / Input Cost deep
section) and the vault behind it. Where the tile is thin or lacks a Q636 field, render the spec's
structure and flag the missing piece as a gap; do not shrink the read to whatever a weak tile emits.

## Tone and rules

Also apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a specific source field or note; where a tile disagrees with the vault, the vault governs and the conflict is reported, never silently resolved; a tile's own internal inconsistency is evidence against that tile, not a tiebreaker.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives, banned-word list, bold key figures, no platform plumbing). The tile's
Credit Synthesis field is where it writes loosest; rewrite it to a plain declarative that leads with the
figure, and never render it verbatim (that is the connector's bad habit).

**Self-check the AI-speak tells before delivering. These keep slipping through:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period. This is a find, not a read.
- Do not pass the tile's synthesis or narrative prose through verbatim; it is written loose. Rewrite to a plain declarative that leads with the mechanism and the figure.
- Headings name content, never function. "The read," "Overview," "Assessment," "The take" are defects.
- No verdict-then-hedge ("resilient but incomplete," "sound, but only if Y"). State the finding, then the constraint as its own sentence.
- No X-not-Y and no hype ("well-positioned," "poised to," "robust," "compelling," "sharp move"). Lead with the fact.
- A finding is a statement carrying a figure, not a question and not a characterization where a number exists.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, if the user named a deal, `deal_list` to resolve. One match → use it. More than one →
  present as a table (Deal, Company, Sponsor, Status, Created — no internal IDs) and ask. Do not guess.
- If no deal is named, ask which deal first.

**Skip-if-known (strict):** if `analysis_get_status` or `dashboard_get(other_risk_factors)` is already
available from earlier in this conversation (e.g. a Commodity Exposure run, same tile), reuse it.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, suggest retrying or `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`dashboard_get` is deferred; if not loaded this conversation, `tool_search` it first. The second read uses
`research_search_documents_by_type` and `get_source_page` — load those when you reach them.

## Retrieve

`dashboard_get(project_id, tile="other_risk_factors")` — a single full-tile call. Section-scoping does not
work for this tile, so pull the full tile and extract the **Cyclicality** deep section client-side. Read
the data-confidence level and generated date first.

Entity discipline (Q1220): report figures for the credit subject. On a carve-out or a combination, label
each period's perimeter and do not carry a standalone perimeter past the point combined figures begin, or
backfill combined figures into earlier periods.

If the Cyclicality deep section is missing or sparse — a business with no disclosed cycle history — say so
plainly and flag it as a gap. Do not fill in from another section or fall back to a vault search.

## Render — built to Q636, figures from the dashboard and vault

Render this order, pulling figures from the tile and vault, prose rewritten to the standard. Where a Q636
field is not in the tile, source it from the vault or mark it a gap; never omit a spec element because the
tile was thin.

**Header:** **Cyclicality — [Deal Name]**, with a meta line (company, sponsor, data-confidence level).

**Structured fields** (Q636, a short header strip):
- Peak Adjusted EBITDA (most recent full cycle), with its period
- Trough Adjusted EBITDA (most recent full cycle), with its period
- Peak-to-trough decline (%)
- Downturn-resilient revenue share (%)

**End-market exposure.** Revenue by segment (the tile's revenue-by-segment table where present), and which
end markets are cyclical versus less cyclical. Keep it to exposure; do not drift into industry growth.

**Recurring vs cyclical.** The downturn-resilient revenue streams, their share, and whether that share is
large enough to matter against the cyclical base (Q636). Name the mechanism that makes them resilient
(installed base, aftermarket, contract), not "recurring revenue" as a bare claim.

**Historical downturn & forward visibility.** The peak-to-trough Adjusted EBITDA move and the percentage
decline over the most recent full cycle, the mechanism of the decline (volume, price, or mix), the
recovery pace, and how current earnings sit against the cycle (if near peak, what prior cycles imply for
the downside). Then forward visibility: booked or contracted revenue, program life, and backlog where
disclosed. Close on how the cyclicality nets out for coverage. Name what is not quantified (a non-recession
sensitivity, aftermarket share of gross profit, backlog dollars) as a gap.

**Cross-check (only if Industry Overview was already run this conversation for this deal; do not fetch new
data for it).** Compare this company read against the sector Cyclicality verdict (Q418) in one line: more
or less resilient than the industry baseline, and why. Skip entirely if Industry Overview was not run.

Every sized figure carries its source and period. Close with the tile's `web_url` as a single
"🔗 Open in Raven" link.

## Second read (mandatory, INTERNAL — a separate pass after the full render, never shown)

Silent, findings woven in. After the render:
1. **Verify the peak and trough Adjusted EBITDA and the percentage decline** against the documents
   (`research_search_documents_by_type` or `get_source_page` on a cited leaf). A tile figure is a claim
   to verify, and this decline drives the whole read.
2. **Confirm the downturn-resilient share and its mechanism** against the source, and that the perimeter
   is the credit subject's, not a parent's.
3. **Confirm the gaps** the tile lists are genuinely absent from the documents.
Findings weave in: a corrected figure appears in place, a confirmed gap strengthens the read. No process
block. The test that it ran is a changed, more accurate artifact.

## Final review (mandatory, INTERNAL — the last step)

Read the finished piece once more and fix: **tone** (findings not directives; no verdict-then-hedge, no
X-not-Y, credit-desk register); **coherence** (structured fields, the blocks, and the coverage read tell
one story; the peak/trough figures match everywhere); **scope** (no drift into industry sizing/growth or
business-model detail); **headings** (name the content, never the function); and a **literal proofread**,
including a literal scan for the em-dash character, which language-standard bans, replaced with a comma,
semicolon, or period. Silent; its only evidence is a cleaner read.

## Rules

- Company earnings cyclicality (Q636), from the company's own history. Sector cyclicality is Industry
  Overview (Q418); business model is Business Overview; commodity is its own skill (same tile).
- Build to Q636's structure (structured fields, end-market exposure, recurring-vs-cyclical, historical
  downturn & forward visibility). Pull figures from the dashboard tile and vault. Where the tile is thin
  or lacks a field, render the spec and flag the gap; do not shrink to the weak tile.
- Faithful stored-read. Never compute, re-score, or invent a figure. Rewrite the tile's prose to
  `language-standard.md`; never render the synthesis field verbatim.
- Every sized figure carries its source and period; label the entity perimeter on a carve-out or
  combination.
- Where cycle history is undisclosed, say so and flag the gap.
- Second read and final review are mandatory, separate, and SILENT.

## Delivery

A focused read, so chat is the default. Offer a Word document when a shareable deliverable is wanted
(docx skill, Arial, navy headers, US Letter; validate and render before delivering, and run the em-dash
scan on the doc). After delivering, offer one next step: the source page behind a figure, the Commodity
Exposure read off the same tile, or a Word export.
