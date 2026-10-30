---
name: "screening-first-screen-memo"
description: "Produces a 13-section First Screen Memo for Investment Committee as a Word document, drawing on Raven's analysis and the underlying data-room documents. Written as a senior credit professional would write it, following Raven's language and conventions rules."
when_to_use: "Use when the user asks for a first screen memo, a full screening memo for IC, or a written first-pass credit memo on a deal. Do not use it to edit or reformat an existing memo, and do not use it for a quick first look at a deal; that is Initial Deal Review."
---

# First Screen Memo

## Positioning

This skill writes the First Screen Memo for a deal: 13 sections, delivered as a Word document, in the register of a senior credit professional. Its core lever is Raven's analysis, which carries pre-computed judgment and is faster to pull than a cold read of raw documents. The verification protocols, the pari passu checks, and the routing table catch the cross-source inconsistencies that a freeform pass lets through: a leverage figure that disagrees across dashboards, a mis-ranked capital structure, a comp set read as absent when only the analysis layer is missing.

Using Raven's analysis is the means, not the end. The end is the best possible memo. That requires sweeping the full corpus, Raven's analysis and the underlying documents, to go beyond the first pass and to challenge whatever looks thin, inconsistent, or suspicious, whichever source it came from. Raven's analysis first for speed and pre-computed synthesis; a full sweep for completeness and accuracy; independent reasoning throughout, not just agreement with the analysis. Treat "Raven's analysis did not have this" as a reason to check the documents next, not as a reason to write "[Not disclosed]." Treat the routing table as a floor of proven starting points, not a ceiling.

The disciplines that follow:
- Do not use Raven's citation tag syntax or JSON output. Cite in plain text, as the memo prompt describes.
- Do not read an existing Screening Memo (the older report type) and reformat it. It is a different product, not a source.
- Prefer facts and judgments from Raven's analysis when they are available and corroborated. Go to the underlying documents when the analysis lacks something, when its sources conflict in a way internal cross-checking cannot resolve, or when a figure is central enough to the memo to confirm against the primary source. Both source types get cited appropriately.

## Starting point

Check whether Raven has already generated a First Screen Memo for this deal (the list of reports carries one with the type `first_screen_memo`; if more than one, take the most recent by created date). If one exists, read it first and use it as the starting draft. Verify its figures and judgments against fresh analysis and the source documents, then edit, correct, and deepen it into the final memo. If none exists, build the memo directly from Raven's analysis and the source documents. Either way, the final memo follows the template and rules in this skill, and a prior memo's wording and section boundaries are not binding. Do not use the older Screening Memo report type as a source. The full workflow is in `references/first-screen-memo.md`.

## Deliverable

The memo is delivered as a Word document built from `assets/first-screen-memo-template.docx`. Copy the template, replace the bracketed placeholders, add table rows by copying an existing row, and delete unused notes, rows, and sections, along with the callout library page. Sections 9 and 10 stay tables. Build and present it with the Word document skill. If this session cannot create files, say so before starting and ask whether to deliver the memo in chat instead.

## Hard rules, always

- Third person only. Never "I," "my," or "our."
- No em-dashes anywhere in the memo, headings included.
- No plumbing language in the memo's prose: never "the vault," "the dashboard," or "the tile." Write "Raven's analysis" where attribution is needed.
- Pass 2 always runs once a full draft exists, and its findings are always reported alongside the memo.

## Read these before you start

- Before drafting, read `references/voice-and-reasoning.md` and `references/language-standard.md`.
- Apply Raven's conventions throughout: `references/rules-deal-context.md`, `references/rules-ebitda-basis.md`, `references/rules-units.md`, `references/rules-periods.md`, and `references/rules-consistency.md`. Establish the deal type, the currency and scale, the period anchors, and the operative EBITDA first, then use them the same way in all 13 sections.
- The 13-section structure and rigor requirements are in `references/memo-prompt.md`. Read it before drafting section 1 and re-check it whenever in doubt about section boundaries. Work from the file, not from memory.
- Before finishing, read `references/verification-and-pass-2.md`.

## Sourcing discipline vs. analytical judgment (read this before treating anything below
as a script)

Everything in the Verification discipline and Per-section sourcing sections below was
built and tested against one real deal (a reference deal). Two different kinds of
content got mixed into that routing table, and they need to be told apart:

**Rigid — follow exactly, on every deal:** the verification protocols themselves (always
check before concluding something's missing, always check documents when the vault is
thin, always weigh corroboration over mere repetition), and the render-vs-synthesize
boundary for specific objects (the scorecard, the pro forma cap table, the Structure Read). This is sourcing discipline. Getting it wrong means citing the wrong fact or
missing one that exists. The SPECIFIC tool sequences named for each field below are a
floor, not a ceiling — per the Exploration mandate above, go broader than the named
queries whenever there's reason to think more is out there.

**Illustrative, not prescriptive — a worked example from the reference deal, not a template:** the
SPECIFIC figures, counts, and conclusions quoted throughout the routing table ("5 merits,"
"Term Loan B is $1,400MM," "STABLE translates to Proceed Conditional," "AI content is
thin on this deal"). A different deal will have a different merit count, different
figures, and quite possibly a different Credit Assessment architecture entirely. Re-run
the verification protocols fresh each time; do not assume the reference deal's findings generalize.
If a future run of this skill on a new deal finds itself reaching for "the routing table
said X" where X is a deal-specific number rather than a sourcing instruction, that is
a sign the table is being read as a script instead of a worked example.

Worth being explicit about why the Verification discipline protocols below are as
detailed as they are: the point is repeatability. Running a deal through Raven's
structured regimen is what makes the same format, the same sourcing discipline, and the
same checks come out the other side on every deal, whether that deal's numbers sit in one
clean capital-structure table or are scattered across a model tab, a CIM page, and a
footnote. Reading documents ad hoc can land an easy deal correctly, but that does not
carry to the next deal or scale across a portfolio; the protocols are what turn a correct
one-off read into a standard that holds run after run. They sit on the sourcing and
formatting side and complement Claude's analytical judgment rather than second-guessing
it — the whole value of the regimen is that the output is consistent and checkable every
time, not dependent on how cooperative the source documents happen to be.

**Where the vault has already made the judgment — render it, translated into the memo's
own voice, per each section's own instruction:** the Structure Read, the Credit
Assessment Call, the scorecard ratings, the merits/risks ranking and severity, the
mitigant classification. These are pre-computed conclusions; Claude's job is to distill
and write them up, not second-guess or re-derive them. This is most of what "RENDER" means
throughout the routing table.

**Where this skill's own value proposition depends on Claude's independent judgment — do not
default to copying a label or a past run's phrasing:** the overall preliminary
recommendation tier (Proceed/Proceed Conditional/Pass) is Claude's own synthesis informed
by the vault's Call, not a mechanical translation of it — on a different deal, or even
re-reading the same facts with a different emphasis, a reasonable analyst could land on a
different tier than "Proceed Conditional," and that's fine; the goal is a well-reasoned
independent view, not agreement with the vault for its own sake. Same for what conviction
items matter most in Section 13, which merits or risks the writing gives the most weight
to within their upstream order, and the overall tone and emphasis of the memo's prose.
This is where a senior credit analyst's judgment is actually supposed to show
up — if every run produces the same conclusions Raven's own house-style Credit
Assessment rendering would have produced verbatim, this skill has quietly become a
copy of that instead of an independent analysis, which defeats the point of running it.

## Scope discipline (read before doing anything else)

- HOUSE RULE: never write "the vault," "the dashboard," "the tile," or similar plumbing
  language in the memo's own prose. This is a Word document for an investment committee,
  not a description of how it was built — a real analyst memo says "the transaction is
  struck at 4.9x EBITDA," not "the vault's deal overview shows the transaction is struck
  at 4.9x." State facts directly, the way a human analyst who had simply read the diligence
  materials would write them. The ONE exception: Analyst Notes specifically about a data
  conflict between sources may name which source said what (e.g. "the capital-structure
  waterfall shows X while the debt registry shows Y") — that is itself the analytical
  content of the note, not incidental plumbing. Outside of that narrow case, if a sentence
  would read strangely to someone who has never heard of Raven or a vault, rewrite it.
- Tools, in the order to reach for them:
  1. **Raven's analysis first**: the dashboards (any of them), a search of the deal's analysis,
     the comp set view, the diligence gaps rollup, the financial model and sheet views (cap table/model
     figures), the deal overview. Start here for every field — this is Raven's
     already-computed analysis, faster to pull and often already carries synthesis worth
     rendering rather than re-deriving. **Pull the core Pass 1 dashboards in one batch, not
     one at a time.** The dashboards a full memo always needs (Deal Summary dashboard,
     Credit Assessment dashboard, Merits & Risks dashboard, Financial Analysis dashboard, Business Overview dashboard,
     Industry Analysis dashboard, plus the comp set view) can be requested together rather than
     sequentially, since which tile fills which section does not depend on the others'
     contents. Batch them, then read. This is a latency change ONLY: the full tile set is
     non-negotiable and batching never narrows it. Do NOT pre-select "only the dashboards a
     section seems to need" — you do not know what is thin until you have read it, and the
     full-tile pull is exactly what lets Pass 2 catch a gap.
  2. **Underlying documents, sanctioned as a first-class next step, not a last resort**:
     a search of the deal's source documents (searches the parsed source documents
     directly) and reading a document page's text (pulls raw page-level text) are both
     fully allowed. Go here when: the vault returns "not available" and Protocol A's
     targeted search comes back empty or thin; vault sources conflict in a way
     vault-internal cross-checking (Protocol B) can't settle; or a figure is central
     enough to the memo (anchor facts — total debt, entry multiple, EBITDA) that
     confirming it against the primary source is worth the extra step regardless of
     whether the vault seemed to answer it. A running audit against the actual source
     documents on the reference deal found real, material content sitting ONLY in the raw
     documents with no vault Q&A object at all — a real estate collateral value slide,
     segment-specific peer trading multiples, net debt figures, specific loan
     prepayment terms. None of that should get left out of the memo just because the
     vault didn't happen to generate a Q&A object for it.
  3. **Still off-limits**: opening any existing Screening Memo, Legal Report, or Underwriting Checklist for this deal (that's a different system's finished output,
     not a source here — reading it and reformatting it defeats the purpose of writing
     an independent memo). Also off-limits: the tools that dump the whole analysis or legal review unfiltered (these
     dump everything and invite copying prose wholesale rather than synthesizing
     it — use a search of the deal's analysis or a search of the deal's source documents
     instead, both of which return targeted passages you still have to write up
     yourself).
- Do not reach for outside knowledge of the company, sponsor, or market beyond what the
  vault or the documents actually contain.
- Cite appropriately regardless of source type — internally track which source backs
  each claim, but the prose itself shouldn't announce which pipeline stage produced it
  (per the plumbing-language rule above).
- See the "Verification discipline" section below — it is not optional, and applies to
  every field in every section, not just the ones it happened to catch on the first run.

## Per-section sourcing

The section-by-section routing table (which view or dashboard surfaces which fact, target page budgets, confirmed gaps and fixes from past runs, the Scorecard exception) lives in `references/per-section-sourcing.md`. Read the "Sourcing discipline vs. analytical judgment" section above before using it. The sourcing steps apply to every deal; the specific figures and counts quoted are worked examples from the reference deal, not a template. That file grows after every real run, so add newly confirmed findings to it rather than leaving them in the conversation.

## Reference files

- `assets/first-screen-memo-template.docx`: the Word template the memo is built from.
- `references/voice-and-reasoning.md`: voice, callout boxes, reasoning and elaboration, length discipline.
- `references/verification-and-pass-2.md`: verification protocols, the Pass 2 exploration mandate, and the end-of-draft checks.
- `references/memo-prompt.md`: the 13-section structure and rigor requirements.
- `references/per-section-sourcing.md`: the section-by-section routing table.
- `references/first-screen-memo.md`: starting from an existing First Screen Memo.
- `references/language-standard.md`: Raven's language, tone and banned-words standard.
- `references/rules-*.md`: Raven's deal type, EBITDA basis, units, periods, and consistency rules.
