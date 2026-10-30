# Layout specification

The template (`assets/Earnings_Quality_Template.docx`) and the helper module (`scripts/eq_docx.js`) carry these
values. Use the helper module to build the document so every run produces the same page. If you cannot run it,
follow these values exactly.

| Item | Value |
|---|---|
| Page | US Letter, landscape (12240 x 15840 twips, orientation landscape) |
| Margins | top and bottom 1008, left and right 1152, header and footer 708 |
| Content width | 13536 twips; every table's column widths sum to this |
| Body font | Open Sans 11 pt, line spacing 1.2, 7.5 pt after |
| Heading font | Libre Baskerville bold, title 19 pt, section headings 12 pt with a thin black rule beneath |
| Fonts embedded | Open Sans (regular, bold) and Libre Baskerville (regular, bold), embedded so the file renders on any machine |
| Table text | 9 pt; appendix table 8.5 pt; wide monthly tables 8 pt |
| Table fills | header D9D9D9, subtotal F2F2F2, group EDEDED, label cells F2F2F2; borders BFBFBF |
| Caption | 9.5 pt bold, number and title, scale in grey after a semicolon |
| Source and Basis lines | 8 pt grey 5A636A |
| Footer | "Confidential: internal work product" left, page number right, 7.5 pt grey |
| Charts | PNG, 860 px wide, brand colors 242D27, 5A636A, 8FA087, C1C8BA, F7F4EE; no gridlines; USD in thousands labeled |
| Numbers in tables | thousands with a comma, negatives in parentheses, nil as a hyphen, percentages to one decimal, multiples to two |
| Numbers in text | millions to one decimal with "MM", thousands as "K", percentages to one decimal, key figures in bold |

Do not use colored borders, tinted boxes or colored badges beyond the grey fills above.

## Building the document

0. Preferred route: write a content file (see `scripts/Content_Template.json`) and run `scripts/build_from_content.js`. The steps below describe what that script does and apply when building by hand.
1. Read the docx skill's SKILL.md first.
2. `const E = require('<skill>/scripts/eq_docx.js')`. Build a `children` array with `E.bullets`, `E.label`, `E.title`, `E.kv4`, `E.noteBox`,
   `E.para`, `E.h1`, `E.basis`, `E.caption`, `E.table`, `E.img`, `E.source`, `E.numbered`.
3. `await E.finish(children, { title, outPath })` writes the file and embeds the fonts.
4. Validate with the docx skill's validator, render to PDF to count pages and look at page 1 and one table page.
5. Build charts with matplotlib in the brand colors and place them with `E.img`.

Table rows are objects: `{ k: 'head' | 'sub' | 'group', i: indent, c: [cells] }`. Use `**bold**` in `E.para` and
`E.numbered` for key figures.
