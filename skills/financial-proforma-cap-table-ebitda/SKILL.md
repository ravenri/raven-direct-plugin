---
name: "financial-proforma-cap-table-ebitda"
description: "Select a deal's anchored EBITDA and show its derivation, outline the proposed debt terms, and build the opening capital structure with leverage metrics off that anchor, for a private-credit deal in Raven, via the Raven Direct connector. Shows the full reported-to-adjusted-to-PF-to-cash walk with per-line dollar figures and per-layer source-document citations. Renders the vault's already-computed reconciliation, layer catalog, and tranche terms; does not re-derive or re-classify any line, and supports a fast-path mode giving just the figure, layer, period, and confidence. Use when asked to build an opening or pro forma cap table, capital structure, entry leverage metrics, an EBITDA bridge, reconciliation or walk, which EBITDA to use, or the proposed debt terms. On software or recurring-revenue deals with a disclosed deferred-revenue delta, the anchor is PF Adjusted Cash EBITDA. Point-in-time only: no coverage or forward projections. Requires Raven Direct."
when_to_use: "Use for \"pro forma cap table,\" \"capital structure,\" \"entry leverage,\" \"EBITDA bridge,\" \"EBITDA walk,\" \"which EBITDA to use,\" or \"the proposed debt terms.\" Do not use for earnings quality, the historical statements, or a term sheet summary (Quick Screen)."
---

# Financial - Proforma Cap Table w/ EBITDA

Up to four outputs, selected by what's asked, always in this order when more than one is
wanted:

0. **Fast-path anchor card** (only when the person wants just the anchor, not a full walk or
   cap table) — the figure, its canonical layer name, the period, a confidence flag, and one
   evidence pointer. The full walk is available on request, this is a shortcut to it, not a
   replacement for it.
1. **Select the anchor EBITDA and show its derivation** — the full reported-to-adjusted
   (-to-PF-to-cash, as disclosed) walk with per-line dollar figures, and the source
   document(s) each layer comes from. This renders Q1001's already-computed reconciliation
   and Q1210's layer catalog — it doesn't re-derive or re-classify anything. The point is that
   the reader can check the anchor against a document instead of taking a headline number on
   faith.
2. **Outline the proposed debt terms** — amount, pricing basis, cash-pay/PIK rate,
   amortization, and fees per tranche, split New Money vs. Existing/Rolled, from Q104. This is
   identity and terms, not leverage, it exists so the reader knows what each tranche actually
   costs and how it pays before looking at the stack it sits in.
3. **Build the opening capital structure** — the pro forma cap table with entry leverage
   metrics, every multiple struck on the selected anchor, one running cumulative column through
   the stack. Structural and point-in-time only, no coverage ratios.

Forward projections (leverage / coverage / PIK buildup over time) are deliberately **out of
scope** for this Skill and belong to a separate projections skill, see "Forward projections are
out of scope" below.

Selecting the anchor correctly — the right layer, the right period, the right leverage basis —
is what makes the cap table analyst-grade instead of a dashboard echo: every multiple in it is
struck on one deliberately chosen figure, not whatever a tile happened to print.

This Skill runs on top of the **Raven Direct** connector: it reads already-computed vault
answers and dashboard tiles through the connector and renders client-side. It does not compute
the vault answers itself, the vault (server-side) is the source of truth; this Skill selects
and presents the right figures from it.

## Workflow

1. **Resolve the deal.** If the user names a deal, call `deal_list` to get its project_id. If
   the name is ambiguous, or dev vs prod is unclear, ask which.

2. **Resolve the anchor block — FIRST, before rendering anything.** Read
   `references/anchor-resolution.md` and follow it exactly. Pull the vault EBITDA
   reconciliation and period anchor via `research_search_analysis`, the vault's canonical
   capital-structure table (e.g. Q1160) via `research_search_analysis` — this is the primary
   source for the debt stack, not the `dashboard_get` cap/coverage tile — and Q104 (tranche
   terms: identity, lien rank, cash/PIK, pricing, amortization, unused fee) in the same pass,
   since the debt terms outline in step 5 needs it and it's the same read. Call `dashboard_get`
   only as a secondary cross-check; if it disagrees with the vault table (tranche amounts,
   totals, or an internal sources-vs-uses mismatch within the tile itself), the vault table
   governs and the conflict gets reported in the footnote, never silently resolved. Read the
   EBITDA layers by FIELD (`pf_adj_ebitda` = anchored_ebitda / leverage denominator for most
   deals; `pf_adj_cash_ebitda` = the anchor instead on software / recurring-revenue deals
   where the deferred-revenue delta is disclosed; `reported_ebitda` = the unadjusted floor of
   the layer list). Do NOT take headline EBITDA, leverage, or debt-tranche amounts from a
   tile's prose — tiles mislabel layers, sometimes strike leverage on the cash line, and can
   hold stale cap-structure figures. The anchor block is the one source of truth every output
   below defers to.

3. **Fast-path branch.** If the person wants only the anchor figure, not a walk, terms, or cap
   table, render `references/render-specs.md` §0 and stop. Offer the full walk as a follow-up,
   don't render it unasked.

4. **Render the EBITDA reconciliation walk** per `references/render-specs.md` §1 — the full
   line-item walk from Q1001, footed to `anchored_ebitda`, with the per-layer source-document
   citations from Q1210. If the person asked only which EBITDA to use (no terms or cap table
   requested), stop here.

5. **Render the debt terms outline** per `references/render-specs.md` §2, from the Q104 terms
   already pulled in step 2. Split New Money vs. Existing/Rolled. Before asserting which value in
   a multi-column facility table belongs to which tranche, confirm against a second source per
   §2's facility-attribution rule, don't take a compressed table's column alignment on faith. If
   the person only wanted the walk plus terms (no cap table), stop here.

6. **Render the opening cap table** per `references/render-specs.md` §3, striking every
   leverage multiple on `anchored_ebitda` and stating gross vs net basis explicitly. No
   coverage ratios in this table. For the commentary, also pull Q1162 (Coverage & Structure
   Assessment) if available — it's the vault's own qualitative read on the structure, and
   house-style requires commentary to trace to a vault note rather than supply an independent
   adjective.

Apply `references/house-style.md` to every figure and line.

## Forward projections are out of scope

Anything that projects the deal forward, leverage by period, coverage over time, the PIK
balance buildup, the deleveraging path, does NOT belong in this Skill and must not be rendered
here, even if the person asks and even though a financial model exists on the deal. A separate
projections skill owns that. The reason is deliberate, not incidental: at screening stage the
forward view has to faithfully reproduce what the customer's own model projects (their sweep
logic, their M&A / cash-deployment plan, their coverage definition), and Raven's generated
model currently applies a house 100% cash-sweep convention that can deviate from the sponsor's
actual assumptions (e.g. a rollup that deploys free cash flow into acquisitions rather than
debt paydown). Presenting that model's forward path as if it were the deal's own projection
would misstate the sponsor's thesis. Until the model-generation layer cleanly separates
faithful reproduction from house sensitivity lenses, this Skill stays point-in-time only. If
the person asks for projections, say plainly that this Skill covers the anchor, terms, and
opening structure, and that forward projections are handled separately.

## The invariants (never violate)

1. **Leverage strikes on `anchored_ebitda`, whatever layer that turns out to be** — the
   most-adjusted disclosed accrual layer for most deals (PF Adjusted when a separate PF layer
   exists, otherwise Adjusted, otherwise Reported), or `pf_adj_cash_ebitda` instead on software
   / recurring-revenue deals where the deferred-revenue delta is disclosed. Every multiple
   states its basis (gross vs net).
2. **On software / recurring-revenue deals, `pf_adj_cash_ebitda` is the anchor when
   disclosed** — it's the leverage basis for those deals, not an overlay beside accrual PF
   Adjusted. When it's the anchor, disclose the accrual PF Adjusted (or Adjusted) figure
   alongside it, stated directionally. Where the deferred-revenue delta isn't disclosed, or the
   deal has no software trigger, this role doesn't apply and the accrual chain governs as
   usual.
3. **One period, one currency** across every output — pinned from the anchor block; never mix
   FY / LTM / interim.
4. **Coverage ratios are out of scope for the cap table; EBITDA-less-capex leverage is not.**
   Interest coverage, DSCR, and fixed-charge coverage require interest expense on the post-close
   capital structure, which is a modeled figure even at close, so they never appear in the
   opening cap table (step 6) and route to Q1161 / the projections skill instead. EBITDA-less-
   capex is different: capex is held to the same sourcing standard as `anchored_ebitda` itself,
   no stricter. Because the anchor is often an estimated / projected-period figure (e.g. an
   "LTM ...E" period), the cap table may legitimately be struck on expected numbers; where
   that's the case, a matching-period capex figure from the deal model's "Less: Capex" line is a
   permitted denominator input, exactly as the estimated EBITDA anchor is. The cap table strikes
   an additional cumulative leverage column on `anchored_ebitda` minus that capex, and the capex
   source is flagged (QoE / disclosed actual vs. model-projected) so the reader knows which it
   is. Only when no capex figure is available anywhere — not in the model, not in the financials
   — does the column show "n/d."
5. **Debt terms come from Q104 only, never invented.** Where a term (maturity, covenant
   package, MFN, call protection) isn't disclosed there, state "Not disclosed" — don't infer
   from market convention or a comparable deal.
6. **No forward projections.** This Skill is point-in-time only, anchor, terms, opening
   structure. Leverage-over-time, coverage-over-time, PIK buildup, and deleveraging paths are
   out of scope and owned by a separate projections skill (see "Forward projections are out of
   scope"). Do not pull the deal's financial model or render a forward view here, even on
   request.

## Reference files

- `references/anchor-resolution.md` — how to resolve the anchor block (read first)
- `references/render-specs.md` — fast-path card (§0), EBITDA walk (§1), debt terms outline
  (§2), cap table (§3)
- `references/house-style.md` — numeric format, spelling, voice, banned words

## Connector tools used

`deal_list` (resolve the deal) · `research_search_analysis` (vault EBITDA reconciliation walk,
layer catalog with source docs, period anchor, Q104 tranche terms, and the canonical
capital-structure table for the debt stack) · `dashboard_get` (cap / coverage tile, secondary
cross-check only). All via Raven Direct.
