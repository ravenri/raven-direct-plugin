# Content file for the build script

The build script fills the Word template from one content file written for the deal at hand. The file is build input only and is never saved inside the skill package. Every value is plain text, already conforming to the language standard.

Fields, in document order:

- cover: Project, Sponsor, Transaction, Earnings basis (the four cover table values).
- stale: only when the dashboard states the data is stale; the analysis date and the dashboard's own stated reason. Leave out otherwise and the shaded note is removed.
- overview: the two to three sentence transaction overview.
- groups: one entry per pari passu group, in capitalization table order. Each has a heading (ranking and type), the facility names (column headings), and the rows. Each row is the term label followed by one value per facility, with n/a where a card does not show the term.
- term_source: the source line under the term sheet, with the pricing estimate footnote if the source labels pricing as an estimate.
- su: sources and uses lines as label and amount pairs, the two totals, the note under the table (balance check and any footnote), and the source line.
- cap: capitalization rows, each starting with 1 for a bold subtotal or total row and 0 for a plain row, followed by Instrument, Amount, Tenor, % of cap, x EBITDA and Note; the EBITDA reference line; and the source line.
- metrics: rows of four values (metric, value, metric, value), and the source line.
- notes: the Analyst Notes, each starting with its label. Leave empty and the Analyst Notes section is removed.
