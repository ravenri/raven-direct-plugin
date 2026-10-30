# Render specs

Four possible sections, rendered in this order whenever more than one is wanted: §0 (fast-path,
only when nothing else is asked for), §1 (the walk, picks `anchored_ebitda`), §2 (debt terms),
§3 (the cap table, strikes every leverage multiple on the anchor). Render the walk before the
cap table so the reader sees where the denominator came from before the multiples that use it;
render terms before the cap table so the reader knows what each tranche costs before seeing
where it sits in the stack.

Forward projections (leverage / coverage / PIK over time) are out of scope for this Skill and
belong to a separate projections skill. Do not render a forward view here.

---

## 0. Fast-Path Anchor Card

For when the person wants only the anchor figure, not a walk, terms, or cap table, e.g. "which
EBITDA are we using," "what's the anchor," "quick EBITDA check." One short block, no table:

- **Figure and layer** — the anchored_ebitda value and its canonical title (never "anchor
  EBITDA" in output — say "Adjusted EBITDA," "Pro Forma Adjusted EBITDA," or "PF Adjusted Cash
  EBITDA," whichever it actually is).
- **Period** — the dated anchor period (e.g. "LTM Jun-26E, ended June 30, 2026"), never LTM
  computed by this Skill.
- **Confidence** — indicative, or validated, per whether Q1001 records a `validated_by` status
  for this period's bridge. State the reason in one clause if indicative (e.g. "no line-specific
  QoE validation recorded for this period").
- **One evidence pointer** — a single source citation (document, page), enough to check the
  figure exists in a document, not the full sourcing table.

Close with one line offering the full walk: "Full reconciliation available on request." Do not
render the bridge_table, sourcing block, or commentary unless asked, that's §1.

---

## 1. EBITDA Reconciliation Walk

Not a re-derivation. This renders Q1001's already-computed walk (its classification,
QoE-validation status, and commentary per line) plus Q1210's per-layer source-document
citations, so the reader can check the anchor against a document rather than take it on faith.
Don't re-classify or re-judge any line; carry Q1001's assignment as-is.

**bridge_table** — columns [Adjustment ($MM), <each disclosed period, most recent last>, Type].
Rows, in walk order, using Q1001's `walk` array directly:
- **Reported EBITDA** (base) — `reported_ebitda`.
- One row per adjustment, `line_item` label verbatim, `values` by period. Add-backs shown as
  "+", deductions in parentheses.
- **Adjusted EBITDA** (subtotal) — `adj_ebitda`.
- **Pro Forma Adjusted EBITDA** (subtotal) — `pf_adj_ebitda`, only if the documents disclose a
  separate PF layer distinct from Adjusted (synergy / run-rate lines sit between the two
  subtotals). If there is no separate PF layer, omit this row, don't manufacture it.
- **PF Adjusted Cash EBITDA** — `pf_adj_cash_ebitda`, software / recurring-revenue deals only,
  where disclosed. Sits one line below PF Adjusted EBITDA, per Q1210.

Mark which row is `anchored_ebitda`.

**sourcing** — for each layer actually shown (Reported / Adjusted / PF Adjusted / PF Adjusted
Cash), cite the source document(s) and page(s) Q1210 recorded for that layer, e.g. "Adjusted
EBITDA: Sponsor Executive Summary (July 2026), p.68." This is the disclosure backbone, the
reason the anchor is checkable rather than asserted, never omit it. Note the limit plainly:
Q1001's line items carry a classification and a QoE-validation status but not an individual
source page each, so the citation is per layer, not per adjustment line, unless a line's own
`commentary` happens to name a specific document. Don't imply a precision the data doesn't
have.

**footnote** — total addbacks from Reported to the anchored EBITDA ($ and % of anchored
EBITDA); whether a separate PF layer exists and, if so, the synergy $ and validation status
(sponsor-only / third-party / management-agreed); the leverage-basis reminder ("leverage
strikes on <anchored EBITDA name> $X"); the confidence flag if indicative. When PF exists and
differs from Adjusted, state both figures so the synergy uplift is visible. When the anchor is
`pf_adj_cash_ebitda`, state both figures too, the deferred-revenue-adjusted anchor and the
accrual PF Adjusted (or Adjusted) figure, plus the delta amount and direction.

**commentary** — one bullet per adjustment larger than 3% of Reported EBITDA (Q1001/Q1002's own
threshold), largest / most judgmental first: [name ($MM)], its `adj_type` → defensibility
(noncash → high, nonrecurring → medium, normalising → low, synergy → low), its `validated_by`
status if Q1001 records one (confirmed / reduced / reversed by QoE, or none), then one plain
sentence from Q1001's own `commentary`. Do not re-derive or re-judge the classification, carry
it. If no line exceeds 3%, give brief general commentary and name the 3-4 largest.

---

## 2. Debt Terms Outline

The proposed (or closing) terms per tranche, from Q104 only. This is identity and economics,
not leverage, no multiples or dollar amounts belong here beyond what a term itself requires
(e.g. an unused fee rate). Split into two groups, senior to junior within each:

**New Money** — tranches funded or newly committed at close (e.g. Incremental Senior Term
Loan, Incremental HoldCo Notes, a new Revolver or DDTL commitment).

**Existing / Rolled** — tranches carried over from the prior capital structure (e.g. Rollover
of Existing Senior Term Loan, Rollover of Existing HoldCo Notes, Rollover of Existing Capital
Leases).

For each tranche within its group, one row:

| Instrument | Amount ($MM) | Pricing Basis | Cash-Pay / PIK | Amortization | Fees |
|---|---|---|---|---|---|

- **Amount ($MM)** — funded amount for funded tranches; committed amount for undrawn
  commitments (revolver, DDTL), labelled "(committed, undrawn)" so it's not read as drawn.
  From Q104 / the cap structure.
- **Pricing Basis** — floating (benchmark + spread + floor, e.g. "SOFR + 3.50%, 0.50% floor")
  or fixed (coupon, e.g. "16.5% fixed"). From Q104 term #7.
- **Cash-Pay / PIK** — cash-pay, PIK, or PIK-toggle. If toggle, state the election mechanic and
  any rate step-up from Q104 term #20. From Q104's roster field and term #20.
- **Amortization** — per annum rate or "None." From Q104 term #16.
- **Fees** — the undrawn/commitment (unused) fee for revolver and DDTL, and any other stated
  fee, folded into this one column rather than a dedicated unused-fee column. "None" for
  fully-funded term tranches with no separate fee. From Q104 term #9 (fees).

Where a term isn't disclosed for a given tranche, state "Not disclosed" in that cell, don't
infer from another tranche's terms or from market convention. Don't include maturity, call
protection, covenants, or other Q104 fields not listed above unless the person specifically
asks for them, this outline is scoped to what determines cash service and PIK accretion, which
is what the cap table downstream depends on.

**Never take a terse multi-column facility table at face value on which value belongs to which
facility — confirm it against a second source first.** A summary-terms table formatted as
"Term | Facility A value | Facility B value" (a common presentation-deck pattern) is genuinely
easy to misattribute: a term that reads naturally as belonging to the first-listed facility can
actually belong to the second, and market convention alone (e.g. assuming a term loan carries
amortization and a revolver doesn't) is not a substitute for confirming it. Confirmed live on
One deal: a two-column "Revolving Credit Facility | Term Loan B" table's amortization and
call-protection rows were initially misattributed to the revolver; a second, independent
tranche-level source (the deal's own debt registry, stated in prose per-tranche rather than a
compressed table) confirmed both terms actually belong to the Term Loan B. Where only the
compressed table is available and no second source exists, say so explicitly rather than
asserting an attribution with unwarranted confidence — "the table lists both a Revolver and Term
Loan B value for this term; which applies to which is not independently confirmed" is the
honest rendering, not a guess dressed as a fact.

**"Not disclosed" and "genuinely confirmed absent" are different findings — state which one
applies.** Where pricing (spread, benchmark, floor, OID) isn't in the table you're reading, check
whether a separate record (an interest-rate-risk read, a debt registry, a diligence-gaps note)
explicitly confirms the gap as real and flagged by the deal's own analysis, versus merely being
absent from the one search that happened to be run. The former is a stronger, more useful
finding — it means the underlying documents themselves lack the term, not that it was missed by
an incomplete search.

---

## 3. Opening Capital Structure

The pro forma capital structure at close, with every multiple struck on `anchored_ebitda` (the
most-adjusted disclosed layer, per anchor-resolution.md, accrual for most deals, the
deferred-revenue-adjusted figure for software / recurring-revenue deals where that's disclosed),
for the anchor period only — never a projected year.

**cap_table** — two running cumulative columns, populated at every row, not just class
subtotals. Columns: [Instrument, Committed ($MM), Funded ($MM), Debt/EBITDA (cum),
Debt/EBITDA-capex (cum), Cum. LTV, Notes]. Attach of one layer always equals detach of the prior
layer, and cushion is just 100% minus Cum. LTV, so the running columns carry that information
without a separate Attach/Cushion pair. `Debt/EBITDA (cum)` = cumulative funded debt through and
including the row ÷ `anchored_ebitda`. `Debt/EBITDA-capex (cum)` = the same cumulative funded-debt
numerator ÷ (`anchored_ebitda` minus anchor-period capex). Capex is sourced to the same standard
as the anchor: a disclosed actual where one exists, otherwise the matching-period "Less: Capex"
figure from the deal model when the anchor is itself an estimated / projected period. Flag the
capex source (disclosed actual vs. model-projected) in the footnote. Show "n/d" only if no capex
figure exists anywhere.

**Analyst note (n/d case)** — whenever Debt/EBITDA-capex (cum) or Total gross leverage (EBITDA
less capex) shows "n/d", attach this standard two-line note inline next to the field, so the
reader sees why it's blank rather than reading it as a missed pull:

> **n/d** — no capex figure aligns with the anchor period, either disclosed or from the model.
> Nearby capex data (a different period) isn't substituted here to avoid estimating.

Use this note verbatim; don't reword per deal. If nearby-period capex exists (e.g. a later
disclosed actual, or a model line that starts after the anchor), that's the case the note is
describing, don't spell out the specific nearby period/figure inline, that belongs in the
footnote instead if it's worth surfacing.

Rows, in priority order through the waterfall:
- Each debt tranche as actually disclosed for the deal (e.g. RCF, TLA, TLB, senior secured
  notes, secured/unsecured bridges, rolled debt), each carrying:
  - **Debt/EBITDA (cum)** — running total of funded debt through and including this row, ÷
    `anchored_ebitda`. Pull from the vault's assembled capital-structure waterfall if it's
    already struck on the same `anchored_ebitda`; if the vault used a different denominator,
    or didn't produce a per-tranche figure, compute it directly, it's a plain running sum, not
    an inferred fact.
  - **Debt/EBITDA-capex (cum)** — the same running total of funded debt ÷ (`anchored_ebitda`
    minus anchor-period capex). Same numerator as Debt/EBITDA (cum), different denominator.
    Compute directly, it's a plain calculation on disclosed figures. Capex is sourced to the same
    standard as the anchor: a disclosed actual where one exists, otherwise the matching-period
    "Less: Capex" figure from the deal model when the anchor is an estimated / projected period;
    flag which source in the footnote. Show "n/d" only if no capex figure exists anywhere.
  - **Cum. LTV** — the same running total ÷ disclosed EV. Where tranches are pari passu within
    a class (no disclosed sub-ranking), it's fine for the per-tranche Cum. x EBITDA / Cum. LTV
    to only be meaningful at the class-subtotal and last-tranche-in-class rows; show the
    running number anyway at intermediate rows (it's still a valid cumulative fact), but don't
    manufacture a sub-ranking within a pari passu class that isn't disclosed.
  - Where EV isn't disclosed at all, show "n/d" for Cum. LTV only, Cum. x EBITDA still
    computes without an EV.
- **Total Senior / First-Lien Debt** (subtotal) — cumulative through this point (the senior
  detachment point).
- **Total Junior Debt** (subtotal), if the deal has one — cumulative through this point (the
  total-debt detachment point).
- **Less: Cash** — net adjustment row.
- **Total Net Debt** — net cumulative figure.
- Sponsor Equity (+ rolled equity if applicable).
- **Total Capitalization** (total) — EV and entry EV multiple, Cum. LTV = 100%.

**leverage_metrics** — a compact block, structural and point-in-time only, every multiple
struck on `anchored_ebitda` and the anchor period, labelled with its basis:
- 1L gross leverage = `senior_debt` / `anchored_ebitda`
- 1L net leverage = (`senior_debt` − `cash`) / `anchored_ebitda`
- Total gross leverage = `total_debt` / `anchored_ebitda`
- Total net leverage = (`total_debt` − `cash`) / `anchored_ebitda`
- Total gross leverage (EBITDA less capex) = `total_debt` / (`anchored_ebitda` − anchor-period
  capex), capex sourced to the same standard as the anchor (disclosed actual, else matching-
  period model "Less: Capex" when the anchor is estimated); flag the source. Show "n/d" only if
  no capex figure exists anywhere. Same analyst note as the cap_table spec above.
- Entry EV multiple = `enterprise_value` / `anchored_ebitda`.
- Equity cushion ($ and % of capitalization).

Interest coverage, DSCR, and fixed-charge coverage still don't belong in this block: they need
interest expense on the post-close structure, which is modeled even at close, not a disclosed
actual. Don't add an "Interest coverage: 3.3x" line just because the number exists somewhere in
the documents. EBITDA-less-capex is the one exception, per the cap_table spec above, since its
capex is sourced to the same standard as the anchor it sits beside (a disclosed actual, or the
matching-period model "Less: Capex" when the anchor is itself estimated) rather than needing
modeled post-close interest. The
opening cap table still answers "what is the structure and how levered is it" rather than "can
it service the debt" — that's the line EBITDA-less-capex sits on, and coverage ratios proper
stay with Q1161 in the vault (cash-pay basis, correctly excludes PIK) or the separate
projections skill for a forward path.

When a separate PF layer exists AND differs from Adjusted, show the pre-synergy look-through
leverage (gross and total, same anchor period, struck on `adj_ebitda` instead) beside the
headline multiples — per the anchor-resolution invariant, never present a synergy-inflated
multiple without it.

When the anchor is `pf_adj_cash_ebitda` (software / recurring-revenue deals), show the accrual
look-through leverage (gross and total, same anchor period, struck on `pf_adj_ebitda` or
`adj_ebitda` instead) beside the headline multiples, same discipline, stated directionally
(deferred-revenue build pushes cash EBITDA and leverage one way, unwind pushes the other).

**footnote** — state the denominator explicitly by its actual layer name ("all multiples
struck on <PF Adjusted Cash | PF Adjusted | Adjusted> EBITDA $X" — whichever is the anchor for
this deal); note gross vs net where both are shown; carry the confidence flag; where a
separate PF layer exists, flag synergy load if > 10% of `anchored_ebitda` and show what total
leverage would be on Adjusted (pre-synergy) alongside; where the anchor is
`pf_adj_cash_ebitda`, show what total leverage would be on the accrual figure alongside,
directionally; flag any tile-vs-vault conflicts found while resolving the cap structure (see
anchor-resolution.md) rather than resolving them silently.

**commentary** — 3 to 5 bullets: entry leverage (gross and net, with basis); equity cushion;
senior vs total attach and the junior cushion between them; liquidity (cash + undrawn
revolver); any floating-rate / hedging exposure; synergy dependency if > 10%. Per house-style's
rule against freestanding adjectives: where the vault has its own qualitative assessment of the
structure (e.g. Q1162's Coverage & Structure Assessment — "moderate-to-aggressive," a cushion
quality note, a de-levering read), pull the characterization from there and cite what it's
based on, rather than adding an independent read of "elevated" or "thin" that isn't traceable
to a vault note. If Q1162 wasn't pulled for this deal, state the numbers plainly without a
qualitative gloss rather than supplying one.

If the person also wants to see how leverage moves forward, that's out of scope for this Skill,
a separate projections skill owns forward views. Don't render a projection table here, and
don't pull the deal's financial model to build one, even if periods might seem to line up. Say
plainly that this Skill covers the anchor, terms, and opening structure only.
