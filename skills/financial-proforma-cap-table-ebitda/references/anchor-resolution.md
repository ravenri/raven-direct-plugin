# Anchor Resolution

The anchor block is the set of headline figures every output in this workflow agrees on. It is
**resolved once, from the vault**, before rendering anything. Selecting the anchor is a
lookup and a fallback rule applied to the vault's disclosed layer figures, not a rendered
reconciliation, that's what stops leverage being struck on one EBITDA figure while the cap
table foots to another.

Resolve the anchor FIRST. Never scrape the headline EBITDA or leverage from a dashboard tile —
tiles routinely mislabel which layer they are showing (a tile may print the deferred-revenue
*cash* line under a "PF Adj. EBITDA" label, or strike leverage on the cash line). Go to the
vault reconciliation and read by field.

## The anchor block

Pull the vault EBITDA reconciliation (Q1001), the EBITDA layer catalog (Q1210), the period
anchor (Q1201), and the canonical capital-structure table (e.g. Q1160) via
`research_search_analysis`. Use `dashboard_get`'s cap/coverage tile only as a secondary
cross-check on the debt stack, never as the primary source. Read the EBITDA layers by FIELD,
not by the source's words.

**There are up to four EBITDA layers. Read all that are disclosed, then SELECT the anchored EBITDA
one — do not assume PF exists.** For each layer, also capture the source document(s) Q1210
records for it — the render spec cites these per layer so the reader can check the walk
against a document instead of taking the headline figure on faith.

| Layer field | Source | Role |
|---|---|---|
| `reported_ebitda` | Q1001 / Q1210 | Unadjusted floor of the layer list. Never a headline. |
| `adj_ebitda` | Q1001 / Q1210 `adj_ebitda` | Reported + normalizing add-backs. |
| `pf_adj_ebitda` | Q1210 — ONLY if a separate PF layer is disclosed | Adjusted + pro-forma overlay (synergies / run-rate saves). **Often absent.** |
| `pf_adj_cash_ebitda` | Q1210 — software / recurring-revenue deals only, gated on the software trigger | PF Adjusted EBITDA converted for the period's movement in short-term deferred revenue (delta sourced from Q2048/Q2068). **For software / recurring-revenue deals, this is the anchor when disclosed — it supersedes accrual PF Adjusted as the leverage basis, it is not an overlay sitting beside it.** |

**Anchor selection (the fallback chain — this is the anchor):**

`anchored_ebitda` = the first of these that applies:
1. `pf_adj_cash_ebitda` — if the deal is software / recurring-revenue AND the deferred-revenue-
   adjusted figure is disclosed. This branch takes priority over the accrual chain below; for
   these deals the deferred-revenue-adjusted figure is the leverage basis, not an overlay.
2. Otherwise, the most-adjusted accrual layer actually disclosed:
   a. `pf_adj_ebitda` — if the documents disclose a separate PF layer distinct from Adjusted;
   b. else `adj_ebitda`;
   c. else `reported_ebitda`.

`pf_adj_cash_ebitda` only exists at all on software / recurring-revenue deals, and even there
it's absent if the deferred-revenue delta isn't disclosed — in that case fall through to the
accrual chain as normal. If Q1210 says "No separate PF layer disclosed — Adjusted EBITDA is
the most-adjusted figure," then `anchored_ebitda` = `adj_ebitda`. (On many deals `adj_ebitda`
and `pf_adj_ebitda` are the same number because there is no separate PF layer — then they
collapse and there is no double-count.)

**Whenever `pf_adj_cash_ebitda` is the anchor:** always carry the accrual PF Adjusted (or
Adjusted, if no PF layer) figure alongside it, stated directionally (e.g. "absent the
deferred-revenue adjustment, EBITDA would be $X and leverage lower/higher"). Never show the
deferred-revenue-adjusted anchor without the accrual figure beside it — same discipline as
never showing a synergy-inflated multiple without the pre-synergy figure.

**Combination / merger deals:** where the deal is a combination (two operating businesses
merging, or a material add-on combining with the platform), the anchor period, the anchor
EBITDA, and everything struck on it use the combined-group figures the combined model
presents. Never build a combined figure yourself by summing the acquiror's and target's
separate EBITDA, debt, or period figures — read the combined-group figure the documents
already present. This does not apply to portfolio companies that simply happen to have
multiple entities under one holdco with no combined model; that's still a single-entity
analysis.

**When a separate PF layer exists AND differs from Adjusted:** carry BOTH figures, plus the
synergy dollar amount and validation status (sponsor-only / third-party / management-agreed,
from Q1210), and show what leverage is on each — never present a synergy-inflated multiple
without the pre-synergy figure beside it.

Remaining anchor fields:

| Anchor field | Source | Role |
|---|---|---|
| `period_anchor` | Q1201 | e.g. FY2024 with date. LTM is never computed — use the disclosed dated anchor. |
| `total_debt` | Vault capital-structure table (e.g. Q1160) — primary; cap/coverage tile is a secondary cross-check only | Total funded debt at close. |
| `senior_debt` | Vault capital-structure table (e.g. Q1160) — primary; cap/coverage tile is a secondary cross-check only | First lien / senior funded debt. |
| `cash` | Vault capital-structure table (e.g. Q1160) — primary; cap/coverage tile is a secondary cross-check only | Balance-sheet cash at close. |
| `enterprise_value` | Vault capital-structure table (e.g. Q1160/Q1103) — primary; cap/coverage tile is a secondary cross-check only | For LTV. Per Q1103's hierarchy: (1) a disclosed purchase price / stated EV, excluding fees; (2) if absent, total capitalization less transaction fees as a proxy; (3) if neither exists, not determinable — don't construct one from market comparables. For a combination deal (see below), sum the acquiror's and target's individually disclosed EVs as a proxy if no combined figure is stated. |
| `equity_contribution` | Vault capital-structure table (e.g. Q1160) — primary; cap/coverage tile is a secondary cross-check only | $ and % of capitalization. |
| `synergy_load` | Q1210 synergies ÷ anchored_ebitda | Only meaningful when a PF layer exists. Flag if > 10%. |

## The invariants (never violate)

1. **Leverage strikes on `anchored_ebitda`, whatever layer that turns out to be.** For most
   deals that's the most-adjusted disclosed accrual layer (PF Adjusted when a separate PF
   layer exists, otherwise Adjusted, otherwise Reported). For software / recurring-revenue
   deals with a disclosed deferred-revenue delta, that's `pf_adj_cash_ebitda` instead, per
   invariant 3. Either way, it's one deliberately selected figure, not whatever a tile prints.
2. **Every multiple states its basis.** Gross vs net is explicit and consistent:
   - Gross leverage = `total_debt` / `anchored_ebitda`
   - Net leverage = (`total_debt` − `cash`) / `anchored_ebitda`
   Never put a gross multiple and a net multiple on the page both labelled "total leverage."
3. **For software / recurring-revenue deals, `pf_adj_cash_ebitda` is the anchor when
   disclosed** — the deferred-revenue-adjusted figure is the leverage basis for these deals,
   not an overlay on top of accrual PF Adjusted. When it is the anchor, the accrual PF
   Adjusted (or Adjusted) figure must be disclosed alongside it, stated directionally. For
   deals without the software trigger, or where the deferred-revenue delta isn't disclosed,
   this role doesn't apply and the accrual chain (PF Adjusted → Adjusted → Reported) governs.
4. **Coverage ratios are out of scope; EBITDA-less-capex leverage is not.** Interest coverage,
   DSCR, and fixed-charge coverage require interest expense on the post-close capital structure,
   which is modeled even at the entry period, so they're a separate projection output (Q1161 or
   the projections skill), never this workflow's cap table. EBITDA-less-capex is treated
   differently: capex is sourced to the same standard as `anchored_ebitda`. When the anchor is
   an estimated / projected-period figure, a matching-period "Less: Capex" figure from the deal
   model is a permitted input, since the anchor itself is estimated; `anchored_ebitda` minus
   that capex is then a second denominator this workflow strikes leverage on, with the capex
   source flagged (disclosed actual vs. model-projected). The denominator is "n/d" only when no
   capex figure exists anywhere in the documents or model.

## Note on generality

EBITDA layer selection is the sharpest instance of anchor resolution, but the same discipline
applies to the other headline figures: pin the period (never mix FY / LTM / H1 across the
output), pin the currency, pin the leverage basis, and keep coverage metrics out of this
workflow entirely, they're a projection concern, not a point-in-time leverage one. This applies
just as much to cap-structure figures as to EBITDA — don't take a dashboard tile's debt-stack
totals at face value if the vault's own capital-structure table (e.g. Q1160) disagrees; the
vault table is the primary source, the dashboard tile is a secondary cross-check. An internal
inconsistency inside a single tile (e.g. a sources & uses tile whose sources total doesn't
equal its uses total) is itself evidence that tile is unreliable, not a coin-flip tiebreaker
against the vault. When any input tile disagrees with the resolved anchor block, the anchor
block wins and the tile is treated as color, and the disagreement is reported in the output's
footnote, not silently dropped.
