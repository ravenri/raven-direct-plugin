# House style

Applies to every figure and line emitted by this workflow.

- **Voice:** Documentary. Describe what the documents establish; do not deliver verdicts or
  recommendations. Rewrite source content in your own analytical voice — never copy sentences
  verbatim.
- **No freestanding editorial adjectives.** Every characterization in commentary must trace to
  a specific vault field or note: a stated classification (`adj_type` → defensibility), a QoE
  status (`validated_by`), an explicit vault assessment (e.g. Q1162's "moderate-to-aggressive"),
  or a number the reader can check. Words like "elevated," "material," "concerning," "notable,"
  or "worth flagging" are fine ONLY when they restate something the vault itself already
  concluded, in different words, never when they're Claude's own independent judgment layered
  on top of the numbers. If there's no vault note or classification backing a characterization,
  state the number and let it speak for itself, don't add an adjective to it.
- **Numeric:** millions use MM (e.g. $596MM); billions use BN (e.g. $1.4BN) — never a lone M
  for millions. Percentages like 24% (no space). Multiples like 4.8x. Negatives in
  parentheses: ($22MM).
- **Spelling:** American throughout (favorable, color, organization, normalize, recognize).
- **No em-dashes** in prose output.
- **Bold** key figures (dollar amounts, percentages, multiples, leverage, periods) in prose —
  2 to 4 per paragraph. Do not bold inside table cells.
- **Banned promotional words:** best-in-class, world-class, market-leading, robust, compelling,
  attractive, well-positioned, mission-critical, significant (without a number), strong
  (without a benchmark), exceptional, unique, differentiated, proven. Neutralize any that
  appear in the source.
- **Missing data:** never fabricate a figure, date, name, or fact. Preserve the literal
  "[Not disclosed]" where a term applies but is not in the documents; use "n/d" or "—" in
  table cells. Never leave a required cell blank; never estimate or infer.
- **Confidence:** if the vault flags a figure as indicative (e.g. sourced without a QoE
  report), carry that flag through — say the figure is indicative and why.
