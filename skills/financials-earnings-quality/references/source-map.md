# Source map

The only reads this skill makes. Make them in one parallel batch with `dashboard_get(project_id, tile, section)`,
and one `dashboard_freshness(project_id)` call. Read the data confidence on each result first; it goes in the
inputs register (Appendix A). Never open source documents and never run a search.

## Reads

| # | Tile | Section | Supplies |
|---|---|---|---|
| 1 | financial_analysis | historical | revenue by period and type, growth, CAGR block, margins, cost lines, the EBITDA basis and the same-basis series |
| 2 | financial_analysis | currentperiod | latest period against prior year, quarterly trend |
| 3 | financial_analysis | projections | forecast revenue and growth, EBITDA and margin, capex, key assumptions, cash flow build, the stored history-versus-projection note |
| 4 | business_overview_v2 | customers-markets | concentration, retention, churn |
| 5 | competition_analysis | (full tile) | position, threats, basis of competition, cost position |
| 6 | industry_analysis | (full tile) | growth, cyclicality, pricing power, margin profile, threats |
| 7 | barriers_to_entry | (full tile) | nine barrier verdicts, overall verdict, credit implications |
| 8 | comp_analysis | peer-benchmarking | peer margins and growth, where a peer set exists |
| 9 | credit_assessment | (full tile) | the lens ratings and drivers for: Business quality, Cash flow durability, Customer concentration, Earnings quality, Headwinds and tailwinds, and the scored key metrics to watch. Ignore the other lenses |
| 10 | (freshness check) | | whether the dashboards are stale, last full analysis, documents changed since, field dates |

Which read feeds which section: Revenue Quality from 1, 2, 4, 5, 6, 7 and the credit assessment lenses for
Business quality, Customer concentration and Headwinds and tailwinds; EBITDA Quality from 1, 2, 5 (cost position),
8 and the lenses for Earnings quality and Cash flow durability; Forecast Credibility from 3 against all of the
others and the scored key metrics to watch.

## Rules

1. **Inputs register.** Record for each read: the period it covers, the EBITDA and revenue basis it uses, its data
   confidence and its date. Use the freshness record's field dates, not a read's generated stamp (which is the time
   of the call). Where a read has no field date, say so in the register. The document shows the register in
   Appendix A without tile or section names.
2. **Same basis only.** Every series carries its basis (for example Adjusted EBITDA, PF Adjusted Cash EBITDA,
   reported). Historical and projected series are often on different bases; say so before any comparison and
   compare like with like. Where the historical read carries an EBITDA series on the projection's basis, use that
   series for the comparison. Where none exists, state that no like-for-like comparison exists in the stored reads.
3. **Same period only.** State the period of every figure. Do not set a historical figure against a forecast on a
   different period or perimeter without saying so.
4. **Fixed comparison rows.** Revenue growth, gross margin, EBITDA margin and the major cost categories, plus each
   assumption the projections read lists under key assumptions. Where a read does not carry a figure, the cell
   reads "not in the stored read".
5. **Missing or empty reads.** One line where it belongs and one question. No further searching. A peer set that
   returns the no-peer-set message is empty, not a failure.
6. **Conflicts.** Where two reads disagree, show both in Appendix A and in the section, and do not choose. Where
   one read contradicts the premise of another (for example a low barriers verdict against projected margin
   expansion), state the contradiction and what would resolve it.
7. **Stored judgments are inputs.** A stored verdict (a barrier verdict, a lens rating) is reported as that read's
   verdict. Do not restate it as Raven's own finding without the comparison behind it. Where this review's
   comparison differs from a lens rating or reading, say so and say why; do not smooth it over.
8. **Lenses are not repeated.** The credit assessment already states its lens narratives. Cite the rating in the
   table note by lens name and rating only. Discuss a lens in a bullet only where this review's comparison
   differs from it.
9. **Peers are context.** A peer figure goes in the benchmark column with the peer's name and how it was derived.
   With fewer than two peers, say no median exists.
