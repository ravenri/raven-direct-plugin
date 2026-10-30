#!/usr/bin/env python3
"""Pre-delivery check for an AI Review. usage: check_deliverable.py <review.docx>
Fails on: em or en dashes, platform wording, prompt IDs or number tags, banned words, British spellings, missing or out-of-order sections,
no Table 2.1 with Risks and Opportunities bands, literal bold markers or placeholders in cells, a question that
is not a question, an opening sentence that characterizes management intent or uses a slogan. Warns on: bullets over two sentences,
generic phrases, a bare strong/weak/material/key. It cannot check that a figure
equals the read it came from or that a peer fact matches its filing: do that by eye."""
import re, sys, subprocess, tempfile, os, shutil
from docx import Document
path = sys.argv[1]
fails, warns = [], []
doc = Document(path)
def sty(p):
    ppr = p._p.pPr
    return ppr.pStyle.val if ppr is not None and ppr.pStyle is not None else 'Normal'
paras = [(sty(p), p.text) for p in doc.paragraphs]
text = '\n'.join(t for _, t in paras)
cells = []
for t in doc.tables:
    for row in t.rows:
        for c in row.cells: cells.append(c.text)
alltext = text + '\n' + '\n'.join(cells)
# wording
if re.search('[\u2014\u2013]', alltext): fails.append('em or en dash found')
for pat in [r'\bvault\b', r'\bdashboards?\b', r'\bAI summary\b', r'\b(the|our|these|those) reads?\b', r'\bthe run\b', r'\bolder run\b', r'Reads missing', r'\btile\b', r'\bprompt', r'\bQ\d{3,4}\b', r'\[\[n\d+\]\]', r'\bstored\b', r'\bthe analysis\b', r'\bthe record\b', r'\bthe leaf\b',
            r'\bRaven\b', r'dashboard_', r'comp_analysis', r'deal_summary', r'significant', r'robust', r'corroborat', r'the story', r'comfortable',
            r'\btension\b', r'translates to', r'compelling', r'attractive', r'well-positioned', r'best-in-class', r'world-class', r'industry-leading',
            r'\bpremier\b', r'exceptional', r'\bhealthy\b', r'\bsolid\b', r'impressive', r'mission-critical', r'considerable', r'meaningful',
            r'proven track record', r'importantly', r'notably', r'crucially', r'on balance', r'net-net', r'from a credit perspective', r'\bleading\b',
            r'headwind', r'competitive pressure', r'arguably', r'\bquite\b', r'\bvery\b']:
    m = re.findall(pat, alltext, flags=re.I)
    if m: fails.append(f'banned or platform wording: {pat} ({len(m)})')
for pat in [r'favour', r'colour', r'organis', r'behaviour', r'\bcentre\b', r'analys(e|ed|ing)\b', r'prioritis', r'labelled', r'modelled']:
    if re.search(pat, alltext, flags=re.I): fails.append(f'British spelling: {pat}')
for pat in [r'\bstrong\b', r'\bweak\b', r'\bmaterial\b', r'\bkey\b', r'keep pace', r'keep up', r'table stakes']:
    m = re.findall(pat, alltext, flags=re.I)
    if m: warns.append(f'check wording: {pat} ({len(m)}); allowed only with a benchmark, a figure, or as a quoted read')
# sections
heads = [t for s, t in paras if s.startswith('Heading')]
order = ['Executive Summary', 'Risks and Opportunities', 'Competitor Activity', 'Competitive Advantages', 'Adoption and Governance', 'Credit Implications and Outlook', 'Priority Diligence']
pos = []
for o in order:
    idx = [i for i, h in enumerate(heads) if o in h]
    if not idx: fails.append(f'missing section: {o}')
    else: pos.append(idx[0])
if pos != sorted(pos): fails.append('sections out of order')
# opening sentence of the executive summary
cur = None; es = []
for s_, t in paras:
    if s_.startswith('Heading'): cur = t; continue
    if cur and 'Executive Summary' in cur and t.strip(): es.append(t)
if not es: fails.append('Executive Summary empty or missing')
else:
    first = es[0]
    if len(first.split()) > 40: warns.append(f'opening sentence is {len(first.split())} words (35 at most)')
    for pat in [r'spending to', r'trying to', r'struggl', r'lagging', r'falling behind', r'catching up', r'racing', r'rather than (to )?lead', r'defense, not growth',
                r'keep(ing)? up', r'behind (its )?peers', r'ahead of']:
        if re.search(pat, first, flags=re.I): fails.append(f'opening sentence characterizes intent or direction: {pat}; state the product, the competitor and what is not disclosed')
# bullets
for s_, t in paras:
    if s_.startswith('Heading') or not t.strip(): continue
    n = len(re.findall(r'[.!?](\s+[A-Z(]|$)', t))
    if len(t) > 60 and n > 2 and not t.startswith(('Terms.', 'Analyst Note', 'Not disclosed', 'Not carried', 'Basis:')):
        warns.append(f'more than two sentences: {t[:70]}...')
# tables
t21 = None
for t in doc.tables:
    first = [c.text.strip() for c in t.rows[0].cells]
    if first[:2] in (['Item', 'Mechanism'], ['Item', 'Mechanism and evidence']): t21 = t
if t21 is None: fails.append('Table 2.1 (Item, Mechanism and evidence, ...) not found')
else:
    labels = [r.cells[0].text.strip() for r in t21.rows]
    for band in ['Risks', 'Opportunities']:
        if band not in labels: fails.append(f'Table 2.1 missing band: {band}')
    if len(t21.rows) > 12: warns.append('Table 2.1 has more than 4 risks and 4 opportunities')
t31 = [t for t in doc.tables if [x.text.strip() for x in t.rows[0].cells][:2] == ['Competitor', 'Competes in']]
if not t31: warns.append('Table 3.1 (Competitor, Competes in, ...) not found; fine only if no competitors are profiled')
elif len(t31[0].rows) > 9: warns.append('Table 3.1 has more than eight competitors')
for c in cells:
    if len(c.split()) > 28 and not c.startswith('Analyst Note'): warns.append(f'dense table cell ({len(c.split())} words): {c[:50]}...')
    if '**' in c: fails.append(f'literal bold markers in a table cell: {c[:50]}')
    if c.strip().startswith('['): fails.append(f'placeholder in a table cell: {c[:50]}')
# questions
q_after = False; qs = []
for s_, t in paras:
    if s_.startswith('Heading'): q_after = 'Priority Diligence' in t; continue
    if q_after and t.strip() and not t.startswith('Sources:'): qs.append((s_, t))
labels_ = [t for s_, t in qs if len(t.split()) <= 6 and '?' not in t]
real = [t for s_, t in qs if t not in labels_]
if not real: fails.append('Priority Diligence is empty')
for t in real:
    if '?' not in t and 'None is disclosed' not in t: fails.append(f'diligence item is not a question: {t[:60]}')
    if len(t.split()) > 35: warns.append(f'question over 35 words ({len(t.split())}): {t[:60]}...')
    if t.count('?') > 1: warns.append(f'more than one ask: {t[:60]}...')
# repetition and length
import collections
figs = re.findall(r'\$\d[\d,.]*(?:MM|B)\b|\b\d+(?:\.\d+)?%', text + '\n' + '\n'.join(cells))
for k, n in collections.Counter(figs).items():
    if n > 2: warns.append(f'figure repeated {n} times: {k} (state each fact once; at most twice)')
dil_words = sum(len(t.split()) for s_, t in qs)
nwords = len((text + ' ' + ' '.join(cells)).split()) - dil_words
# pages
soffice = shutil.which('soffice') or shutil.which('libreoffice')
if soffice:
    d = tempfile.mkdtemp()
    try:
        subprocess.run([soffice, '--headless', '--convert-to', 'pdf', '--outdir', d, path], capture_output=True, timeout=120)
        pdf = os.path.join(d, os.path.splitext(os.path.basename(path))[0] + '.pdf')
        out = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
        m = re.search(r'Pages:\s+(\d+)', out)
        pass
    except Exception as e:
        warns.append(f'page count not checked: {e}')
for w in warns: print('WARN ', w)
for f in fails: print('FAIL ', f)
print('PASS' if not fails else f'{len(fails)} failures')
sys.exit(1 if fails else 0)
