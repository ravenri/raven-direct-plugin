---
name: "portfolio-analysis-deal-compare"
description: "Builds a PDF that puts two Raven deals side by side: headline terms, capital structure and paydown charts, a rated scorecard with Raven's lens drivers, and the repayment read and screening view. Figures and ratings are quoted from Raven's analysis, never recomputed."
when_to_use: "Use when asked to compare two deals, put two credits side by side, or show which of two deals repays faster or is more levered, and a document to keep or send is wanted. Not for three or more deals, not for a written memo (use the first screen memo), not for a single deal."
---

# Deal Compare PDF

Produces one PDF that puts two Raven deals next to each other. Open diligence items are not in it. The layout is fixed in `scripts/build_pdf.py` and styled by `assets/layout.cfg`. `assets/compare-template.pdf` shows the finished layout with invented figures. Do not redesign it or add tiles, colored boxes or badges. Each run only gathers Raven's figures, writes the build input, and runs the script.

## Rules

- Take every figure, rating and verdict from Raven's analysis. Quote ratings exactly. If Raven gives no rating, the PDF says Not rated. Never compose one, and check Raven's credit assessment before calling anything not rated.
- Leverage is shown gross of cash only: total debt over the anchor EBITDA, labeled gross. Never show net leverage or net debt, and never use pro forma cash funded at close to net anything.
- Leave blank any lens driver, repayment read or screening basis whose wording states a figure net of cash, and say so in a footnote. Never paraphrase it to remove the net figure.
- Third person, American spelling, no em dashes anywhere, headings included.
- Never refer to the vault, the dashboard, tiles, prompts or Raven Direct in the PDF or in the reply. Say "Raven's analysis" and name the underlying documents.
- If the two deals sit on different anchor periods, currencies or EBITDA bases, say so in the footnotes. Do not convert or restate to force a match. Name the EBITDA basis for every leverage multiple.
- If one figure differs between Raven surfaces, show the value from the deal summary and report the conflict in the reply, not in the PDF.
- The one calculation allowed is gross leverage by year. When Raven states a deal's total debt and PF Adjusted EBITDA for each year but states only net leverage (or gross at close only), divide the two, gross of cash. Say it is an analyst calculation in the leverage note, and in a footnote say which EBITDA each year carries if it differs from the anchor. Anything else you derive is labeled "analyst calculation" and stays out of the datasets.
- Carry nothing over between runs. Every run pulls fresh.

## Steps

1. Resolve both deals with `deal_list`. Ask the user only if a name matches more than one deal. Deal A is the first one named.
2. Run `dashboard_freshness` on each. Record any stale or ungenerated page for the footnotes and the reply.
3. Hand the pulls to one helper agent. Give it both project ids and the list of figures and quoted text the build input needs. It pulls both deals' pages together, takes only those items, and returns the finished build input file plus a list of any figure that differs between Raven's pages. It does not return the pages themselves. The helper pulls with `portfolio_compare`, one call per page, passing both project ids: `deal_summary_dashboard` for facilities, pricing, maturity, capitalization, entry leverage and loan to value, and `credit_assessment` for lens scores, ratings and one-sentence drivers, the overall rating, the repayment read, the preliminary screening view and its basis, modeled debt, share repaid and total debt to EBITDA by year. It takes the anchor period and EBITDA basis from the deal summary header and capitalization notes, and does not pull `financial_analysis`. If a result is marked shortened, it pulls that deal's page alone with `dashboard_get`, and uses `research_search_analysis` only to fill a specific blank.
4. The build input file is written in the scratchpad using the shape in `references/build-input.md`. Check the helper's file against its list of differing figures before building.
5. Run `python3 -I scripts/build_pdf.py <build_input> <out.pdf>`. If it prints FAIL, fix the input and run again. Do not hand edit the output. The script checks columns, deal names, blank ratings, capital structure shares, leverage and share repaid by year, net-of-cash wording, banned words, em dashes and file size, and warns where a deal's stated entry gross leverage does not equal funded debt over anchor EBITDA within 0.02x. If reportlab or matplotlib is missing, install it first. Run no other data check.
6. Name the file "<Deal A> and <Deal B> comparison.pdf" and deliver it to the user.

## Reply

Two or three sentences: what the PDF is and the single largest difference between the deals, with figures. Then a short numbered list of anything stale, missing or conflicting between Raven's surfaces, including any script warning. Say in one line what the build script's checks found.
