---
name: "legal-compare-loan-agreements"
description: "Compares credit agreement key terms and creditor protections across 2-4 deals in tables (facilities, pricing, financial covenants, incrementals, mandatory/voluntary prepayments, debt baskets, restricted payments, creditor protections), plus a one-line-per-cell summary and an open-items list. Distinct from Deal Compare (metrics and credit read) - this is terms only. Sections 1-7 are tile-sourced (legal_review), reusing credit-agreement-grid's Borrower Proposed cells if that skill already ran for a deal this conversation. Section 8 (creditor protections) is ALWAYS independently vault-verified, never trusting the tile's present/absent flag, which has a confirmed false-negative pattern on J.Crew/Chewy-style protections that live unlabeled inside other covenant sections. Use for \"compare loan agreements,\" \"compare credit agreements,\" \"terms comparison across deals,\" or how 2-4 deals' provisions stack up against each other."
when_to_use: "Use for \"compare loan agreements,\" \"compare credit agreements,\" \"terms comparison across deals,\" or how two to four deals' provisions stack up. Do not use for one agreement alone (Credit Agreement Grid) or for comparing deal metrics."
---

# Legal - Compare Loan Agreements

Compares credit agreement key terms and creditor protections across 2-4 deals, rendered as one table per
topic with a column per deal. This is the **terms** comparison — distinct from Deal Compare, which covers
metrics and the credit read. Output is tables only; no prose sections unless the user asks for narrative.

## Scope and cross-skill sourcing

**Distinct from `credit-agreement-grid`.** That skill produces a single deal's full 30-section grid as an
Excel workbook (Borrower Proposed / Lender Response / Status / Source). This skill produces a cross-deal
comparison across 2-4 deals at a coarser, 8-topic grain, in chat tables. The two share a data source
(`legal_review`) and, loosely, a taxonomy: this skill's Sections 1-7 map onto several of that skill's 30
sections (roughly: Section 1 here ≈ grid Sections 2/5/6; Section 2 here ≈ grid Sections 3/4; Section 3 here
≈ grid Section 7; Section 4 here ≈ grid Section 17; Section 5 here ≈ grid Sections 5/16; Section 6 here ≈
grid Section 17; Section 7 here ≈ grid Sections 18-21; Section 8 here ≈ grid Section 29) — approximate and
many-to-one, not a strict 1:1, since the grid is far more granular.

**Reuse where safe, never where risky.** If `credit-agreement-grid` has already run for one or more of the
deals being compared this conversation, reuse its Borrower Proposed cell values for the corresponding
Sections 1-7 rows rather than re-pulling `dashboard_get(legal_review)` for that deal from scratch — both
skills draw on the same tile-sourced extraction for those sections, so there's no accuracy divergence risk
in reusing it, only a real efficiency gain. **Section 8 is the one exception, always.** Never reuse
`credit-agreement-grid`'s Section 29 cell even if that skill already ran, and never trust this skill's own
`legal_review` tile flag either — both inherited the same confirmed false-negative pattern (see Section 8's
own discipline below), so Section 8 always gets its own independent vault verification pass regardless of
what any other source says about it.

## Tone and rules

Apply `references/analyst-grade-discipline.md` and `references/language-standard.md` (American spelling,
credit-desk register, no em-dashes). Do not surface search mechanics to the user, and do not expose
platform plumbing (no raw tool names, `research_search_analysis`, `report_type`, or internal section keys)
in the body.

**Never editorialize; report only what the documents say**, same discipline as `legal-key-definitions`.

**Self-check the AI-speak tells before delivering:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period.
- No hedge-then-verdict, no hype, no editorial adjective not traceable to the text.
- Headings and table labels name content, never function.

## STEP 0 — Deal count check

Count the deals provided before doing anything else.
- Fewer than 2: stop and say "Please provide at least 2 deals to compare."
- More than 4: stop and say "This workflow supports a maximum of 4 deals. You provided [N] — please
  select up to 4 to proceed." List the deals and wait for confirmation.
- Note at the top of the output: "This workflow supports up to 4 deals. For the clearest output, 2-3 deals
  is recommended — tables become wide and harder to read at 4."

## STEP 1 — Project resolution and document check

For each deal, call `deal_list(name="...")` to resolve its project_id. If a name returns no matches, try
`deal_list(company_name="...")` before giving up; if still no match, tell the person and stop for that
deal only. If a name returns multiple matches, present all matches via `ask_user_input_v0` (name, created
date, sponsor, loan amount — enough to distinguish test/scratch entries) and ask which one before
proceeding. Do not guess.

Then call `deal_list_documents(project_id)` for each resolved deal. For any deal with no documents
uploaded, note inline: "No documents found for [DEAL NAME] — legal review searches will return [NV]."

## STEP 1.5 — Tool pre-load

`dashboard_get` and `research_search_analysis` are deferred; if not loaded this conversation, `tool_search`
them first.

## STEP 2 — Retrieval and progressive rendering

**Sections 1-7 — tile only, per deal, unless `credit-agreement-grid` already ran.** For each deal not
already covered by a `credit-agreement-grid` run this conversation, pull `dashboard_get(project_id,
tile="legal_review")` once. This single call returns the whole structured provision set — facilities,
pricing, covenants (with headroom), ECF/asset-sale sweeps and stepdowns, incrementals (Free & Clear, ratio,
MFN plus carve-outs), every debt/lien/RP/investment basket with capacity and section refs, and its own
data-gaps list, all with section citations. Do not run a vault search for Sections 1-7 to "verify" what the
tile already carries — that doubles the calls for no gain. Go to the vault for a 1-7 cell only when it is
(a) blank, (b) internally contradictory, or (c) flagged in the tile's own Gaps list. Surface the tile's
freshness flag per the staleness rule and still render.

**Thin-cell watchlist (the one 1-7 exception).** A few 1-7 provisions are conditional/nested, and the tile
can render a plausible-looking cell while silently dropping the nested detail — absence of detail is the
tell, not a blank cell. If the tile shows a headline figure with no accompanying detail for any of these,
run one targeted vault query for that cell:
- ECF sweep — headline % present but no leverage-based stepdowns
- Asset-sale sweep — headline % present but no stepdown/reinvestment mechanics
- MFN — present but no carve-out list
- "Greater of $X or Y% EBITDA" basket floors — only one limb shown
Otherwise trust the tile. A wrong 1-7 conditional cell misprices a sweep or basket, real but lower-stakes
than a wrong Section 8 flag, which tells a reader a leakage blocker is missing when it isn't — effort is
calibrated to that asymmetry.

**Section 8 — creditor protections — ALWAYS independently verified against the vault; NEVER trust the
tile's present/absent flag, and never trust `credit-agreement-grid`'s Section 29 cell either, even if that
skill already ran.** Confirmed in live testing: the tile reported J.Crew and Chewy protections as "absent"
on a deal whose credit agreement plainly contained both, because these protections live unlabeled inside
the investment / asset-sale / lien-release / subsidiary-designation machinery rather than as their own
named clause. Run one combined creditor-protections vault query per deal and read the underlying sections
directly:

`research_search_analysis(project_id, "creditor protections IP separation transaction unrestricted subsidiary guarantee lien release wholly owned non-pro-rata subordination affected lender", report_type="legal_review", top_k=3)`

One query is enough — these protections are indexed together under the vault's creditor-protections
category, and a single well-formed query returns all three vectors plus related asset-sale/subordination
material in one payload. Only if that combined query returns empty on a specific vector, run one targeted
follow-up for that vector alone; do not otherwise fire per-vector searches. What to read for:
- **IP transfer to an unrestricted sub** — an "IP Separation Transaction" definition and carve-outs in the
  Investments / Asset Sales / subsidiary-designation sections ("this Section shall not permit an IP
  Separation Transaction"). Market shorthand: J.Crew.
- **Guarantee/lien release on loss of wholly-owned status** — in the Release of Liens and Guarantees
  section, whether release is automatic or conditioned on a bona-fide-business-purpose / anti-evasion test.
  Market shorthand: Chewy.
- **Lien/payment subordination and non-pro-rata repurchases** — in Waivers & Amendments, whether
  affected-lender or all-lender consent (or a pro-rata offer) is required. Market shorthand: Serta.

Describe each provision with its section and page; a bare "present" without a citation is insufficient, and
silence is a stated gap ("no restriction found"), never a bare "absent." Do not surface search mechanics.

**Render progressively:** complete all deals for one section, render it, move to the next. Note open items
(including the tile's Gaps section) as you go; consolidate at the end.

## STEP 3 — Detailed output

Output each section as a comparison table, one column per deal. Omit columns for deals not being compared
— never leave blank columns. Where a provision is absent, state [NV] inline.

### 1. Facilities & Economics
Identify all facility types present across any deal first, then one table per type (TLA/TLB/RCF): Size,
Tenor, Amortization, Call protection, Call carveouts, MFN.

### 2. Pricing
Disclosed terms only. Absent/not yet set: ⚠️ Not yet set. Redacted in the posted document: [NV — redacted].
Rows: TLB margin, TLA margin, RCF margin, Floor, OID, Commitment fee.

### 3. Financial Covenants
Rows: TLB covenant, RCF ratio type, Exact ratio, Trigger (% drawn), Testing frequency, Equity cure.

### 4. Incremental Facilities
Rows: Free & Clear, Prepayments/Extensions basket, 1st Lien ratio, Junior lien ratio, Unsecured ratio, MFN
spread/sunset.

### 5. Mandatory & Voluntary Prepayments
Rows: ECF rate/stepdowns, ECF threshold, Asset Sale rate/stepdowns, Asset Sale threshold, Reinvestment
period, Call protection rate/period, Call carveouts.

### 6. Debt Baskets
Rows: General/non-LP, Acquisition, Capital lease/purchase money, Sr Secured refinancing, Sr Unsecured
refinancing, Sponsor/investor debt.

### 7. Restricted Payments
Rows: General RP basket, Builder/Cumulative starter, Ratio RP, Unrestricted sub investment basket,
Available Amount mechanics.

### 8. Creditor Protections
Ask what the agreement **does** on each vector — never whether a named protection (J.Crew, Serta, Chewy)
is "present." Naming the protection invites a label-lookup that misses the mechanic when it lives
unlabeled in the covenant body, and forces a false present/absent verdict. For each row, describe the
actual provision and cite section and source document; where the agreement is genuinely silent, state
that as a gap ("no restriction found"), never a bare "absent." The row labels name the vector, not a trade
name; the cell holds the mechanic. Once a mechanic is found and described, tag it with its market
shorthand where one applies — e.g. "...blocks IP transfer to an unrestricted sub via the 'IP Separation
Transaction' carve-out (§6.04/§6.05) — aka J.Crew protection." The nickname is an annotation on a
described, cited provision, never the thing searched for.

Rows: Transfer of material IP to an unrestricted/non-guarantor subsidiary — permitted or blocked?;
Guarantee/lien release when a loan party ceases to be wholly owned or is designated unrestricted —
automatic or conditioned?; Subordination of lien or payment priority / non-pro-rata or open-market debt
repurchases — what lender consent is required?; Affiliated/disqualified lender voting cap or exclusion;
Minimum cash consideration on collateral asset sales; Unrestricted-subsidiary designation limits (default
condition, investment cap, IP restriction); EBITDA add-back cap and realization window.

## STEP 4 — Summary table

One line per cell, a brief characterization of the deal's position on that dimension, across all 8
categories: Facilities, Pricing, Financial Covenants, Incrementals, Prepayments, Debt Baskets, Restricted
Payments, Creditor Protections.

## STEP 5 — Open items

List only IC-material gaps — terms absent, redacted, or unconfirmed and material to the credit decision.
Format: an "all deals" block, then one block per deal.

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time.
1. **Confirm every figure traces to a retrieved chunk** (tile or vault). A cell not backed by Step 2's
   results is fabricated; remove it or re-search.
2. **Confirm Section 8 was independently vault-verified for every deal**, including any deal where
   `credit-agreement-grid` had already run — a reused Section 29 cell here is a defect, not an efficiency.
3. **Confirm the thin-cell watchlist was actually checked** for ECF sweep, asset-sale sweep, MFN, and
   "greater of" basket floors on every deal, not just assumed clean because the tile showed a number.
4. **Confirm Section 8 rows describe the mechanic and cite section/page before any market-shorthand tag
   appears.** A bare "J.Crew: present" with no cited mechanic is a defect.
5. **Confirm no bare "absent" appears anywhere in Section 8**; every negative is either a described,
   cited "no restriction found" or an actual described-but-weaker mechanic.
6. **Confirm columns for uncompared deals were omitted, not left blank.**
7. **Confirm the summary table and open items are consistent with the detailed tables above them.**

Findings weave into the render in place; nothing labeled "second read" reaches the output.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

Read the finished piece top to bottom once more and fix: **tone** (credit-desk register, no hedge-then-
verdict, strictly reportorial); **platform plumbing** (no raw tool/parameter names, no internal section
keys anywhere in the body); **table labels** (name content, never function); and a **literal proofread** of
every heading, citation, and figure. Scan literally for the em-dash character and replace each with a
comma, semicolon, or period. Silent; its only evidence is a cleaner artifact.

## STEP 6 — Delivery options

After rendering the full comparison in chat, ask via `ask_user_input_v0` (single-select): "How would you
like this delivered?" — "📄 Export as Word doc" / "Skip — chat is fine". If
the person already signaled a destination, skip the ask and go straight there.

**Word doc:** read the docx skill before generating. Produce a clean Word document: summary table first,
then all detailed sections, then open items. Use the deal names as the document title. Save to
`/mnt/user-data/outputs/` and `present_files`.

**Skip:** wrap up politely.

## Rules

- Sections 1-7 are tile-sourced; never re-verify them against the vault unless a cell is blank,
  contradictory, or tile-flagged as a gap, or it's on the thin-cell watchlist.
- Section 8 is always independently vault-verified, for every deal, every time — never trust the tile's
  flag and never reuse `credit-agreement-grid`'s Section 29 cell, since both share the same confirmed
  false-negative risk.
- Never ask whether a named protection (J.Crew, Serta, Chewy) is present; describe the mechanic first,
  cite it, then tag the shorthand.
- Never render a bare "absent" in Section 8; silence is a stated gap ("no restriction found").
- Reuse `credit-agreement-grid`'s Sections 1-7 output for a deal if that skill already ran this
  conversation, rather than re-pulling the tile from scratch for that deal.
- Omit columns for deals not being compared; never leave a blank column.
- Never editorialize; report only what the documents say.
- No platform plumbing in the body: no raw tool/parameter names, no internal section keys, no search
  mechanics surfaced to the person.
- Second read and final review are mandatory, separate, and silent; the evidence they ran is a changed
  artifact, never a narrated process block.

## Design intent

This is a terms comparison, not a credit read — Deal Compare covers metrics and credit judgment; this
skill stays in its lane (what the documents say, tranche by tranche and provision by provision) and
doesn't drift into assessing which deal is "better."
