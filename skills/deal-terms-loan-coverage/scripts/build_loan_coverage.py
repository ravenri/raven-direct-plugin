#!/usr/bin/env python3
"""Fill assets/loan_coverage_template.docx from a spec file and save a Word document.

Usage: python build_loan_coverage.py spec.json out.docx

The spec is a build input written fresh each run from the page's own figures. Keep no real
deal spec in the skill package. The script does only layout work: it clones the template's
rows, keeps header and body column counts equal, fills footnotes, source lines, shaded notes
and the numbered gap list. It never computes or alters a figure.

Spec keys (all text is written exactly as given):
  cover: [project line, currency and units, anchor period, anchor EBITDA, base case]
  stale_note: text or null            (shaded note under the cover table)
  anchor_label: anchor period label, for example "LTM 3Q22"
  years: list of projected period labels (up to 7)
  cap:      {rows: [{label, values[6], bold}], footnotes: [..], source, note}
            values order: Amount, Pricing, x EBITDA, Cum. x EBITDA, Cum. LTV, Covenant
  ops:      {rows: [{label, values[len(years)], bold}], footnotes, source, note}
  forecast: {rows: [{label, values[1+len(years)], bold}], footnotes, source, note}
  ratios:   {rows: [{label, values[1+len(years)], bold}], footnotes, source, note}
  liq_anchor: {rows: [{label, values[2], bold}]}
  liq_years:  {rows: [{label, values[len(years)], bold}], footnotes, source, note}
  gaps: [{title, text, priority}]   (priority optional)
"""
import copy, json, sys
from docx import Document
from docx.oxml.ns import qn

TEMPLATE = __file__.rsplit('/scripts/', 1)[0] + '/assets/loan_coverage_template.docx'
XS = '{http://www.w3.org/XML/1998/namespace}space'

def rows(t): return t.findall(qn('w:tr'))
def cells(r): return r.findall(qn('w:tc'))
def ptext(p): return ''.join(t.text or '' for t in p.iter(qn('w:t')))

def set_p(p, text):
    runs = p.findall(qn('w:r'))
    for r in runs[1:]: p.remove(r)
    t = runs[0].find(qn('w:t')); t.text = text; t.set(XS, 'preserve')

def is_bold(tr):
    r = cells(tr)[0].find('.//' + qn('w:r'))
    return r is not None and r.find(qn('w:rPr')).find(qn('w:b')) is not None

def set_widths(tbl, widths):
    g = tbl.find(qn('w:tblGrid')).findall(qn('w:gridCol'))
    for c, w in zip(g, widths): c.set(qn('w:w'), str(w))
    for tr in rows(tbl):
        for tc, w in zip(cells(tr), widths):
            tc.find(qn('w:tcPr')).find(qn('w:tcW')).set(qn('w:w'), str(w))

def fill(tbl, header, data, ncols):
    rs = rows(tbl)
    hdr = rs[0]
    normal = next((r for r in rs[1:] if not is_bold(r)), rs[1])
    bold = next((r for r in rs[1:] if is_bold(r)), rs[1])
    for r in rs[1:]: tbl.remove(r)
    if len(header) != ncols: raise SystemExit(f'header has {len(header)} cells, table needs {ncols}')
    for tc, h in zip(cells(hdr), header): set_p(tc.find(qn('w:p')), h)
    for row in data:
        vals = row['values']
        if len(vals) != ncols - 1:
            raise SystemExit(f"row '{row['label']}' has {len(vals)} values, expected {ncols-1}")
        tr = copy.deepcopy(bold if row.get('bold') else normal)
        for tc, v in zip(cells(tr), [row['label']] + vals): set_p(tc.find(qn('w:p')), v)
        tbl.append(tr)

def pad_year_cols(tbl, width_label, width_period, nperiods):
    """Template columns are fixed at label + 8 periods. Trim unused period columns."""
    n = 1 + nperiods
    for tr in rows(tbl):
        cs = cells(tr)
        for tc in cs[n:]: tr.remove(tc)
    g = tbl.find(qn('w:tblGrid')).findall(qn('w:gridCol'))
    for c in g[n:]: c.getparent().remove(c)
    total = 14112
    w = (total - width_label) // nperiods
    set_widths(tbl, [width_label] + [w] * nperiods)

def main(spec_path, out_path):
    spec = json.load(open(spec_path))
    d = Document(TEMPLATE)
    body = d.element.body
    kids = list(body.iterchildren())
    tbls = [k for k in kids if k.tag == qn('w:tbl')]
    notes = [t for t in tbls if len(rows(t)) == 1 and ptext(t).startswith('Analyst Note')]
    data_tbls = [t for t in tbls if t not in notes]
    cover, cs, ops, fc, rt, lq1, lq2 = data_tbls
    note_proto = copy.deepcopy(notes[0])
    for n in notes: body.remove(n)

    paras = [k for k in kids if k.tag == qn('w:p')]
    srcs = [p for p in paras if ptext(p).startswith('Source:')]
    fns = [p.getprevious() for p in srcs]
    src_cs, src_ops, src_fc, src_rt, src_lq = srcs
    fn_cs, fn_ops, fn_fc, fn_rt, fn_lq = fns
    head_ops = next(p for p in paras if ptext(p).startswith('Operating results'))
    gap_paras = [p for p in paras if p.find('.//' + qn('w:numPr')) is not None]

    years = spec['years']; ny = len(years)
    anchor = spec['anchor_label']

    # cover
    for tr, v in zip(rows(cover), spec['cover']): set_p(cells(tr)[1].find(qn('w:p')), v)
    if spec.get('stale_note'): add_note(body, cover, note_proto, spec['stale_note'])

    set_p(head_ops, f"Operating results: projected {years[0]} to {years[-1]}")

    # capital structure (7 columns in template)
    fill(cs, ['Instrument', 'Amount', 'Pricing', 'x EBITDA', 'Cum. x EBITDA', 'Cum. LTV', 'Covenant'],
         spec['cap']['rows'], 7)
    # operating results: label + years
    pad_year_cols(ops, 3605, 1501, ny)
    fill(ops, ['USD MM'] + years, spec['ops']['rows'], 1 + ny)
    # forecast and ratios: label + anchor + years
    for t in (fc, rt): pad_year_cols(t, 3600, 1314, 1 + ny)
    fill(fc, ['Balance, end of period', anchor] + years, spec['forecast']['rows'], 2 + ny)
    fill(rt, ['Ratio', anchor] + years, spec['ratios']['rows'], 2 + ny)
    fill(lq1, ['Anchor period and revolver access', 'Amount', 'Notes'], spec['liq_anchor']['rows'], 3)
    pad_year_cols(lq2, 3605, 1501, ny)
    fill(lq2, ['Component'] + years, spec['liq_years']['rows'], 1 + ny)

    def foot(fn_p, src_p, sec):
        fl = sec.get('footnotes') or []
        if fl:
            set_p(fn_p, fl[0]); last = fn_p
            for t in fl[1:]:
                n = copy.deepcopy(fn_p); set_p(n, t); last.addnext(n); last = n
        else:
            body.remove(fn_p)
        set_p(src_p, 'Source: ' + sec['source'].removeprefix('Source: '))
        if sec.get('note'): add_note(body, src_p, note_proto, sec['note'])
    foot(fn_cs, src_cs, spec['cap']); foot(fn_ops, src_ops, spec['ops'])
    foot(fn_fc, src_fc, spec['forecast']); foot(fn_rt, src_rt, spec['ratios'])
    foot(fn_lq, src_lq, spec['liq_years'])

    # gaps
    proto = gap_paras[0]
    for p in gap_paras[1:]: body.remove(p)
    last = proto
    for i, g in enumerate(spec['gaps']):
        txt = f"{g['title']}: {g['text']}" + (f" Priority: {g['priority']}." if g.get('priority') else '')
        p = proto if i == 0 else copy.deepcopy(proto)
        set_p(p, txt)
        if i: last.addnext(p); last = p
    d.save(out_path)

def add_note(body, after, proto, text):
    n = copy.deepcopy(proto)
    for p in n.iter(qn('w:p')):
        if p.findall(qn('w:r')): set_p(p, text); break
    after.addnext(n)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
