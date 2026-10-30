---
name: "financial-capex-analysis"
description: "Analyzes a deal's capital expenditure - historical/projected figures with YoY change, the maintenance/growth split where disclosed, a Major Projects table, capex intensity trend, a projected-vs-historical step-change flag, a peer/industry comparison (~3%-of-revenue materiality threshold), forward visibility, a discretionary-vs-committed/mandated commitment profile (downturn flexibility), deferred-capex/bow-wave risk detection, the qualitative nature of spend, and an adequacy judgment (maintenance capex vs. D&A, qualified by the company's capitalization policy, deferred-maintenance risk, asset-condition corroboration, growth-constraint check). Fully independent, vault-search-based; never re-derives an undisclosed split. Mandatory check: Maintenance + Growth = Total Capex. Periods render as columns. Use for \"capex,\" \"capital expenditure,\" \"maintenance vs. growth capex,\" \"capex adequacy,\" \"capex vs peers,\" \"deferred maintenance,\" or how reinvestment compares to historical run rate."
when_to_use: "Use for \"capex,\" \"capital expenditure,\" \"maintenance versus growth spend,\" or whether capex is enough. Do not use for the full projections (Projections, Base Case) or the historical cash flow statement."
---

# Financial - Capex Analysis

Analyzes a deal's capital expenditure: historical and projected dollar figures, the maintenance/growth
split, intensity trend, a projected-vs-historical comparison, the qualitative nature of spend, and an
adequacy judgment. Vault-search-based and fully independent — no dashboard tile owns this ground, and this
skill does not depend on any other skill having already run.

**This is judgment-informed on the adequacy question, a faithful stored-read everywhere else.** The
dollar figures, the maintenance/growth split, and the intensity trend are rendered exactly as disclosed,
never computed or invented. The adequacy assessment (capex vs. D&A, deferred-maintenance risk) is a
genuine analytical judgment built from those figures, per the discipline below — but the inputs to that
judgment are never themselves fabricated.

## Scope

Owns: historical capex (dollar figures, maintenance/growth split, % of revenue, YoY change, trend),
projected capex (same structure), the projected-vs-historical comparison, major projects as a structured
schedule, peer capex comparison, forward visibility, the qualitative nature-of-spend narrative, and the
capex adequacy/reinvestment judgment. Does not own EBITDA derivation (that's `financials-snapshot`), the
full cash flow statement (`financials-historical-income-statement-cash-flow`), the balance sheet
(`financials-historical-balance-sheet`), or whether the underlying asset base is structurally hard to
replicate — that's `barriers-to-entry`'s "Capital" dimension (asset value, replication difficulty,
structural vs. operational barrier), already rendered there as one of nine barrier verdicts. This skill's
own peer comparison is a narrow capex-intensity slice, not a substitute for that fuller read. This skill
re-sources its own capex figures independently via vault search rather than reusing any other skill's
already-rendered capex line.

**EBITDA cross-check, lightweight only.** Apply `references/conventions.md` so any EBITDA figure used in
the credit-implication line is named on the correct basis. If `financials-snapshot` has already run this
conversation and established an anchor EBITDA figure, note whether this skill's own figure matches; this is
not a hard dependency, and this skill proceeds independently if that skill hasn't run.

**Peer comparison, lightweight only.** If `peer-set` has already run this conversation and established
peer capex-as-%-of-revenue figures, use them for the Peer Capex Comparison section below. If it hasn't run,
say plainly that a peer comparison would require it rather than fabricating a benchmark, and don't treat
this as a hard dependency that blocks the rest of the render.

## Tone and rules

Apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a
specific disclosed figure; an internal inconsistency in the documents is evidence against trusting them
blindly, not a tiebreaker.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives). Read it and apply it. Do not expose platform plumbing (no raw tool names,
`research_search_analysis`, similarity scores, or search mechanics) in the body.

**Never force a maintenance/growth split the documents don't support.** Where only a single aggregate
capex figure is disclosed, report Total Capex only and state plainly that a split isn't disclosed — do not
estimate or infer one. Use the source's own category labels where they differ from "maintenance" and
"growth" (e.g. "sustaining," "recurring," "replacement," "expansion," "discretionary").

**Every multi-period table renders periods along the top as columns, metrics as rows.** No exceptions —
this matches the standing convention already used across the other financials skills in this suite.

**A material projected capex step-change relative to history is a specific credit flag in either
direction, not a neutral observation.** State it plainly when it occurs, and note any documented
justification (a completed build-out, a one-time historical spend rolling off, a stated expansion or
integration program); where none is disclosed, flag it, naming whether it flatters FCF (a decline) or
pressures it (an increase).

**Self-check the AI-speak tells before delivering:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period.
- No verdict-then-hedge. State the finding, then the qualifying detail as its own sentence.
- Headings name content, never function ("The read," "Overview," "Assessment" are defects).
- No hype ("prudent reinvestment," "disciplined capex program"). Lead with the fact and the figure.
- Where the documents disclose only a bare capex figure with no further description, say so plainly rather
  than manufacturing a nature-of-spend narrative that isn't there.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, `deal_list` to resolve by name. One match → use it. More than one → present as a table (Deal,
  Company, Sponsor, Status, Created; no internal IDs) and ask. Do not guess.
- If no deal is named, ask which deal first.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, and suggest retrying once analysis completes or running `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`research_search_analysis` is deferred; if not loaded this conversation, `tool_search` it first.

## STEP 1 — Retrieve (parallel batch, seven searches in one turn)

`report_type="diligence_summary"` for all seven; content-based queries only, never a hardcoded question ID:

1. `research_search_analysis(project_id, "historical capex maintenance growth replacement expansion split", top_k=7)` — historical dollar figures and any disclosed split.
2. `research_search_analysis(project_id, "projected capex forecast model maintenance growth", top_k=7)` — projected figures and any disclosed split.
3. `research_search_analysis(project_id, "capex nature major projects facilities equipment capitalized software", top_k=7)` — the qualitative nature-of-spend narrative and major projects.
4. `research_search_analysis(project_id, "depreciation amortization asset condition capacity utilization capitalization policy repairs maintenance expensed", top_k=7)` — D&A (for the adequacy ratio), any disclosed asset-condition or capacity signal, and the company's capitalization accounting policy.
5. `research_search_analysis(project_id, "capex peer comparison industry benchmark competitors recurring capital requirements", top_k=7)` — any disclosed peer or industry capex-intensity benchmark, and whether recurring capex is characterized as a competitive requirement in this industry.
6. `research_search_analysis(project_id, "capex regulatory mandated environmental safety compliance committed contractual joint venture capital call lease obligation discretionary", top_k=7)` — how much of capex is regulatory/legally mandated, contractually committed, or purely discretionary.
7. `research_search_analysis(project_id, "capex reduced deferred COVID liquidity constrained underspend catch-up backlog", top_k=7)` — any disclosed period of capex materially below normal run-rate, and any stated catch-up or deferred-maintenance commentary.

Discard results with similarity below 0.02.

## STEP 2 — Render

**Header:** deal name, sponsor, reporting currency.

**Historical Capex**

| Metric | [Period 1] | [Period 2] | ... | [Anchor Period] |
|---|---:|---:|---:|---:|
| Total Capex | | | | |
| Maintenance Capex | | | | |
| Growth Capex | | | | |
| Capex as % of Revenue | | | | |
| YoY $ Change | — | | | |
| YoY % Change | — | | | |

Periods as columns, chronological, oldest to newest, ending at the canonical anchor period. **YoY change is
not optional** — a level-only table hides the direction and magnitude of movement year to year; compute and
render both the dollar and percentage change for every period after the first. **Arithmetic check:**
Maintenance Capex + Growth Capex = Total Capex within rounding, every period both sub-categories are
disclosed. Flag, never force, a period that doesn't reconcile. Where only a single aggregate figure exists,
render Total Capex only and state the split isn't disclosed. State the intensity trend (rising, falling,
stable) and quantify it, distinct from the year-by-year YoY figures — a stable multi-year intensity can
still mask a sharp single-year swing that the YoY row will show and the trend line alone won't.

**Deferred Capex / Bow-Wave Risk.** Check whether any historical period sits materially below the
company's own multi-year average or stated normal run-rate (a COVID-era pullback, a liquidity-constrained
year, an ownership-transition gap). Quantify a shortfall if one exists ($ and % of revenue relative to
surrounding periods), and state whether the documents disclose a subsequent catch-up (spend rising back
above trend) or any explicit deferred-maintenance/backlog commentary. **Distinguish this from an ordinary
low year with a stated, non-deferral explanation** (a one-time prior project rolling off) — that's a
trend note, not a bow-wave risk. Flag Bow-Wave Risk as Elevated only where a real shortfall exists with no
stated explanation and no confirmed catch-up; otherwise state Limited or Not determinable.

**Projected Capex** (same table structure including the YoY rows, projected periods, same arithmetic check)

**Major Projects**

| Project | Cost | Timing | Status |
|---|---:|---|---|
| | | | |

A dedicated table, not a paragraph buried in prose — render every named or specifically described capital
project the documents disclose (new facilities, major renovations, large equipment purchases, large
capitalized IT builds, de novo locations, infrastructure builds), with cost and timing where available.
Exclude business acquisitions. If no specific project is named or described beyond an aggregate figure,
state that plainly and omit the table rather than rendering an empty shell.

**Projected vs. Historical.** State projected capex intensity (% of revenue) against the historical
average or trend, aligned period-for-period where possible. Flag a material step-change in either
direction, not only a decline: **a projected decline below the historical run rate can flatter projected
free cash flow** (a specific FCF-inflation risk) **and a projected increase above the historical run rate
pressures projected free cash flow downward relative to a naive extrapolation of history** (a different,
but equally real, credit-relevant signal, and it also raises the question of what's driving the step-up).
Either direction gets flagged when it's material and undisclosed; render whatever documented justification
exists (a completed build-out, a one-time historical spend rolling off, a stated capacity expansion or
integration program), or state plainly that none is disclosed.

**Peer Capex Comparison.** If `peer-set` has already run this conversation, compare this deal's capex-as-%-
of-revenue (historical and/or anchor period) against the peer figures it established, and state whether
this company runs above, at, or below the peer range. If `peer-set` hasn't run, say plainly that a peer
comparison would require it rather than fabricating a benchmark. Where any peer or industry capex-intensity
context surfaced directly in Step 1's search (without `peer-set` having run), render it and cite the
source. Apply the materiality framing directly: capex intensity below roughly 3% of revenue is generally
not a meaningful competitive requirement or barrier; above that level, a new entrant or competitor would
need comparable ongoing investment to compete, which is itself a credit-relevant fact about the industry's
structure. **This section is a narrow capex-intensity slice, not a full barriers-to-entry read.** Whether
the underlying asset base is structurally hard to replicate (third-party valuation, replication difficulty,
structural vs. operational barrier) is `barriers-to-entry`'s own "Capital" dimension, already rendered
there faithfully as one of nine barrier verdicts — point to that skill for the fuller industry-structure
picture rather than re-deriving it here.

**Forward Visibility.** State plainly how many projected years are actually disclosed, and whether the
forward capex figures are tied to specific named or committed projects versus a generic run-rate or model
assumption with no supporting detail. A short disclosed window (e.g. one or two projected years) or a
figure with no stated basis is lower-confidence than a multi-year figure grounded in named, budgeted
projects — say which case applies rather than treating every projected number as equally reliable.

**Nature of Capex.** What the spend funds (plant and equipment, facilities, technology/IT, fleet, tooling,
de novo locations, capitalized software), tied to specific assets where disclosed. Describe what
maintenance spend sustains and what growth spend builds, per the historical split above. If only a bare
aggregate figure exists with no further description, state that plainly rather than inferring a narrative.

**Capex Commitment Profile.** Classify capex by how deferrable it is under stress, distinct from the
maintenance/growth split above: regulatory or safety-mandated spend (environmental compliance, safety
upgrades, permit conditions), contractually committed spend (JV capital calls, lease-embedded capital
obligations, contract-driven capacity commitments), and purely discretionary spend the company could defer
or cancel without breaching an obligation. State the dollar or percentage split where disclosed. **A
maintenance item can be discretionary in timing while a growth item can be contractually committed — don't
conflate this classification with the maintenance/growth split.** Where the documents don't characterize
capex by commitment level, state that plainly rather than inferring discretion from the maintenance/growth
label alone. Close with an explicit Downturn Flexibility read: High (mostly discretionary), Moderate, Low
(mostly committed or mandated), or Not determinable.

**Capex Adequacy & Reinvestment.**
- **Maintenance capex vs. D&A**, same periods: state the ratio and its direction. Maintenance capex
  materially below D&A signals the asset base may be aging faster than it's being replaced, flag deferred-
  maintenance risk. At or above D&A signals reinvestment is keeping pace. If D&A isn't disclosed, compare
  Total Capex to D&A instead and note the substitution; if neither exists, state adequacy can't be
  assessed.
- **Capitalization policy check, before trusting the ratio above.** State the company's disclosed
  accounting policy for what counts as capitalized capex versus expensed repairs/maintenance. A policy that
  expenses routine repairs and capitalizes only capacity-adding or life-extending spend will structurally
  show a lower capex-to-D&A ratio without necessarily indicating under-investment — this qualifies how much
  weight the ratio above can bear, and two companies with different policies aren't directly comparable on
  this ratio alone. If no policy is disclosed, say so rather than assuming a standard one.
- **Asset-condition corroboration**, if disclosed: cross-check the capex-vs-D&A read against any stated
  asset condition (aging facilities or equipment). A low ratio alongside aging assets is a stronger signal
  than either alone.
- **Growth-constraint check**: if capacity utilization is disclosed above roughly 85% and Growth Capex is
  minimal or undisclosed, flag a potential constraint on future growth.
- **Credit implication**, one line: what the capex profile means for free cash flow available to service
  debt (e.g. sustained high maintenance capex relative to EBITDA limits FCF; a coming growth program will
  pressure near-term FCF; an under-maintained asset base may face a looming catch-up spend).

**Data gaps table** — one line per missing item, status only, no filled-in guesses.

**Source citations** at the bottom.

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time.
1. **Confirm every figure traces to a retrieved chunk.** A number in a table or commentary not backed by
   Step 1's results is fabricated; remove it or re-search.
2. **Re-run the arithmetic check.** Maintenance + Growth = Total, within rounding, for every period both
   sub-categories are disclosed, historical and projected alike.
3. **Confirm no split was forced.** Where only an aggregate figure exists, confirm the render says so
   plainly rather than presenting an inferred maintenance/growth breakdown.
4. **Confirm the step-change flag fired if warranted, in either direction.** If projected capex intensity
   is materially above or below the historical trend, the render must flag it, with or without a stated
   justification, and name which direction of risk applies (FCF-flattering decline vs. FCF-pressuring
   increase).
5. **Confirm every multi-period table has periods as columns, metrics as rows.**
6. **Confirm the adequacy judgment's inputs are real, not assumed.** The D&A figure, the capacity
   utilization figure, and any asset-condition signal used in the adequacy section must each trace to a
   retrieved chunk; where any is missing, the corresponding check states insufficient disclosure rather
   than proceeding on a guess.
7. **Confirm data gaps are reported, not filled.**
8. **Confirm YoY change was computed and rendered for every period after the first**, both historical and
   projected, not just the levels.
9. **Confirm the Major Projects table only includes projects the documents actually name or specifically
   describe.** A generic capex category is not a project; don't manufacture entries to fill the table, and
   omit the table entirely if nothing qualifies.
10. **Confirm the peer comparison correctly used `peer-set`'s output if that skill ran this conversation**,
    and correctly declined to fabricate a benchmark if it didn't.
11. **Confirm the Forward Visibility assessment names an actual basis** (specific named projects vs. a
    generic model assumption) rather than asserting confidence without grounding it in what Step 1 found.
12. **Confirm the Bow-Wave check didn't over-fire on an ordinary explained low year.** A shortfall with a
    stated, non-deferral explanation is a trend note, not an Elevated bow-wave risk; confirm the
    distinction was actually applied, not just the shortfall detected.
13. **Confirm the Commitment Profile classification wasn't conflated with the maintenance/growth split.**
    These are two different cuts of the same spend; a maintenance item can be discretionary and a growth
    item can be committed. Check that the render kept them separate.
14. **Confirm the capitalization policy check ran before the adequacy ratio was presented as conclusive.**
    Where a policy is disclosed that skews the ratio (e.g. repairs expensed, not capitalized), the render
    must qualify the ratio's weight accordingly, not present it as a clean, comparable figure.

Findings weave into the render in place; nothing labeled "second read" reaches the output.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

Read the finished piece top to bottom once more and fix: **tone** (credit-desk register, no hedge-then-
verdict, no hype); **platform plumbing** (no raw tool or parameter names anywhere in the body);
**headings** (clean, parallel, name content); and a **literal proofread** of every heading and figure. Scan
literally for the em-dash character and replace each with a comma, semicolon, or period. Silent; its only
evidence is a cleaner artifact.

## Rules

- Flag Bow-Wave Risk as Elevated only where a genuine shortfall exists with no stated non-deferral
  explanation and no confirmed catch-up; an explained low year is a trend note, not a bow-wave finding.
- Keep the Commitment Profile classification (discretionary/committed/mandated) separate from the
  maintenance/growth split; never conflate the two even though they can overlap in either direction.
- Check the capitalization policy before treating the capex-vs-D&A ratio as conclusive; state the policy if
  disclosed, and qualify the ratio's weight accordingly if it skews toward expensing routine spend.
- Never force a maintenance/growth split the documents don't support; report Total Capex only and say so
  when no split exists.
- Mandatory arithmetic check every period: Maintenance + Growth = Total Capex within rounding. Flag, never
  force, a mismatch.
- Every multi-period table renders periods as columns, metrics as rows, with no exceptions, and includes a
  YoY $ and % change row, not just levels.
- Render Major Projects as a dedicated table, never folded into prose; omit it entirely if no specific
  project is named or described.
- A material projected capex step-change relative to history is a specific credit flag in either
  direction; state it plainly, with or without a documented justification, and name which risk applies.
- Peer comparison reuses `peer-set`'s output if that skill has already run this conversation; never
  fabricate a peer benchmark if it hasn't. Apply the roughly-3%-of-revenue materiality threshold when
  assessing whether capex intensity represents a real competitive requirement.
- State forward visibility explicitly: how many projected years are disclosed, and whether they're grounded
  in named projects or a generic model assumption.
- The adequacy judgment's inputs (D&A, capacity utilization, asset condition) must each trace to a
  retrieved figure; state insufficient disclosure rather than guessing where any is missing.
- Fully independent: re-source capex figures via this skill's own vault search rather than reusing another
  skill's already-rendered capex line. The EBITDA basis cross-check against `financials-snapshot` is
  lightweight only, never a hard dependency.
- Never hardcode a question ID for any search in this skill; search by content, since prompt IDs get
  renumbered.
- No platform plumbing in the body: no raw tool or parameter names, no similarity scores.
- Flag data gaps plainly rather than filling them.
- Second read and final review are mandatory, separate, and silent; the evidence they ran is a changed
  artifact, never a narrated process block.

## Delivery

Render in chat by default. Only produce a Word document if asked; when generating one, use the docx skill
with a title block (deal name, sponsor, currency) and the same section structure as the chat render. Save
to `/mnt/user-data/outputs/` and `present_files`. After delivering, offer one natural next step: a deeper
look at a specific flagged risk or gap, the `financials-snapshot` read if EBITDA hasn't been pulled yet, or
the Word export if the read was in chat.
