# Analyst-grade discipline — shared standard

Distilled from raven-ebitda-cap, the most rigorously specified skill in the suite. Apply these five
patterns to every skill that reads a dashboard tile and the vault.

## 1. Vault-primary is structural, stated more than once, in different words

Don't say "the vault is a source" in one sentence and move on. State it in the description, in the
retrieval step, and again wherever a figure could plausibly come from the wrong place. Redundancy is the
point: a rule stated once gets skipped under pressure; stated three times in different words, it survives.
Name the reason a tile can't be trusted blind: it mislabels layers, strikes a ratio on the wrong line,
holds stale figures.

## 2. Real decision procedures, not vague instructions

Where a skill has to choose among several candidate figures or classifications, write the actual fallback
chain, in order, with the gating condition for each branch spelled out — not "select the most appropriate
figure" but "A if condition X, else B if condition Y, else C." A procedure can be followed and checked; a
vague instruction gets interpreted differently every run.

## 3. No freestanding editorial adjective — every characterization traces to a source field or note

The sharpest anti-hallucination rule in the suite. A word like "elevated," "material," "aggressive," or
"thin" is only allowed when it restates a classification, a validation status, or an explicit qualitative
note the source already recorded — never when it's an independent judgment layered on top of a number.
Where no such note exists, state the number and stop; don't dress it with an adjective. This is stronger
than a generic "findings not directives" rule because it gives a checkable test: can this word be traced
to a specific field or note? If not, cut it.

## 4. Scope boundaries carry their reason, not just their existence

"X is out of scope" is not enough on its own. State the substantive reason the boundary exists — what
would go wrong, specifically, if the skill did the excluded thing. A boundary with a reason is a design
decision the next person can evaluate; a boundary stated as a bare rule is one they'll eventually override
without understanding what it was protecting against.

## 5. Tile-vs-vault conflicts: vault wins, tile becomes color, conflict goes in the footnote

Never resolve a disagreement silently. When a dashboard tile disagrees with the vault's own figure, the
vault governs, and the disagreement is reported, not dropped. Extend the logic one step further: an
internal inconsistency inside a single tile (its own subtotals don't foot) is itself evidence against
trusting that tile — not a coin-flip to break some other way.
