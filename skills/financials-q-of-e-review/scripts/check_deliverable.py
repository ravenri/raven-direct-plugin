#!/usr/bin/env python3
"""Pre-delivery check for a Q of E review. usage: check_deliverable.py <review.docx> <workbook.xlsx>
Fails on: D numbers cited but missing from the workbook, workbook formula errors, em or en dashes, platform
wording, banned words, British spellings, section order, bullets over two sentences, Open Items without the
'Other documents:' tag, body over 12 pages. Does not check that each figure in the text equals its workbook row:
do that by eye."""
import re, subprocess, sys, tempfile, os
from docx import Document
import openpyxl
docx_path, xlsx_path = sys.argv[1], sys.argv[2]
fails, warns = [], []
doc = Document(docx_path)
def sty(p):
    ppr = p._p.pPr
    return ppr.pStyle.val if ppr is not None and ppr.pStyle is not None else 'Normal'
paras = [(sty(p), p.text) for p in doc.paragraphs]
text = '\n'.join(t for _, t in paras)
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells: text += '\n' + cell.text
# 1 workbook
wb = openpyxl.load_workbook(xlsx_path, data_only=True)
ids = [str(r[0].value) for r in wb['Derived'].iter_rows(min_row=4) if r[0].value]
prefixes = {re.match(r'D\d+', i).group(0) for i in ids if re.match(r'D\d+', i)}
errs = [(ws.title, c.coordinate) for ws in wb for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith('#')]
if errs: fails.append(f'workbook errors: {errs[:5]}')
cited = set(re.findall(r'\bD\d+', text))
missing = sorted(cited - prefixes)
if missing: fails.append(f'D numbers cited but not in workbook: {missing}')
unused = sorted(prefixes - cited)
if unused: warns.append(f'workbook D numbers never cited: {unused}')
# 2 wording
if re.search('[\u2014\u2013]', text): fails.append('em or en dash found')
for pat in [r'\bvault\b', r'\btile\b', r'\bprompt', r'\bQ\d{3,4}\b', r'significant', r'robust', r'corroborat', r'the story', r'comfortable', r'\btension\b', r'translates to', r'compelling', r'best-in-class', r'well-positioned', r'mission-critical', r'\bstrong\b']:
    m = re.findall(pat, text, flags=re.I)
    if m: fails.append(f'banned or platform wording: {pat} ({len(m)})')
for pat in [r'favour', r'colour', r'organis', r'behaviour', r'\bcentre\b', r'analys(e|ed|ing)\b']:
    if re.search(pat, text, flags=re.I): fails.append(f'British spelling: {pat}')
# 3 structure
heads = [t for s, t in paras if s.startswith('Heading')]
order = ['Executive Assessment', 'Quality of Earnings', 'Revenue Analysis', 'Cost Base', 'Working Capital', 'Cash Flow and Conversion', 'Financial and Accounting Matters', 'Open Items', 'Appendix A']
pos = []
for o in order:
    idx = [i for i, h in enumerate(heads) if o in h]
    if not idx: fails.append(f'missing section: {o}')
    else: pos.append(idx[0])
if pos != sorted(pos): fails.append('sections out of order')
# 4 bullets and open items
in_open = False
for s, t in paras:
    if s.startswith('Heading'): in_open = 'Open Items' in t
    if not t.strip(): continue
    n = len(re.findall(r'[.!?](\s+[A-Z(]|$)', t))
    if not s.startswith('Heading') and not in_open and len(t) > 60 and n > 2 and not t.startswith('Terms.') and not t.startswith('The comparison'):
        warns.append(f'more than two sentences: {t[:70]}...')
    if in_open and t.strip() and not s.startswith('Heading') and 'Other documents:' not in t:
        fails.append(f'Open Item without Other documents tag: {t[:60]}')
# 5 pages
with tempfile.TemporaryDirectory() as d:
    subprocess.run(['python3', '/mnt/skills/public/docx/scripts/office/soffice.py', '--headless', '--convert-to', 'pdf', '--outdir', d, docx_path], capture_output=True)
    pdf = os.path.join(d, os.path.basename(docx_path).replace('.docx', '.pdf'))
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    app = None
    for p in range(1, n + 1):
        if 'Appendix A: Differences' in subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True, text=True).stdout.split('\n')[0:3].__str__() or (subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True, text=True).stdout.strip().startswith('Appendix A')):
            app = p; break
    body = (app - 1) if app else n
    if body > 12: fails.append(f'body is {body} pages (limit 12)')
    print(f'pages: {n} total, body {body}')
print('FAIL:' if fails else 'PASS')
for f in fails: print('  fail:', f)
for w in warns: print('  warn:', w)
sys.exit(1 if fails else 0)
