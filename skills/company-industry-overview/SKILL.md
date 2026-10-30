---
name: "company-industry-overview"
description: "The industry read for a deal, delivered as a Word document built from Raven's industry_analysis dashboard: industry definition and scorecard, market structure, labor margins and pricing, end markets and cyclicality, drivers and threats, diligence gaps, peer and comp positioning, and a closing synthesis. Renders the dashboard's verdicts, tables and ranked lists faithfully, verifies the material gaps and the peer margin table against the source documents, and never recomputes. Always Word. Use for \"industry overview,\" \"the industry,\" \"industry analysis,\" or a read on the sector the borrower operates in. Fast mode available."
when_to_use: "Use for \"industry overview,\" \"the industry,\" \"industry analysis,\" or a read on the sector the borrower operates in. Do not use for the borrower's own competitive position (Competition) or for barriers to entry."
---

# Industry Overview

Produces the industry read for a deal as a Word document: market size and growth, cycle position and how deferrable demand is, competition and concentration, margins and pricing, and the sector-level drivers, threats and diligence gaps. The industry companion to Business Overview.

**Stored-read, not an analysis pass.** Ratings, severities, verdicts and figures come from the industry_analysis dashboard and the deal documents. Never compute, re-score or invent one. A rating is never called "not stated" without checking the dashboard first. "Not disclosed" renders as such. The dashboard can be wrong, so where it disagrees with a source page, the source page governs and the conflict is reported in the document in plain terms.

**Always Word.** The output is long and committee-facing, so do not ask the user to choose a format. Chat carries a three to five sentence summary only.

## Fast mode

If the user asks for fast, quick or raw, call `dashboard_export(project_id, tile="industry_analysis", format="word")`, present the link, and say the export has had no rewrite or source verification. Otherwise run the full workflow.

## Workflow (keep every step to the minimum calls shown)

1. **Resolve the deal and load tools in one pass.** `deal_list(name=...)`. One match: use it. More than one: show a table (Deal, Company, Sponsor, Status, Created; no IDs) and ask. If the row says "Ready to view!", skip `analysis_get_status`; otherwise call it and stop if not ready. In the same turn run one `tool_search` that loads `dashboard_get`, `research_search_documents_by_type`, `get_source_page`. Skip anything already known in the conversation.
2. **Retrieve.** One call: `dashboard_get(project_id, tile="industry_analysis")`. Read the data-confidence note first.
3. **Verify, as one parallel batch in a single turn.** Do not run these one at a time.
   - One `research_search_documents_by_type(["deal"])` per HIGH priority open gap, to confirm it is absent from the deal documents. A gap confirmed once stays confirmed.
   - One search on rating-agency industry views, and one on peer filings (`["comp_set"]`) for customer concentration and supplier dependence if those are gaps.
   - `get_source_page(as_image=true)` for: the peer margin chart (always); any table whose column label disagrees with its own narrative; the downturn chart if the dashboard says peak-to-trough is not disclosed. Read the image, not the text extraction, which scrambles chart labels.
   - Cap: about six searches and three page images.
4. **Write the markdown, build, check.** Write one markdown file following the structure below, then run `scripts/build.sh draft.md /mnt/user-data/outputs/Industry_Overview_<Deal>.docx`. The script builds from `assets/industry-overview-template.docx` and runs `scripts/check.py`. If the check fails, fix the draft and rebuild. Do not render pages to images unless the check passes and something looks structurally wrong.
5. **Deliver.** `present_files` on the document. In chat, give a three to five sentence summary: the headline findings, the source conflicts found, and the dashboard data problems that belong upstream. Offer one next step: charts, the business read, or the source behind a figure.

## Document structure

Title: `Industry Overview: [Deal Name]`. Then a Meta line (borrower, sponsor, industry, currency, prepared month) and a Data confidence paragraph stating the confidence level and its practical limit (evidence dates, forecast horizons, missing independent sources). Then these sections, as numbered Heading 1 labels:

1. **Industry definition and scorecard.** Definition and demand inputs in prose; market size and growth in prose; the Scorecard table (dimension, assessment, evidence written as readable phrases, not bare numbers) with the dashboard's definitions of the rating scales as a note; the weakest dimension; the full market size and growth table with every row; the growth credit implication.
2. **Market structure.** Competitive landscape table; fragmentation; basis of competition; captive demand and regulation; buyer concentration (peer filings table where used); supply chain and the chokepoints table; credit implications.
3. **Labor, margins and pricing.** Labor; peer margins table with basis labeled; pricing power with the supports and constrains table; credit implications.
4. **End markets and cyclicality.** End markets table; aftermarket demand base where the dashboard or documents give it; cyclicality (assessment and cycle position, with the evidence date); demand shocks and downturn table; demand shock drivers table; the deferrable versus non-deferrable split stated plainly; credit implication.
5. **Drivers and threats.** The summary table, then tailwinds, mixed factors and headwinds each with its body, trade policy and peer filing context, and Technology and artificial intelligence (AI and cyber as the dashboard reports them, including "not determinable").
6. **Diligence gaps.** Key issues each with its "what to obtain" bullets; the open data gaps table (gap, what is not disclosed, priority) updated for anything the verification step found.
7. **Peer and comp positioning.** A table: growth, cyclicality, margins, pricing power, customer concentration; industry or borrower position beside peer context. Only dimensions the sources support.
8. **Synthesis.** Two or three short paragraphs of findings that run through the whole document (see Final review).

Close with a hyperlink to the dashboard `web_url`, labeled "Open in Raven".

Every dashboard credit implication is kept, in the section where the dashboard puts it, in the Credit Implication style, reworded to the rules below. Check this by counting them against the dashboard before building.

## Rendering rules

- Structured content (tables, ranked lists) renders as tables and lists with figures and order intact. Trim narratives, never a table.
- Tables are pipe tables. Set column widths with the dash counts in the separator row, for example `|:----|:--------------|`.
- Custom styles go in fenced divs: `::: {custom-style="Credit Implication"}`, `Note`, `Source Line`, `Meta`.
- No KPI tiles, stat strips, colored boxes or colored badges. Tables and prose only.
- Source lines name the document and page in plain terms (for example "lender presentation pp. 34, 37"; "peer filings"). Never source-index brackets.
- Spell out every acronym on first use. Bold key figures inside prose only, not inside table cells.
- The dashboard's own cross-reference lines ("covered under...", "on Technology Risk") are dropped. The document refers to no other page.
- Peer benchmarks are peer context, never the industry's own established facts.

## Language rules (checked by `scripts/check.py`)

American spelling. Credit-desk register: measured, precise, declarative; quantify rather than characterize.

Never use: em dashes or en dashes; the words vault, tile, dashboard, prompt IDs; sell-side or punch phrasing ("the cover is real," "throws off cash"); "real" as an intensifier; metaphor or rhetorical questions; hype adjectives (robust, compelling, attractive, well-positioned, mission-critical, world-class, market-leading, premier, stellar, best-in-class); "significant" without a number; "strong" without a benchmark; "proven track record"; "corroborated"; "translates to"; "tension"; "arguably," "quite," "very," "key" as filler; verdict-then-hedge ("manageable but relevant"); X-not-Y constructions.

Also: no freestanding editorial adjective. A word such as "elevated" or "thin" is allowed only where it restates a rating or note the source already carries. Where the dashboard text is loose (duplicated sentences, "rather than" constructions, "the vault's reads"), rewrite to a plain declarative that leads with the mechanism and the figure. Do not pass dashboard prose through verbatim.

Headings are plain noun labels. Never "Overview," "Assessment," "The read," "The take," or "Summary." Where a rating is shown in a table, do not repeat the rating word in the prose beside it.

## Verification rules

- Peer margin table: always built from the source chart image. Report any median the sources print and any disagreement between sources. Include every company on the chart.
- A dashboard "not disclosed" gap that a document search or source page fills is updated in the gaps table and in the relevant section, stating what is now disclosed and what remains absent.
- A dashboard table that contradicts its own narrative is evidence against that table. Rebuild it from the source and say which basis it uses.
- Peer filing facts (tariffs, customer concentration, supplier dependence, AI) are labeled as peer filings and attributed to the named peer.

## Final review (before building, over the whole draft)

1. Verdicts and the Synthesis state findings. A line that tells the reader what to do ("underwrite X, not Y") is restated as what is true. The "what to obtain" bullets under Diligence gaps are the only directives.
2. The scorecard, the cyclicality read and the Synthesis tell one story. If verification changed the evidence quality or a figure, it is reflected everywhere.
3. A figure that appears more than once matches everywhere.
4. Enumerable content is a table or list. No paragraph is a wall.
5. Headings are parallel noun labels. Proofread headings and figures as text.

`scripts/check.py` covers the mechanical parts (dashes, banned words, British spellings, function-label headings). The judgment parts above are still yours.

## Scope

The industry and sector read only. The company's own business profile is Business Overview; competition, barriers to entry, and AI and cyber have their own reads. Scope is kept this way so that a sector figure is never presented as a company figure; where a company figure helps (for example the share of revenue exposed to a trend), it is labeled as a company figure.

## Files

- `assets/industry-overview-template.docx`: layout and style guideline (Arial, navy headings, light gray table header, US Letter). Contains no deal content. Rebuild only with `scripts/make_template.py` when the house style changes.
- `scripts/build.sh`: markdown to Word through the template, then the check.
- `scripts/check.py`: house-rule scan of the finished document.
