# Retrieval notes

How the report and the deal are indexed, and how to read them cheaply. Measured on two reports: a 119-page report
(443 chunks) and a 100-page report (212 chunks).

## Order of sources

1. Raven's stored analysis first. For each element in `expected-report.md`, check whether an answer already exists
   (search the analysis, then fetch the whole answer by ID if a search returns part of it; the response reports
   which chunks are missing). Quality of Earnings has no prompts of its own yet, so expect partial coverage:
   existing answers on the EBITDA layers, the key EBITDA adjustments, the adjustments, net working capital and
   its position over time touch the report, and a legal review answer covers the EBITDA definition.
2. The indexed report, for every element the stored analysis does not hold, and to verify any figure taken from the
   stored analysis. Run the batches below in parallel, with the report's title and provider's label in every query, and open pages where a chunk is partial. Do not read the report end to end.
3. The other deal documents, stored analysis first and documents second, for Appendix A.

## Stored answers need a check

Stored answers often combine several documents, so a label can sit on another document's basis. Three defects were
found: an answer reading a December balance where the report's average applies; an answer placing one document's
adjusted figure under another document's management-adjusted label; an answer mixing two documents' working capital
figures and reading the difference as a conflict. Verify every figure you use against the report page, and prefer
the report for report facts.

Three further defects were found on a later run: the EBITDA layer catalog placed the CIM's 2020 figure under the management adjusted label, though the report's management adjusted figure was lower by the provider's own diligence items. The credit statistics labeled a multiple as PF Adjusted EBITDA that used the Adjusted figure. The CIM's forecast 2021 EBITDA was labeled reported.

Later runs also found: a stored answer called pro forma adjustments third-party validated because they appear in the report, though the provider stated no procedures on one component and another is a run-rate estimate; a stored leverage multiple was rounded down (5.4x against 5.49x computed); a stored pro forma burden used a different basis from the report's figures (25.8% against 28.8%); and a stored synergies figure missed a line inside the pre-acquisition adjustment ($162K against $465K).

## What the index holds well

- Tables: cell-accurate, including very wide tables and multi-period schedules. All spot checks matched the PDF.
- Text: chunked by section heading, with page numbers.
- Classification: the report is tagged as a Quality of Earnings report by sub-type. The category differs between
  projects (it sat under Other Diligence in one and Third Party Reports in another), so find the report by
  sub-type, not category.

## What it holds poorly

- Charts become machine-written descriptions. Some carry the plotted values, some only the structure, and some have
  scrambled labels. Never take a figure from a chart description. Use the table behind it, or open the page.
- A plain-language query can rank prose above a table. Query a table with its row labels and a few of its figures.

## Search batches

Run these in parallel as document-type searches (top_k 7), with the report's title and provider's label in every query; the search cannot filter to one document, so discard results from other documents. Use the provider's own
labels in the queries.

1. Front matter: scope, procedures performed, reliance, basis of preparation, periods, draft status.
2. The bridge: reconciliation from net income or reported EBITDA, each adjustment with amounts by period, support
   and testing, recurrence, items shown outside the figure, not quantified.
3. Growth mechanism: acquisitions (pre-acquisition earnings, price, synergies) or new markets (ramp, start-up losses).
4. Revenue: revenue by type or channel, price and volume, concentration, retention, backlog, seasonality, recognition.
5. Cost: cost of sales by nature, operating expenses, headcount, bonus and incentive pay, capital expenditure.
6. Financial statements: reconciliation to audit or trial balance, balance sheet, debt and debt-like items, cash.
7. Net working capital: definition, bridge, monthly table, adjustments, drivers.
8. Accounting and systems: policies, finance organization, systems, close, controls, pending standards.
9. Open points: "illustrative", "pro forma", "not included", "not quantified", "n.q.", "not performed", "management
   representation".
10. Gaps, run last: vendor and customer concentration, backlog in dollars and jobs, retention, monthly working capital. Say "not presented" for an element only after this batch has returned nothing. Until then write "not located in the sections reviewed".

When a figure matters, open its source page. Cite pages from the result metadata, not from memory.

## Project and document resolution

Resolve the deal by name. If more than one project matches, show a table (deal, company, sponsor, status, created)
and ask, and say in the document which project was used. If the deal has more than one report of this kind (a draft
and a final, or buy-side and sell-side), list them and ask which is primary. Load deferred tools with tool search
before first use. Analysis status must read ready before anything else runs.
