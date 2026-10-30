---
name: "legal-key-definitions"
description: "Pulls the credit agreement's key definitions (Consolidated EBITDA, Closing Date EBITDA, Closing Date leverage ratios, First Lien Net Leverage Ratio, Excess Cash Flow, Test Period, Available Amount/Builder Basket, springing covenant ratio level, Permitted Acquisition, Change of Control, Incremental Facilities capacity) and structural protections (J.Crew IP protection, Serta/uptier protection, Chewy/guarantee release protection, Restricted/Unrestricted Subsidiary designation mechanics) via vault search against the legal_review report type. Prose only, 3-5 sentences per entry, no bullets, section-and-page citation on every entry, a flag for every undisclosed threshold or schedule. Distinct from credit-agreement-grid/loan-terms-grid (facilities, sweep, basket tables) - definitions and protections only. Use for \"key definitions,\" \"Consolidated EBITDA,\" \"J. Crew protection,\" \"Serta protection,\" \"Excess Cash Flow,\" \"Available Amount,\" \"incremental facilities,\" or what the credit agreement's defined terms say."
when_to_use: "Use for \"key definitions,\" \"Consolidated EBITDA definition,\" \"how is leverage defined,\" \"J.Crew protections,\" or the agreement's structural protections in plain language. Do not use for the full grid (Credit Agreement Grid) or a basket model (Basket Capacity)."
---

# Legal - Key Definitions

Pulls the credit agreement's key definitions and structural protections directly from the document via
vault search, and renders each in tight, citation-backed prose. This is a judgment-informed read on legal
text, not a stored-read off a dashboard tile — there's no tile for this content, so every entry is
assembled from what the search actually surfaces.

## Scope

Owns: the eleven definitions in Part 1 (Consolidated EBITDA, Closing Date EBITDA, Closing Date leverage
ratios, First Lien Net Leverage Ratio, Excess Cash Flow, Test Period, Available Amount/Builder Basket,
Springing Financial Covenant ratio level, Permitted Acquisition, Change of Control, Incremental Facilities)
and the four structural protections in Part 2 (J. Crew IP Protection, Serta/Uptier Protection, Chewy/Guarantee Release Protection,
Restricted/Unrestricted Subsidiary designation mechanics). Does not own facilities tables, sweep tables, or
basket tables — those are `credit-agreement-grid` / `loan-terms-grid`'s job; if asked for those, point
there rather than attempting them here.

**Consolidated EBITDA cross-check, lightweight only.** The credit agreement's own defined "Consolidated
EBITDA" (a contractual construct with its own add-back categories, synergy caps, and realization windows)
is not automatically the same figure as the deal's canonical anchor EBITDA used elsewhere in this suite. If
`financial-proforma-cap-table-ebitda` has already run this conversation, note whether the credit
agreement's own add-back treatment (particularly any synergy/cost-savings cap) is consistent with what the
anchor build assumed, and flag a material divergence if one exists. This is not a hard dependency; proceed
independently if that skill hasn't run.

## Tone and rules

Apply `references/analyst-grade-discipline.md` and `references/language-standard.md` (American spelling,
credit-desk register, no em-dashes). Do not expose platform plumbing (no raw tool names,
`research_search_analysis`, `report_type`, or search mechanics) in the body.

**Never editorialize. Report only what the documents say.** This skill's entire value is precision on legal
text; an added adjective or characterization not traceable to the document is a defect, not color.

**Prose only, no bullet lists within an entry.** Each definition and protection is exactly 3-5 sentences,
never more, never a list. If the content genuinely doesn't fit in 3-5 sentences, tighten it rather than
expanding the limit or switching to bullets.

**Every entry ends with a section and page citation.** No exceptions.

**Flag every undisclosed threshold, dollar amount, ratio level, or schedule explicitly**, using the exact
form: "⚠️ [what's missing] not disclosed in vault — confirm before IC." Never fill a gap with a plausible-
sounding market-standard assumption.

**Self-check the AI-speak tells before delivering:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period.
- No hedge-then-verdict, no hype, no editorial adjective not traceable to the text.
- Headings name content, never function.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, `deal_list` to resolve by name. One match → use it. More than one → present as a table (Deal,
  Company, Sponsor, Status, Created; no internal IDs) and ask. Do not guess.
- If no deal is named, ask which deal first.

## STEP 0 — Pre-check

Call `deal_list_documents(project_id)` — using the resolved project_id, never the raw deal name; passing
the deal name here is a parameter-type error the source connector had and this skill must not repeat.
Confirm a credit agreement is present in the document inventory. If not, stop and say: "No credit agreement
has been uploaded for this deal." If confirmed, proceed.

## STEP 0.5 — Tool pre-load

`research_search_analysis` is deferred; if not loaded this conversation, `tool_search` it first.

## STEP 1 — Retrieve (parallel batch, seven searches in ONE turn, no dependency between them)

All seven calls use `report_type="legal_review"`, `top_k=10`, issued together in a single response turn —
never sequentially; there is no dependency between them, and running them one at a time defeats the point
of a parallel batch.

1. `"Consolidated EBITDA definition add-backs cost savings synergies cap realization window unrestricted subsidiaries"`
2. `"Closing Date EBITDA First Lien Net Leverage Ratio numerator denominator netting Test Period definition"`
3. `"Excess Cash Flow definition starting point deductions commencement Available Amount builder basket springing financial covenant numerical ratio level"`
4. `"J. Crew IP protection material intellectual property IP separation transaction Serta uptier non-pro-rata open market lender consent Chewy dropdown lien guarantee release"`
5. `"Restricted Subsidiary Unrestricted Subsidiary designation mechanics Event of Default investment basket initial schedule"`
6. `"Permitted Acquisition definition conditions Change of Control definition trigger Closing Date leverage ratios FLNLR SNLR TNLR"`
7. `"Incremental Facilities Incremental Amount ratio-based capacity pari passu junior lien unsecured thresholds"`

Do not write any output until all seven have returned.

## STEP 2 — Render

### Part 1 — Key Definitions

For each of the eleven, 3-5 sentences of prose, no bullets, ending with a section/page citation:

1. **Consolidated EBITDA** — base definition starting from Consolidated Net Income; characterize add-back
   categories by type (interest, taxes, D&A, non-cash charges, restructuring, sponsor fees, pro forma
   run-rate adjustments) without an exhaustive list; state any disclosed cap on run-rate cost
   savings/synergies and the realization window, flagging if absent; note Unrestricted Subsidiary
   treatment. Apply the cross-check against `financial-proforma-cap-table-ebitda`'s anchor per the Scope
   section above if that skill has run.
2. **Closing Date EBITDA** — confirm whether the specific dollar figure is disclosed; explain its role as
   the fixed floor in the "greater of" construct used across baskets, sweeps, and ratio-based thresholds;
   name which key baskets reference it; flag if the dollar amount is absent.
3. **Closing Date Leverage Ratios** — Closing Date First Lien Net Leverage Ratio, Secured Net Leverage
   Ratio, and Total Net Leverage Ratio if disclosed; these anchor every ratio-based basket stepdown and
   sweep reduction in the agreement; flag any that are absent.
4. **First Lien Net Leverage Ratio** — numerator (Total Net Debt secured by first-priority lien on
   Collateral, excluding junior/subordinated), denominator (Consolidated EBITDA for the Test Period),
   netting convention (unrestricted cash and equivalents), key numerator exclusions.
5. **Excess Cash Flow** — starting point (Consolidated Net Income); characterize key deduction categories
   (taxes, capex and software, debt service, working capital movements) without enumerating every line;
   commencement date (first full fiscal year after Closing Date); any unusual or borrower-favorable
   feature.
6. **Test Period** — definition and measurement frequency; note the standalone section reference if
   available.
7. **Available Amount / Builder Basket** — the fixed-floor EBITDA-based "greater of" component; the
   variable accumulator in one sentence (the "greatest of" among Retained ECF, 50% of cumulative
   Consolidated Net Income, and 100% of cumulative EBITDA less 1.40x Fixed Charges) without listing every
   other accumulator prong; permitted uses across covenants and any pro forma ratio condition on use.
8. **Springing Financial Covenant — Ratio Level** — the specific numerical ratio level if disclosed; flag
   if absent.
9. **Permitted Acquisition** — key conditions: no Event of Default, pro forma compliance requirement, any
   business-line or geographic limitation; note if the definition is absent or only partially defined.
10. **Change of Control** — trigger events and any Sponsor retain-control carveout (whether the Sponsor and
    affiliates retaining majority economic or voting interest prevents a CoC); the acceleration
    consequence under Events of Default.
11. **Incremental Facilities** — the ratio-based capacity governing additional debt the borrower can layer
    on without further lender consent, and the applicable test for each lien priority (pari passu secured,
    junior secured, unsecured) with its specific threshold; state whether an uncapped, ratio-only prong
    exists alongside any fixed-dollar "freebie" basket, since that combination is what actually bounds how
    much the capital structure could still deteriorate post-close.

### Part 2 — Structural Protections

For each of the four, 3-5 sentences of prose, no bullets, ending with a section/page citation:

2.1 **J. Crew IP Protection** — scope of the prohibition; the defined term ("IP Separation Transaction");
    definition of "Material Intellectual Property" including any customer-lists carveout; permitted
    exceptions (bona fide transition services, arm's-length licensing to non-affiliates); which covenant
    sections implement the restriction.
2.2 **Serta / Uptier Protection** — whether the agreement requires consent from the affected lender class
    specifically (not just required lenders across all classes) for amendments adversely affecting that
    class's rights or duties; the specific threshold language and section; state explicitly if the
    protection is absent or limited.
2.3 **Chewy / Guarantee Release Protection** — whether the agreement restricts automatic release of
    guarantees or liens solely because a subsidiary ceases to be wholly owned through an affiliate
    transfer; conditions required for release; any bona fide business purpose test.
2.4 **Restricted / Unrestricted Subsidiary — Designation Mechanics** — base definitions of each; designation
    conditions (a Specified Event of Default test, no EOD on a pro forma basis immediately before and
    after; Investment-basket consumption, designation counts as an Investment at FMV of net assets);
    confirm whether the initial Unrestricted Subsidiary schedule is reproduced in the vault, flagging if
    not.

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time.
1. **Confirm every entry traces to a retrieved chunk.** A claim in any definition or protection not backed
   by Step 1's results is fabricated; remove it or re-search.
2. **Confirm every entry is 3-5 sentences and contains no bullet list.** This is the most common drift
   point on a strict-format skill; check it explicitly.
3. **Confirm every entry ends with a section/page citation.** No exceptions, including entries that are
   mostly a flagged gap.
4. **Confirm every genuinely undisclosed threshold, amount, or schedule carries the exact flag wording**
   ("⚠️ ... not disclosed in vault — confirm before IC"), not a softened paraphrase.
5. **Confirm nothing editorializes.** Scan for any adjective or characterization not directly traceable to
   the document text.
6. **Confirm the Consolidated EBITDA cross-check ran** if `financial-proforma-cap-table-ebitda` has already
   run this conversation, and that any divergence found was reported, not smoothed over.

Findings weave into the render in place; nothing labeled "second read" reaches the output.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

Read the finished piece top to bottom once more and fix: **tone** (credit-desk register, no hedge-then-
verdict, no hype, strictly reportorial); **platform plumbing** (no raw tool or parameter names anywhere in
the body); **headings** (clean, parallel, name content); and a **literal proofread** of every heading,
citation, and figure. Scan literally for the em-dash character and replace each with a comma, semicolon, or
period. Silent; its only evidence is a cleaner artifact.

## Rules

- Report only what the documents say; never editorialize or add a characterization not traceable to the
  text.
- Prose only, 3-5 sentences per entry, no bullet lists within an entry.
- Every entry ends with a section and page citation, with no exceptions.
- Flag every undisclosed threshold, dollar amount, ratio level, or schedule explicitly, using the exact
  flag wording; never fill a gap with a market-standard assumption.
- Run all six Step 1 searches in a single parallel batch; never sequentially.
- Always resolve project_id before calling `deal_list_documents`; never pass the raw deal name to it.
- Scope: definitions and structural protections only. Facilities, sweep, and basket tables are
  `credit-agreement-grid` / `loan-terms-grid`'s job.
- Cross-check Consolidated EBITDA's add-back/synergy-cap treatment against
  `financial-proforma-cap-table-ebitda`'s anchor if that skill has already run this conversation; not a
  hard dependency otherwise.
- No platform plumbing in the body: no raw tool or parameter names.
- Second read and final review are mandatory, separate, and silent; the evidence they ran is a changed
  artifact, never a narrated process block.

## Delivery

Render in chat by default. Only produce a Word document if asked; when generating one, use the docx skill
with a title block (deal name) and the same Part 1 / Part 2 structure as the chat render. Save to
`/mnt/user-data/outputs/` and `present_files`. After delivering, offer one natural next step:
`credit-agreement-grid` for the facilities/sweep/basket detail, or the Word export if the read was in chat.
