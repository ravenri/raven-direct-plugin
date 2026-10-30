// Financials - Q of E Review: document helpers. Require this module, build a `children` array, then call finish().
// Layout values are fixed here so every run produces the same page: landscape US Letter, Open Sans body,
// Libre Baskerville headings, content width 13536 twips (every table must sum to CW).
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, Footer, PageNumber, LevelFormat, TabStopType, VerticalAlign,
  HeadingLevel, PageOrientation, ImageRun
} = require('docx');

const FONT = 'Open Sans';
const HFONT = 'Libre Baskerville';
const GREY = '5A636A';
const CW = 13536;
const bd = { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF' };
const borders = { top: bd, bottom: bd, left: bd, right: bd };

function run(text, o = {}) {
  return new TextRun({ text, font: o.font || FONT, size: o.size || 22, bold: !!o.bold, italics: !!o.italics, color: o.color || '000000' });
}
// **double asterisks** in text become bold runs (key figures in narrative)
function richRuns(text, o = {}) {
  const parts = text.split('**');
  return parts.map((seg, i) => run(seg, { ...o, bold: i % 2 === 1 ? true : o.bold })).filter((r, i) => parts[i] !== '');
}
function para(text, o = {}) {
  return new Paragraph({
    spacing: { before: o.before ?? 0, after: o.after ?? 150, line: 288 },
    keepNext: !!o.keepNext,
    children: Array.isArray(text) ? text : richRuns(text, o)
  });
}
function h1(t, pageBreak = false) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1, keepNext: true, pageBreakBefore: pageBreak,
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '000000', space: 2 } },
    spacing: { before: 240, after: 100 },
    children: [run(t, { size: 24, bold: true, font: HFONT })]
  });
}
function title(t) { return new Paragraph({ spacing: { before: 0, after: 100 }, children: [run(t, { size: 38, bold: true, font: HFONT })] }); }
function label(t) { return para(t, { bold: true, size: 22, before: 100, after: 60, keepNext: true }); }
function caption(num, ttl, scale) {
  const kids = [run(`${num}  ${ttl}`, { bold: true, size: 19 })];
  if (scale) kids.push(run(`;  ${scale}`, { size: 19, color: GREY }));
  return para(kids, { before: 140, after: 50, keepNext: true });
}
function source(t) { return para(t, { size: 16, color: GREY, before: 40, after: 160 }); }
function basis(t) { return para(t, { size: 16, color: GREY, before: 0, after: 200 }); }
function bullets(items) {
  return items.map(t => new Paragraph({
    numbering: { reference: 'bul', level: 0 },
    spacing: { before: 0, after: 90, line: 288 },
    children: richRuns(t, { size: 22 })
  }));
}
function numbered(items, inst = 1) {
  return items.map(t => new Paragraph({
    numbering: { reference: 'nums', level: 0, instance: inst },
    spacing: { before: 0, after: 100, line: 288 },
    children: richRuns(t, { size: 22 })
  }));
}
const gap = (n = 80) => new Paragraph({ spacing: { before: 0, after: n }, children: [] });
function img(file, w, h) {
  return new Paragraph({
    spacing: { before: 0, after: 40 }, keepNext: true,
    children: [new ImageRun({ type: 'png', data: fs.readFileSync(file), transformation: { width: w, height: h } })]
  });
}
function cell(text, w, o = {}) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA }, borders,
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: 'auto' } : undefined,
    margins: { top: 40, bottom: 40, left: 90, right: 90 },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: o.align === 'right' ? AlignmentType.RIGHT : AlignmentType.LEFT,
      indent: o.indent ? { left: o.indent } : undefined,
      keepNext: !!o.keep,
      spacing: { before: 0, after: 0 },
      children: [run(text, { size: o.size || 18, bold: o.bold, color: o.color })]
    })]
  });
}
// rows: [{k:'head'|'sub'|'group'|undefined, i:indent (twips), c:[cells]}]
function table(widths, aligns, rows, size = 18, keepAll) {
  const total = widths.reduce((a, b) => a + b, 0);
  if (total !== CW) throw new Error('width mismatch ' + total + ' for ' + rows[0].c[0]);
  rows.forEach(r => { if (r.c.length !== widths.length) throw new Error('col mismatch: ' + r.c[0]); });
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map(r => {
      const fill = r.k === 'head' ? 'D9D9D9' : r.k === 'sub' ? 'F2F2F2' : r.k === 'group' ? 'EDEDED' : undefined;
      const bold = r.k === 'head' || r.k === 'sub' || r.k === 'group';
      return new TableRow({
        tableHeader: r.k === 'head', cantSplit: true,
        children: r.c.map((t, i) => cell(t, widths[i], { align: aligns[i], bold, fill, size, indent: i === 0 ? r.i : 0, keep: keepAll === undefined ? rows.length <= 8 : keepAll }))
      });
    })
  });
}
// four-column label/value table (report profile, accounting summary)
function kv4(rows) {
  const w = [2200, 4568, 2200, 4568];
  return new Table({
    width: { size: CW, type: WidthType.DXA }, columnWidths: w,
    rows: rows.map(r => new TableRow({
      cantSplit: true,
      children: [
        cell(r[0], w[0], { bold: true, fill: 'F2F2F2', size: 19 }), cell(r[1], w[1], { size: 19 }),
        cell(r[2], w[2], { bold: true, fill: 'F2F2F2', size: 19 }), cell(r[3], w[3], { size: 19 })
      ]
    }))
  });
}
function noteBox(boldLead, text) {
  return new Table({
    width: { size: CW, type: WidthType.DXA }, columnWidths: [CW],
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: CW, type: WidthType.DXA }, borders,
        shading: { fill: 'F2F2F2', type: ShadingType.CLEAR, color: 'auto' },
        margins: { top: 60, bottom: 60, left: 110, right: 110 },
        children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: [run(boldLead, { size: 19, bold: true }), run(text, { size: 19 })] })]
      })]
    })]
  });
}
// Build, write and embed fonts. opts: { title, outPath }
async function finish(children, opts) {
  const doc = new Document({
    creator: 'Raven',
    title: opts.title,
    styles: {
      default: { document: { run: { font: FONT, size: 22 } } },
      paragraphStyles: [{
        id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: HFONT, size: 24, bold: true, color: '000000' },
        paragraph: { spacing: { before: 280, after: 100 }, outlineLevel: 0 }
      }]
    },
    numbering: {
      config: [{
        reference: 'bul',
        levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 400, hanging: 280 } }, run: { font: FONT, size: 22 } } }]
      }, {
        reference: 'nums',
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 400, hanging: 400 } }, run: { font: FONT, size: 22 } } }]
      }]
    },
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
          margin: { top: 1008, right: 1152, bottom: 1008, left: 1152, header: 708, footer: 708 }
        }
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            tabStops: [{ type: TabStopType.RIGHT, position: CW }],
            children: [
              new TextRun({ text: opts.footer || 'Confidential: internal work product', font: FONT, size: 15, color: GREY }),
              new TextRun({ text: '\tPage ', font: FONT, size: 15, color: GREY }),
              new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 15, color: GREY })
            ]
          })]
        })
      },
      children
    }]
  });
  const buf = await Packer.toBuffer(doc);
  fs.mkdirSync(path.dirname(opts.outPath), { recursive: true });
  fs.writeFileSync(opts.outPath, buf);
  execFileSync('python3', [path.join(__dirname, 'embed_fonts.py'), opts.outPath], { stdio: 'inherit' });
  return opts.outPath;
}
module.exports = { run, richRuns, para, h1, title, label, caption, source, basis, bullets, numbered, gap, img, cell, table, kv4, noteBox, finish, CW, GREY, FONT, HFONT };
