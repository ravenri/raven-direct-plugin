---
name: "memos-credit-assessment-full"
description: "Renders a deal's Credit Assessment as a Word document covering the eight-factor scorecard and rating, recommendation, each factor in full, key metrics to watch, other matters and analyst notes."
when_to_use: "Use for the credit assessment as a Word document, the full credit assessment, or the rating on all eight factors. Use this instead of answering ad hoc from the dashboard. For a quick rated read in chat, use screening-credit-assessment."
---

# Memos - Credit Assessment - Full

The deal's complete Credit Assessment as a Word document that follows the assessment's own structure: scorecard and rating, recommendation, eight factors in full, key metrics to watch, other matters. It is Raven's own export, cleaned and with analyst notes added, so the assessment is never retyped.

## Language
Apply references/language-standard.md. Its one-to-three-sentence limit does not apply: factor narratives keep the length the assessment carries. Ratings, scores, the composite, the recommendation and every figure stay exactly as stated; never re-score. Never expose platform terms (the vault, the tile, prompt IDs); sources are the underlying deal documents.

## Steps
1. Use the deal already identified in the conversation. Otherwise look it up by name; if several match, show a table and ask. If none is named, ask.
2. Get Raven's Word export of the deal's Credit Assessment. The export returns a download link that expires in about five minutes: download it into the working folder at once. If the assessment is not available, check the analysis status, report it, and stop. Never assemble an assessment from searches.
3. Run `python3 scripts/clean_export.py scan <export.docx> work.docx`. It fixes citation markers that landed mid-word or mid-sentence, rejoins split words, removes em dashes and platform wording in the footer, It also puts a Sources line under each factor heading naming the documents its numbers cite, taking the numbers out of the heading, and splits dense factor narratives into shorter paragraphs. It then prints a QA summary, the document text and every sentence carrying banned phrasing. Read that output once. If Summary Scorecard, Assessment Lenses, Other Matters or Sources is missing, stop and say the export format has changed.
4. Write `fixes.tsv`, one line per sentence to change: the smallest phrase to replace, a tab, its replacement, rewritten to the language standard (for example "likely repaid as structured," "supported by," "real" as an intensifier, "sound"). Never include a figure in a phrase; digits cannot change.
5. Write `notes.txt`, one note per line as `Label: text`, with **bold** on key figures. Labels: Analyst Note (inconsistency or figure to reconcile), Key Credit Concern, Counterargument, Diligence Item. Look for:
   1. The composite stated versus the mean of the rated scores in the QA summary; a rounding difference is an Analyst Note.
   2. What the Cross-Lens Checks flag, restated in plain language, plus anything they missed. An EBITDA basis seam matters most because it sets the leverage denominator.
   3. A factor whose narrative reads more negative or positive than its score.
   4. A recommendation that rests on an unresolved condition.
   5. A stress the assessment says it did not model.
   Always include the section; if nothing is real, write one line: `Analyst Note: No material issues identified.` Refer to "Raven's analysis," never "the tile."
6. Run `python3 scripts/clean_export.py apply work.docx "<Company> Credit Assessment.docx" --fixes fixes.tsv --notes notes.txt`. Fix any NOT FOUND line and rerun.
7. Present the file. The chat reply is a short summary only: recommendation, composite, headline notes. Offer one next step. Never construct an Open in Raven link or a generated date.
