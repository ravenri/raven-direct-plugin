---
name: "deal-terms-test-covenants"
description: "Tests a deal's financial covenants against the lender model and shows the work — identifies the governed metric (e.g. First Lien Net Leverage, never defaulting to Total Debt/EBITDA), renders the covenant structure, then tests period-by-period compliance against the threshold with an as-if-sprung result for springing covenants, and derives an EBITDA breakeven and a stress grid (-10% / -20% / -30%). Pulls the covenant structure from Raven's legal_review and the leverage series, debt and PF Adjusted EBITDA from the lender model on the Financial Analysis projections page via Raven Direct. Unlike Loan Coverage (a faithful stored-read), this skill computes — the breakeven and stress figures are derived. Renders in chat, then optionally exports an Excel workbook or a Word doc. Use for \"test covenants,\" \"covenant headroom,\" \"will this deal trip its covenant,\" \"covenant compliance,\" or \"how far can EBITDA fall before breach.\""
when_to_use: "Use for \"test covenants,\" \"covenant headroom,\" \"will this deal trip its covenant,\" \"covenant compliance,\" or \"how far can EBITDA fall before breach,\" in underwriting against the lender model. Do not use for checking a post-close compliance certificate."
---

# Test Covenants

Tests a deal's financial covenants against the lender model: what the covenant governs, where the
threshold sits, whether the deal complies period by period, and how far PF Adjusted EBITDA can fall before it
trips. It answers the question a credit committee asks after the term sheet — not what the covenants are, but
whether this deal breaches them and with how much room. Covenants are read and tested by tranche: the
regime differs across the revolver, term loans, and any other facility, and the output leads with that
package rather than collapsing the stack to one metric.

**This skill computes.** Loan Coverage renders Raven's own coverage figures faithfully; this one takes the
covenant structure and a model's leverage series and derives the compliance result, the breakeven EBITDA,
and the stress grid. The covenant structure and the metric series come from Raven as-is; the Pass/Fail,
headroom, and stress figures are calculated here, each tagged so the reader sees what was derived versus
disclosed.

**The model tested is the lender model**, the sponsor or borrower projection delivered in the deal
materials and shown on the Financial Analysis projections page. A Raven-generated projection is never a
substitute. If that page carries no lender model, stop and report that.

## Scope

The covenant test against the lender model. It is NOT the covenant/basket documentation read — that is
Deal Terms — Legal, which extracts the covenant package from the legal review. This skill takes the
governed metric and threshold and tests them against the lender model. When the request is for the covenant
package itself (baskets, prepayments, MFN), point to Deal Terms — Legal.

## Assets

- `references/build_covenant_workbook.py` — the canonical Excel builder. Parse the render into its
  `data` dict and call `build(data, out_path)`; sheets adapt to what the deal carries (a cov-lite +
  springing deal with one binding covenant produces one spread block and one stress grid).
- `references/language-standard.md` — the house language standard.

## Language

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives, house banned-word list). Read it and apply it. Additionally, per this
skill's own register: be concise, state facts directly, and do not explain your reasoning unless asked —
no "the reality is," "to be direct," "plainly stated," or similar throat-clearing. Do not expose platform
plumbing (no "the tile," "legal_review," prompt IDs, source-index brackets); present a covenant as a
covenant and a figure as a figure. No source citations or page numbers in the body.

## Project Resolution

- If a project_id is already known from earlier in this conversation, use it.
- Otherwise, if the user named a deal, call `deal_list` to resolve it. One match → use it. More than
  one → present as a markdown table (Deal, Company, Sponsor, Status, Created — no internal IDs) and ask.
  Do not guess.
- If no deal is named, ask which deal first.

**Skip-if-known (strict):** skip `analysis_get_status`, `dashboard_get(legal_review,
section="covenants")`, or `dashboard_get(financial_analysis, section="projections")` if already available from earlier in this conversation.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, suggest retrying or running `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`dashboard_get` is deferred and will error if called before loading. If not already loaded this
conversation, call `tool_search` to load it first.

## PHASE 1 — Covenant structure and lender model

### 1A — Pull covenant structure

`dashboard_get(project_id, tile="legal_review", section="covenants")`.

**Identify the governed metric first** from `Structure` (e.g. "First Lien Net Leverage Ratio") — never
default to Total Debt/EBITDA. Extract:
- **Governed metric** — from `Structure`.
- **Current level and stated threshold** — from `Headroom → Current Performance`. Do NOT reconcile this
  figure against the model's own leverage series in Phase 2 — different EBITDA bases at different points
  in a deal's life legitimately disagree.
- **Cushion %** — from `Headroom → Cushion Pct`. Default to 35% `[Assumed]` only if absent.
- **Springing mechanic** — from `Test Mechanics → Springing Threshold` and `Test Frequency`.
- **Cov-lite flag** — from `Structure`.
- **Step-downs** — commonly undisclosed; apply the market-standard schedule below unless a schedule is
  stated.

**First lien debt.** Use the lender model's first lien debt row where it presents one. Where the model shows a
single term loan row equal to total debt, with any delayed draw or revolver not shown separately, take first
lien debt as total debt and state that once. Where the governed metric is narrower than Total Debt and the
model shows several tranches whose lien ranking can't be confirmed, use Total Debt ÷ EBITDA as a
conservative proxy (Total Debt ≥ true first-lien debt, so this understates headroom, not overstates it) and
flag once: *"Covenant is defined on [metric] per the credit agreement; this test uses Total Debt ÷ EBITDA as
a conservative proxy since the exact first-lien composition couldn't be confirmed."*

Calculate only where the source is silent: **Threshold = Current level × (1 + cushion)**.

**If current level, threshold, AND cushion are ALL absent:** substitute the lender model's own earliest-period
leverage as "current," assume a 35% cushion, and flag both `[Assumed]`.

Market-standard step-downs (only if silent): Year 1 opening threshold; Year 2 −0.50x; Year 3 −0.50x
(cumulative −1.00x); Year 4+ floor.

**If cov-lite**, render this before the structure table:
> **⚠️ Cov-Lite Structure** — Term loans have no maintenance covenant. Springing [metric] covenant on the
> revolver only (tested at [X]% utilization, ~[$Y]). Thresholds below apply only when sprung.

### 1B — Covenant package, by tranche

Covenants live at the tranche level and the regime differs across the stack. Lead with the package table
— one row per facility — never collapse the deal to a single governed metric:

| Facility | Regime | Governed metric | Level | Frequency | Springing trigger | Equity cure |
|---|---|---|---|---|---|---|

- **Regime** is one of: Maintenance (tested every period), Springing (tested only when the revolver draw
  trigger is met), or Cov-lite (no maintenance covenant). A typical stack: revolver springing, Term Loan A
  maintenance, Term Loan B cov-lite — but read the actual structure, don't assume this shape.
- **Level / Frequency / Springing trigger** come from the covenant structure; tag `[Per docs]` /
  `[Assumed]` / `[Derived]` inline. Render the market-standard step-down only where a maintenance level is
  stated and the schedule is silent; a springing level is typically flat, so do not manufacture a
  step-down for it.
- **Equity cure** — render the cure availability and, if disclosed, its mechanics (max cures, consecutive-
  quarter limits). This is material to whether a breach actually defaults; the covenant structure carries
  it and it must appear here.
- A **cov-lite** tranche gets its row with "None" across the covenant columns — its absence of protection
  is the finding, stated, not omitted.

### 1C — Confirm the lender model

Read the projections page of the financial analysis dashboard. State the model source file and its date in
the header. If the projections are not available, stop and report that. There is no model picker; the
dashboard carries one lender case.

## PHASE 2 — Test and render

### 2A — Pull metrics

`dashboard_get(project_id, tile="financial_analysis", section="projections")`. Relay the dashboard's own
freshness warning if one appears.

Pull from the lender model:
- PF Adjusted EBITDA by period, from the model's own PF Adjusted EBITDA row.
- Total Debt by period.
- The model's own Total Debt to PF Adjusted EBITDA row from its credit statistics. Never substitute total
  leverage if the covenant governs something else.
- Any revolver or delayed draw balance rows, where the model shows them.

Use these as the model presents them. Do not recompute them. Where a row is not in the model, mark it `[NF]`.

Flag once near the top: *"Covenant EBITDA basis: PF Adjusted EBITDA as the lender model presents it. The
credit agreement's defined EBITDA may permit additional pro forma add-backs not captured here; actual
headroom may differ."* Do not chase reconciling this to 1A's stated current leverage if they differ.

If a period tested is a stub (for example a partial first year tied to a mid-year close), name it in the
spread and say where the model's EBITDA is full-year while its cash flow is a stub.

### 2B — Spread each binding covenant (one block per covenant)

Spread every covenant that binds — a maintenance test and a springing test are separate blocks, because
they govern different metrics that trip at different EBITDA levels. A cov-lite tranche is not spread; it is
stated as unprotected. Order: maintenance covenants first (they always test), then springing.

Each block: a heading naming the facility and metric, then the spread across the model's projection years:

| Period | [Metric] | Threshold | Pass/Fail | Headroom |
|---|---|---|---|---|

- **Maintenance covenant** — a real Pass/Fail every period; it always tests.
- **Springing covenant:** test as sprung in any period where the lender model's revolver usage exceeds the
  trigger. Otherwise test as-if-sprung: compute Pass/Fail and headroom against the threshold anyway (the
  cushion that would exist if it activated); never blank it as "not tested." Where the model does not show
  revolver usage on its own line, frame once per block: *"Revolver usage is not separately disclosed in the
  lender model, so the test is run as-if-sprung. Pass/Fail and headroom below are as-if-sprung."* State the
  trigger draw level from the covenant terms.
- **Cov-lite tranche** — no block; one line stating it carries no maintenance covenant, so downside
  protection rests only on the springing test (dormant while undrawn) and any equity cure. When the
  cov-lite tranche is the largest, say so — it is the point.

Flags: 🔴 Breach (exceeds threshold) · ⚠️ Tight (headroom < 0.25x) · ✅ Pass.

### 2C — Summary (exactly three lines)

- **Compliance:** [status across the binding covenants] — tightest point: [covenant, period, headroom]
- **Key risk:** [one sentence]
- **Springing exposure:** [revolver draw level that would activate it, or "N/A — maintenance covenant"]

### 2D — EBITDA breakeven and stress (required when Debt and PF Adjusted EBITDA are both available)

Run this per binding covenant — each metric trips at a different EBITDA level, so a maintenance total-
leverage test and a springing first-lien test each get their own grid. Per period: `Breakeven EBITDA = Debt ÷ Threshold`; `Breakeven Decline % = 1 − (Breakeven EBITDA ÷ Lender Model
PF Adjusted EBITDA)`.

Stress grid, the next three periods with both Debt and PF Adjusted EBITDA:

| Year | PF Adj. EBITDA | Debt | Threshold | Base Leverage | -10% EBITDA | -20% EBITDA | -30% EBITDA | Breakeven Decline to Trip |
|---|---|---|---|---|---|---|---|---|

Stressed columns = `Debt ÷ (PF Adj. EBITDA × (1 − stress%))`, against that period's stepped-down threshold.
Flag any stressed cell that breaches or comes within 0.25x of the threshold.

**Threshold provenance (required):** if a threshold is a step-down stacked on an already-assumed prior
year, spell out the full chain (e.g. "4.61x → −0.50x → 4.11x → −0.50x → 3.61x, all `[Assumed]`") — never a
bare `[Assumed]` implying a single-step assumption when it is stacked.

`[NF]` for any period missing Debt or PF Adjusted EBITDA; don't drop below three periods without saying why.

## Rules

- Test the actual governed metric; never default to total leverage without the proxy disclosure.
- Test springing covenants as sprung where the lender model shows usage above the trigger, otherwise
  as-if-sprung; never blank as "not tested."
- `[NF]` for missing data, never invent. `[Assumed]` / `[Derived]` / `[Per docs]` inline.
- Lender model figures are used as presented. The Pass/Fail, headroom, breakeven and stress figures are
  calculated here and tagged `[Derived]`. A Raven-generated model is never a substitute.
- No source citations or page numbers in the body.
- Covenant ratios are unitless; dollar figures in the deal's stored currency.
- Scope: covenant testing only. The covenant/basket documentation read is Deal Terms — Legal.

## Delivery

Render in chat first. Then `ask_user_input_v0`: "📗 Excel workbook" /
"📄 Export as Word doc" / "Skip — chat is fine". **Stop and wait for the choice.**

- **Excel workbook:** build via `references/build_covenant_workbook.py` — parse the render into its
  `data` dict (title, meta, cov-lite warning, the by-tranche `package`, `summary`, one `spreads` block
  per binding covenant with a Pass/Fail status per row, and one `stress` block per binding covenant with
  a numeric threshold and float leverage cells) and call `build(data, out_path)`. Three sheets — Covenant
  Package, Spread (Pass/Fail color-coded), Stress (stressed cells color-coded green/amber/red vs the
  threshold) — collapsing to what the deal carries. Read the xlsx skill (`/mnt/skills/public/xlsx/SKILL.md`) only to adjust the builder. Save to
  `/mnt/user-data/outputs/` and `present_files`.

- **Export Word doc:** tell the user it takes ~25 seconds. Generate via the docx skill (Arial, navy
  headers #1F2D3D, gray labels #F2F2F2, US Letter portrait, 0.5" margins). Save to
  `/mnt/user-data/outputs/<ProjectName>_Covenant_Test.docx` and `present_files`.
- **Skip:** wrap up briefly.
