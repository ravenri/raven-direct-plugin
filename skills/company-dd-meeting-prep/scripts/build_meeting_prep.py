#!/usr/bin/env python3
"""Build the meeting prep Word document from a structured input file.

Usage:
    python build_meeting_prep.py input.json output.docx [--base template.docx]

The base document supplies the page setup, fonts and footer. The input file
holds the content. Question and request numbers are assigned here, so every
cross-reference stays correct when questions are added, removed or reordered.

Cross-reference tokens, usable in any text field:
    {q:ID}  becomes the number of the question with that id
    {r:ID}  becomes the number of the follow-up request with that id

A section with no content is left out of the document.
"""
import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

FONT = "Open Sans"
GRAY = "5A636A"


def build(data, base, out):
    doc = Document(base)
    body = doc.element.body
    sect = body.find(qn("w:sectPr"))
    for el in list(body):
        if el is not sect:
            body.remove(el)

    # ---- numbering: questions follow topic order, requests follow list order
    qnum, rnum = {}, {}
    n = 0
    for t in data.get("topics", []):
        for q in t.get("questions", []):
            n += 1
            if q.get("id"):
                qnum[q["id"]] = n
    for i, r in enumerate(data.get("requests", []), 1):
        if r.get("id"):
            rnum[r["id"]] = i

    def sub(text):
        if not isinstance(text, str):
            return text
        text = re.sub(r"\{q:([^}]+)\}", lambda m: str(qnum[m.group(1)]), text)
        text = re.sub(r"\{r:([^}]+)\}", lambda m: str(rnum[m.group(1)]), text)
        return text

    # ---- low-level helpers
    def rpr(bold=False, italic=False, size=18, color="000000"):
        r = OxmlElement("w:rPr")
        f = OxmlElement("w:rFonts")
        for a in ("ascii", "hAnsi", "cs", "eastAsia"):
            f.set(qn("w:" + a), FONT)
        r.append(f)
        if bold:
            r.append(OxmlElement("w:b"))
            r.append(OxmlElement("w:bCs"))
        if italic:
            r.append(OxmlElement("w:i"))
            r.append(OxmlElement("w:iCs"))
        c = OxmlElement("w:color")
        c.set(qn("w:val"), color)
        r.append(c)
        for tag in ("w:sz", "w:szCs"):
            s = OxmlElement(tag)
            s.set(qn("w:val"), str(size))
            r.append(s)
        return r

    def run(text, **kw):
        r = OxmlElement("w:r")
        r.append(rpr(**kw))
        t = OxmlElement("w:t")
        t.set(qn("xml:space"), "preserve")
        t.text = sub(text)
        r.append(t)
        return r

    def para(runs, before=40, after=60, left=None, hanging=None,
             keep_next=False, page_break=False, border=None, style=None):
        p = OxmlElement("w:p")
        pp = OxmlElement("w:pPr")
        if style:
            ps = OxmlElement("w:pStyle")
            ps.set(qn("w:val"), style)
            pp.append(ps)
        if keep_next:
            pp.append(OxmlElement("w:keepNext"))
        if page_break:
            pp.append(OxmlElement("w:pageBreakBefore"))
        if border:
            b = OxmlElement("w:pBdr")
            bt = OxmlElement("w:bottom")
            bt.set(qn("w:val"), "single")
            bt.set(qn("w:color"), "000000")
            bt.set(qn("w:sz"), str(border))
            bt.set(qn("w:space"), "2")
            b.append(bt)
            pp.append(b)
        sp = OxmlElement("w:spacing")
        sp.set(qn("w:before"), str(before))
        sp.set(qn("w:after"), str(after))
        pp.append(sp)
        if left is not None:
            ind = OxmlElement("w:ind")
            ind.set(qn("w:left"), str(left))
            if hanging:
                ind.set(qn("w:hanging"), str(hanging))
            pp.append(ind)
        p.append(pp)
        for r in runs:
            p.append(r)
        body.insert(list(body).index(sect), p)

    def title(text):
        para([run(text, bold=True, size=40)], before=0, after=160, border=12)

    def h1(text, page_break=False):
        para([run(text, bold=True, size=22)], before=240, after=100,
             keep_next=True, border=6, page_break=page_break, style="Heading1")

    def label(text):
        para([run(text, bold=True, size=18)], before=120, after=40, keep_next=True)

    def note(text):
        para([run(text, size=16, italic=True)], before=40, after=60)

    def table(headers, rows, widths, size=16, label_col=False):
        tbl = OxmlElement("w:tbl")
        tp = OxmlElement("w:tblPr")
        tw = OxmlElement("w:tblW")
        tw.set(qn("w:type"), "dxa")
        tw.set(qn("w:w"), str(sum(widths)))
        tp.append(tw)
        lay = OxmlElement("w:tblLayout")
        lay.set(qn("w:type"), "fixed")
        tp.append(lay)
        tbl.append(tp)
        g = OxmlElement("w:tblGrid")
        for w in widths:
            gc = OxmlElement("w:gridCol")
            gc.set(qn("w:w"), str(w))
            g.append(gc)
        tbl.append(g)

        def add_row(cells, is_header=False):
            tr = OxmlElement("w:tr")
            trPr = OxmlElement("w:trPr")
            trPr.append(OxmlElement("w:tblHeader" if is_header else "w:cantSplit"))
            tr.append(trPr)
            for i, txt in enumerate(cells):
                tc = OxmlElement("w:tc")
                tcPr = OxmlElement("w:tcPr")
                w = OxmlElement("w:tcW")
                w.set(qn("w:type"), "dxa")
                w.set(qn("w:w"), str(widths[i]))
                tcPr.append(w)
                b = OxmlElement("w:tcBorders")
                for side in ("top", "left", "bottom", "right"):
                    e = OxmlElement("w:" + side)
                    e.set(qn("w:val"), "single")
                    e.set(qn("w:color"), "BFBFBF")
                    e.set(qn("w:sz"), "4")
                    b.append(e)
                tcPr.append(b)
                shade = "D9D9D9" if is_header else ("F2F2F2" if (label_col and i == 0) else None)
                if shade:
                    s = OxmlElement("w:shd")
                    s.set(qn("w:val"), "clear")
                    s.set(qn("w:color"), "auto")
                    s.set(qn("w:fill"), shade)
                    tcPr.append(s)
                m = OxmlElement("w:tcMar")
                for side, v in (("top", 40), ("left", 80), ("bottom", 40), ("right", 80)):
                    e = OxmlElement("w:" + side)
                    e.set(qn("w:w"), str(v))
                    e.set(qn("w:type"), "dxa")
                    m.append(e)
                tcPr.append(m)
                tc.append(tcPr)
                p = OxmlElement("w:p")
                pp = OxmlElement("w:pPr")
                sp = OxmlElement("w:spacing")
                sp.set(qn("w:before"), "20")
                sp.set(qn("w:after"), "20")
                pp.append(sp)
                p.append(pp)
                p.append(run(txt, bold=is_header or (label_col and i == 0), size=size))
                tc.append(p)
                tr.append(tc)
            tbl.append(tr)

        if headers:
            add_row(headers, True)
        for r in rows:
            add_row(r)
        body.insert(list(body).index(sect), tbl)
        para([run("", size=8)], before=0, after=60)

    # ---- front section
    title(data["title"])
    if data.get("logistics"):
        table(None, data["logistics"], [2400, 7536], size=18, label_col=True)
    para([run("Confidential: internal work product, prepared for Investment Committee discussion.",
              italic=True, size=16)], before=40, after=60)

    if data.get("objectives"):
        h1("Objectives")
        for i, t in enumerate(data["objectives"], 1):
            para([run(f"{i}.  {t}")], before=40, after=40, left=360, hanging=360)

    if data.get("topics"):
        h1("Questions")
        note("Questions are grouped by topic in rank order. An asterisk marks a must-ask. "
             "Each question carries one data point; the probe follows if the first answer is thin.")
        k = 0
        for ti, t in enumerate(data["topics"], 1):
            para([run(f"Topic {ti}. {t['heading']}", bold=True)], before=160, after=20,
                 keep_next=True)
            if t.get("mechanism"):
                para([run(t["mechanism"])], before=0, after=20, keep_next=True)
            for q in t.get("questions", []):
                k += 1
                star = "* " if q.get("must") else ""
                para([run(f"{k}.  {star}{q['text']}")], before=100, after=30,
                     left=360, hanging=360, keep_next=True)
                if q.get("probe"):
                    para([run("Probe: ", bold=True), run(q["probe"])], before=0, after=30,
                         left=360, keep_next=True)
                parts = []
                if q.get("source"):
                    parts.append("Source: " + q["source"].rstrip(".") + ".")
                if q.get("need"):
                    parts.append("Need: " + q["need"].rstrip(".") + ".")
                if q.get("changes"):
                    parts.append("Changes: " + q["changes"].rstrip(".") + ".")
                if q.get("docs"):
                    parts.append(q["docs"].rstrip(".") + ".")
                if parts:
                    para([run(" ".join(parts), italic=True, size=15, color=GRAY)],
                         before=40, after=0, left=360)

    if data.get("requests"):
        h1("Follow-up Requests")
        if data.get("requests_note"):
            note(data["requests_note"])
        for i, r in enumerate(data["requests"], 1):
            para([run(f"{i}.  {r['text']}")], before=40, after=40, left=360, hanging=360)

    # ---- appendices
    letters = iter("ABCDE")
    if data.get("gap_tables"):
        h1(f"Appendix {next(letters)}. Full Gap List", page_break=True)
        for gt in data["gap_tables"]:
            label(gt["label"])
            table(["Priority", "Topic", "Description", "Diligence ask", "Status for this meeting"],
                  gt["rows"], [900, 1500, 3100, 3000, 1436], size=15)
    if data.get("sources"):
        h1(f"Appendix {next(letters)}. Sources Used")
        table(["Document", "Pages cited"], data["sources"], [6400, 3536], size=16)
    if data.get("findings"):
        h1(f"Appendix {next(letters)}. Status and Conflict Findings")
        table(["Item", "Finding with figures from both sources", "Basis", "Feeds"],
              data["findings"], [1500, 4100, 3000, 1336], size=15)
    peer = data.get("peer")
    if peer:
        h1(f"Appendix {next(letters)}. Peer Set and Filing Signals")
        if peer.get("intro"):
            note(peer["intro"])
        if peer.get("table"):
            table(["Company and period", "Revenue", "EBITDA and basis", "Margin", "Leverage"],
                  peer["table"], [2300, 1100, 2900, 2236, 1400], size=15)
        if peer.get("signals"):
            label("Filing signals")
            table(["Signal", "What the peer filings show", "What the deal documents show", "Feeds"],
                  peer["signals"], [1700, 3600, 3400, 1236], size=15)
        if peer.get("closing"):
            note(peer["closing"])
    if data.get("claims"):
        h1(f"Appendix {next(letters)}. Claims Check")
        if data.get("claims_note"):
            note(data["claims_note"])
        table(["Claim", "What the documents support", "Diligence request"],
              data["claims"], [2800, 4200, 2936], size=15)

    doc.save(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    base = str(Path(__file__).resolve().parent.parent / "assets" / "dd_meeting_prep_template.docx")
    if "--base" in args:
        i = args.index("--base")
        base = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    with open(args[0], encoding="utf-8") as f:
        data = json.load(f)
    build(data, base, args[1])
    print("saved", args[1])
