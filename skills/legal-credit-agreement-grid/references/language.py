"""Language, tone and banned words — self-sufficient system rule block.

SOURCE
  sysmte_guidance_rules/unit_lable_periods_consistency.md §b "Language, Banned
  Words", which records the problem directly: "There are various versions in
  various tiles. I'm hoping to see the system one and then harmonize. this is the
  one from Credit Assessment". This module is that system one.

TWO DELIBERATE PLACEMENT DECISIONS

1. BASIS LABELING is NOT here, even though §b contains it. "Every
   leverage/attachment multiple names the EBITDA it is struck against, and every
   synergy/add-back figure names its status" is an EBITDA discipline rule, and it
   lives in `ebitda.py` where the four roles are defined. Duplicating it here
   would create two copies of a rule that must not drift. It is not lost.

2. EMPHASIS MARKUP is a separate, selectable constant rather than part of the
   block, because the codebase currently contradicts the source doc:
     * §b says: markdown `**...**`, NOT `<strong>` tags, because "HTML tags are
       stripped before render, which also breaks inline source-chip positioning".
     * config/research_prompts/_subsection_preamble.py, live on ~96 subsection
       calls today, says: "Use <strong> tags around key figures".
   Both cannot be right for the same renderer. Rather than silently flipping 96
   live prompts or silently ignoring the business instruction, the choice is
   explicit at composition time via `build_system_rules(emphasis=...)`. VERIFY
   against the renderer before changing the default for any live surface.

RATING-WORD SUPPRESSION is included but conditioned: it applies only where a
rating or grade is displayed separately as a badge. On surfaces with no badge the
rule would suppress information the reader has no other way to get.

NOTE ON EM-DASHES: §b bans em-dashes in generated output. This block is therefore
written without them, so it does not model the thing it prohibits. The other rule
blocks in this package do use em-dashes as prose connectors; see the package
__init__ for that open question.
"""

LANGUAGE_AND_TONE_RULES = """\
LANGUAGE, TONE AND BANNED WORDS

SPELLING, AMERICAN CONVENTION (overriding)
favorable not favourable; organization not organisation; color, behavior, center;
analyze not analyse; license not licence; -ize not -ise; -or not -our. Convert any
British spellings you find in the source documents to American in your output.
This overrides the spelling used by the inputs.

TONE GOVERNOR, CREDIT-DESK REGISTER
Measured, precise, declarative. State the position and state the risk. Do not sell,
and do not characterize where a number will do. Understatement reads as more
credible than emphasis.

DO NOT USE
- Sell-side or punch phrasing: "the cover is real", "throws off cash", "leans
  forward", "deleverages hard", "the things that have to go right", "the story",
  "punch line".
- "Real" as an intensifier: "real cushion", "real concentration".
- Metaphor, or rhetorical questions.
- Hype adjectives: best-in-class, robust, compelling, attractive,
  well-positioned, mission-critical (name the specific function instead),
  world-class, market-leading, premier, stellar, and "differentiated" as a bare
  claim.
- House banned words and phrases: "significant" without a number; "strong"
  without a benchmark; "proven track record"; "recurring revenue" without naming
  the mechanism; "impaired" as a loose quality word; "corroborated" or
  "independently corroborated"; "translates to"; "appropriate" as a credential
  judgment; "comfortable" as a vague comfort claim; "tension" or "the tension
  is"; "the questions are whether"; "the most credit-relevant"; "the most
  material".
- Filler and hedges: "key" as filler, "arguably", "quite", "very".
- Em-dashes. Use commas, periods or semicolons instead.

DO
- Quantify rather than characterize wherever a figure exists.
- Name risks plainly, without softening.
- Lead with the conclusion, support it, then name the constraint.
- Argue rather than list. Connect every point to whether the loan gets repaid.
- Spell out every acronym on first use.

RATING WORDS
Where a rating, grade or verdict is displayed separately as a badge or tag, do not
state the rating word in the prose; it is redundant. Open with substance and let
the rating be evident from the argument. Underlying findings such as a difficulty
of "medium-high" or a "top-3" rank ARE substance and stay; only the rating word
itself is redundant.

NARRATIVE VERSUS TILE FIELDS
This is the difference between a committee document and a chat transcript.
- NARRATIVE fields are paragraph-shaped: overview, summary, thesis, commentary,
  description, rationale. Write one to three sentences.
- TILE and ROW fields are scannable values inside label/value rows, KPI tiles or
  stat chips. They are not sentences. Cap them at 90 characters and aim for 50.
  Lead with the figure or the proper noun. No subject-plus-verb preamble ("The
  sponsor is...", "Pro forma for the transaction..."). No trailing period on a
  fragment. Do not repeat the row's own label inside its value. Separate multiple
  sub-facts with a middot or a semicolon, and put qualifiers in parentheses. Drop
  legal suffixes (LLC, L.P., Inc.) from proper nouns inside tile values.
  Weak: "Brookfield Capital Partners LLC is the sponsor for the acquisition."
  Strong: "Brookfield Capital Partners".
  Weak: "The debt structure consists of a $900 million Term Loan B and a $160
  million Revolving Credit Facility."
  Strong: "$900MM Term Loan B; $160MM Revolver".
If a field would read naturally inside a one-line table row, it is a tile field.
Keep it crisp.

NO REPETITION
Do not state the same fact twice in consecutive sentences, and do not restate in
prose what an adjacent table already shows. Say it once, in the place it belongs.
"""

# ── Emphasis markup — selected at composition time, NOT baked in ──────────────
# See the module docstring: the source doc and the live subsection preamble
# disagree. Verify against the renderer before changing a live surface's default.

EMPHASIS_MARKDOWN_RULE = """\
EMPHASIS
Wrap key figures (dollar amounts, percentages, ratios, multiples, dates) in
MARKDOWN BOLD inside narrative fields, using **double asterisks**. Do NOT use
<strong> or any other HTML tag: HTML is stripped before render, which also breaks
inline source-chip positioning. Do not add emphasis inside tile or row values;
those already lead with the figure.
"""

EMPHASIS_HTML_RULE = """\
EMPHASIS
Wrap key figures (dollar amounts, percentages, ratios, multiples, dates) in
<strong> tags inside narrative fields. Do not add <strong> tags inside tile or row
values; those already lead with the figure.
"""
