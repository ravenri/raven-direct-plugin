# Build input for build_pdf.py

One JSON file per run, written to the scratchpad. It is never shipped with the skill and holds no standing content.

Top level fields: deal_a, deal_b, pull_date, notes (optional, any of terms, leverage, scorecard, creditread), footnotes (list of sentences), datasets.

Datasets and their columns, one row per line item:

1. headline: key, metric, format (mm, x, pct, score or text), deal_a, deal_b. Two keys are required: repaid_final_pct (share of debt repaid by the final projection year) and gross_leverage_x (entry total debt to the anchor EBITDA, gross of cash). Add rows for facility size, tenor, pricing, anchor period, anchor EBITDA (key anchor_ebitda_mm), funded debt (key funded_debt_mm), loan to value, sponsor equity share and overall rating. Numbers are plain numbers (mm in millions, pct as 12.5 for 12.5%). Text rows such as ratings use format text.
2. scorecard: lens, a_score, a_rating, a_driver, b_score, b_rating, b_driver. Score may be blank where Raven leaves a lens unscored. Rating is never blank. A driver is Raven's one-sentence driver for that lens, quoted exactly with formatting marks removed. Leave a driver blank when its wording states a figure net of cash, and say so in a footnote.
3. capital_stack: deal, layer, amount_mm, pct_of_cap. List layers in capital order. Shares per deal add to 100.
4. paydown: deal, step (0 is the anchor period), period, repaid_pct, gross_leverage_x. Gross leverage by year is total debt over the anchor EBITDA as Raven states it. Where Raven states only net leverage by year, calculate gross as Raven total debt over Raven PF Adjusted EBITDA for that year, keep the anchor value as Raven states it, and say so in the leverage note and a footnote. Otherwise leave a value empty where Raven does not disclose it.
5. repayment: deal, read. One row per deal. The read is Raven's repayment read, quoted exactly. Leave it blank if it states a figure net of cash.
6. screening: deal, tranche, view, basis. One row per deal and tranche, from Raven's preliminary screening view. The view is quoted exactly. The basis is Raven's stated basis, quoted exactly, and left blank when it states a figure net of cash.

Footnotes carry what a reader needs to read the PDF correctly: each deal's anchor period and EBITDA basis, any stale source, any difference in basis between the two deals, and which drivers, reads or bases were left blank because they state figures net of cash.
