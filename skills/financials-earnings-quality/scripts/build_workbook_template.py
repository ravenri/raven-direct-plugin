"""Regenerates assets/Derived_Figures_Template.xlsx: the layout for the derived-figures workbook.
Inputs are stated figures with a source (blue). Derived figures are live formulas (black) that point at Inputs.
Every D number cited in the document must have a row here."""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
F = lambda **k: Font(**{'name': 'Open Sans', 'size': 10, **k})
BLUE = F(color='0000FF'); BLK = F(); BOLD = F(bold=True); HDR = F(bold=True, color='FFFFFF')
HFILL = PatternFill('solid', fgColor='242D27'); GFILL = PatternFill('solid', fgColor='F2F2F2')
N = '#,##0;(#,##0)'; P = '0.0%'
wb = Workbook()
g = wb.active; g.title = 'Guide'
lines = ['Derived figures workbook: how to fill it (Earnings Quality)',
 '1. Inputs: one row per stated figure. Key, label, value, source (report, page). Values in blue. USD in thousands unless the label says otherwise.',
 '2. Derived: one row per derived figure, ID (D1a, D1b...), label, a live formula that points at Inputs, number format, note. Never type a derived value.',
 '3. D numbers cited in the document must match the ID prefix here (D1 covers D1a, D1b, ...).',
 '3a. Type: Calculation (arithmetic on stored inputs only) or Assumption-dependent (the result depends on what an input covers or its basis). Every Assumption-dependent row needs a Caveat.',
 '4. Recalculate and confirm zero errors before delivery. Compare every figure in the document with its row.',
 '5. Figures from other deal documents go under their own header on Inputs with the document and page as the source.',
 '6. Lines: adjustment lines or any multi-period schedule, one row per line with the periods across, values in blue. Derived formulas can point at these rows.',
 '7. Checks: every sum of lines is tied to the stated total; a difference other than rounding (1 or 2 in the last digit) is a finding to report, not a figure to fix.']
for i, t in enumerate(lines, 1):
    g.cell(i, 1, t).font = F(bold=(i == 1), size=12 if i == 1 else 10)
g.column_dimensions['A'].width = 140
ws = wb.create_sheet('Inputs')
ws['A1'] = 'Inputs: stated figures from the report and other deal documents'; ws['A1'].font = F(bold=True, size=12)
for i, h in enumerate(['Key', 'Figure', 'Value', 'Source'], 1):
    c = ws.cell(3, i, h); c.font = HDR; c.fill = HFILL
rows = [('hdr', 'Stored figures by series (example values)'),
        ('rev0', 'Revenue, latest historical period', 100000, 'Example: stored read, historical financials'),
        ('rev1', 'Revenue, first projected period', 110000, 'Example: stored read, projections'),
        ('ebm', 'EBITDA margin, latest historical period (basis stated)', 0.25, 'Example: stored read, projections')]
ref = {}; r = 4
for it in rows:
    if it[0] == 'hdr':
        ws.cell(r, 1, it[1]).font = BOLD
        for c in range(1, 5): ws.cell(r, c).fill = GFILL
        r += 1; continue
    k, l, v, s = it
    ws.cell(r, 1, k).font = BLK; ws.cell(r, 2, l).font = BLK
    c = ws.cell(r, 3, v); c.font = BLUE; c.number_format = N
    ws.cell(r, 4, s).font = BLK
    ref[k] = f'Inputs!$C${r}'; r += 1
for col, w in zip('ABCD', [10, 58, 14, 34]): ws.column_dimensions[col].width = w
wd = wb.create_sheet('Derived', 1)
wd['A1'] = 'Derived figures: live formulas on the Inputs sheet'; wd['A1'].font = F(bold=True, size=12)
for i, h in enumerate(['ID', 'Figure', 'Value', 'Note', 'D group', 'Type', 'Caveat'], 1):
    c = wd.cell(3, i, h); c.font = HDR; c.fill = HFILL
drv = [('D1a', 'Revenue growth, first projected period over latest historical', f"={ref['rev1']}/{ref['rev0']}-1", P, 'same basis and period required'),
       ('D1b', 'EBITDA margin, latest historical period', f"={ref['ebm']}", P, 'state the basis')]
for i, (d, l, f, fmt, n) in enumerate(drv, 4):
    wd.cell(i, 1, d).font = BLK; wd.cell(i, 2, l).font = BLK
    c = wd.cell(i, 3, f); c.font = BLK; c.number_format = fmt
    wd.cell(i, 4, n).font = BLK
    wd.cell(i, 5, '1').font = BLK
    wd.cell(i, 6, 'Calculation').font = BLK
    wd.cell(i, 7, '').font = BLK
for col, w in zip('ABCDEFG', [8, 70, 14, 40, 10, 22, 70]): wd.column_dimensions[col].width = w
wl = wb.create_sheet('Lines')
wl['A1'] = 'Lines: multi-period schedules, one row per line (USD thousands)'; wl['A1'].font = F(bold=True, size=12)
for i, h in enumerate(['Ref', 'Line', 'Group', 'Period 1', 'Period 2', 'Period 3', 'Period 4'], 1):
    c = wl.cell(3, i, h); c.font = HDR; c.fill = HFILL
for i, row in enumerate([(1, 'Example line A', 'Management', 100, 120, 130, 140), (2, 'Example line B', 'Management', -20, 30, 10, 15), (3, 'Example line C', 'Provider', 0, -5, 25, 40)], 4):
    for j, v in enumerate(row, 1):
        c = wl.cell(i, j, v); c.font = BLUE if j >= 4 else BLK
        if j >= 4: c.number_format = N
for col, w in zip('ABCDEFG', [6, 40, 14, 12, 12, 12, 12]): wl.column_dimensions[col].width = w
wk = wb.create_sheet('Checks')
wk['A1'] = 'Checks: sums of lines against stated totals'; wk['A1'].font = F(bold=True, size=12)
for i, h in enumerate(['Check', 'Sum of lines', 'Stated total', 'Difference', 'Status'], 1):
    c = wk.cell(3, i, h); c.font = HDR; c.fill = HFILL
wk.cell(4, 1, 'Management lines, Period 1').font = BLK
wk.cell(4, 2, '=SUMIF(Lines!$C$4:$C$6,"Management",Lines!D4:D6)').font = BLK
c = wk.cell(4, 3, 80); c.font = BLUE
wk.cell(4, 4, '=B4-C4').font = BLK
wk.cell(4, 5, '=IF(ABS(D4)<=2,"ties (rounding)","REPORT AS A FINDING")').font = BLK
for col, w in zip('ABCDE', [40, 14, 14, 12, 24]): wk.column_dimensions[col].width = w
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'Derived_Figures_Template.xlsx')
wb.save(out); print('saved', out)
