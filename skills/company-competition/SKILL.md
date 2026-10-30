---
name: "company-competition"
description: "The competition read from Raven's competition_analysis vault tile: competitive position and the market-share picture, the named-competitor profiles table, margin-vs-peers, revenue defensibility, the ranked threats and opportunities with mitigants, the basis-of-competition differentiation areas, and the cost position. Its distinctive feature is the tile's own \"Claimed vs. Supported\" fact-check and data-conflict blocks (what the company asserts versus what peer filings actually corroborate), which the skill always preserves as credit-relevant, never editorial padding. Faithful stored-read: renders the tile's verdicts, tables, ranked lists, and peer benchmarks, and runs a mandatory silent second read that reconciles figures, connects sections, verifies gaps against the documents, and closes with a synthesis. Never recomputes. Offers a Word document or a chat render. Use for \"competition,\" \"competitive position,\" \"who are the competitors,\" \"moat vs peers,\" or a read on how the borrower competes."
when_to_use: "Use for \"competition,\" \"competitive position,\" \"who are the competitors,\" \"moat vs peers,\" or a read on how the borrower competes. Do not use for benchmarking against public peer filings (Peer Set), barriers to entry, or the industry read."
---

# Competition

Produces the read on how the borrower competes: where it genuinely leads and where the leadership claim
outruns the evidence, who the named competitors are and at what scale, how its margins and defensibility
screen against peers, and the threats and opportunities to its position. A companion to Business Overview
and Industry Overview.

**This is a stored-read, not an analysis pass.** Raven's Competition analysis has already synthesized
this, verdict-scored it, and — critically — fact-checked the company's claims against peer filings. This
skill renders it cleanly in the house voice and never recomputes a figure, re-scores a verdict, or
invents a claim.

**Source: the vault, section-scoped.** Read `competition_analysis` directly — the same discipline as
Business and Industry Overview. It returns the full analysis in one call across its sections (overview,
landscape & threats, basis of competition, cost position). A `comp-set` section exists but is often empty
(the named-competitor content lives in the Competitor Profiles table instead); only pull it if the user
specifically asks for peer-filing-level comp data, and if it returns empty, say so plainly and point to
the separate Peer Set skill (the `comp_analysis` tile), a different, deeper peer-filing analysis.

**The "Claimed vs. Supported" fact-check is the credit core of this read — never drop it.** Throughout the
tile, alongside each position claim, is a block comparing what the company's materials assert to what the
evidence (its own documents plus peer filings) actually supports — rendered as Claimed vs. Supported,
Company Framing Check (Framing / Evidence / Delta), and Data Conflicts (Claim / Resolution). This is not
editorial padding; it is the tile's own mechanism for separating a real competitive advantage from a
marketing claim, and it is exactly what a credit committee needs. Render every such block, faithfully.

**Two competitor lenses — keep them separate, produce both.** The read has two distinct competitor
populations, and they must not be merged:
- **The competitive field the deal describes** — the competitors named or implied in the deal materials,
  framed by product or service (who the company actually competes with in each category), including the
  market-share picture and any directly named or anonymous ("Competitor 1 / 2") competitors.
- **The public peer set** — the comp-set companies used to benchmark scale, margin, and disclosure.
These are different populations: a direct product competitor is often private and absent from the comp
set, and a public comp is often a large diversified benchmark rather than a direct competitor. Present
both, in separate blocks. Never fold a diversified public benchmark into the deal's direct-competitor
list, and never drop a named direct competitor because it is not a public comp.

**The two lenses come from different sources — pull both.**
- The **competitive field** is in `competition_analysis` (the tile you already read): the Competitor
  Profiles table, market-share table, and product-category positions.
- The **public peer set** is NOT in `competition_analysis` (its peer fields are usually empty) and is
  usually NOT in the `comp_analysis` tile either. It lives in the confirmed comp set: call
  `comp_set_get(project_id)`. If `state` is "ready" with `selected_comps`, that is the public peer set —
  render those names, and pull their financials (revenue, growth, gross/operating margin) from the
  `comp_set` filings corpus via `research_search_documents_by_type(document_types=["comp_set"], ...)`.
  Use the `target_summary` it returns for the borrower's own comparable figures. If `state` is not ready
  or there are no selected comps, the peer lens is genuinely absent: say so plainly and offer to run the
  peers (`comp_set_suggest` → `comp_set_confirm`), rather than fabricating a benchmark. Do not treat the
  empty `comp-set` section of `competition_analysis` as evidence either way — it is empty even when the
  peers are run.
The deeper filing-level peer benchmarking is the Peer Set skill's domain; this skill presents the peer
set at competition-read depth off the same comp_set source and points to Peer Set for more.

## Tone and rules

Also apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a specific source field or note; where a tile disagrees with the vault, the vault governs and the conflict is reported, never silently resolved; a tile's own internal inconsistency is evidence against that tile, not a tiebreaker.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives, house banned-word list). Read it and apply it. Do not expose platform
plumbing (no "the tile," "competition_analysis," section names, source-index brackets, `c##` IDs). Do NOT
render the tile's source-tiering language (no "Tier 3 company materials," "Tier 1 peer filings," "thin
evidence mode") — Raven has moved off that model; where the tile draws a source distinction, render it in
plain terms ("the company's materials" vs. "peer filings"), never as tiers. Note the plain data-confidence
level in the header. Peer benchmarks are labeled peer / comparable context, never the company's own facts.


**Self-check the AI-speak tells before delivering. These keep slipping through:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period. This is a find, not a read.
- Do not pass the tile's synthesis or narrative prose through verbatim; it is written loose. Rewrite to a plain declarative that leads with the mechanism and the figure.
- Headings name content, never function. "The read," "Overview," "Assessment," "The take" are defects.
- No verdict-then-hedge ("manageable but relevant," "sound, but only if Y"). State the finding, then the constraint as its own sentence.
- No X-not-Y and no hype ("well-positioned," "poised to," "robust," "compelling," "sharp move"). Lead with the fact.
- A finding is a statement carrying a figure, not a question and not a characterization where a number exists.
## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, if the user named a deal, `deal_list` to resolve. One match → use it. More than one →
  present as a markdown table (Deal, Company, Sponsor, Status, Created — no internal IDs) and ask. Do not
  guess.
- If no deal is named, ask which deal first.

**Skip-if-known (strict):** if `analysis_get_status` or `dashboard_get(competition_analysis)` is already
available from earlier in this conversation, do not re-call it.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, suggest retrying or `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`dashboard_get` is deferred; if not loaded this conversation, `tool_search` it first. The public-peer lens
uses `comp_set_get` and `research_search_documents_by_type(document_types=["comp_set"])`; the second read
uses `research_search_documents_by_type` and `deal_get_document_content` — load those when you reach them.

## Retrieve

`dashboard_get(project_id, tile="competition_analysis")` for the competitive field — one call returns the
full analysis. Then `comp_set_get(project_id)` for the public peer set; if it is ready, pull peer
financials from the `comp_set` corpus for the numbers. Read the data-confidence level and any freshness
notice first; they belong in the header.

## Render

**Render the tile's artifacts as artifacts, but write connected analysis around them — not a flat list of
headings.** Tables (Competitor Profiles, peer comparison, market share) and ranked lists (Threats,
Opportunities, differentiation areas) render as tables and ranked lists, in full, figures and ordering
intact. But the prose around them is analysis, not one-line declaratives stacked on each other: connect
the findings, and write at the level of a senior credit analyst, not a summary.

**Organize the output into FIVE numbered sections.** Group the tile's many sub-blocks into logical
sections, number them 1-5, and let each read as a section with a thesis, not a bin of headings. The order
matters — the basis of competition comes before the competitor names, and the peer positioning read comes
below the peer data, not above it.

**Lean into the Data Conflicts.** The tile's Data Conflicts and Claimed-vs-Supported blocks are the
sharpest thing in the read — where the company's claim and the evidence genuinely diverge, with a
resolution. Never bury them as inline asides. Surface each as a distinct, framed element inside the
section it belongs to, rendered as **Claim → Counter-claim → Resolution**. This is the fact-check a
committee reads first, and it is the spine of the analysis.

**Length and readability — the difference between a usable read and a wall of text. Write tight.**
- **Word budget.** Aim for ~1,200-1,500 words total across the five sections, excluding tables. No
  paragraph over ~80 words; if a point runs longer, it becomes bullets. If a section is three paragraphs
  of "first... second... third...", that is a bulleting failure.
- **Bullet anything enumerable.** Vendor groups, differentiation areas, supports/constraints, input-cost
  advantages/exposures, threats, opportunities, per-competitor reads — these are lists. Render them as
  one-line bullets (≤25 words each), not prose paragraphs strung together. Each differentiation area is a
  bullet (its claimed-vs-supported inline or as a nested line), not a paragraph.
- **One thesis paragraph per section, then artifacts.** Lead each section with a short thesis (≤60 words),
  then the tables and bullets that carry the detail. Never narrate what a table already shows.
- **No scaffolding sentences.** Never write a meta line describing the format instead of the content — no
  "the scorecard, as four judgments," "rendered in full," "the areas below each carry the same pattern,"
  "the differentiation areas are as follows." Just render the content. These are banned.
- **Keep every analytical point, but say it once, in fewer words.** Concision means removing repetition,
  hedging, and connective throat-clearing — not dropping a fact-check, a differentiation area, or a
  competitor read. Each survives, as a tight bullet or a lean sentence.

**Header:** **Competition — [Deal Name]**, with a meta line (company, sponsor, data-confidence level).

**1. Position & Verdict** — the punch line as the lead, then the **Verdict** (headline and rationale) and
the **Company Framing Check** (the claimed-vs-supported at the whole-position level, as a framed block).
Where the market splits into vendor groups (cloud-native platforms, hybrid/legacy, log/open-source),
bullet them, don't narrate them. Render the **scorecard** as clean dimension-and-assessment bullets — no
"Metric / Value" headers, and no lead-in line describing them ("the scorecard, as four judgments" and the
like are banned). Keep the verdict's meaning exact, but render obvious tile wording in standard credit
terms (e.g. "defensible," not "defendable"). This section answers: where does the company stand, and what
is the call.

**2. Basis of Competition** — up front, BEFORE the competitor names, because it is the frame that makes
the competitor discussion mean anything. A short thesis on what buyers decide on, then render the
**differentiation areas** (brand, customer base, switching costs, on-prem vs cloud dynamics, pricing, IP)
as a bullet each — the finding in a line, its claimed-vs-supported as a nested line where it matters —
never a paragraph apiece. **Pricing power** as supports/constraints bullets. **Cost position** as a
short thesis plus bulleted advantages/exposures and its cost Data Conflicts. Keep every area; render
each tight.

**3. The Competitive Field** — who the company competes with AND how it actually fares, not a bare list.
Lead with the **market position by context** (where strong, where secondary). Then the **competitive
field** — the deal's competitors by product/service — rendered WITH analysis: for each competitor or
segment, where the company wins, where it loses, and on what basis, from the Competitor Profiles and the
market-position narratives. Include the **market-share** picture (flag when the headline share is one
segment only, e.g. a low APM share that understates a stronger named presence in adjacent segments) and
**revenue defensibility** (retention, switching costs, why customers stay). Surface the market-position
and share **Data Conflicts** here. The value is the vis-à-vis, not the roster.

**4. Peer Benchmarking** — the public peer set from `comp_set_get` + the `comp_set` corpus (sourcing
above). Render the peer comparison **table first**, with the borrower's OWN figures on the SAME metric as
the peers — show operating margin, not only Adjusted EBITDA, so the comparison is like-for-like; where a
metric basis differs, normalize it or fall back to gross margin (comparable) and flag the rest. Then,
BELOW the table, the **Peer & Comp Positioning** read — the heading and synthesis sit beneath the data
they interpret, never above it. Call out lens-membership differences (a public comp that is not a direct
rival; a direct competitor absent from the comp set). If no comp set is confirmed, say the lens is absent
and offer to run it (`comp_set_suggest` → `comp_set_confirm`). **If the deal supplies its own peer-margin
chart AND a comp set is confirmed, compare the two peer universes** — they are frequently different
populations, and the peer-set choice drives the margin verdict (a deal may benchmark against a
flatteringly weak or a punishingly strong set). Show both, say which is more representative, and weight
the closest structural comp; a "below median" verdict against a cherry-picked set can flip against a
representative one, and that flip is a finding.

**5. Risks & Bottom Line** — the ranked **Threats** (severity · timeframe · scope · flagged-in-CIM · body ·
structural/operational mitigants) and **Opportunities** (timeframe · scope · already-capturing · body),
then the closing **Synthesis**: the bottom-line credit take that ties the position, the field, and the
peer read to repayment.

Close with the tile's `web_url` as a single "🔗 Open in Raven" link.

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Same discipline as Business and Industry Overview and the screening memo. It runs every time and improves
the artifact; the reader sees only its results, never the pass. After the full render exists, go back
through it and:

1. **Reconcile the two competitor lenses (do this first — it overrides the rest).** Read the deal's
   competitive-field view and the public-peer view together and make sure they are presented logically
   and do not fight each other. Resolve the common tensions coherently rather than leaving them
   contradictory: the deal's "market leader / #1" framing against public peers that are materially larger
   and more diversified; a direct product competitor's disclosed position against the benchmark peers'
   margins on a different basis; the same name appearing in both lenses. Present the two as
   complementary — the deal view answers who the company competes with, the peer view answers how it
   screens against public comps — and where they genuinely disagree, say so in the Synthesis rather than
   smoothing it over. **Also compare peer universes:** if the deal supplies its own peer-margin chart,
   check its chosen peers against the confirmed comp set — they are often different populations, and the
   peer-set choice, not the company's performance, can drive a "below/above median" verdict. Flag the
   divergence and weight the confirmed set and the closest structural comp as the more representative
   benchmark.
2. **Read across every section for consistency and connection.** Reconcile any figure appearing in more
   than one place (share, margin, EBITDA, installed-base scale) and flag disagreements. Surface the
   throughline — for a deal where the verdict is "leader in the core but not a proven whole-portfolio
   leader," the market-share table, the #2/#3 adjacency ranks, the unnamed competitors, and every
   "Claimed vs. Supported: narrower than the broad claim" block are one story about where the competitive
   advantage genuinely holds and where it is asserted.
3. **Verify the material gaps and the Claimed-vs-Supported diligence requests against the documents.** For
   the tile's "not disclosed" items and its stated diligence requests (named-peer share, retention data,
   margin on a like-for-like basis), run ONE targeted `research_search_documents_by_type` (or
   `deal_get_document_content`) to confirm each is genuinely absent. A tile's own gap is a claim to
   verify. A gap confirmed once is confirmed; don't re-query it.
4. **Run 2-3 open-ended document searches** — "what would a credit committee want to know about this
   company's competitive position that nothing in the render addresses yet" (a named competitor the tile
   missed, a lost-contract disclosure, a like-for-like peer margin).
5. **Confirm the anchor facts** (regional share, the named competitors and their scale, the margin-vs-peer
   figures) trace to source.

**The second read is silent.** No "Second Read" process block, and none of its process language reaches
the output ("a separate pass," "verified against the documents," "the open-ended search surfaced"). Its
findings weave in as substance: a reconciled figure appears corrected in place; a confirmed gap
strengthens the relevant Claimed-vs-Supported or diligence note; a material fact the tile missed (a named
competitor, a lost award) is folded into its section with its source in plain terms; and the cross-section
take is rendered as a short closing **Synthesis**, presented as a conclusion. The test that it ran is a
changed artifact, not a narrated report. Do not tell the reader it occurred; show it in a better artifact.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

After the render and the second read, read the finished piece top to bottom ONE more time, as an editor
would, and fix what this pass catches. It is internal — the reader never sees it, only its result. Check
four things:

1. **Tone and voice.** Every verdict, Resolution, and Synthesis line states a FINDING, not an instruction
   to the reader. "Underwrite the franchise, not a margin-led moat" is a defect — it directs the analyst
   and uses the banned X-not-Y construction; the fix is a finding: "the franchise breadth is evidenced;
   broad cost and margin superiority is not." Purge X-not-Y constructions, scaffolding lines ("the
   scorecard, as four judgments"), AI-speak headings, hype adjectives, and anything off the credit-desk
   register (apply `references/language-standard.md`).
2. **Coherence — does it pull together.** The §1 verdict, the §4 peer read, and the §5 bottom line must
   tell ONE consistent story. If the peer benchmarking shifted the margin read (e.g. below-median on the
   deal's chart but mid-pack on the confirmed comp set), that shift must be reflected in the verdict and
   the bottom line, not just section 4. No section may contradict another; the throughline holds end to
   end.
3. **Consistency.** A figure that appears in more than one place (share, margin, revenue, EBITDA) matches
   everywhere. No leftover metric-basis mismatch, no stale number the second read already corrected in one
   spot but not another.
4. **Readability.** Within the ~1,200-1,500 word budget, no paragraph over ~80 words, enumerable content
   actually bulleted, no scaffolding, no wall of prose.
5. **Headings and proofread.** Every section and theme heading is a clean, parallel LABEL — a noun phrase,
   plus its materiality tag where the others carry one — never an editorial phrase or a mini-thesis; the
   commentary goes in the line beneath the heading, not in it. Every heading names the content, never the analytical function — no "The read," "The take," "Overview," or "Assessment" as a heading; that is a meta-label defect. Then proofread literally: read every heading
   and figure as text, not just the layout, because a builder does not spell-check and an inconsistent or
   misspelled heading is exactly what a layout-only check misses. Then scan literally for the em-dash character (the long dash): language-standard bans it, so replace every one with a comma, semicolon, or period. This is a character search, not a judgment; a prose proofread keeps missing it, so run it as a find, not a read.

This pass is silent and its only evidence is a cleaner artifact. A read delivered without it — a directive
sitting in a Resolution, a §5 bottom line that ignores what §4 found — has not had the final review run.

## Rules

- Faithful stored-read. Never compute, re-score, or invent a verdict, band, severity, or claim — render
  what the source stores. "Not disclosed" / "N/A" renders as such.
- Organize into five numbered sections (Position & Verdict; Basis of Competition; The Competitive
  Field; Peer Benchmarking; Risks & Bottom Line) — basis of competition BEFORE the competitor names, peer
  positioning BELOW the peer table. Write connected analysis, not a stack of headings.
- Render structured artifacts as artifacts (tables, ranked lists) with figures and ordering intact;
  over-summarizing an artifact into a prose blob is the primary failure mode. The competitive field is
  rendered with per-competitor / per-segment analysis, never as a bare roster.
- Clean the scorecard (no Metric/Value headers). Render the borrower's peer-comparison figures on the
  same metric as the peers (operating margin, not only Adjusted EBITDA). Normalize metric basis before
  ranking. Render obvious tile verdict wording in standard credit terms ("defensible," not "defendable").
- NEVER drop a Claimed vs. Supported, Company Framing Check, or Data Conflicts block — it is the tile's
  fact-check of the company's claims against the evidence, and it is credit-relevant, not editorial. Lean
  INTO them: surface each as a framed Claim → Counter-claim → Resolution element, not an inline aside.
- Do not render source-tiering language (no Tier 3 / Tier 1 / thin-evidence); render source distinctions
  in plain terms. Note the plain data-confidence level in the header.
- Keep the two competitor lenses SEPARATE and produce BOTH: the deal's competitive field (competitors by
  product/service) and the public peer set (comp-set benchmarking). Never merge a diversified public
  benchmark into the direct-competitor list, or drop a named direct competitor because it is not a public
  comp. A reconciling review (see second read, step 1) ensures the two cohere and do not contradict.
- Render the peer benchmarks and Competitor Profiles, labeled as peer context; close with Peer & Comp
  Positioning. Where the tile carries no comp data, say so rather than inferring.
- If `comp-set` is pulled and returns empty, say so and point to the Peer Set skill (`comp_analysis`).
- The second read is mandatory, a separate pass after the full render, and SILENT — findings weave in as
  substance, never a rendered process block. The test that it ran is a changed artifact.
- A final whole-artifact review runs last: findings stated as findings (never directives to the reader),
  §1/§4/§5 telling one consistent story, figures matching across sections, within the word budget. It is
  silent; its only evidence is a cleaner artifact.
- Scope: the competitive read. The business profile is Business Overview; the sector read is Industry
  Overview; the deeper peer-filing benchmarking is Peer Set.

## Delivery

This is a long, committee-facing artifact, so **offer to produce it as a Word document** rather than only
dumping the full render into chat. When the user has not specified a format, offer the choice up front
with `ask_user_input_v0`: "📄 Word document (recommended for the full read)" / "💬 Render in chat". Lean
toward the document.

- **Word document** — generate via the docx skill (Arial, navy section headers, US Letter portrait),
  carrying the Competitor Profiles and Market Share tables, the ranked threats/opportunities, every
  Claimed-vs-Supported block, the Peer & Comp Positioning, and the closing Synthesis. Save to
  `/mnt/user-data/outputs/` and `present_files`. Always validate and render the docx before delivering.
- **Chat** — render inline for a quick read; still offer the Word document at the end.

After delivering, offer one natural next step: the business or industry read, the deeper Peer Set, the
source behind a figure, or the Word document if the read was in chat.
