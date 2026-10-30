---
name: "company-other-risks"
description: "The read on a deal's other risk factors from Raven's other_risk_factors dashboard and the underlying analysis: legal and litigation, pension and legacy liabilities, environmental, tax, off-balance-sheet and debt-like items, trade policy and tariffs, the transaction situations (carve-out, bankruptcy emergence, restructuring, regulatory approval, acquisition integration), and business continuity and insurance. Gives the finding, evidence and credit implication for each live factor, then ranked diligence gaps and a closing summary. Commodity, energy and cyclicality are separate skills. Chat by default, Word on request. Use for \"other risk factors,\" \"legal and litigation risk,\" \"pension liabilities,\" \"environmental exposure,\" \"tax risk,\" \"off-balance-sheet items,\" \"carve-out risk,\" or \"business continuity and insurance.\""
when_to_use: "Use for \"other risk factors,\" \"legal and litigation risk,\" \"pension liabilities,\" \"environmental exposure,\" \"tax risk,\" \"off-balance-sheet items,\" \"carve-out risk,\" or \"business continuity and insurance.\" Do not use for commodity, cyclicality, FX or interest rate risk, which have their own skills."
---

# Other Risk Factors

Produces the read on the deal's other risk factors: legal, pension and legacy, environmental, tax,
off-balance-sheet and debt-like items, trade policy, the transaction situations, and business continuity
and insurance. Each live factor states whether it is a sized exposure or a disclosure gap, and why.

**This is the factor read, not the deep sections.** The `other_risk_factors` dashboard also carries
Cyclicality and Commodity / Input Cost deep sections, each its own skill. This skill reads the live
factors and the closing summary only. Do not repeat the deep sections' content.

**Two sources, both primary.** The dashboard is a rendering of the underlying analysis and by design does
not carry everything the analysis has. For every run, retrieve BOTH the dashboard (`dashboard_get`) AND a
direct read of the underlying answer for each applicable factor (`analysis_get_question` once the answer
is found with `research_search_analysis`; `references/vault-access.md` names them). Merge them. Where the
underlying answer carries a fact, figure or sub-point the dashboard omits, include it under that factor.
Where the dashboard is thin, query harder; do not render a gap without having checked.

**Identify answers by name, never by number.** The numbering and the set of answers differ between older
and newer runs. An older run carries Carve-out / Separation, Emergence from Bankruptcy, Active
Restructuring, Regulatory Approval Conditions and Acquisition Integration as separate answers; a newer run
carries one Transaction Situation answer. Read either form into the single Transaction Situation section
below.

## Tone and rules

Apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a
specific source field or note; where the dashboard and the underlying answer disagree, the underlying
answer governs and the conflict is reported, never silently resolved; a dashboard's own internal
inconsistency is evidence against it, not a tiebreaker.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives, banned-word list, bold key figures, no platform plumbing). Never refer to
the vault, the dashboard, prompt names or IDs in the output; name sources as the underlying documents.
Stored prose is frequently loose: rewrite to a plain declarative that leads with the fact, never pass
verbatim.

**Self-check before delivering. These keep slipping through:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon or period. This is a find, not a read.
- Do not pass stored prose through verbatim. Lead with the fact and the figure.
- Headings name content: the factor name. "Overview," "Assessment" or "The read" as a heading is a defect.
- No card wording or card layout. The page no longer uses cards, so neither does this output.
- No verdict-then-hedge ("modest but real"), no X-not-Y, no hype ("well-positioned," "robust").
- A gap is a gap, not a clean bill of health. Never let an absence of disclosure read as an all-clear.
- No KPI tiles or stat strips. Use prose and tables.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, if the user named a deal, `deal_list` to resolve (try the deal name, then the company name). One
  match, use it. More than one, present a table (Deal, Company, Sponsor, Status, Created, no internal IDs) and ask.
- If no deal is named, ask which deal first.

**Skip-if-known (strict):** if `analysis_get_status` or `dashboard_get(other_risk_factors)` is already
available from earlier in this conversation, reuse it, do not re-call.

## STEP 0: Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" proceeds. Anything else: stop, report
the status, suggest retrying or `analysis_apply_start`.

## STEP 0.5: Tool pre-load

`dashboard_get`, `research_search_analysis` and `analysis_get_question` are deferred; `tool_search` them
once if not loaded. Load `research_search_documents_by_type` and `get_source_page` when you reach the second read.

## Retrieve: dashboard AND underlying answers, both primary

1. **Dashboard:** `dashboard_get(project_id, tile="other_risk_factors")`, one full call. Extract the live
   factors and the Section Summary; ignore the Cyclicality and Commodity / Input Cost deep sections. Read
   the data-confidence level and generated date first.
2. **Underlying answers:** for each factor the dashboard marks live, and for each always-on factor
   whatever the dashboard says, read the underlying answer per `references/vault-access.md`: Legal &
   Litigation Risk, Pension & Legacy Liabilities, Environmental & Remediation, Tax Risk,
   Off-Balance-Sheet and Debt-Like Items, Trade Policy & Tariff Exposure, Transaction Situation, and
   Business Continuity & Insurance. Also read the Other Risk Factors Assessment, which ranks the live factors.
3. **Merge.** Dashboard structure and synthesis, plus any fact the dashboard omits. A fact found only in
   the underlying answer is still rendered under its factor.
4. **Not assessed.** If the deal's analysis has no answer at all for a factor (the run predates it), do not
   render that factor as clear. List it in one line: "Not assessed on this run."

## Render

**Header:** **Other Risk Factors: [Deal Name]**, with one meta line (company, sponsor, data confidence, date generated).

Open with one line naming the live factors in order of credit materiality, and one line naming the factors
that do not apply.

Then one section per live factor, headed by the factor name, in order of credit materiality (the order
the Other Risk Factors Assessment gives, not the order of this list):

- **Legal & Litigation**
- **Pension & Legacy Liabilities**
- **Environmental & Remediation**
- **Tax**
- **Off-Balance-Sheet and Debt-Like Items**
- **Trade Policy & Tariff Exposure**
- **Transaction Situation** (one block for each situation that applies: carve-out or separation, emergence from bankruptcy, active restructuring, regulatory approval conditions, acquisition integration)
- **Business Continuity & Insurance**

Within each section: a status line (sized exposure or disclosure gap), the finding in one sentence,
the evidence with figures, each sized figure carrying its source document and period, and the credit
implication as its own line. Where the analysis marks a gap, say so in the section.

Close with:

1. **Diligence gaps:** one numbered list across all factors, ranked by analytical impact, each item leading
   with the specific ask. Include factors that are not live but carry a disclosure gap, and name any factor
   not assessed on this run.
2. **Summary:** the dashboard's Section Summary rewritten to the standard, as the closing synthesis across
   the factors.
3. A single link: "Open in Raven" with the dashboard's `web_url`.

## Second read (mandatory, INTERNAL: a separate pass after the full render, never shown)

Silent, findings woven in. Uses `research_search_documents_by_type` and `get_source_page`. After the render:
1. **Verify each sized figure** (deferred consideration, earnouts, pension obligation, tax reserve,
   separation or restructuring cost, guarantee and lease balances) against the documents. A dashboard figure is a claim to verify.
2. **Confirm each gap** is genuinely absent from the documents, not just missing from the dashboard, with one
   targeted query.
3. **Check for a factor the analysis omitted that the documents support**, for example a disclosed
   acquisition integration, regulatory condition, multiemployer plan, or restricted cash balance.
4. **Check that figures agree across sections.** A figure that appears in two sections carries the same value and period.
Findings weave in: a corrected figure appears in place, a confirmed gap strengthens the read. No process block.

## Final review (mandatory, INTERNAL: the last step)

Read the finished piece once more and fix: **tone** (findings not directives; no verdict-then-hedge, no
X-not-Y, credit-desk register); **coherence** (the sections and the closing summary tell one story);
**no false all-clear** (a disclosure gap never reads as a clean bill of health); **headings** (factor
names, never meta labels); **no card wording**; and a **literal proofread**, including a scan for the
em-dash character, replaced with a comma, semicolon or period. Silent; its only evidence is a cleaner read.

## Rules

- Live factors and the closing summary only. Commodity, energy and cyclicality are separate skills off the same dashboard.
- The dashboard and the underlying answers are BOTH primary retrieval. Where the dashboard is thin, query harder; do not flag a gap without having checked.
- Faithful stored read. Never compute, re-score or invent a figure. Rewrite stored prose to `language-standard.md`.
- Every sized figure carries its source and period.
- A disclosure gap is stated as a gap, never as a clean read. A factor with no answer on this run is "not assessed," never clear.
- Second read and final review are mandatory, separate and SILENT.

## Delivery

A focused read, so chat is the default. Offer a Word document when a shareable deliverable is wanted
(docx skill, Arial, navy headers, US Letter; validate, render and run the em-dash scan before delivering).
After delivering, offer one next step: the source page behind a figure, the Commodity Exposure or
Cyclicality read off the same dashboard, or a Word export.
