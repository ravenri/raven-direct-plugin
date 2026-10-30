# Conventions — EBITDA basis and period selection (shared across skills)

Shared verbatim from the platform's own system rule package
(`audit-conventions-and-rules/references/rules/ebitda.py` and `periods.py`), which is itself sourced
from the Credit Vault Prompt Workbook's Conventions layer (native Q1210 EBITDA Layer Catalog and Q1201
Canonical Period Anchors). Copied here rather than re-derived, so this skill's anchor logic matches the
platform's own definitions exactly instead of drifting from a separately-written approximation.

**Do not cite a question ID when searching for this content live.** Prompt IDs in this system get
renumbered, and the same conventions answer has been observed under more than one ID scheme depending on
which layer of the system serves it. Search by content and category (`conventions`) instead — see the
skill's own Step 2.5 / Tone and rules section for how this file's definitions get checked against a live
deal.

---

## EBITDA definitions and basis discipline

Deals disclose several EBITDA figures under several names. Reporting the wrong one, or reporting one
without naming it, is how the same company ends up with different earnings on different pages. Use the
definitions below, and name the figure every time you use it.

**The documents define the content.** Use the labels the documents use, and let the documents determine
what falls into each figure. Do not impose an independent definition of EBITDA, and never infer or
construct a figure the documents do not state. The role descriptions below describe typical content so a
label can be mapped to a role — they are not a definition to enforce against the documents.

**The four canonical roles:**
- **Reported EBITDA** — EBITDA per the financial statements before adjustments; the unadjusted starting
  point.
- **Adjusted EBITDA** — the borrower's primary adjusted figure, and the one predominant in credit
  analysis. Typically adds back non-cash items (stock-based compensation, impairments), non-recurring or
  one-time costs (restructuring, transaction and deal costs, litigation), and normalizing items (owner
  compensation, discontinued lines) — that is, adjustments to results already earned. Idiosyncratic labels
  such as "Sponsor Adjusted" or "Management Adjusted" map here when they describe the borrower's primary
  adjusted figure.
- **Pro Forma Adjusted EBITDA** — the further-adjusted figure, present only where the documents disclose
  it separately from Adjusted EBITDA. Typically layers forward-looking or transaction-driven items on top:
  run-rate cost savings, synergies, the annualized effect of acquisitions or price increases, and other
  not-yet-realized adjustments — that is, items reflecting a future or pro forma state rather than results
  already earned. Where the documents disclose only one adjusted figure, there is no separate pro forma
  layer; do not invent one.
- **PF Adjusted Cash EBITDA** (software and recurring-revenue deals only) — Pro Forma Adjusted EBITDA
  further adjusted for the period change in short-term deferred revenue, converting the figure from an
  accrual basis to a cash-collections basis. A decrease in deferred revenue is subtractive, an increase
  additive. Where the current/non-current split is not disclosed, use total deferred revenue. Do not apply
  it where the source's adjusted figure already includes the deferred-revenue movement; in that case state
  that it is already included. It sits one line below Pro Forma Adjusted EBITDA in the walk.

**The operative (anchor) figure** for the deal is the most-adjusted EBITDA the documents disclose: Pro
Forma Adjusted EBITDA, or Adjusted EBITDA where there is no separate pro forma figure. For software and
recurring-revenue deals where the documents present the deferred-revenue adjustment, it is PF Adjusted
Cash EBITDA. Where the credit is against a combined group rather than a single company, the operative
figure is the combined-group figure the combined presentation gives — never build one by summing
constituents. If an operative figure has already been established for this deal, use it and do not
re-select; otherwise select it by this rule and hold it for everything produced.

**Name it by its canonical title.** When reporting the operative figure, call it by its canonical title —
Reported EBITDA, Adjusted EBITDA, PF Adjusted EBITDA, or PF Adjusted Cash EBITDA. Never write "anchor
EBITDA," "operative EBITDA," or any internal shorthand in output a reader sees; those are role names for
reasoning, not labels for the page.

**The leverage basis rule.** Every leverage, coverage, and attachment multiple strikes on the operative
figure, and names the EBITDA it is struck against. A multiple without its basis is not a usable fact: 4.4x
against Reported and 4.4x against PF Adjusted are different statements about the credit. Where two related
figures across different sections appear to contradict, the cause is usually an unnamed basis rather than
an error. Leverage multiples strike on drawn debt, not committed; undrawn facilities are excluded, and
committed vs. drawn are stated separately where both are disclosed.

**Software deals — keep the accrual figure visible.** Where the operative figure is the
deferred-revenue-adjusted one, always disclose alongside it both the deferred-revenue adjustment amount
and the accrual pro forma or adjusted figure, stated directionally (e.g. "absent the deferred-revenue
adjustment, EBITDA would be $X and leverage lower"). The accrual figure must never disappear behind the
cash figure.

**Mapping idiosyncratic labels.** Where a label is idiosyncratic ("Financing EBITDA," "Financeable
EBITDA," "Run-Rate EBITDA"), map it to the closest of the four roles and state the reasoning in one
sentence. Where two or more differently-labeled figures map to the same role, keep them as separate
entries with their own values and sources rather than merging them, and state which one governs. A
disclosed EBITDA corresponding to none of the four roles (a segment EBITDA, a covenant-specific EBITDA) is
not one of these figures and need not be carried, unless it is an alias of one of them.

**Add-backs and synergies — label the status.** Every add-back and synergy figure names its status:
identified, included in the adjusted or pro forma figure, or targeted run-rate. Where the operative figure
includes cost saves or synergies, state the dollar amount, the label the documents use (in their exact
term), and the validation status (sponsor-identified only, third-party validated, or agreed with
management, naming the validating source). Where it includes none, say so explicitly. Status labeling is
for clarity, not for surfacing a discrepancy: two figures that differ only because one includes synergies
and the other does not are not in conflict once both are labeled.

**The walk must be honest, not tidy.** A reconciliation walks Reported to Adjusted to Pro Forma Adjusted,
in that order: base, then typed add-backs and deductions, then a subtotal, then synergies, then the total.
Deductions carry negative values. Where the documents disclose no pro forma layer, the walk ends at the
subtotal. Where a walk's total legitimately differs from the operative figure, do not force it to
reconcile — state both and note the difference; a forced reconciliation hides exactly the fact a credit
committee needs.

**When sources disclose different values.** Where two sources disclose a differing value for the same
role in the same period beyond a trivial rounding difference, report both with their sources and state
that they diverge. Do not average them, and do not silently prefer one.

---

## Period conventions

Every deal has ONE canonical anchor period and ONE historical range. Every headline figure, and every
leverage, coverage, and attachment multiple, is struck on the anchor. If an anchor has already been
established for this deal, use it exactly and do not revisit the choice; otherwise determine it by the
rules below and hold it for everything produced.

**Period vocabulary.** Every period has a TYPE (q1, q2, q3, fiscal_year, or ltm) and a BASIS (actual,
budget, forecast, or estimate). A period may additionally be PRO FORMA, orthogonal to type: an LTM
presented pro forma for an acquisition is type=ltm, pro_forma=Yes. Where a period is pro forma, describe
the adjustment behind it (acquisition, synergies, divestiture, or other). A period is a distinct point in
time, identified by its end date — "2023 A" and "FY 2023" are the same period when they share an end date;
carry it once, noting both labels, never as two columns.

**The actual periods boundary** is the most recent fiscal year with disclosed actuals. This bounds the
historical range but is not necessarily the anchor — a deal can have actuals through FY2025 and still be
anchored on an LTM or a current-year expected figure. Establish it separately and do not conflate the two.

**Selecting the canonical anchor:**
1. Determine the fiscal year in progress as of the analysis date, using the company's own fiscal
   year-end, not the calendar year. Any period that is not a fiscal_year or ltm period is ineligible for
   the anchor position.
2. If the documents disclose a TTM/LTM period ending within that fiscal year, the anchor is that period.
   Use it as disclosed; do not calculate it. Where more than one such TTM/LTM exists, the anchor is the
   most recent one, in whichever document discloses it, including a later addendum or supplement.
3. If no TTM/LTM ends within the current fiscal year, the anchor is the full-year expected figure for the
   current fiscal year (e.g. FY2026E).
4. Never anchor on a q1/q2/q3 period. Never construct a period the governing source does not state.
5. Where the credit is against a combined group rather than a single company, the anchor is the
   combined-group period the combined presentation itself gives; do not assemble one from constituents.

Name the anchor, its end date, its type, whether it is actual or projected, and the document that
discloses it.

**The historical range** is the full span of disclosed actual fiscal years, earliest through the most
recent fiscal year with actuals. Do not drop an interior year for being volatile, anomalous, or
inconvenient. Where a year is missing one metric, keep the year and note the gap in that metric.

**The forecast horizon** is the projection range as disclosed; where none exists, say so rather than
extending history forward.

**Type eligibility — the rule violated most often.** Annual analysis is drawn only from `ltm` and
`fiscal_year` periods. A q1/q2/q3 period may never appear in the historical financials table or any
annual series, the EBITDA reconciliation or bridge, any leverage/coverage/attachment multiple, or the
canonical anchor position. Quarterly periods are the correct basis for intra-year work: seasonality,
working-capital swings, liquidity troughs, covenant testing dates, and current-period performance. Where
used, label them explicitly as quarters and never mix them into an annual series.

**Stub periods.** A partial-period figure is not comparable in magnitude to a full period. Where a stub
appears beside full periods, flag it as a stub and treat any level comparison as directional only.

**Never construct a period.** Report only periods a source states. Do not build an LTM by summing
quarters, do not annualize a partial period, and do not interpolate a missing year, even when the
arithmetic looks obvious. Once rendered, a constructed period is indistinguishable from a disclosed one,
which is what makes it dangerous.

**Labeling.** Use the period label as the source discloses it, verbatim. Do not restyle "LTM 6/30/24"
into "TTM Jun-24," or "FY 2023" into "2023A." In any annual series at most one LTM-style label may appear,
and only in the final position; earlier interim or LTM disclosures belong in current-period analysis, not
the annual series.

**Ordering** is chronological, always: oldest on the left, most recent on the right, in tables, series,
and chart axes alike.

**Actual versus projected.** Where a series mixes them, the boundary must be visible; a reader must never
have to infer where history ends and forecast begins.

**Misaligned period sets.** Some statements legitimately render on their own period set (a balance sheet
on fiscal year-ends plus an interim, a cash flow statement on a shorter window). Where a set cannot align
to the annual periods, render it on its own disclosed periods and note the difference once. Do not
force-fit it or pad it with nulls to match a series it does not belong to.

**Comparison discipline.** Compare like with like: a year-over-year read pairs a period with the same
period type one year earlier, never a stub against a full prior-year quarter, and never an LTM against a
fiscal year without saying so. State the comparison basis wherever the pairing is not self-evident.

**Every figure carries its period.** State the period any figure belongs to; a figure without a period is
not a fact a credit committee can use.
