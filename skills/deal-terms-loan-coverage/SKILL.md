---
name: "deal-terms-loan-coverage"
description: "Renders a deal's coverage and liquidity read from Raven's Coverage & Liquidity page as a landscape Word document: capital structure and covenants at the anchor period, operating results and cash flow by projected year, debt balances over the forecast period by pari passu class, coverage and leverage ratios by period, liquidity availability, and diligence gaps. A faithful stored-read: it renders the page's own figures and never recomputes, re-scores, or invents a ratio. Adds a silent check that stated totals tie and no metric appears at two values, surfaced as Analyst Notes. Deliberately a coverage read, not a covenant deep-dive (that is Deal Terms Legal) or a lender-return calc (that is Loan Returns). Use for \"loan coverage,\" \"coverage and liquidity,\" \"can this deal service its debt,\" \"leverage and interest coverage,\" \"liquidity,\" or \"debt by year.\""
when_to_use: "Use for \"loan coverage,\" \"coverage and liquidity,\" \"can this deal service its debt,\" \"leverage and interest coverage,\" \"liquidity,\" or \"debt by year.\" Do not use for testing covenants (Test Covenants) or lender returns (Loan Returns)."
---

# Loan Coverage

Renders the deal's Coverage & Liquidity page as a Word document: whether the loan is covered by earnings (leverage and
interest coverage), by cash (free cash flow after debt service), and by liquidity, year by projected year, with the
capital structure and covenants at the anchor period. One read, faithful to the source.

**This is a stored-read, not an analysis pass.** The page presents what Raven's analysis already produced and
computes nothing. This skill retrieves it and renders it into the template. It never recomputes a ratio, fills a gap
the source leaves open, or adds a verdict. Where a figure is "Not disclosed", it renders it as such.

## Scope

The coverage and liquidity read, at the depth the page carries it. It is NOT the covenant, prepayment, and basket
deep-dive (that is Deal Terms Legal) and NOT a lender IRR/MOIC calculation (that is Loan Returns). The page carries no
verdict, rating, scorecard, or recovery grid, and this skill adds none. When the request is for any of those, say so
and point to the right read. Flag and point; do not perform.

## Assets

- `assets/loan_coverage_template.docx`: the Word template the document is built from. It carries placeholders only,
  never deal content. Never save a filled deal output into the skill.
- `scripts/build_loan_coverage.py`: fills the template from a spec file (its header lists every key). It does layout
  only and computes nothing. Write the spec fresh each run, outside the skill folder.
- `references/language-standard.md`: the house language standard.

## Language

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, quantify rather
than characterize, no em dashes, no hype adjectives, house banned-word list). Read it and apply it; do not restate its
rules here. The standard's markdown bold rule for dashboard fields does not apply in the Word document. Source lines
cite the documents and pages the page lists for that table. Never name Raven, dashboards, the vault, or records in the
document, and never expose prompt IDs or source-index brackets.

## Project Resolution

- If a project_id is already known from earlier in this conversation, use it directly.
- Otherwise, if the user named a deal, call `deal_list` to resolve it by name. Exactly one match: use it. More than
  one: present as a table (Deal, Company, Sponsor, Status, Created, no internal IDs) and ask the user to confirm. Do
  not guess.
- If no deal has been named, ask which deal before doing anything else.

**Skip-if-known (strict):** if `analysis_get_status` or the `dashboard_get(coverage_liquidity)` call is already
available from earlier in this conversation, do not re-call it.

## STEP 0: Analysis readiness

Read the analysis status from the deal list when it already returned it, and call `analysis_get_status(project_id)`
only when it did not. "Ready to view!" means proceed. Anything else: stop,
report the status, and suggest retrying once analysis completes or running `analysis_apply_start`. Do not render
coverage figures from an unready deal.

## STEP 0.5: Tool pre-load

`dashboard_get` is deferred and will error if called before it is loaded. If it has not already been loaded this
conversation, call `tool_search` to load it first.

## STEP 0.6: Staleness

Check the response's freshness signal. Coverage figures drive decisions, so a stale read is worse than a missing one.
If the source flags the data as stale, fill in the shaded Analyst Note under the cover table: the figures reflect the
last full analysis date. In the shaded note, give the dashboard's own stated reason, for example "Some figures were
edited after that analysis." Say the deal documents changed only if the freshness field says so. Confirm any figure
that drives a decision. If
no staleness signal is present, do not manufacture one; delete the note.

## Retrieve

Read the Coverage & Liquidity dashboard, whole, once, via `dashboard_get(project_id, tile="coverage_liquidity")` with
no section. The page returns four headed parts: Capital structure, Liquidity availability, Projections, and Diligence
gaps. Render them as the six parts below: Capital structure and covenants; Operating results and Capital structure
over the forecast period (both from the projected results table); Coverage and leverage ratios (from the credit
metrics); Liquidity availability; and Diligence gaps. Do not render the key assumptions. Stop and say the page has not
been regenerated on the new layout only if it returns a verdict, rating, scorecard, or recovery grid. Do not pull the
Deal Summary or any other dashboard to complete, enrich, or cross-check the page; if it appears to be missing an
instrument or a row, that is a data question for the page's own rendering, not something this skill resolves.

## How to render the six parts

- **Compute nothing.** Do not derive, total, net, subtotal, average, annualize, convert, or re-round any figure, and
  do not build a ratio from two stored inputs, even when both appear on the page.
- **Two kinds of blank.** Where the page says the documents do not disclose a figure, write "Not disclosed" and carry
  the page's reason in the note where it gives one. Where the page produced no value, leave the cell blank. Never
  convert one into the other.
- **Omit any row with no value in any period.** In a row that has some values, leave the periods without one blank.
- **Periods exactly as stored.** The anchor-period column is labeled as the page labels it, and projection columns use
  the model's own period labels. Never write "close" or "at close" in a column header or title. If the model runs
  longer than seven projected years, show the first seven and state in the source line how many were omitted.
- **Net before gross.** Where the page states both a net and a gross figure, show net first. Where only gross exists,
  label the cell gross.
- **Signs.** Outflows (interest, taxes, capital expenditures, working capital outflows, scheduled amortization) show
  in parentheses, as the page carries them.
- **Estimate markers.** Carry "~", "est.", "(estimated)", and "(derived)" exactly as the page gives them. Never add an
  estimate label to a figure the page states as fact.
- **Rows the page does not carry.** Omit any template row the page does not carry, including mandatory amortization,
  FCF after debt service, covenant level, and scenario rows. Never build them from other rows.
- **Earnings build and section rows.** Carry the earnings build lines and the page's section header rows (for example
  Earnings, Operating, Financial) as stored. Where one label carries two values, render both under that label, never
  merge or rename them, and raise an Analyst Note.
- **Page notes.** Rewrite page notes to the language standard: remove any reference to a search of the vault, spell
  out acronyms on first use, and give one consolidated source line per table.
- **Own labels.** Show each cash flow line between EBITDA and levered free cash flow as its own row under the model's
  own label. Do not drop, merge, rename, or total these lines. Debt is shown by pari passu class, with each class
  subtotal placed after the class's instruments. Label the anchor EBITDA by its canonical title, identically everywhere.

## Word Document Layout

Build the landscape Word document by writing a spec file and running `scripts/build_loan_coverage.py spec.json
out.docx`, which fills `assets/loan_coverage_template.docx` and keeps header and body column counts equal. The script
stops with a message if a row has the wrong number of values; fix the spec and rerun. Render the output to check the
layout before sharing it. Write the spec outside the skill folder. If this session cannot create files, say so and
render the same parts in chat as tables.

Sections in this order: cover table with the staleness note, Capital structure and covenants, Operating results,
Capital structure over the forecast period, Coverage and leverage ratios, Liquidity availability, Diligence gaps. Every
table has a source line underneath.

- **Cover table:** Project (project, company, sponsor), Currency and units, Anchor period, Anchor EBITDA (by its
  canonical title), Base case (model type and source file).
- **Capital structure and covenants:** columns Instrument, Amount, Pricing, x EBITDA, Cum. x EBITDA, Cum. LTV, Covenant, with the multiple by layer, the
  cumulative multiple, and the cumulative loan-to-value (LTV) as stored. Class
  subtotal rows, the Total debt row, equity rows, and Total capitalization as stored. At most two footnotes.
- **Operating results:** columns are each projected year, with no anchor column. Revenue, the anchor EBITDA, EBITDA
  margin, every model cash flow line, levered free cash flow, mandatory amortization, FCF after debt service, and
  cumulative FCF, each only where the page carries it. At most two footnotes, including the first-year basis.
- **Capital structure over the forecast period:** the anchor period then each projected year. The same instruments,
  class subtotals, and Total debt as the first table, then cash at end of period and cash interest expense. At most
  three footnotes.
- **Coverage and leverage ratios:** the anchor period then each projected year, rows in the page's own order:
  interest coverage, (EBITDA less capex) over cash interest, fixed-charge coverage, first lien net leverage, total net
  leverage, the covenant metric, one indented row per stored scenario, and the covenant level. One note, from the page
  only.
- **Liquidity availability:** an anchor period and revolver access table (item, amount, notes), then a table by year.
  One footnote.
- **Diligence gaps:** a plain numbered list of the page's open data gaps in its own order, with each title and
  description as stored and its priority. Render the diligence focus areas only if asked.

## Analyst Notes

Check silently, never narrated, that each stated total equals its stated parts within rounding, and that no metric
appears at two different values on the page. Add a shaded Analyst Note under the table it affects, for example: "Does
not tie: cash of 5.0 plus the 40.0 commitment less 0.0 drawn gives 45.0; the stored total liquidity is 25.0." Never
resolve a conflict and never pick a side. Name each figure and where it came from. If the check finds nothing, add no
note. Staleness goes in the note under the cover table.

In chat, after delivering the file, close with a plain-text link to the dashboard and one natural next step: the
source page behind a specific figure, or the covenant read (Deal Terms Legal) if covenant mechanics matter.

## Rules

- Faithful stored-read. Never compute, re-score, or invent a figure. Render exactly what the page returns.
- Render only the six parts the page carries. Never add a verdict, rating, scorecard, key metrics list, narrative,
  stress callout, or recovery grid.
- The page's capital structure is the cap table for this read. Never pull one from another source to complete it.
- Surface staleness when flagged; never manufacture it when absent.
- The check for totals that do not tie is silent. Only its output appears, as Analyst Notes.
- Language standard applies to all prose. No platform plumbing in the output.
- Scope: coverage and liquidity only. Covenant depth is Deal Terms Legal; lender returns are Loan Returns.
