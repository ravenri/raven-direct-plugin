---
name: "company-ai-review"
description: "Produces a Word AI review for any borrower in the house analysis format, built from the deal's own dashboards and analysis answers: the AI strategy section of the Business Overview (rated threats, opportunities and net assessment), revenue by product, AI adoption and governance, the peers' filings where a peer set exists, credit implications and priority diligence. Nothing invented. AI only; not for cyber or IT risk."
when_to_use: "Use this instead of answering ad hoc when asked for an AI review, AI exposure, AI disruption risk, what peers are doing in AI, or how AI affects a borrower's credit."
---

# Company - AI Review

A credit analyst's read of how AI affects one borrower: which revenue is exposed, how the dashboards rate each threat and opportunity, what the
company is doing and whether it is funded and governed, what peers are doing where a peer set exists, how it reaches repayment, and what to ask.
It is built only from the deal's dashboards and analysis answers, and from the peers' filings where a peer set exists. Same page as the other
analysis skills, built from a content file so every run produces the same layout.

## Scope and sources

AI only. Cyber and IT risk are out of scope. The dashboards and the analysis answers are the only sources for facts about the company. The
peers' filings are the only other source, and only through the peer search in step 4, labeled peer filing. Nothing comes from general knowledge
of the company, its competitors or the sector. Ratings and verdicts are quoted exactly as the dashboards and answers state them, never composed
and never omitted: before writing that a rating is not stated, check the dashboards.

## Language

Follow `references/language-standard.md`; do not restate it. The document never refers to the system that produced its facts: no "vault", "the AI
summary", "the reads", "the run", "the answers", "the analysis", "the tile", "the dashboard", "stored", Raven or prompt IDs. Present each finding as a
finding and name its source as the underlying document: deal materials, customer interviews, Gartner and IDC commentary, peer filings, deal
supplement, lender model, the merger proxy. Where something is not available, say what is not available, not which source lacks it. No tiles,
badges, tinted boxes or colored borders.

## Steps

1. **Resolve the deal.** Use a project_id already known; otherwise call `deal_list` once and match by project or company name. More than one match: ask. Use the borrower name from the analysis answers, not the name in a dashboard header, and tell the user in the delivery message about any mismatch between the deal, project and borrower names. Date a source only from a date it states. The same response carries `analysis_status`; stop if it is not "Ready to view!". Do not call `analysis_get_status`.
2. **Read the dashboards.** `dashboard_get` is deferred: load it with `tool_search` if needed. Section-scoped calls in one block:
   - tile `business_overview_v2`, section `strategy`: the AI Strategy block holds the threats (each with severity, exposed revenue segment and
     mechanism), the opportunities (each with timeline and mechanism), the net assessment (verdict, near-term threat, highest-credibility
     opportunity, rationale) and the regulatory risk narrative. The same section holds the strategic differentiation dimensions, the strategic moat
     with its durability, and the value creation thesis with its biggest risk;
   - tile `business_overview_v2`, section `company-summary`: the product categories with revenue and share of revenue, and the deal at a glance
     (loan, pro forma revenue and Adjusted EBITDA). These give the weights and the credit anchor;
   - tile `competition_analysis`, section `landscape-threats`: the competitor profiles (name, category, segments in competition, basis of
     competition), the market position by product line, what the company claims against what the documents support, the competitive threats with
     severity and timeframe, the revenue defensibility (switching costs, contract structure, win-loss and retention evidence, brand lock-in, IP), and the
     data conflicts. Valid sections of this tile are overview, landscape-threats, basis-of-competition,
     cost-position, competitive-advantages and differentiation-pricing; use no other name, because an unknown name returns the whole tile;
   - tile `comp_analysis`, section `peer-insights`: the peer set. If it says Comp Analysis is not available, there is no peer set.
   Record each response's freshness flag and data confidence. Take findings and figures only; skip the source lists. If the strategy section carries no AI threats, opportunities or net assessment, build Table 2.1 from AI Strategy and Competitive Position, AI Operational Threats and AI Operational Opportunities (step 3), drop the Rating or timing column, state in the Analyst Note that no source assigns severity or timeline, and put the net assessment as stated in AI Strategy and Competitive Position in the profile row. Do not compose a rating.
3. **Read the analysis answers.** One `analysis_get_question` call: AI Summary (id 290), AI Governance & Trajectory (id 289), AI Adoption & Deployment (id 274), AI Sector Exposure & Use-Case Map (id 431), AI Strategy and Competitive Position (id 262), AI Operational Opportunities (id 275), AI Operational Threats (id 276) and Diligence Focus Areas (id 2101). For a software deal add AI Impact on Industry (id 2025), AI Feature Integration & Roadmap (id 2018) and Third-Party AI Infrastructure Dependence (id 2019). Refer to each by name, never by id, in the document. A read that returns not found is simply absent. Do not read the comp set answers (ids 549, 550): they have said "not available" on a deal that has a peer set and have cited the deal's own presentation
   as peer filings.
4. **Dig into the peers' filings, only if step 2 returned a peer set.** Load the search tools with `tool_search` ("research search documents comp set"), then run
   `research_search_documents_by_type` with document_types ["comp_set"] and top_k 5, one query each: (1) AI agents, agentic and autonomous capabilities
   and strategy; (2) AI products launched, such as assistants, agents and automation features (adapt to the sector); (3) research and development
   expense, growth and percentage of revenue; (4) competition from generic LLMs, new entrants, acquisitions and consolidation; (5) pricing and
   licensing model; (6) AI regulation and governance. Then run `research_search_documents` on the deal documents for the company's own research and
   development spend and plan, and read the page with `deal_get_document_content` if only a heading comes back. Take findings and figures only. Check every peer fact taken from the peer set page against the filing before using it: its citations can point to the wrong filing. Omit any fact that cannot be confirmed.
5. **Strip number tags.** Answers carry tags such as [[n3]]. Strip every tag. Use each answer's numbers record for period and entity. A figure whose
   entity is not the subject is labeled as what it is (a customer rating, a sector survey, a peer figure), and a threshold is a limit, not an actual.
6. **Write the content file** from `references/section-spec.md`, starting from `scripts/content_skeleton.json` (the structure of
   `assets/ai_review_template.docx`).
7. **Second read.** A separate pass after the draft, never skipped. For every rating, verdict, figure and peer fact, confirm it against the dashboard or
   answer it came from and remove anything that cannot be confirmed. Confirm that no rating is described as not stated where a dashboard states it;
   that where the dashboards and the answers name different risks or opportunities both are shown; that each fact appears once; that the opening sentence
   names the largest exposed revenue and what is missing; and that nothing in a row, bullet or question would be true of any software company.
8. **Build and check.** Run `node scripts/build_from_content.js <content.json> <out.docx>` (it embeds the fonts), then
   `python scripts/check_deliverable.py <out.docx>`. Fix every FAIL, read every WARN, rebuild and check once more. The check covers dashes, system
   wording, banned words, British spellings, section order, Table 2.1, the opening sentence, bullet and question length and repeated figures; it cannot confirm that a figure matches its source, so step 7 does that. Then convert the file to PDF and view every page for split tables and layout. If scripts cannot run, say so in the first line and give the same
   sections in chat.
9. **Deliver.** Present the file with a chat summary of at most 80 words: the net assessment, the main gaps and any conflicts between sources. Do not
   rebuild to polish.

## Writing rules

1. Quote ratings; never compose or drop them. Carry each threat's severity, each opportunity's timeline, the net assessment verdict, the near-term
   threat and the highest-credibility opportunity exactly as stated. Do not carry a credibility rating for an opportunity (the house rules forbid
   rating an inferred opportunity); the highest-credibility opportunity appears only as the net assessment states it. Carry the net assessment verdict together with the qualifier its rationale gives (for example that the margin is narrow or depends on
   execution); never print the verdict bare when the rationale qualifies it, and never replace it with a conclusion of your own.
2. Section 2 opens with a lead-in of two sentences, then Table 2.1. The lead-in says how many threats are rated and how severity splits, which
   segments they bear on, and how many opportunities are timed and whether any is quantified; it states only counts, splits and timings the dashboard
   shows, never a characterization beyond it, and does not repeat the net assessment or the summary bullets. Table 2.1 carries the dashboard's threats and
   opportunities by their own names and in their order: up to four threats and up to three opportunities, leaving out any item for which no timing,
   segment or evidence is disclosed and saying so under the table. Four columns: Item, Mechanism, Exposed segment, Rating or timing. The mechanism is one
   sentence of at most 15 words, rewritten tersely and never passed through verbatim; peer filing evidence goes in a row only where it changes how the row
   reads, labeled peer filing. Exposed segment is as the dashboard states it, with the revenue and share from the product categories only where the
   dashboard names that product line directly; do not map a described exposure to a product line the dashboard does not name. Items the answers name
   that the dashboard does not go in one short grey line under the table, "Also identified, not rated:". A missing disclosure is a gap, not a risk: it
   goes in the Adoption and Governance bullets and the diligence section.
3. Weight by revenue. The opening sentence and Credit Implications lead with the revenue pool that combines the highest stated severity with its share
   of revenue. Show the loan and pro forma Adjusted EBITDA side by side where the deal at a glance gives them; compute no ratio.
4. Competitor Activity is a section of its own: a one-sentence lead, Table 3.1, then a few bullets. Table 3.1 is the competitor profiles from the
   competition dashboard, up to eight rows grouped by product line, with the columns Competitor, Competes in, and Basis of competition. Add a Scale column
   only if the dashboard discloses scale or share for at least one competitor, and a Stated AI activity column only if a source states something a
   competitor does in AI (a product shipped with its date, an acquisition, an R&D or pricing statement, labeled peer filing); never add a column whose
   cells would all read "not disclosed", and say that fact in the lead instead. Names the dashboard gives without a profile go in one short grey line
   under the table, "Also named in the filing:". The bullets carry what the table cannot: where the company's claim conflicts with its own risk language,
   the competitive threats the dashboard rates, and where a peer set exists what the peers' filings show (R&D growth against the company's plan, with the
   difference in basis stated, acquisitions, pricing, statements on competition, AI and regulation), each ending in what it means for the borrower. State
   the data gap where no source says what competitors do in AI (no peer set, comparison set omits direct competitors); never fill it from general
   knowledge of the competitors. Keep peer evidence out of Table 2.1 unless it changes how a row reads.
5. Bullets and tables, not paragraphs. Each section opens with one line that states its conclusion. A bullet states what the source shows with its
   figure and period, then why it matters to a lender, in at most two sentences, with one comparison and at most three figures. No sub-bullets and no
   bold run-in labels. Key figures in bold in bullets; table cells are plain text with no bold markers.
6. The executive summary is one sentence and three bullets. The opening sentence is one factual sentence of at most 35 words naming the
   revenue most exposed and its share, the net assessment verdict with its qualifier, and what is not disclosed. It never characterizes management intent, effort or direction
   ("spending to keep up", "falling behind", "lagging", "catching up") unless a source states it. The bullets are the highest-severity threat and the most
   credible opportunity as the dashboard states them, with what is missing, and the loan against pro forma EBITDA with how the effect reaches repayment.
   Every summary and Credit Implications bullet ties to repayment (revenue and EBITDA, then debt service); a point that cannot be tied is cut.
7. State each fact once. A figure appears at most twice in the document, once in the table or section that owns it and once where it carries a
   conclusion. A gap stated in Adoption and Governance is not repeated elsewhere except as a diligence question.
8. Report figures only as stated, with period. Do not add, subtract or combine figures. No time horizon unless a source states it. Do not carry an
   estimate a source supplies from general knowledge. When two sources give different figures or ratings for the same fact, show both and say the
   difference is not explained. Where the AI character of a disclosed capability is inferred (the filing does not call it AI), say so wherever the
   capability is called AI.
9. Adoption and Governance is four short bullets, not a table, each opening with a plain lead (In production, Results, Ownership and oversight,
   Regulation) and holding AI facts only: what is in production and whether the filing calls it AI, any result, spend or target, who owns AI, board
   oversight, third-party model and data terms, the R&D plan against peers' growth, and the regulatory framework with its basis. Revenue growth,
   executive rosters and ownership events are not AI facts and stay out. Each bullet is at most two sentences, and absences are stated here once.
10. Priority Diligence is the most important section, and it has no fixed limit. Write as many questions as the sources support, each grounded in a
    stated gap, a focus area, a data gap or the missing peer comparison. Group them under short plain labels that name the exposure each closes, with
    continuous numbering, ordered by what would most change the credit view, no intro line. Each question is one ask of at most 30 words, names a product,
    competitor or figure, and ends with the source that would answer it in a clause (a customer KPI pack, win-loss records, model validation reports,
    vendor and data contracts, reference calls, management meeting). Build them from the Diligence Gaps in the AI summary, the focus areas that bear on
    AI, competitiveness or renewals, the dashboard's data gaps that bear on technology transition, and the ownership question in the governance read.
    Never repeat a question, never ask what a source already answers or says plausibly does not exist, and never pad to reach a number.
11. Depth follows evidence. Include every finding the sources support and do not trim for length; do not pad, and do not draw on industry context to supply a risk, an opportunity or a control no source returned. State the period the deal documents cover and flag it when more than two years old; carry the dashboard's freshness flag into the profile. Where two sources disagree on a fact, say so in the Analyst Note. The Analyst Note is at most two sentences, and the terms line defines only acronyms the document uses. Sources are named once, in a single grey line at the end. Say in the Analyst Note when nothing shows low risk. Number sections consecutively after any omission.

12. Competitive Advantages is a short section of its own on what protects the borrower and what AI erodes: four bullets from the strategic moat and
    differentiation dimensions, the revenue defensibility evidence, and the AI threats and opportunities, never from general knowledge. State what
    protects the company (with its durability as stated), whether the protection is tested by retention or win-loss data or untested, what is not
    protected (patents, brand, lighter modules, as the sources say), and where AI cuts both ways, labeled inferred.

## References

- `references/language-standard.md`: language, tone and banned words.
- `references/section-spec.md`: sections, profile and formatting. Read once before writing.
- `assets/ai_review_template.docx`: a Word file showing the layout and style, with bracketed placeholders; a guideline, not the canonical form of the output.
- `scripts/content_skeleton.json`: the build input skeleton behind that template. It is a working file for the build script, not something to edit by hand or show the user.
