"""Embed the Raven brand fonts (Open Sans, Libre Baskerville) into a .docx so it renders the same on any machine.
Usage: python3 embed_fonts.py path/to/file.docx
Both fonts are open licensed (OFL). The four font files live in ../assets/fonts."""
import zipfile, uuid, sys, re, os
here = os.path.dirname(os.path.abspath(__file__))
fd = os.path.join(here, '..', 'assets', 'fonts')
fonts = {
 'Open Sans': (os.path.join(fd, 'OpenSans-Regular.ttf'), os.path.join(fd, 'OpenSans-Bold.ttf')),
 'Libre Baskerville': (os.path.join(fd, 'LibreBaskerville-Regular.ttf'), os.path.join(fd, 'LibreBaskerville-Bold.ttf'))}
def obfuscate(data, guid):
    key = bytes.fromhex(guid.replace('-', '').strip('{}'))[::-1]
    b = bytearray(data)
    for i in range(32): b[i] ^= key[i % 16]
    return bytes(b)
src = sys.argv[1]
zin = zipfile.ZipFile(src); items = {n: zin.read(n) for n in zin.namelist()}; zin.close()
if any(k.startswith('word/fonts/') for k in items):
    print('fonts already embedded'); sys.exit(0)
rels = []; entries = []; n = 0
for name, (reg, bold) in fonts.items():
    parts = []
    for tag, path in (('embedRegular', reg), ('embedBold', bold)):
        n += 1; guid = '{' + str(uuid.uuid4()).upper() + '}'
        items[f'word/fonts/font{n}.odttf'] = obfuscate(open(path, 'rb').read(), guid)
        rid = f'rIdFont{n}'
        rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/font{n}.odttf"/>')
        parts.append(f'<w:{tag} r:id="{rid}" w:fontKey="{guid}"/>')
    entries.append(f'<w:font w:name="{name}"><w:charset w:val="00"/><w:family w:val="swiss"/><w:pitch w:val="variable"/>{"".join(parts)}</w:font>')
ft = items['word/fontTable.xml'].decode('utf8')
if ft.rstrip().endswith('/>') and '</w:fonts>' not in ft:
    ft = re.sub(r'/>\s*$', '>' + ''.join(entries) + '</w:fonts>', ft)
else:
    ft = ft.replace('</w:fonts>', ''.join(entries) + '</w:fonts>')
items['word/fontTable.xml'] = ft.encode('utf8')
items['word/_rels/fontTable.xml.rels'] = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(rels) + '</Relationships>').encode('utf8')
st = items['word/settings.xml'].decode('utf8')
if 'embedTrueTypeFonts' not in st:
    m = re.search(r'<w:displayBackgroundShape[^>]*/>', st) or re.search(r'<w:zoom[^>]*/>', st)
    if m: st = st[:m.end()] + '<w:embedTrueTypeFonts/>' + st[m.end():]
    else:
        m = re.search(r'<w:settings[^>]*>', st); st = st[:m.end()] + '<w:embedTrueTypeFonts/>' + st[m.end():]
items['word/settings.xml'] = st.encode('utf8')
ct = items['[Content_Types].xml'].decode('utf8')
if 'Extension="odttf"' not in ct:
    ct = ct.replace('<Override', '<Default ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont" Extension="odttf"/><Override', 1)
items['[Content_Types].xml'] = ct.encode('utf8')
order = ['[Content_Types].xml'] + [k for k in items if k != '[Content_Types].xml']
with zipfile.ZipFile(src, 'w', zipfile.ZIP_DEFLATED) as z:
    for k in order: z.writestr(k, items[k])
print('embedded', n, 'font files')
