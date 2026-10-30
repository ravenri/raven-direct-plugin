#!/usr/bin/env python3
"""Pre-delivery check for a software tearsheet.
Usage: python check_tearsheet.py <file.docx>
Checks: page count and where each page starts, em dashes, banned words, system jargon,
leftover placeholders and number tags, and acronym spell-out on first use."""
import re, subprocess, sys, os, tempfile

path = sys.argv[1]
problems = []

text = subprocess.run(['pandoc', '-t', 'plain', '--wrap=none', path], capture_output=True, text=True).stdout

# --- language checks ---
if '\u2014' in text: problems.append('Em dash found.')
banned = ['significant', 'robust', 'best-in-class', 'compelling', 'attractive', 'well-positioned', 'mission-critical',
  'world-class', 'market-leading', 'premier', 'stellar', 'proven track record', 'translates to', 'the tension',
  'comfortable', 'arguably', 'corroborated', 'the most material', 'the most credit-relevant', 'throws off cash',
  'real cushion', 'real concentration', 'favourable', 'organisation', 'colour']
for b in banned:
    if re.search(r'\b' + re.escape(b), text, re.I): problems.append(f'Banned word or phrase: "{b}"')
for m in re.finditer(r'\bstrong(est)?\b', text, re.I): problems.append(f'"strong" needs a benchmark: ...{text[max(0,m.start()-30):m.end()+30]!r}')
for m in re.finditer(r'\b(quite|very)\b', text, re.I): problems.append(f'Filler word: ...{text[max(0,m.start()-30):m.end()+30]!r}')
jargon = ['Raven', 'vault', 'the tile', 'tile ', 'as stored', 'the analysis', 'the answers', 'diligence_summary', 'dashboard']
for j in jargon:
    if re.search(re.escape(j), text, re.I): problems.append(f'System jargon: "{j}"')
if re.search(r'\[\[n\d+\]\]', text): problems.append('Number tag left in text.')
if re.search(r'\bQ\d{3,4}\b', text): problems.append('Prompt ID left in text.')
if re.search(r'\[[A-Za-z .,]{2,}\]', text): problems.append('Placeholder in square brackets left in text.')

# --- acronym spell-out on first use (expansion must appear within 220 characters of first use) ---
expansions = {
  'ARR': 'annual recurring revenue', 'EBITDA': 'earnings before interest, taxes, depreciation and amortization',
  'SMB': 'small and medium-sized business',
  'SaaS': 'software as a service', 'LTV': 'lifetime value', 'CAC': 'customer acquisition cost',
  'GAAP': 'generally accepted accounting principles',
  'PF': 'pro forma', 'AI': 'artificial intelligence', 'EU': 'European Union', 'NPS': 'Net Promoter Score',
}
for ac, ex in expansions.items():
    m = re.search(r'\b' + ac + r'\b', text)
    if not m: continue
    window = text[max(0, m.start() - 220): m.end() + 220].lower()
    if ex.lower() not in window:
        problems.append(f'Acronym "{ac}" first used without "{ex}" nearby.')

# --- pages ---
tmp = tempfile.mkdtemp()
subprocess.run(['python', '/mnt/skills/public/docx/scripts/office/soffice.py', '--headless', '--convert-to', 'pdf', '--outdir', tmp, path],
               capture_output=True)
pdf = os.path.join(tmp, os.path.splitext(os.path.basename(path))[0] + '.pdf')
info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
if pages > 4: problems.append(f'{pages} pages; the cap is 4.')
starts = {2: 'Customers and contracts', 3: 'AI exposure', 4: 'Key metrics'}
for p, head in starts.items():
    if p <= pages:
        first = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True, text=True).stdout.strip().split('\n')[0]
        if head not in first: problems.append(f'Page {p} should start with "{head}" but starts with "{first[:50]}".')
print(f'Pages: {pages}')
if problems:
    print('PROBLEMS:'); [print(' - ' + x) for x in problems]; sys.exit(1)
print('All checks passed.')
