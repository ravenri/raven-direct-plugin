#!/usr/bin/env python3
"""Reads the Word export of the Comp Analysis dashboard and writes stored.json, the mechanical content
of the Peer Set: benchmarking rows, capital structure rows, filing signals, item labels, and the
source list. Nothing is rewritten here except cleanup (source brackets removed, dashes and dates
normalized). Judgment fields are written separately and merged by assemble_input.py.

Usage: python extract_comp_export.py comp_export.docx stored.json
"""
import json
import re
import sys
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

TICKER_NAME = {"LEA": "Lear", "BWA": "BorgWarner", "DAN": "Dana"}


def clean(t):
    t = re.sub(r"\s*\[\d+(?:,\s*\d+)*\]", "", t or "")
    t = t.replace("—", "–").replace("●", "").replace("●", "")
    return re.sub(r"\s+", " ", t).strip()


def blocks(doc):
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:p"):
            p = Paragraph(el, doc)
            if p.text.strip():
                yield "p", p
        elif el.tag == qn("w:tbl"):
            yield "t", Table(el, doc)


def fy(period):
    m = re.search(r"(\d{4})", period or "")
    return f"FY{m.group(1)}" if m and "December" in period else clean(period)


def issuer_filing(src):
    m = re.match(r"\[(\d+)\]\s*(.+?)\s+—\s+(.+?)\.pdf\s*\((\w+)\)", src)
    if not m:
        return None
    n, comp, filing, tick = int(m.group(1)), m.group(2), m.group(3), m.group(4)
    name = TICKER_NAME.get(tick, comp.title())
    return n, name, filing.strip()


def main(src, out):
    doc = Document(src)
    items = list(blocks(doc))
    s = {"company": "", "deal": "", "generated": "", "bench": {}, "developments": [], "insights": [],
         "signals": [], "capital": {"paras": [], "blocks": []}, "sources": {}}
    section = None
    pending = None
    tables = []
    for kind, o in items:
        if kind == "t":
            tables.append(o)
            if section == "bench":
                s["bench"]["table"] = o
            elif section == "capital":
                s["capital"]["table"] = o
            continue
        text = o.text.strip()
        if text in ("Peer Benchmarking", "Industry Developments", "Peer Insights", "Filing Signals",
                    "Capital Structure", "Sources"):
            section = {"Peer Benchmarking": "bench", "Industry Developments": "dev", "Peer Insights": "ins",
                       "Filing Signals": "sig", "Capital Structure": "capital", "Sources": "src"}[text]
            pending = None
            continue
        if section is None:
            if not s["company"] and text not in ("◉  COMP ANALYSIS", "Comp Analysis") and "COMP ANALYSIS" not in text:
                s["company"] = clean(text)
            elif s["company"] and not s["deal"] and "·" in text:
                s["deal"] = re.sub(r"\s+\d{1,2}\s+[A-Z][a-z]{2}$", "", text.split("·")[0].strip())
            elif text.startswith("Generated"):
                s["generated"] = text.split("—")[-1].strip()
            continue
        if section == "bench":
            if text == "Takeaways":
                pending = "take"
            elif text == "Pro forma (reference only)":
                pending = "pf"
            elif pending == "take" and o.style.name == "List Bullet":
                s["bench"].setdefault("takeaways", []).append(clean(text))
            elif pending == "pf":
                s["bench"]["pf"] = clean(text); pending = None
            else:
                s["bench"].setdefault("caveats", []).append(clean(text))
        elif section == "dev":
            if re.match(r"\[(WARN|INFO)\]", text):
                title, _, tag = text.partition("·")
                s["developments"].append({"title": clean(re.sub(r"^\[\w+\]\s*", "", title)), "tag": tag.strip().title(),
                                          "cited": [int(n) for g in re.findall(r"\[([\d,\s]+)\]", title) for n in re.findall(r"\d+", g)],
                                          "paras": []})
            elif s["developments"]:
                if text.startswith("Named sources"):
                    s["developments"][-1]["named"] = text.split(":", 1)[1].strip()
                else:
                    s["developments"][-1]["paras"].append(text)
        elif section == "ins":
            if re.match(r"\[(WARN|INFO)\]", text):
                s["insights"].append({"title": clean(re.sub(r"^\[\w+\]\s*", "", text)),
                                      "cited": [int(n) for g in re.findall(r"\[([\d,\s]+)\]", text) for n in re.findall(r"\d+", g)],
                                      "paras": []})
            elif s["insights"]:
                s["insights"][-1]["paras"].append(text)
        elif section == "sig":
            parts = [p.strip() for p in text.split("·")]
            if len(parts) == 3 and parts[1] in ("High", "Medium", "Low"):
                s["signals"].append({"title": clean(parts[0]), "severity": parts[1],
                                     "classification": parts[2].replace("_", " ").capitalize(),
                                     "cited": [int(n) for g in re.findall(r"\[([\d,\s]+)\]", parts[0]) for n in re.findall(r"\d+", g)],
                                     "deal_says": "", "filings_reveal": ""})
                pending = None
            elif text == "Public filings reveal":
                pending = "fr"
            elif text == "Deal docs say":
                pending = "ds"
            elif s["signals"] and pending:
                key = "filings_reveal" if pending == "fr" else "deal_says"
                s["signals"][-1][key] = clean(text)
                s["signals"][-1].setdefault("raw_" + key, text)
                pending = None
        elif section == "capital":
            if text not in ("Covenants", "Pro forma (reference only)"):
                s["capital"]["paras"].append(clean(text))
        elif section == "src":
            r = issuer_filing(text)
            if r:
                s["sources"][r[0]] = {"issuer": r[1], "filing": r[2]}

    # benchmarking table
    bt = s["bench"].pop("table")
    rows, notes = [], []
    peer_derived = False
    for r in bt.rows[1:]:
        c = [x.text.strip() for x in r.cells]
        name, tick, period, rev, gm, sga, ebit, ebitda, gl, nl, note = c[:11]
        kind = "target" if c[0].startswith("●") else "median" if name.startswith("Median") else "peer"
        m = re.match(r"(.+?)\s*\((.+)\)\s*$", re.sub(r"\s*\[\d+(?:,\s*\d+)*\]", "", ebit))
        ebit_v, ebit_m = (m.group(1), m.group(2)) if m else (clean(ebit), "–")
        basis = re.search(r"\[(\w+)\]\s*$", ebitda)
        ev = clean(re.sub(r"\s*\[\w+\]\s*$", "", ebitda))
        if ev not in ("–", ""):
            if kind == "target":
                ev += f" ({basis.group(1).capitalize() if basis else 'Adjusted'})"
            else:
                derived = "derived" in note.lower() or kind == "median"
                peer_derived = peer_derived or derived
                ev += " (derived)" if derived else " (reported)"
        label = clean(name) if kind != "peer" else f"{clean(name)} ({tick})"
        if kind == "target":
            label += " (target)"
        if kind == "median":
            label = clean(name).replace("peers", "peers").replace("Median (n=", "Median (n=")
        rows.append({"kind": kind, "cells": [label, "–" if kind == "median" else fy(period), clean(rev), clean(gm), clean(sga),
                                           ebit_v, ebit_m, ev, clean(gl), clean(nl)]})
        notes.append({"company": clean(name), "note": clean(note)})
    s["bench"]["columns"] = ["Company", "Period", "Revenue", "Gross margin", "SG&A % of sales", "EBIT", "EBIT margin",
                             "EBITDA", "Gross leverage", "Net leverage"]
    s["bench"]["rows"] = rows
    s["bench"]["row_notes_raw"] = notes

    # capital structure table
    ct = s["capital"].pop("table")
    grouped, order = {}, []
    boiler = re.compile(r"\s*Peer leverage null because CFS D&A not locatable in provided chunks\.?", re.I)
    for r in ct.rows[1:]:
        c = [x.text.strip() for x in r.cells]
        comp, tick, inst, amt, rate, mat, sec, gl, nl, basis, note = c[:11]
        comp_n = TICKER_NAME.get(tick, clean(comp).replace(" Inc.", "").replace(" Incorporated", "").replace(" Corporation", ""))
        if c[0].startswith("●"):
            comp_n = clean(comp)
        note_c = boiler.sub("", clean(note)).strip(" ;.")
        if re.search(r"vault|provided (deal-doc )?chunks", note_c, re.I):
            note_c = "[REWRITE]"
        row = [clean(inst), clean(re.sub(r" in provided deal-doc chunks", "", amt)), clean(rate), clean(mat), clean(sec), note_c]
        if comp_n not in grouped:
            grouped[comp_n] = []
            order.append(comp_n)
        grouped[comp_n].append(row)
    s["capital"]["blocks"] = [{"company": k, "rows": grouped[k]} for k in order]
    s["peers"] = [(TICKER_NAME.get(r["cells"][0].split("(")[-1].rstrip(") "), None) or r["cells"][0].split(" (")[0],
                   r["cells"][0].split("(")[-1].rstrip(") ")) for r in rows if r["kind"] == "peer"]
    s["peer_derived"] = peer_derived
    json.dump(s, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
    print(f"stored: {len(rows)} benchmark rows, {len(s['developments'])} developments, {len(s['insights'])} insights, "
          f"{len(s['signals'])} signals, {sum(len(b['rows']) for b in s['capital']['blocks'])} facilities, "
          f"{len(s['sources'])} source entries")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
