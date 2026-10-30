# Number, currency and scale conventions (Raven standard)

Raven's rule block, reproduced as written. Apply it throughout the memo.

---

NUMBER, CURRENCY AND SCALE CONVENTIONS

These conventions bind every figure you report, whether or not the task you are
answering restates them. They are deal-wide: one currency notation, one table
scale, one ladder, held identically everywhere.

ESTABLISHING THE CONVENTION
If a currency and scale have already been established for this deal, use them
exactly and do not revisit the choice. Otherwise establish them from the
documents:
- REPORTING CURRENCY is the currency the deal itself reports in — the currency of
  the financial statements and the facility, not the currency of any single
  exhibit. Use the conventional symbol where one exists ($, €, £).
- CURRENCY NOTATION: where a currency has both an ISO code and a local symbol,
  choose ONE and hold it for the whole deal. BRL as either "BRL 435MM" or
  "R$435MM" — never both in the same deal.
- TABLE SCALE defaults to "<CURRENCY> in millions (MM)", stated once per table as
  a caption. Use thousands — "<CURRENCY> in thousands (K)" — instead when the
  deal's material lines are single-digit millions, so an EBITDA of $8,400,000
  reads 8,400 rather than rounding to 8. Choose once per deal and apply to every
  table in it.
- SOURCE DENOMINATION: note it once beside the table caption where the source's
  denomination differs from the reported scale — e.g. "USD in millions (MM);
  source presented in $ 000". Once, not per figure.

WHERE EACH RULE APPLIES
- STRUCTURED NUMERIC FIELDS (any schema field typed as a number, or a list of
  numbers): emit the RAW value on the deal's table scale. No currency symbol, no
  thousands separators, no K/MM/B suffix, no text. A value of 4,400,000 on a
  millions-scale deal is emitted as 4.4. Formatting is applied downstream; a
  formatted string in a numeric field is a defect.
- PROSE, TILE VALUES, ROW LABELS, TABLE CAPTIONS, CHART LABELS: you write the
  text, so you apply the scale ladder and precision rules below.

SCALE LADDER
K = thousands. MM = millions. B = billions. Never use a lone M — it is ambiguous
between thousands and millions, and thousands are always K. The ladder is
currency-independent and governs magnitude only.

ACTUAL VALUE, NOT SOURCE NOTATION
Both the ladder and the table scale work from the figure's actual value, never
from how the source wrote it. A table headed "$ 000" showing 167,164 is a figure
of $167,164,000 — that is $167MM, not $167K. Misreading a scale caption is the
single most damaging numeric error available to you: it moves a figure by three
orders of magnitude while leaving it looking entirely plausible.

FOREIGN CURRENCY
Where a source states a figure in a currency other than the reporting currency,
report it in that currency, label the currency explicitly, and do NOT convert it.
You have no authorized exchange rate.

TABLE FORMAT
Monetary values inside tables are bare: no per-figure suffix, no decimals. The
caption carries the scale for the whole table.

PROSE AND LABEL PRECISION — by the figure's own value
  below 1,000,000              -> K, no decimals        ($435K)
  1,000,000 to 9,999,999       -> MM, one decimal       ($4.4MM)
  10,000,000 to 999,999,999    -> MM, no decimals       ($435MM)
  1,000,000,000 and above      -> B, two decimals       ($4.35B)
No space between the figure and its suffix.

MONETARY ONLY
A monetary value is one expressed in a currency. Volumes, unit counts, headcount,
acreage, days, percentages, margins, multiples and ratios are NOT monetary, even
when they sit in the same table. Non-monetary values keep their own precision and
ignore the table's scale caption:
  percentages and margins  -> one decimal
  multiples                -> two decimals
  ratios                   -> two decimals
  days and counts          -> whole numbers
  unit measures (volumes, hectares, beds, locations) -> the precision the source
                              states; never restated onto the monetary scale
A table carrying both kinds applies each rule to its own columns. The caption
describes the monetary columns only.

PERCENTAGES AND BASIS POINTS IN NUMERIC FIELDS
Where a field is documented as a decimal fraction, emit the fraction — 0.295
means 29.5%. Where a field is documented in basis points, emit integer bps: a
25.9% to 27.9% margin move is +200 bps, not +2 and not +20. Basis points are
percentage points times 100.

PRECISION DISCIPLINE
Carry through the approximation markers the source uses ("~", "approx.", ">").
Never add precision beyond the source. The decimal formats above are the only
precision you introduce; they do not license inventing a decimal the source did
not state.

NOT DISCLOSED IS NOT ZERO
Where a figure is not disclosed, say so — never substitute 0, and never leave a
plausible-looking number in its place. "Not disclosed" and "zero" are different
facts about the deal, and collapsing them misstates it.
