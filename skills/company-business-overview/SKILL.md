---
name: "company-business-overview"
description: "Produces the comprehensive business-profile read from Raven's business_overview_v2 vault tile (not the screening memo): company summary and revenue composition, business model (revenue quality, pricing, commoditization, vulnerabilities), strategy and the moat / value-creation thesis, AI strategy, segments, products, operations (incl. cyber and carve-out readiness), and data gaps. Covers customers, suppliers, and management concisely as normal sections (their deep-dives are Customer Diligence, Suppliers & Supply Chain, Management Team). Renders the tile's verdicts, tables, ranked lists, and peer / comp benchmarks faithfully, then runs a mandatory silent second read that reconciles figures, connects sections, verifies material gaps against the documents, and closes with a synthesis. Never recomputes. Offers a Word document or a chat render. Use for \"business overview,\" \"what does this company do,\" \"business profile,\" \"company summary,\" or a first read on the business."
when_to_use: "Use for \"business overview,\" \"what does this company do,\" \"business profile,\" \"company summary,\" or a first read on the business. Do not use for a first screen memo, or for a deep read of one topic such as customers, suppliers or management."
---

# Business Overview

Produces the comprehensive read on the business itself: what the company does and how it makes money,
where the revenue is durable and where it is exposed, the strategy and what actually protects it, the
segments and products, and how it operates. The business-side companion to the credit reads.

**This is a stored-read, not an analysis pass.** Raven's Business Overview analysis has already
synthesized this, verdict-scored it, and peer-benchmarked it in the vault. This skill retrieves that and
renders it cleanly in the house voice. It never recomputes a figure, re-scores a verdict, or invents a
narrative — where a field is "Not disclosed," it renders it as such.

**Source: the vault, section-scoped — not the screening memo.** Read `business_overview_v2` directly.
It is richer, already peer-benchmarked, and section-addressable, so there is no memo pagination, no
page-budget cap, and no schema-boundary detection. This is the same source Customer Diligence,
Management Team, and Suppliers & Supply Chain read.

## Scope

The comprehensive business profile. It covers everything in `business_overview_v2`. Three sections have
their own standalone deep-dive skills — Customer Diligence, Suppliers & Supply Chain, Management Team —
so here they are kept concise (a few lines of the essentials) rather than exhaustive. But they are
presented as normal sections: no "slim" label, no inline "full read: X" pointer. Everything else
(company summary, business model, strategy, differentiation, AI strategy, segments, products,
operations, cyber, standalone readiness, data gaps) is rendered in full.

## Tone and rules

Also apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a specific source field or note; where a tile disagrees with the vault, the vault governs and the conflict is reported, never silently resolved; a tile's own internal inconsistency is evidence against that tile, not a tiebreaker.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register,
quantify rather than characterize, no em-dashes, no hype adjectives, house banned-word list). Read it and
apply it. Do not expose platform plumbing (no "the tile," "business_overview_v2," section names,
source-index brackets like `[33]`, `c##` citation IDs). Present a finding as a finding; where a source
attribution genuinely matters, say "the deal documents" or "peer filings," never the raw citation ID.
Peer benchmarks in the tile are labeled peer/comparable context, not company facts.


**Self-check the AI-speak tells before delivering. These keep slipping through:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period. This is a find, not a read.
- Do not pass the tile's synthesis or narrative prose through verbatim; it is written loose. Rewrite to a plain declarative that leads with the mechanism and the figure.
- Headings name content, never function. "The read," "Overview," "Assessment," "The take" are defects.
- No verdict-then-hedge ("manageable but relevant," "sound, but only if Y"). State the finding, then the constraint as its own sentence.
- No X-not-Y and no hype ("well-positioned," "poised to," "robust," "compelling," "sharp move"). Lead with the fact.
- A finding is a statement carrying a figure, not a question and not a characterization where a number exists.
## Project Resolution

- If a project_id is already known from earlier in this conversation, use it.
- Otherwise, if the user named a deal, call `deal_list` to resolve it. One match → use it. More than one
  → present as a markdown table (Deal, Company, Sponsor, Status, Created — no internal IDs) and ask. Do
  not guess.
- If no deal is named, ask which deal first.

**Skip-if-known (strict):** if `analysis_get_status` or the `dashboard_get(business_overview_v2)` call is
already available from earlier in this conversation, do not re-call it.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, suggest retrying or running `analysis_apply_start`.

## STEP 0.5 — Tool pre-load and staleness

`dashboard_get` is deferred; if not loaded this conversation, `tool_search` it first. The second read
(below) uses `research_search_documents_by_type` and `deal_get_document_content` — load those too when
you reach it. On the response,
check the freshness signal — if the source flags the data stale, or the generated date materially
predates the deal's latest documents, surface it as the first line of the read, plainly. Note the
tile's data-confidence level (HIGH / MEDIUM / LOW) in the header; it bears on how much weight to place
on the read. Do not manufacture a staleness claim when the field is absent.

## Retrieve

`dashboard_get(project_id, tile="business_overview_v2")` — one call returns the full profile. (The tile
is section-addressable; use a section only when the user asks for a single focused piece.) The tile
carries chart blocks (revenue mix, segment split, margins) — note the data exists and offer to visualize
it; do not echo raw chart-spec data.

## Render

**Header:** **Business Overview — [Deal Name]**, with a meta line (company, sponsor, sector, currency,
data-confidence level).

**Render the tile's artifacts as artifacts — this is the skill's core discipline.** The source is
highly structured: product tables, segment tables, ranked strengths and risks, the revenue-quality mix,
differentiation dimensions, the customer-concentration table, the margin profile, the vulnerabilities
list. These are tables and ranked lists in the source, and they render as tables and ranked lists — in
full, with their specific figures and their ordering preserved. Do NOT collapse a table or a ranked
list into a summary paragraph; that is the failure mode. The distinction: a NARRATIVE field (overview,
rationale, credit read, closing read) is prose and may be trimmed for length; a TABLE or RANKED LIST is
structured data and is rendered as-is. When a section has both, render the narrative as a lead line or
two, then the artifact beneath it — never fold the artifact into the narrative.

**Render the peer / comp benchmarks.** Most sections carry Peer Benchmark fields comparing the company
to named public comps (margins, R&D intensity, footprint, disclosure practice, pass-through terms, AI
adoption). These are third-party comparison data and a core part of the read — render them wherever the
tile provides them, labeled as peer / comparable context, never as the company's own facts. Do not drop
them. Then close the profile with a short **Peer & Comp Positioning** synthesis: how the company screens
against its comp set on the dimensions the tile benchmarks (margins, growth, disclosure, footprint,
technology / AI), drawn from the inline benchmarks — a consolidated read, not a re-derivation.

Render the sections the tile returns, in this order, each faithful to the source's own verdicts and
narratives:

1. **Company Summary** — the overview narrative (what the business does, revenue and EBITDA, the revenue
   composition by vertical and by product/service), the Deal At A Glance figures, and the product
   categories with market position. Lead here.
2. **Business Model** — a short model narrative, then the artifacts:
   - **Revenue composition and quality (combine these — both live under Business Model in the source).**
     Render the composition as tables (segment mix and end-market mix: name, revenue, %), and the
     revenue-quality mix as a table (recurring / reoccurring / transactional / project-based, each with
     its % and one-line basis), followed by the visibility indicators (backlog, contract structure,
     coverage). Together they answer where the revenue comes from and how durable it is.
   - **Margin profile** (the margin table), the **pricing model** (framework, basis, and the
     supports/constraints), and the **commoditization** verdict with its ranked competitive attributes
     and risks.
   - The ranked **business-model vulnerabilities** as a table (rank · vulnerability · severity), in the
     source's order. These are business-model-specific and may overlap the deal's Merits & Risks; do not
     assume they are the same list.
   - **Demand drivers** as a short list.
3. **Strategy & Differentiation** — render each **strategy pillar as its own item** with its specific
   figures (savings breakdowns, targets, timelines) and its peer benchmark. Do not compress the pillars
   into one paragraph — the pillars and their numbers are the point. Then the **differentiation
   dimensions** (each with its advantage type), the **strategic moat** and its durability, and the
   **value-creation thesis** (whether the tile calls it differentiated, and its biggest risk). This is
   the "reason to exist / reason to continue" read.
4. **AI Strategy** — the net assessment, the ranked threats and opportunities by revenue segment, and
   the peer-relative adoption read, when present.
5. **Segments** and **Products & Services** — the segment breakdown as a table (segment, revenue, %,
   position, and EBITDA margin where present), then the **product table** in full (product, revenue, %,
   brand, market position, verticals). Then the ranked product **strengths** and **risks** as lists,
   preserving their order and figures. Products & Services is a rich section — render its table and its
   ranked lists, never a summary paragraph in their place.
6. **Operations & Processes** — the operations areas (manufacturing/footprint, supply chain, execution,
   R&D, technology/IT, AI adoption, standalone readiness) with their strengths and risks, plus the
   **cyber risk** read (narrative, the not-disclosed data points, credit implications) and the carve-out
   / standalone-readiness picture where the deal is a carve-out.
7. **Customers & Markets** — a concise read: concentration, the retention / NRR headline, satisfaction,
   and any flagged gap. Kept brief (Customer Diligence is the deep-dive), but presented as a normal
   section — no "slim" label, no inline pointer.
8. **Suppliers** — a concise read: input categories, any single-source or concentration flag, the
   disclosure gaps. Kept brief (Suppliers & Supply Chain is the deep-dive); presented normally.
9. **Management** — the roster snapshot and any critical leadership gap (e.g. no CEO named, an interim
   CFO). Kept brief (Management Team is the deep-dive); presented normally.
10. **Peer & Comp Positioning** — the consolidated peer / comp read described in the artifact principle:
    how the company screens against its named comps across margins, growth, disclosure, footprint, and
    technology / AI, from the tile's own benchmarks. Labeled as peer context.
11. **Data Gaps** — the high- and medium-priority diligence gaps as the tile ranks them, each with its
    specific ask.

Close with the tile's `web_url` as a single "🔗 Open in Raven" link.

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

This is a committee-input artifact, so it gets a second read, the same discipline the screening memo
uses. It is an internal working step: it runs every time and improves the artifact, but the reader sees
only its results, never the pass itself (see the close of this section). It must be a distinct pass done after the Pass-1 render is complete, not a mindset carried through
the first pass — a principle folded into drafting quietly collapses into "render the tile and call it
done," with the verification never actually run. Go back through the completed overview and do all of
the following before calling it finished:

1. **Read across every section for consistency and connection.** The tile writes each section
   independently; this is where they connect. Reconcile any figure that appears in more than one place
   (revenue, EBITDA, margins, leverage, add-backs) and flag a disagreement rather than silently picking
   one. Surface the cross-section throughline — for example, an earnings base leaning on unrealized
   synergies, a value-creation thesis marked "not differentiated," and a top-of-house management
   transition are one story about execution dependence, not three unrelated facts.
2. **Verify the material gaps against the documents — do not inherit them.** For the high-priority
   "Not disclosed" items and data gaps the tile lists, run ONE targeted document search
   (`research_search_documents_by_type`, or `deal_get_document_content` for a specific page) to confirm
   each is genuinely absent, not just missing from this tile. A tile's own gap list is a claim to
   verify, not a fact to inherit. A gap confirmed once is confirmed; do not re-query it from three
   angles.
3. **Run 2-3 genuinely open-ended document searches** with no specific field in mind — "what would a
   credit committee want to know about this business that nothing in the render addresses yet." This is
   where the thing no instruction named gets found.
4. **Confirm the anchor facts** (revenue, PF Adjusted EBITDA, the add-back total, segment mix, entry
   leverage if shown) trace to the source, not just the tile's restatement.

**The second read runs every time, but the reader never sees it run.** It is silent — no "Second Read"
process block, and none of its process language reaches the output: not "a separate pass," "verified
against the documents," "the open-ended search surfaced," or "anchor facts confirmed to source." What
the reader sees is only the *result*: a sharper, internally-consistent overview whose figures reconcile,
with the second read's findings woven in as substance —
- a reconciled or corrected figure simply appears corrected, in place;
- a gap confirmed against the documents strengthens the relevant Data Gaps entry;
- a genuinely material fact the tile omitted (e.g. a pension underfunding, a thin tangible-asset base, a
  contingent liability) is folded into the section where it belongs, stated as a fact with its source
  in plain terms (not "the second read found");
- the cross-section throughline is rendered as a short closing **Synthesis** — the analytical take that
  ties the profile to what matters for repayment, presented as a conclusion, not as a process report.

The internal test that it actually ran is whether the artifact changed: if the second read leaves the
overview identical to the raw Pass-1 render, it did not happen. But that evidence is in the content, not
in a narrated report. Do not tell the reader the second read occurred; show it in a better artifact.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

After the render and the second read, read the finished piece top to bottom ONE more time, as an editor
would, and fix what this pass catches. It is internal — the reader never sees it, only its result:

1. **Tone and voice.** Every verdict and the closing Synthesis state a FINDING, not an instruction to the
   reader. A line that tells the analyst what to do ("underwrite the X, not the Y") is a defect — restate
   it as what is true. Purge X-not-Y constructions, scaffolding lines (meta-sentences describing the
   format), AI-speak headings, hype adjectives, and anything off the credit-desk register (apply
   `references/language-standard.md`).
2. **Coherence — does it pull together.** The company summary, the business-model read, and the closing Synthesis must tell one consistent story; if the second read surfaced something material (a reconciled figure, an omitted liability), it is reflected in the Synthesis, not left in one section. No section may contradict another; the
   throughline holds end to end.
3. **Consistency.** A figure that appears in more than one place (revenue, EBITDA, margins, add-backs, segment mix) matches everywhere — no
   stale number the second read corrected in one spot but not another.
4. **Readability.** Enumerable content is bulleted, not strung into prose; no paragraph is a wall; the
   piece reads at senior-analyst level, not as a stack of headings.
5. **Headings and proofread.** Every section and theme heading is a clean, parallel LABEL — a noun phrase,
   plus its materiality tag where the others carry one — never an editorial phrase or a mini-thesis; the
   commentary goes in the line beneath the heading, not in it. Every heading names the content, never the analytical function — no "The read," "The take," "Overview," or "Assessment" as a heading; that is a meta-label defect. Then proofread literally: read every heading
   and figure as text, not just the layout, because a builder does not spell-check and an inconsistent or
   misspelled heading is exactly what a layout-only check misses. Then scan literally for the em-dash character (the long dash): language-standard bans it, so replace every one with a comma, semicolon, or period. This is a character search, not a judgment; a prose proofread keeps missing it, so run it as a find, not a read.

This pass is silent and its only evidence is a cleaner artifact. A read delivered without it — a directive
sitting in the Synthesis, a closing read that ignores what an earlier section found — has not had the
final review run.

## Rules

- Faithful stored-read. Never compute, re-score, or invent a verdict, figure, or narrative — render what
  the source stores. "Not disclosed" / "N/A" renders as such, never filled.
- Render structured artifacts as artifacts: tables as tables, ranked strengths/risks as ordered lists,
  with their figures and ordering intact. Over-summarizing a table or a ranked list into a prose blob is
  the primary failure mode — do not do it. Trim narrative fields for length; never trim away a table.
- Render the peer / comp benchmarks the tile carries, labeled as peer context; never drop them and never
  present them as the company's own facts. Close with a consolidated Peer & Comp Positioning read.
- The second read is mandatory and is a separate pass after the full render, but it is SILENT — its
  findings weave into the artifact as substance (corrected figures in place, strengthened gap entries, a
  material omitted fact folded into its section, a closing Synthesis). The reader never sees the process
  or its language. The test that it ran is a changed artifact, not a narrated report.
- Render the sections the source returns; skip an empty section silently rather than rendering a blank.
- Slim, don't duplicate: customers, suppliers, and management get a few lines plus a pointer to their
  deep-dive skill, never the full treatment.
- Peer benchmarks are labeled peer/comparable context, never presented as the company's own facts.
- Vulnerabilities here are business-model-specific; do not conflate them with the full credit risk set.
- Language standard applies to all prose; no platform plumbing, no raw citation IDs, in the output.
- Surface staleness and data-confidence; never manufacture staleness when absent.
- Scope: the business profile. Coverage, covenants, and returns are the credit reads (their own skills).

## Delivery

This is a long, committee-facing artifact, so **offer to produce it as a Word document** rather than
only dumping the full render into chat. When the user has not specified a format, offer the choice up
front with `ask_user_input_v0`: "📄 Word document (recommended for the full read)" / "💬 Render in chat".
Lean toward the document — it is the natural home for a read this length, and the second read's synthesis
and folded-in findings land better in a document than in a long chat scroll.

- **Word document** — generate via the docx skill (Arial, navy section headers, US Letter portrait),
  carrying the full overview with its tables and ranked lists intact, the peer / comp benchmarks and the
  Peer & Comp Positioning read, and the closing Synthesis. Save to `/mnt/user-data/outputs/` and
  `present_files`.
- **Chat** — render inline when the user wants a quick read in the conversation; still offer the Word
  document at the end so they can keep or share it.

The chart blocks (revenue mix, segment split, margins) can be offered as inline visuals. An Excel export
is available for the purely tabular pieces if specifically wanted, but is not the default — the narrative
belongs in a document.

After delivering, offer one natural next step: the deep-dive on customers, suppliers, or management; the
source behind a specific figure; or the Word document if the read was in chat.
