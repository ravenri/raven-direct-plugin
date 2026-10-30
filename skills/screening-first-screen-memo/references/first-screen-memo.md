# Starting from an existing First Screen Memo

Raven's memo builder can generate a First Screen Memo for a deal. When one exists, it is a cheaper starting point than building from scratch. When none exists, the skill does not stop; it builds directly from Raven's analysis and the source documents.

## Step 1: check whether one exists

Look at the deal's list of reports for a report whose type is exactly `first_screen_memo`.
- None found: skip to the normal build (Pass 1 and Pass 2). Do not stop and do not send the user anywhere.
- One found: use it as the starting draft.
- More than one found: take the one with the most recent created date. Array order is not guaranteed to be chronological, so check the dates.

Do not use the older Screening Memo report type as a source, however many exist and however long they are. It is a different product.

## Step 2: read it as a starting draft, not as a finished answer

Open the report and extract:
- Which of the 13 sections it already covers, and at what depth.
- Every figure, claim, and citation it carries, tagged internally as "from the existing memo." A figure in the existing memo is not verified because it is already written up. Apply the same checks as for any other sourced figure.
- Where it states a judgment (a read, a characterization, a preliminary tier) as opposed to restating a figure. Judgments are worth checking against a fresh pull of Raven's analysis, since the underlying analysis can update after the memo was generated.

Its section boundaries, wording, and formatting are not binding. If you find yourself keeping its exact sentences, stop and rewrite from the underlying facts.

## Step 3: go beyond it

Run the normal build and the Pass 2 verification exactly as if no First Screen Memo existed, with one addition: for every section it already covers, treat its coverage as a floor. Ask specifically what it missed. Where the deeper read finds something it lacked (a document-level fact, a corrected figure, a richer read), say so when reporting results.

## Step 4: merge into one memo

Produce one memo on the template, following the structure in `memo-prompt.md`.
- Where the existing memo and the deeper read agree, use the richer version. Confirm rather than assume; the existing memo's wording is sometimes tighter.
- Where they conflict on a figure, apply Protocol B in `verification-and-pass-2.md`. Neither source is automatically right.
- Where the existing memo covers a section the deeper read found thin, use its material after verifying it under Protocol A, not copied wholesale.
- Where the deeper read found something new, add it.

The result is a single memo in one voice, not two documents stitched together.
