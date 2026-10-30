---
name: "financials-snapshot"
description: "Renders a deal's historical and current-period financials, revenue, margins, EBITDA, capex, NWC, LTM/YTD trajectory, and compliance/liquidity position, sourced from Raven's financial_analysis tile (historical and currentperiod sections). Faithful stored-read: the tile carries multi-year trend data, a CAGR block, an LTM-vs-prior spread table, a quarterly trend, compliance and liquidity snapshots, and pre-written discussion for each; the skill renders this in house voice, never recomputes a figure, and never passes the tile's prose through verbatim. Distinct from EBITDA & Cap Table (anchor-EBITDA derivation and cap structure), Loan Coverage (coverage/recovery read), and Test Covenants (covenant testing) - this is the financial-performance snapshot those reads assume as background. Use for \"financials snapshot,\" \"financial performance,\" \"historical financials,\" \"LTM financials,\" \"current period,\" \"revenue and margin trend,\" \"NWC,\" or a quick read on how the company is performing financially."
when_to_use: "Use for \"financials snapshot,\" \"financial performance,\" \"historical financials,\" \"LTM financials,\" \"revenue and margin trend,\" \"NWC,\" or a quick read on how the company is performing. Do not use for the full line-item statements or a deep read of the latest quarter (Current Period Results)."
---

# Financials Snapshot

Renders the deal's financial-performance read: the historical multi-year trend and the current-period
(LTM/YTD) signal, including compliance and liquidity, sourced from Raven's `financial_analysis` tile. A
quick, data-dense screening read, not a modeled analysis.

**This is a stored-read, not an analysis pass.** The tile already holds the trend tables, the CAGR block,
the LTM spread, the quarterly series, the compliance and liquidity snapshots, and written discussion for
each. This skill renders that faithfully, in house voice, and never recomputes a figure, re-derives a
margin, or invents a trend.

**Source: two scoped tile calls, not vault search.** An earlier version of this workflow rebuilt this
ground from three fixed vault searches; that approach is retired because the tile's own stored content,
including its pre-written analytical discussion, is more complete and more reliable than a fresh
search-and-synthesize pass. Read `dashboard_get(tile="financial_analysis", section="historical")` and
`dashboard_get(tile="financial_analysis", section="currentperiod")` — both, every time; the historical
section alone omits the LTM/compliance/liquidity signal, and the current-period section alone omits the
multi-year trend.

## Scope

Financial-performance read only. The anchor-EBITDA derivation and the reported-to-adjusted-to-PF-to-cash
walk belong to EBITDA & Cap Table; do not re-derive an EBITDA bridge here, just render the tile's own
Adjusted EBITDA and margin figures. Coverage ratios and the recovery read belong to Loan Coverage.
Covenant-by-covenant compliance testing and stress scenarios belong to Test Covenants; this skill renders
the tile's own compliance snapshot (leverage, headroom, coverage) as a point-in-time fact, not a test.
Where those skills have already run earlier in the conversation, note whether the figures agree rather
than re-deriving anything.

## Tone and rules

Also apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces
to a specific tile field or note; where a figure disagrees with another surface, the disagreement is
reported, never silently resolved; a tile's own internal inconsistency (a subtotal that doesn't foot) is
evidence against that tile, not a tiebreaker.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives, house banned-word list). Read it and apply it. Do not expose platform
plumbing (no "the tile," "financial_analysis," "historical," "currentperiod," section names, or raw
source-index brackets) in the body — present a figure as a figure, a trend as a trend.

**The tile's written discussion needs rewriting, not verbatim rendering — this is the main trap on this
skill.** The `historical` and `currentperiod` sections both carry genuinely useful analytical prose
(Revenue, Margins, Cash flow, Composition & Adjustments; Compliance Position), and every substantive point
and figure in that prose stays. But the tile's own sentences are frequently written in exactly the
register the standard bans (sell-side framing, hedge-then-verdict, filler adjectives). Passing it through
"close to verbatim" imports that language. Rewrite each discussion block into plain declarative sentences
that lead with the figure; keep every causal or quality point the tile makes, cut nothing but the loose
phrasing.

**Self-check the AI-speak tells before delivering. These keep slipping through:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period. This is a find, not a read.
- Do not pass the tile's discussion prose through verbatim; it is written loose. Rewrite to a plain declarative that leads with the mechanism and the figure.
- Headings name content, never function. "The read," "Overview," "Assessment," "The take" are defects.
- No verdict-then-hedge ("manageable but relevant," "sound, but only if Y"). State the finding, then the constraint as its own sentence.
- No X-not-Y and no hype ("well-positioned," "poised to," "robust," "compelling," "sharp move"). Lead with the fact.
- A finding is a statement carrying a figure, not a question and not a characterization where a number exists.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, if the user named a deal, `deal_list` to resolve. One match → use it. More than one →
  present as a markdown table (Deal, Company, Sponsor, Status, Created — no internal IDs) and ask. Do not
  guess.
- If no deal is named, ask which deal first.

Capture the deal's display name, sponsor, and reporting currency for the header.

**Skip-if-known (strict):** if `analysis_get_status` or either `dashboard_get(financial_analysis, ...)`
call is already available from earlier in this conversation (e.g. EBITDA & Cap Table already pulled this
tile's `ebitda` section), do not re-call.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, and suggest retrying once analysis completes or running `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`dashboard_get` is deferred; if not loaded this conversation, `tool_search` it first.

## Retrieve

Issue both calls together, in one turn:
1. `dashboard_get(project_id, tile="financial_analysis", section="historical")` — multi-year
   revenue/margin/EBITDA/capex/NWC trend, reported vs. organic CAGR, and the four discussion blocks.
2. `dashboard_get(project_id, tile="financial_analysis", section="currentperiod")` — LTM vs. prior-year
   spread, quarterly trend, compliance snapshot, liquidity snapshot, and the four discussion blocks.

If either call returns thin or unavailable content, say so plainly rather than filling from the other
section.

## Render

**Header:** deal name, sponsor, reporting currency, LTM end date (from either response's own header
field).

**1. Historical Trend**
- **Summary table** — Revenue, YoY Growth, Gross Profit, Gross Margin, Adj. EBITDA, EBITDA Margin, Capex,
  Capex % Revenue, across every disclosed period. Render "Not disclosed" exactly where the tile's own
  `Disclosed: No` flag says so; do not fill from a `Not Disclosed Note`'s context unless it states an
  actual number.
- **Basis-consistency check on the Revenue row (mandatory before rendering the table, not just in the
  second read).** Companies commonly report on more than one revenue basis (e.g. total revenue vs.
  value-add revenue net of pass-through material costs), and a tile can stitch periods measured on
  different bases into what looks like one continuous series. The tell is usually buried in a discussion
  block elsewhere on the tile: if any discussion cites an alternate revenue figure for a period already in
  the table (e.g. "$14.0B of value-add revenue" for a period the table shows at a different total-revenue
  figure) and that alternate figure is materially closer to the OTHER periods' reported level than the
  table's own figure for that period is, treat the row as basis-inconsistent, not as a single clean trend.
  When this happens: (1) do not render the YoY growth or CAGR figures spanning the mismatched periods as a
  clean growth rate without a caveat directly under the table, since they mix two denominators; (2) do not
  let the mismatched period's margin figures (gross margin, EBITDA margin, and anything else denominated
  in that period's revenue) pass as directly comparable to the other periods' margins without the same
  caveat, since a bigger denominator alone will show as margin compression; (3) name the two bases in
  plain terms and say which periods use which, rather than silently picking one or averaging. This is a
  read-time check on the table as assembled, not something to defer entirely to the second read.
- **Cross-page figure conflicts on ANY metric, not only revenue basis.** The tile's own Composition &
  Adjustments (or equivalent) discussion sometimes states outright that two source pages disclose
  different figures for the same metric, period, and role (seen live: a reconciliation page and a
  historical-trend page giving different Adjusted EBITDA levels for the same period). Where this happens,
  the two disciplines are separate and both apply: render the summary table using ONE named source page's
  figure and say which page it is, and separately state the walk or bridge is anchored on whichever figure
  its own source page uses, even if that differs from the table. Never silently harmonize the two into one
  number, and never let the conflict pass unmentioned because both figures individually look plausible. If
  the tile's own text asserts a conflict but the two cited figures are actually identical (a
  tile-generation artifact, not a real conflict), say so instead of repeating a conflict that doesn't
  exist in the numbers as given.
- **Period/value array-length gaps.** A metric's disclosed-values array is sometimes shorter than the
  Periods array for the same section, with no explicit `Disclosed: No` flag marking which specific periods
  are missing. Where this happens, work out which periods the shorter array actually covers from the
  surrounding discussion (a discussion block will usually anchor at least one end of the series to a named
  period), and render "Not disclosed" explicitly for every period the shorter array does not cover, rather
  than silently dropping those columns or reproducing the array misaligned against the wrong periods.
- **CAGR line** — the stored Revenue Reported, Revenue Organic, and Adj. EBITDA CAGRs, with their period
  label, as one line.
- **Discussion** — the Revenue, Margins, Cash flow, and Composition & Adjustments blocks, rewritten to the
  language standard. Keep every causal and quality point (what drove a margin move, what a composition
  shift means); cut only the loose phrasing. Do not compress to a stricter sentence cap; the content is
  real and stays.

**2. Current Period (LTM/YTD Signal)**
- **LTM vs. prior-year spread table** — Revenue, Gross Profit, Gross Margin, SG&A, R&D, D&A, Reported
  EBITDA, Adj. EBITDA, EBITDA Margin, Compliance EBITDA, Capex, Capex % Revenue, with the tile's own
  comparison note above it, rewritten to the language standard.
- **Quarterly trend** — the quarterly Revenue / Adj. EBITDA / Gross Margin / EBITDA Margin series as a
  compact table, with any tile `Data Note` (e.g. a margin dip flagged as transaction or separation-cost
  driven rather than organic). A single strong or weak quarter is not a trend: where the series shows one
  outlier period, note seasonality or post-close data thinness rather than reading it as directional,
  especially on a recently-closed deal with only one or two post-close quarters.
- **Compliance snapshot** — First Lien Net Leverage, Covenant Max, Headroom (turns and %), Total Net
  Leverage, Interest Coverage, FCF Coverage, Mandatory Amortization, Compliance Status. If Loan Coverage or
  Test Covenants have already run this conversation, note whether the figures agree; do not re-derive.
- **Liquidity snapshot** — Cash, Revolver Committed / Drawn / Available, Total Liquidity, Liquidity as % of
  LTM EBITDA.
- **Discussion** — the Revenue, Margins, Cash flow & liquidity, and Compliance position blocks, rewritten
  to the language standard on the same terms as the historical discussion.

Bullet anything enumerable inside a discussion block rather than stacking short declarative sentences into
one paragraph. No paragraph over ~80 words.

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time; the reader sees only the result.
1. **Verify the anchor figures trace to source.** For the LTM Adjusted EBITDA, the covenant leverage
   figure, and any figure a discussion block leans on, confirm it traces to the tile (a tile figure is
   already a claim to verify, not a computed one to re-derive). If a material figure looks internally
   inconsistent (a spread table cell that doesn't foot against the historical table's own current period),
   flag it rather than silently picking one.
2. **Reconcile against Loan Coverage / Test Covenants if either already ran this conversation.** Compare
   the compliance snapshot's leverage, headroom, and coverage figures against those skills' own numbers.
   Agreement is worth a one-line note; a disagreement is reported, never smoothed over.
3. **Check the CAGR and quarterly trend against the summary table.** A CAGR that implies a trajectory the
   summary table's own period-over-period figures don't support is an inconsistency to flag, not to trust
   blind.
4. **Re-run the basis-consistency check across the whole render, not just the table.** The historical
   summary table's own render step (above) catches an alternate-basis mismatch on the Revenue row before
   the table is built; here, extend the same check to every other metric fed by that row (YoY growth,
   CAGR, gross margin, EBITDA margin, PF Adjusted EBITDA margin in the KPI snapshot) and to any other
   series in the render (the current-period spread table, the quarterly trend) where a discussion block
   elsewhere on the tile cites an alternate basis for the same metric. A caveat added to one figure derived
   from a mismatched row must propagate to every other figure derived from the same row, not stay
   contained to where it was first noticed.
5. **Confirm every cross-page figure conflict and array-length gap identified during Render actually made
   it into the finished artifact**, not just into working notes. A conflict caught while assembling the
   table but dropped by the time the discussion prose is written is the same failure as never catching it.
6. **Confirm currency and disclosure flags carried through correctly** — every figure in the deal's stated
   reporting currency, no silent conversion, and every "Not disclosed" rendered as such rather than
   dropped or guessed.

Findings weave into the render: a reconciled figure appears corrected in place, an agreement or
disagreement with Loan Coverage/Test Covenants appears as a plain one-line note in the compliance section.
No "second read" language reaches the output.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

Read the finished piece top to bottom once more and fix: **tone** (every discussion block states a
finding, not a directive; no X-not-Y constructions, no scaffolding lines, credit-desk register); **figure
consistency** (a figure appearing in more than one place, LTM revenue, Adj. EBITDA, leverage, matches
everywhere); **readability** (bulleted where enumerable, no paragraph walls); **headings** (each is a
clean, parallel label naming content, never "The read," "Overview," or "Assessment"); and a **literal
proofread** of every heading and figure as text. Then scan literally for the em-dash character and replace
each with a comma, semicolon, or period. Silent; its only evidence is a cleaner artifact.

## Rules

- Faithful stored-read. Never compute, re-score, or invent a figure or trend; render exactly what the tile
  returns, including its own "Not disclosed" flags and notes.
- Rewrite the tile's discussion prose to the language standard; never pass it through verbatim. Keep every
  figure and analytical point; cut only the loose phrasing.
- Both `historical` and `currentperiod` are in scope, every run; do not restrict to historical-only.
- If either section is thin or unavailable, say so plainly rather than filling from the other.
- Currency: render every figure in the deal's stated reporting currency, unit intact; never assume USD or
  convert.
- A single outlier quarter is not a trend; note seasonality or post-close data thinness instead, especially
  on recently-closed deals.
- Never render a multi-period Revenue row as one clean trend without checking whether every period is on
  the same basis (total vs. value-add revenue, etc.). A discussion block elsewhere on the tile citing an
  alternate figure for a period already in the table is the tell; when found, caveat the row directly and
  propagate the caveat to every growth rate, CAGR, and margin figure that row feeds, rather than confining
  it to a footnote on the discussion paragraph where it was first mentioned.
- When two source pages on the same tile disclose different figures for the same metric, period, and role
  (an Adjusted EBITDA reconciliation vs. a historical-trend page, for example), name both figures and both
  source pages; render the summary table off one named page and the walk or bridge off its own source, even
  if they differ, and never harmonize them into a single number. If the tile's own text claims a conflict
  but the two cited figures are actually identical, say so rather than repeating a nonexistent conflict.
- When a metric's disclosed-values array is shorter than its section's Periods array with no explicit
  per-period disclosure flag, work out from the surrounding discussion which periods the array covers and
  render "Not disclosed" explicitly for every period it does not, rather than dropping or misaligning
  columns.
- No platform plumbing in the body (no "the tile," "financial_analysis," "historical"/"currentperiod" as
  section names).
- Second read and final review are mandatory, separate, and silent; the test that either ran is a changed
  artifact, never a narrated process block.
- Scope: financial-performance snapshot only. EBITDA derivation is EBITDA & Cap Table; coverage and
  recovery is Loan Coverage; covenant testing is Test Covenants. Note agreement or disagreement with those
  reads if already run; never re-derive their output.

## Delivery

Render in chat by default. Only produce a Word document if asked; when generating one, use the docx skill
(Arial, navy section headers, US Letter) with a title block (deal name, sponsor, currency, LTM end date),
the Historical Trend section, and the Current Period section, matching the chat structure. Save to
`/mnt/user-data/outputs/` and `present_files`. After delivering, offer one natural next step: the source
page behind a specific figure, the EBITDA & Cap Table read, Loan Coverage, or the Word export if the read
was in chat.
