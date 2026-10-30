# Input file guide

The build script fills the Word layout from one input file (written per run into the working folder, never saved in the
skill). `scripts/placeholder_input.json` shows every field with bracketed placeholders. Plain-language map:

- Header: company, project line (units, period convention, EBITDA layer), optional stale-data note, one italic line, optional transaction table.
- Business: two paragraphs. Revenue model: stream rows, total rows, one note, one credit implication.
- Market position: one paragraph, then all nine barrier dimensions (the names are fixed in the script; supply the stated level and one line of evidence for each), the overall verdict with one note, one credit implication.
- Customers: two paragraphs, the facts rows, a contract paragraph, optional named-client table, credit implication.
- Financial summary: period columns, rows (mark key lines), a footnote, one paragraph, credit implication, sources line.
- AI exposure: two paragraphs, the exposure table, credit implication. Key issues: up to six rows.
- Key metrics: the thirteen metric rows are fixed in the script with their formulas and reference ranges. Supply only the company value for each, plus an optional note on how it was measured and an optional replacement for a reference range that does not apply.
- Open diligence (up to five asks) and an optional "figures that do not reconcile" note listing borrower figures that differ, each with both figures.

Length: every prose field has a character budget in `scripts/length_budgets.json`. The build script prints a warning when a field is over. Write to the budget; do not write long and trim.
