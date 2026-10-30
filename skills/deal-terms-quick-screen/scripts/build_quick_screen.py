#!/usr/bin/env python3
"""Fill the Deal Terms Quick Screen template from a content file.

Usage: python build_quick_screen.py content.json output.docx [template.docx]

The content file is the build input only; it is written fresh for each deal and
is never part of the skill package. Format: see references/content-format.md.
"""
import copy, json, sys, os
import docx
from docx.oxml.ns import qn
from lxml import etree

W = lambda t: qn('w:' + t)
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'


def set_p(p, text):
    runs = p.findall(W('r'))
    for r in runs[1:]:
        p.remove(r)
    t = runs[0].find(W('t'))
    t.text = text
    t.set(XML_SPACE, 'preserve')


def set_note(p, text):
    """Analyst note: bold label before the first colon, plain text after."""
    set_p(p, text)
    r = p.find(W('r'))
    label, sep, rest = text.partition(':')
    if not sep:
        return
    r.find(W('t')).text = label + ':'
    r2 = copy.deepcopy(r)
    r2.find(W('t')).text = rest
    r2.find(W('t')).set(XML_SPACE, 'preserve')
    rpr = r.find(W('rPr'))
    rpr.insert(1, etree.Element(W('b')))
    r.addnext(r2)


def cells(tr): return tr.findall(W('tc'))
def set_cell(tc, text): set_p(tc.find(W('p')), text)


def set_widths(tbl, widths):
    grid = tbl.find(W('tblGrid'))
    for g in list(grid): grid.remove(g)
    for w in widths:
        etree.SubElement(grid, W('gridCol')).set(W('w'), str(w))
    for tr in tbl.findall(W('tr')):
        for tc, w in zip(cells(tr), widths):
            tc.find(W('tcPr')).find(W('tcW')).set(W('w'), str(w))


def unkeep(tbl):
    """Long tables must be free to break across pages: drop keep-with-next from body rows."""
    for tr in tbl.findall(W('tr'))[1:]:
        for k in list(tr.iter(W('keepNext'))):
            k.getparent().remove(k)


def build(content, out, template):
    d = docx.Document(template)
    body = d.element.body
    el = list(body)
    (title, cover, spacer, stale, h_ov, ov, h_qts, grp_head, grp_tbl, grp_src,
     h_su, su, su_note, su_src, cap, cap_note, cap_src,
     h_km, km, km_src, h_notes) = el[:21]
    note_protos = el[21:25]
    sect = el[25]

    # cover
    rows = cover.findall(W('tr'))
    for tr, key in zip(rows, ['project', 'sponsor', 'transaction', 'basis']):
        set_cell(cells(tr)[1], content['cover'][key])

    # staleness note (only when the dashboard states it)
    st = content.get('stale')
    if st:
        set_cell(stale.find(W('tr')).find(W('tc')),
                 'Analyst Note: The terms shown reflect the last full analysis on %s. %s Confirm any figure that drives a decision.'
                 % (st['date'], st['reason']))
    else:
        body.remove(stale)

    set_p(ov, content['overview'])

    # term sheet groups
    head_proto, tbl_proto = copy.deepcopy(grp_head), copy.deepcopy(grp_tbl)
    body.remove(grp_head); body.remove(grp_tbl)
    for g in content['groups']:
        h = copy.deepcopy(head_proto); set_p(h, g['heading'])
        t = copy.deepcopy(tbl_proto)
        trs = t.findall(W('tr'))
        hdr, proto = trs[0], trs[1]
        for tr in trs: t.remove(tr)

        def mkrow(src, vals):
            tr = copy.deepcopy(src); c = cells(tr)
            for x in c[2:]: tr.remove(x)
            set_cell(c[0], vals[0]); set_cell(c[1], vals[1])
            for v in vals[2:]:
                nc = copy.deepcopy(c[1]); set_cell(nc, v); tr.append(nc)
            return tr

        t.append(mkrow(hdr, [''] + g['facilities']))
        for r in g['rows']:
            t.append(mkrow(proto, r))
        n = len(g['facilities']); lab = 2200
        set_widths(t, [lab] + [(9936 - lab) // n] * n)
        unkeep(t)
        grp_src.addprevious(h); grp_src.addprevious(t)
    set_p(grp_src, content['term_source'])

    # sources and uses
    trs = su.findall(W('tr'))
    hdr, d1, tot = trs[0], trs[1], trs[4]
    for tr in trs[1:]: su.remove(tr)
    S, U = content['su']['sources'], content['su']['uses']
    for i in range(max(len(S), len(U))):
        a = S[i] if i < len(S) else ['', '']
        b = U[i] if i < len(U) else ['', '']
        tr = copy.deepcopy(d1); c = cells(tr)
        set_cell(c[0], a[0]); set_cell(c[1], a[1]); set_cell(c[3], b[0]); set_cell(c[4], b[1])
        su.append(tr)
    c = cells(tot)
    set_cell(c[0], 'Total sources'); set_cell(c[1], content['su']['total_sources'])
    set_cell(c[3], 'Total uses'); set_cell(c[4], content['su']['total_uses'])
    su.append(tot)
    set_p(su_note, content['su']['note'])
    set_p(su_src, content['su']['source'])

    # capitalization (kind 1 = bold subtotal row, 0 = plain row)
    trs = cap.findall(W('tr'))
    plain, bold = trs[1], trs[3]
    for tr in trs[1:]: cap.remove(tr)
    for kind, *vals in content['cap']['rows']:
        tr = copy.deepcopy(bold if kind else plain)
        for c, v in zip(cells(tr), vals): set_cell(c, v)
        cap.append(tr)
    unkeep(cap)
    set_p(cap_note, content['cap']['note'])
    set_p(cap_src, content['cap']['source'])

    # key metrics: list of [label, value, label, value]
    trs = km.findall(W('tr'))
    proto = trs[1]
    for tr in trs[1:]: km.remove(tr)
    for r in content['metrics']:
        tr = copy.deepcopy(proto)
        for c, v in zip(cells(tr), r): set_cell(c, v)
        km.append(tr)
    set_p(km_src, content['metrics_source'])

    # analyst notes (omit the heading when there are none)
    proto = note_protos[0]
    for p in note_protos: body.remove(p)
    if content.get('notes'):
        for n in content['notes']:
            p = copy.deepcopy(proto); set_note(p, n); sect.addprevious(p)
    else:
        body.remove(h_notes)

    d.save(out)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = sys.argv[3] if len(sys.argv) > 3 else os.path.join(here, '..', 'assets', 'deal_terms_quick_screen_template.docx')
    build(json.load(open(sys.argv[1])), sys.argv[2], tpl)
