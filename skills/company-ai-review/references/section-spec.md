# Section specification

Same page as the other analysis skills: US Letter landscape, Open Sans body, Libre Baskerville headings, grey table fills, a thin rule under each
section heading. The helper in `scripts/ai_docx.js` fixes these values; write only the content file. Short cells and short bullets; Table 2.1 and Table 3.1 are the only tables.

## Profile (top of page 1)
A four-column table of three rows: project and company with sector; AI net assessment (the verdict as stated with the qualifier its rationale gives, its near-term threat and
highest-credibility opportunity, or Not stated) with peer set (names, or Not available for this deal); what the deal documents cover (and flag if more
than two years old) with the last full refresh (the dashboard's date and whether figures were edited since, or Current). Then an Analyst Note of at most
two sentences, only when a trigger applies: no peer set, two sources name different risks or opportunities, a source stale or missing, R&D bases differ,
or the deal documents are more than two years old. Then, only if needed, a one-line terms line in small grey type defining the acronyms the document
uses and the basis labels.

## Sections, in this order
1. **Executive Summary.** One sentence of at most 35 words, then three one-sentence bullets, built per writing rules 6 and 3. 
2. **Risks and Opportunities.** A two-sentence lead-in, then Table 2.1 with a Risks band and an Opportunities band: up to four threats and up to three
   opportunities, the dashboard's own, in its order, leaving out any with nothing disclosed. Columns and widths: Item 2400, Mechanism 6400, Exposed segment
   3000, Rating or timing 1736; where no source assigns severity or timeline, drop the last column and use 2800, 7600, 3136. The mechanism is one sentence of at most 15 words. Rating or timing is the severity for a risk and the timeline for an
   opportunity, with "benefit unverified" where no benefit is quantified. Size 18, keepAll true so the table is never split across pages, band rows of kind sub. One short grey line under the
   table lists what is identified without a rating and what is not carried.
3. **Competitor Activity.** A one-sentence lead (how many competitors are profiled across how many product lines, whether any scale is disclosed, and
   whether any source states AI activity), then Table 3.1, then 2 to 4 bullets, per writing rule 4. Table 3.1 columns: Competitor, Competes in, Basis of
   competition; add Scale only where the dashboard discloses it, and Stated AI activity only where a source states it. Widths: three columns 2600, 4800,
   6136; with Scale 2200, 3800, 4800, 2736; with Stated AI activity 2200, 3400, 3600, 4336; with both 2000, 3000, 3200, 1900, 3436. Size 18, keepAll true,
   rows grouped by product line. One short grey line under the table lists names given without a profile. The bullets carry the company's claim against its
   own risk language, the rated competitive threats, and, where a peer set exists, what the peers' filings show; each is at most two sentences and ends in
   what it means for the borrower. A bullet states the data gap where no source says what competitors do in AI.
4. **Competitive Advantages.** One line, then four bullets per writing rule 12: what protects the borrower, with its stated durability; whether that
   protection is tested by retention or win-loss data or untested; what is not protected; and where AI cuts both ways, labeled inferred. Each bullet is at
   most two sentences.
5. **Adoption and Governance.** One line, then four short bullets with plain leads, where the sources produce them: In production (what is in production
   or planned, whether the filing calls it AI), Results (any disclosed result, spend or target, with no unquantified benefit), Ownership and oversight (who
   owns AI, board oversight, third-party model providers and data terms, and the R&D plan), Regulation (frameworks only where a source gives a basis). AI
   facts only, at most two sentences each; absences are stated here once.
6. **Credit Implications and Outlook.** One line, then three short bullets: retention and price led by the weighted exposure, reinvestment, and one
   monitoring line. Keep it short; do not size what the sources cannot size.
7. **Priority Diligence.** As many questions as the sources support, grouped under short labels, per writing rule 10. There is no fixed limit.
A single grey Sources line closes the document, naming the underlying documents once; do not cite page numbers the sources do not give.

## Length
No word or page limit. Include every finding the sources support, and keep each bullet and cell short.

## Formatting
Use the block types in `scripts/content_skeleton.json` (title, kv4, noteBox, source, h1, para, bullets, caption, table, basis, label, numbered). In
`numbered`, pass the items and the same instance number (1) for every group so numbering continues. Table 2.1 is the only table in the body (no peer,
margin or leverage tables), and there are no tiles, badges, tinted boxes or colored borders. Numbers: millions to one decimal with "MM", billions with
"B", percentages as stated.
