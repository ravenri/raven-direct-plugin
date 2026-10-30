---
name: "financials-current-period-results"
description: "Renders a deal's current-period results, anchored on the most recently disclosed QUARTER, never LTM or full fiscal year (that's financials-snapshot's job). YoY and QoQ comparisons, a 4-quarter trend, arithmetic-checked figures (Revenue-COGS=Gross Profit, sub-components summing to totals), and the full-year forecast vs. prior-year actual where the company's own budget is disclosed (distinct from a sponsor/lender multi-year model). Partial periods (e.g. a 1-month interim) get their duration stated and dollar levels marked non-comparable to a full quarter, though margins stay comparable. Split from financials-snapshot, which now owns Historical Trend only; reuses its basis-consistency findings on Revenue/EBITDA rather than re-deriving them. Also renders the tile's compliance and liquidity snapshots as point-in-time facts, not tests. Use for \"current period,\" \"quarterly results,\" \"this quarter,\" \"QoQ,\" \"YoY,\" \"quarterly trend,\" or how the company is performing right now."
when_to_use: "Use when the user asks how a company is performing right now, or for the latest quarter: current period, quarterly results, this quarter, QoQ, YoY, or quarterly trend. Do not use for LTM or full-year trends (financials-snapshot), covenant tests, or coverage."
---

# Financials — Current Period Results

Renders the deal's current-period results, anchored on the **most recently disclosed quarter** — never LTM
or full fiscal year, which is `financials-snapshot`'s Historical Trend. A quick, data-dense screening
read, not a modeled analysis.

**This is quarter-anchored, not LTM-anchored — the most common framing error on this skill.** The
underlying prompt registry is explicit and repeated on this point: current-period figures anchor on the
most recent disclosed quarter (period type q1/q2/q3), with year-over-year (same quarter, prior year) and
quarter-over-quarter (immediately preceding quarter) as the two comparisons. LTM and full-fiscal-year
figures belong to the historical anchor and are out of scope here, even though the tile surfaces a
deal-level LTM KPI snapshot alongside this section for headline context. Do not let that headline block
turn the rest of the render LTM-flavored — the QoQ read specifically is this section's distinguishing
content, since Historical Trend and any annual view structurally cannot show it. Lead with it.

**This is a stored-read, not an analysis pass.** The tile already holds the comparison tables, the
quarterly series, the compliance and liquidity snapshots, and written discussion for each. This skill
renders that faithfully, in house voice, and never recomputes a figure, re-derives a margin, or invents a
trend — except for the specific, narrow arithmetic checks in Render, below, which confirm the tile's own
figures foot rather than adding new ones.

**Split from `financials-snapshot`.** That skill originally covered both Historical Trend and Current
Period from the same tile; the two were split into single-purpose skills, matching the convention already
established for Balance Sheet and Income Statement & Cash Flow. `financials-snapshot` now owns Historical
Trend (including the deal's LTM/FY anchor) only. This skill owns everything anchored on the current
quarter.

## Scope and cross-skill sourcing

This skill owns the current-period signal only: the KPI snapshot, YoY/QoQ comparisons, quarterly trend,
compliance snapshot, and liquidity snapshot. It does not own the multi-year historical trend or the
Revenue/Adjusted EBITDA CAGR — that is `financials-snapshot`'s job. It does not own coverage ratios, the
recovery read, or covenant-by-covenant testing — those are `loan-coverage` and `test-covenants`; this skill
renders the tile's own compliance snapshot as a point-in-time fact, never a test.

**Before rendering, check whether `financials-snapshot` has already run this conversation and flagged a
basis-consistency issue** (e.g. a Revenue-basis mismatch across historical periods, or a cross-page EBITDA
conflict). Figures in this skill's KPI snapshot (PF Adjusted EBITDA, Revenue, PF Adjusted EBITDA margin)
are frequently built on the same base as the historical series. A caveat found there must propagate here
too — never treat the current-period figures as independently clean just because they live in a different
skill's output. If `financials-snapshot` hasn't run yet, apply the same basis-consistency and cross-page
conflict checks independently (see Render, below) rather than assuming the tile is internally consistent.

## Tone and rules

Apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a
specific tile field or note; where a figure disagrees with another surface, the disagreement is reported,
never silently resolved; a tile's own internal inconsistency is evidence against that tile, not a
tiebreaker.

Apply `references/conventions.md`: the platform's own EBITDA-role definitions and period-anchor selection
rules, shared verbatim from the system rule package, so this skill's figures use the same basis
`financials-snapshot` and the other financials skills already apply.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives). Read it and apply it. Do not expose platform plumbing (no "the tile,"
`financial_analysis`, `currentperiod`, section names, or raw source-index brackets) in the body.

**The tile's written discussion needs rewriting, not verbatim rendering.** The `currentperiod` section
carries genuinely useful analytical prose (Revenue, Margins, Cash flow & liquidity, Compliance position),
and every substantive point and figure in that prose stays. But the tile's own sentences are frequently
written in the register the standard bans (sell-side framing, hedge-then-verdict, filler adjectives).
Rewrite each discussion block into plain declarative sentences that lead with the figure; keep every causal
or quality point the tile makes, cut nothing but the loose phrasing.

**Self-check the AI-speak tells before delivering:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period.
- Do not pass the tile's discussion prose through verbatim; rewrite to a plain declarative that leads with
  the mechanism and the figure.
- Headings name content, never function ("The read," "Overview," "Assessment" are defects).
- No verdict-then-hedge. State the finding, then the constraint as its own sentence.
- No X-not-Y and no hype ("well-positioned," "robust," "compelling"). Lead with the fact.
- A finding is a statement carrying a figure, not a characterization where a number exists.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, `deal_list` to resolve by name. One match → use it. More than one → present as a table (Deal,
  Company, Sponsor, Status, Created; no internal IDs) and ask. Do not guess.
- If no deal is named, ask which deal first.

Capture the deal's display name, sponsor, and reporting currency for the header.

**Skip-if-known (strict):** if `analysis_get_status` or `dashboard_get(financial_analysis, ...)` is already
available from earlier in this conversation (e.g. `financials-snapshot` already pulled this tile's
`historical` section, or `financial-proforma-cap-table-ebitda` already pulled its `ebitda` section), do not re-call
`analysis_get_status`; the `currentperiod` section itself must still be fetched fresh if not already
available, since a different section was pulled.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, and suggest retrying once analysis completes or starting the analysis from within Raven. This chat cannot start it.

## STEP 0.5 — Tool pre-load

`dashboard_get` is deferred; if not loaded this conversation, `tool_search` it first.
`research_search_analysis` is also deferred; load it too if the full-year-forecast fallback search (below)
turns out to be needed.

## Retrieve

`dashboard_get(project_id, tile="financial_analysis", section="currentperiod")` — KPI snapshot, current
year and YoY/QoQ comparisons, quarterly trend, compliance snapshot, liquidity snapshot, and the four
discussion blocks.

If the call returns thin or unavailable content, say so plainly. If the tile section doesn't surface a
company-own full-year forecast/budget (distinct from a sponsor/lender multi-year model), run one targeted
`research_search_analysis` search for it (content-based query, e.g. "current fiscal year revenue EBITDA
forecast budget" — never a hardcoded question ID) before concluding it isn't disclosed.

## Render

**Header:** deal name, sponsor, reporting currency, current-quarter period label (from the response's own
header field, not the LTM end date — state the LTM end date only as a secondary reference for the KPI
snapshot below).

- **KPI Snapshot** — PF Adjusted EBITDA, Revenue, PF Adjusted EBITDA margin, entry net leverage, enterprise
  value, each labeled with its LTM period. Present this explicitly as the deal's frozen LTM anchor,
  carried for headline context and consistency with `financials-snapshot`, not as this section's own
  current-period fact. If `financials-snapshot` flagged a basis issue on Revenue or EBITDA this
  conversation, carry the same caveat here rather than presenting these as clean.

- **Current quarter identification.** State the most recently disclosed quarter's period label and type
  (q1/q2/q3), and its duration. **Partial periods:** where the most recent disclosed period is shorter than
  a full quarter (e.g. a one-month interim from monthly management accounts), state the duration explicitly
  in the period label everywhere it appears (e.g. "Jan-25 (1 mo.)"), and do not compare its dollar levels
  to a full quarter or to a full-quarter prior period — a one-month figure will read as a collapse against
  a three-month column. Margins and ratios remain comparable across a partial period; dollar levels do
  not. Say so inline, not just once at the top.

- **YoY and QoQ comparison tables** — Revenue, COGS, Gross Profit/Margin, Adjusted EBITDA/Margin, for the
  current quarter against the same quarter prior year (YoY) and the immediately preceding quarter (QoQ).
  **Table format: periods along the top as columns, metrics as rows** — never the reverse. Render exactly
  as disclosed, including every "Not disclosed" cell where a comparison period isn't available; never
  fabricate a same-quarter-prior-year or immediately-preceding-quarter figure to fill a gap, and never
  substitute a differently-sized period as if it were the missing comparator (a six-month interim is not a
  valid stand-in for a discrete second quarter). State plainly when a comparison basis itself isn't
  disclosed. **The QoQ read is this section's distinguishing content** — Historical Trend structurally
  cannot show it. Lead with it rather than restating the YoY figures as the headline.
  **Arithmetic checks, every period shown:** Revenue minus COGS equals Gross Profit within rounding; any
  disclosed sub-components sum to their stated total within rounding. Flag, do not silently force, any
  period that doesn't reconcile. Where COGS or Gross Profit isn't stated directly, derive it only from two
  other disclosed (not themselves derived) figures, and label it "derived."
- **EBITDA role and anchor layer.** The Adjusted EBITDA figure here uses the same canonical role
  `references/conventions.md` defines, excluded by role, not by label — an idiosyncratic label mapped to
  the Adjusted role is the right figure even if it doesn't say "Adjusted." Where a more-adjusted anchor
  layer applies to this deal (Pro Forma Adjusted, or PF Adjusted Cash on software/recurring-revenue deals),
  state its canonical title and current-quarter value alongside the Adjusted figure where disclosed for
  this period — a read that shows only the Adjusted layer understates the basis leverage actually strikes
  on. Do not derive an anchor figure the documents don't state for this specific period.

- **Quarterly trend** — the last four disclosed full quarters plus the current period (chronological,
  oldest to newest). **Table format: periods along the top as columns, metrics (Revenue, Adjusted EBITDA,
  Gross Margin, EBITDA Margin) as rows** — never the reverse; this is the same orientation as the YoY/QoQ
  tables and every other multi-period table in this render, so a reader scans consistently across the
  whole document. Include only quarters the documents actually disclose; **never pad to four columns**,
  and **never construct a quarter by subtracting cumulative figures** (e.g. inferring Q2 from a six-month
  total minus a disclosed Q1) unless the source itself performs that arithmetic. Where a metric isn't
  disclosed for a period, render "n/d" verbatim in that column, never a zero or an interpolation, and never
  drop the column silently — a column that exists for one metric (e.g. Gross Margin, often fully
  disclosed) but not another (e.g. Adjusted EBITDA, often thin) still gets rendered, with "n/d" in the
  metric's own row for that period. A single disclosed quarter, or a series with only one or two data
  points, is not a trend: say so explicitly rather than implying a trajectory the data can't support.

- **Full year forecast, where disclosed.** If the company's own current-fiscal-year revenue and Adjusted
  EBITDA forecast/budget is disclosed (distinct from a sponsor or lender multi-year projection model, which
  is out of scope here and belongs to a separate projections read), render it against prior-year actual
  with YoY growth, on the same canonical Adjusted EBITDA basis as the historical series. If only a
  sponsor/lender model exists and no separate company budget is disclosed, say so plainly rather than
  substituting the model's projection as if it were the company's own forecast — check
  `research_search_analysis` for this specifically if the tile section doesn't surface it, since it may not
  always appear in the same tile section as the rest of this render.

- **Compliance snapshot** — First Lien Net Leverage, Covenant Max, Headroom (turns and %), Total Net
  Leverage, Interest Coverage, FCF Coverage, LTM Excess Cash Flow, Mandatory Amortization, Compliance
  Status. Where no compliance certificate is in the document set, render every metric as "Not disclosed"
  with its own reason rather than substituting a proxy figure silently; a close-date or projected figure
  may be cited only as an explicitly labeled proxy, never presented as the tested ratio. If `loan-coverage`
  or `test-covenants` have already run this conversation, note whether the figures agree; do not re-derive.
- **Liquidity snapshot** — Cash, Revolver Committed / Drawn / Available, Total Liquidity, Liquidity as % of
  LTM EBITDA.
- **Discussion** — the Revenue, Margins, Cash flow & liquidity, and Compliance position blocks, rewritten
  to the language standard.

Bullet anything enumerable inside a discussion block rather than stacking short declarative sentences into
one paragraph. No paragraph over ~80 words.

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time.
1. **Verify the anchor figures trace to source.** For PF Adjusted EBITDA, the covenant leverage figure, and
   any figure a discussion block leans on, confirm it traces to the tile. If a figure looks internally
   inconsistent (a comparison-table cell that doesn't match the KPI snapshot), flag it rather than silently
   picking one.
2. **Confirm the cross-skill basis check actually ran.** If `financials-snapshot` flagged a Revenue or
   EBITDA basis issue this conversation, confirm every figure here built on that same base carries the same
   caveat; a caveat that stayed in the other skill's output and never made it here is a defect.
3. **Reconcile against `loan-coverage` / `test-covenants` if either already ran this conversation.**
   Agreement is worth a one-line note; a disagreement is reported, never smoothed over.
4. **Confirm every "Not disclosed" cell rendered as such**, and that no proxy or close-date figure was
   substituted for a tested ratio without an explicit label.
5. **Confirm currency carried through correctly** — every figure in the deal's stated reporting currency,
   no silent conversion.
6. **Re-run the arithmetic checks.** Revenue minus COGS equals Gross Profit within rounding, and disclosed
   sub-components sum to their stated totals, for every period shown in the comparison tables and the
   quarterly trend. A mismatch caught here that didn't make it into the render as a flagged inconsistency
   is a defect to fix now, not a footnote to add later.
7. **Confirm the quarterly trend wasn't padded or constructed.** No column should exist that wasn't
   actually disclosed as a discrete quarter, and no figure should be the result of subtracting a
   cumulative total from another period unless the source itself performs that subtraction.
8. **Confirm partial-period handling.** If the current period is shorter than a full quarter, its duration
   must appear in the label everywhere it's used, and no dollar-level figure from that period should be
   compared to a full-quarter column without the non-comparability being stated.
9. **Confirm the render never drifted LTM-flavored.** The KPI Snapshot's LTM figures should read as
   headline context, not as the substance of the current-period analysis; if the Discussion or comparison
   tables ended up leaning on LTM framing instead of the current quarter, that's the core failure mode this
   skill exists to avoid.
10. **Confirm every multi-period table has periods as columns, metrics as rows.** Check the YoY table, the
    QoQ table, and the Quarterly Trend table individually; a table built the other way around is a defect
    to fix now, not a formatting nitpick to leave for the reader.

Findings weave into the render in place; nothing labeled "second read" reaches the output.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

Read the finished piece top to bottom once more and fix: **tone** (every discussion block states a
finding, not a directive; no X-not-Y constructions, credit-desk register); **figure consistency** (a
figure appearing in more than one place matches everywhere); **readability** (bulleted where enumerable,
no paragraph walls); **headings** (clean, parallel, name content); and a **literal proofread** of every
heading and figure. Scan literally for the em-dash character and replace each with a comma, semicolon, or
period. Silent; its only evidence is a cleaner artifact.

## Rules

- Faithful stored-read. Never compute, re-score, or invent a figure or trend; render exactly what the tile
  returns, including its own "Not disclosed" flags and notes.
- **Every multi-period table renders periods along the top as columns and metrics as rows, with no
  exceptions.** This applies to the YoY table, the QoQ table, and the Quarterly Trend table alike, so the
  whole render reads consistently. Never orient a table with periods as rows.
- **Anchor on the most recently disclosed quarter, never LTM or full fiscal year.** The KPI Snapshot's LTM
  figures are headline context carried for consistency with `financials-snapshot`, not this section's own
  current-period fact; the substance of this render is the current quarter and its YoY/QoQ comparisons.
- Rewrite the tile's discussion prose to the language standard; never pass it through verbatim.
- If the tile section is thin or unavailable, say so plainly rather than filling from elsewhere.
- Currency: render every figure in the deal's stated reporting currency, unit intact; never assume USD or
  convert.
- Arithmetic checks are mandatory on every period shown: Revenue minus COGS equals Gross Profit within
  rounding, and disclosed sub-components sum to their stated totals. Flag, never silently force, a period
  that doesn't reconcile.
- Never pad the quarterly trend to four columns, and never construct a quarter by subtracting a cumulative
  total from another period unless the source itself performs that subtraction. Missing periods render as
  "n/d," never zero or an interpolation.
- Partial periods (shorter than a full quarter) get their duration stated in the label everywhere it's
  used; their dollar levels are never compared to a full-quarter column, though their margins remain
  comparable.
- The company's own current-fiscal-year forecast/budget, where disclosed, is distinct from a sponsor or
  lender multi-year projection model; never substitute one for the other, and say plainly if only the
  model exists.
- A single disclosed quarter, or a series with only one or two post-close data points, is not a trend;
  say so rather than implying a trajectory.
- Reuse `financials-snapshot`'s basis-consistency findings on Revenue/EBITDA where that skill has already
  run this conversation; never present a figure here as independently clean if the same base was already
  flagged elsewhere.
- No proxy or close-date figure stands in for a tested compliance ratio without an explicit label; where no
  compliance certificate exists, every metric renders as "Not disclosed."
- No platform plumbing in the body (no "the tile," `financial_analysis`, `currentperiod` as a section
  name).
- Second read and final review are mandatory, separate, and silent; the evidence they ran is a changed
  artifact, never a narrated process block.
- Scope: current-quarter signal only. Historical trend, LTM, and CAGR are `financials-snapshot`'s job;
  coverage and recovery is `loan-coverage`; covenant testing is `test-covenants`. Note agreement or
  disagreement with those reads if already run; never re-derive their output.

## Delivery

Render the read in the answer. The platform's export produces a Word document; do not create a file. After delivering,
offer one natural next step: the `financials-snapshot` read if Historical Trend hasn't been pulled yet, `loan-coverage`
or `test-covenants` for the compliance figures, or the export if the user wants a document.
