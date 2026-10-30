---
name: "financials-q-of-e-review"
description: "Produces a credit analyst's reading of a quality of earnings (QoE) or financial due diligence report: who stands behind each layer of the EBITDA bridge, how each adjustment holds up on recurrence, support, substance and conditionality, items shown outside the earnings figure, revenue, cost, working capital, cash conversion, accounting, and where the report differs from the audited statements and other deal documents. Delivers a Word document and a derived-figures workbook. Interprets; does not recommend a structure or set an underwriting earnings basis. Use when a QoE or financial due diligence report is in the deal and the user asks for an earnings quality read, what the QoE says, whether the adjustments hold up, or how the report compares with the CIM, model or audited statements. Not for the EBITDA anchor and cap table, the historical statements, or reconciling Raven's own output."
when_to_use: "Use when a QoE or financial due diligence report is in the deal and the user asks for an earnings quality read, \"what the QoE says,\" \"whether the adjustments hold up,\" or how the report compares with the CIM, model or audited statements. Do not use for the EBITDA anchor and cap table, the historical statements, or reconciling Raven's own output."
---

# Financials - Q of E Review

Reads a QoE or financial due diligence report as a credit analyst would and says what the earnings are made of,
what they rest on, and what the report leaves open. It interprets. It does not condense the report, recommend a
structure, set an earnings basis for underwriting, or draw leverage or covenant conclusions in the body.

Delivered as a Word document built from `assets/Q_of_E_Review_Template.docx`, a derived-figures workbook built
from `assets/Derived_Figures_Template.xlsx`, and a short summary in chat. Body of up to 12 pages, no minimum; Appendix A up to 3.

## Output contract

Before the first data call, read these in full: `references/output-structure.md`, `references/expected-report.md`,
`references/language-standard.md`, `references/retrieval-notes.md`, and `references/layout-spec.md`. They define
the output. A reply is complete only when it follows the section order in `output-structure.md`. Do not substitute a
free-form summary, do not skip a section because the report is thin (state what is not presented, once), and do not
add a view the report and the stored analysis do not support. If you cannot build the Word document, say so in the
first line and render the same sections in chat in the same order.

Before sending, check:
1. The profile table, Analyst Note (only if a trigger applies) and terms line come first, then Executive Assessment.
2. Sections follow the fixed order (Executive Assessment, Quality of Earnings, growth section if needed, Revenue Analysis, Cost Base, Working Capital, Cash Flow and Conversion, Financial and Accounting Matters, Open Items, Appendix A).
3. Every section opens with a one-line conclusion and figure, then bullets. Each material bullet states what the diligence established and why it matters to a lender, in at most two sentences. Key figures are bold and there are no bold run-in labels.
4. Items outside the bridge are reported beside the headline and never added to it.
5. Every derived figure has a D number and a live formula; the workbook recalculates with no errors and matches.
6. Body is up to 12 pages. Appendix A starts on a new page.
7. No platform wording in the document: no vault, tile, prompt or prompt ID. Cite documents and pages.
8. Open Items is a plain numbered list.

## Step 0: Project and readiness

- Use the project already named in the conversation. Otherwise resolve the deal by name with the deal list. One
  match: use it. More than one: show a table (deal, company, sponsor, status, created) and ask. Say in the
  document which project was used when names were shared. If several projects match and only one has completed analysis, use that one and say so in the profile table.
- Analysis status must read ready. Anything else: stop and report the status.
- Load the deferred tools you need with tool search before first use: analysis search, search across all data,
  whole-answer fetch, document search, document list, document content, source page.
- Find the report in the document list by its classification sub-type (quality of earnings). The category differs
  between projects, so do not rely on it. If there is none, say the deal has no such report and stop.
- Always confirm the report before reading anything. Name the report found (provider, title, date, draft or final,
  side) and ask the user to confirm it is the one to run. If there is more than one (draft and final, buy side and
  sell side, or reports from different providers), list them and ask which. Run on one report per review and never
  combine reports. Skip the question only if the user has already named the report.
- Note provider, report date, draft status and period from the document's classification and first pages.

## Step 1: Read Raven's stored analysis first

For each element in `references/expected-report.md`, check whether an answer already exists. Quality of Earnings
has no prompts of its own yet, so coverage is partial: stored answers on the EBITDA layers, key EBITDA adjustments,
adjustments, net working capital and the EBITDA definition touch the report. If a search returns only part of an
answer, fetch the whole answer by ID. Treat stored answers as a map, not a source of record: they combine
documents and have been found on the wrong basis. Verify every figure you use against the report page, and prefer
the report for report facts.

## Step 2: Retrieve from the report

Run the nine search batches in `references/retrieval-notes.md` in parallel, in one turn, each as
`research_search_documents_by_type(project_id, ["deal"], query, top_k=7)`, with the report's title and the provider's
label in every query. This search cannot filter to one document, so discard results from other documents. Quality of
Earnings has no stored prompts, so the report is the primary source, not a fallback. Use a returned chunk only when it
is a complete table or passage. If it is partial, thin or a chart description, open the page with `get_source_page`,
and read the contents page first to choose pages. Confirm every figure traces to a retrieved chunk or an opened page.
Cite pages from the result metadata. Search mechanics never appear in the document.

## Step 3: Read the other deal documents

For Appendix A and cross-checks, read the stored analysis first and the documents second: CIM, lender or sponsor
model, consultant reports, credit agreement, audited statements, management presentations. Look for the earnings
figure in each, forecasts and the add-backs they carry, debt, working capital, seasonality and market-growth
claims, and anything the report says it did not address. Open only the pages of other documents that carry an
earnings figure, a forecast or a debt figure needed for the comparison, such as the CIM or lender presentation, the
model summary and the term sheet, at most three pages per document. Do not read documents in full. Name in the
Appendix A introduction any document not opened. If there are no other documents, say the comparison covers the
report only.

## Step 4: Classify and analyze

1. Give each element a coverage state (`expected-report.md`). Use the states to decide what to write; do not render
   them as a table.
2. Classify every earnings item as in the bridge, shown but excluded, or not addressed (`output-structure.md`).
3. For the bridge, ask of each layer who stands behind it and what was tested. Test every material adjustment on
   four points: recurrence, support, economic substance (does the cost disappear or get replaced) and
   conditionality (does it depend on future performance). Name questionable or conditional adjustments. Do not
   select an underwriting EBITDA figure.
4. Ask of each section what the figure depends on. Margins depend on cost removals and run-rate items; working
   capital depends on restricted cash, timing and terms; growth depends on price and ramp. Say so with the number.
5. Look across sections. A finding in one usually bears on another; connect them in the Executive Assessment.
6. Where a carried amount differs from a contractual or forecast amount, state both and the gap.
7. Do not invent. If the report and another document disagree, show both and do not choose.
8. For every earnings figure in another document, state which layer of the report it equals and whether the two labels agree.

## Step 5: Derived figures and workbook

Record every stated input with its source and every derived figure as a live formula, from
`assets/Derived_Figures_Template.xlsx`. Recalculate with the spreadsheet skill's script, confirm zero errors, and
confirm each figure in the document matches its row.

## Step 6: Write and build

Write to `references/output-structure.md` and `references/language-standard.md`: lead with the conclusion and its
figure, a one-line conclusion and then bullets in every section, key figures in bold, no metaphor or hype words, no em dashes,
American spelling, acronyms spelled out on first use, and "appears" or "suggests" on every inference. Write the
content to a content file that follows `scripts/Content_Template.json` (blocks in document order), then build with
`node scripts/build_from_content.js <content.json> <out.docx>`, which applies the layout in `references/layout-spec.md`.
Read the docx skill first, embed fonts through the helper, validate, render to PDF, look at page 1 and one table
page, and trim to the cap if needed. Before delivery run `python3 scripts/check_deliverable.py <review.docx>
<workbook.xlsx>` and fix every failure. It checks cited D numbers, workbook errors, dashes, banned and platform words,
section order, Open Items tags and page count; it does not check that each figure in the text equals its workbook row,
so compare those by eye.

## Delivery

Word document and workbook, plus a short chat summary (output-structure.md, Delivery). Open with the findings. No
progress narration. At most six lines for what the report shows, then the items outside the bridge, the Open Items
count, the page count, the documents compared and not compared, and any disagreement between stored analysis and the
report. Do not offer to save to a Raven sheet.

## Boundaries

- No recommendation on structure, pricing or leverage. Multiples that combine the report with another document
  appear only in Appendix A as differences.
- Do not re-derive the provider's adjustments or substitute your own earnings figure. Show the provider's, say what
  was tested, and say what was not.
- Do not name the platform in the document. In chat, name documents and pages.
