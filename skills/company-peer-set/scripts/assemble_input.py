#!/usr/bin/env python3
"""Merges stored.json (mechanical content from extract_comp_export.py) with authored.json (the judgment
fields written for this deal) into build_input.json for build_peer_set.py.

Usage: python assemble_input.py stored.json authored.json build_input.json

authored.json carries only what needs judgment:
  executive_summary {lead, points[]}; caveats[]; data_notes[]; row_notes[]; takeaways[]
  industry_developments[], same order as stored: {label, body, credit_implication}
  peer_insights[], same order: {label, body, credit_implication, deal_note}
  filing_signals[], same order: {label, deal_says?, filings_reveal?}   (stored text is used when omitted)
  capital_structure: {covenant_narrative, structural_caveat, target_reference, leverage_basis,
                      target_rows? (replaces the target block rows), as_of {company: date text},
                      row_edits? [{company, facility, any of outstanding, rate, maturity, security, key_terms}],
                      block_sources? {company: text}}
  optional: deal, sources_overrides {section.index: text}
Source lines are proposed from the filings cited by each item and the issuers named in its text.
"""
import json
import re
import sys

ISSUERS = ["BorgWarner", "Dana", "Lear"]


def propose_sources(cited, text, index):
    names = [n for n in set(v["issuer"] for v in index.values()) if re.search(r"\b" + re.escape(n) + r"\b", text)]
    found = []
    for n in cited:
        v = index.get(str(n))
        if v and v["issuer"] in names:
            pair = (v["issuer"], v["filing"])
            if pair not in found:
                found.append(pair)
    for name in names:
        if not any(p[0] == name for p in found):
            for v in index.values():
                pair = (v["issuer"], v["filing"])
                if v["issuer"] == name and pair not in found:
                    found.append(pair)
    order = {n: text.find(n) for n in names}
    found.sort(key=lambda p: order.get(p[0], 0))
    return "; ".join(f"{i} {f}" for i, f in found)


def latest_filing(issuer, index):
    fl = {v["filing"] for v in index.values() if v["issuer"] == issuer}
    q = [f for f in fl if f.startswith("10-Q")]
    return f"{issuer} {sorted(q)[-1]}" if q else "; ".join(f"{issuer} {f}" for f in sorted(fl))


def main(stored_p, authored_p, out):
    s = json.load(open(stored_p, encoding="utf-8"))
    a = json.load(open(authored_p, encoding="utf-8"))
    errs = []
    idx = s["sources"]
    peers = ", ".join(f"{n} ({t})" for n, t in s["peers"])
    d = {"title": "Peer Set", "company": s["company"], "deal": a.get("deal", s["deal"]),
         "meta_line": a.get("meta_line", f"Confirmed public peers: {peers}  |  Generated {s['generated']}"),
         "executive_summary": a.get("executive_summary")}
    d["benchmarking"] = {"caveats": a.get("caveats", s["bench"].get("caveats", [])), "columns": s["bench"]["columns"],
                         "rows": s["bench"]["rows"], "row_notes": a.get("row_notes", []),
                         "data_notes": a.get("data_notes", []),
                         "takeaways": a.get("takeaways", s["bench"].get("takeaways", []))}
    for key, stored_key in (("industry_developments", "developments"), ("peer_insights", "insights")):
        auth = a.get(key, [])
        if len(auth) != len(s[stored_key]):
            errs.append(f"{key}: {len(auth)} authored items for {len(s[stored_key])} stored items")
            continue
        items = []
        for i, (st, au) in enumerate(zip(s[stored_key], auth)):
            it = {"label": au.get("label"), "body": au.get("body"), "credit_implication": au.get("credit_implication")}
            if stored_key == "developments":
                it["tag"] = st["tag"]
            else:
                it["deal_note"] = au.get("deal_note")
            text = " ".join([it["body"] or "", it["credit_implication"] or ""] + st["paras"])
            it["sources"] = a.get("sources_overrides", {}).get(f"{key}.{i}") or propose_sources(st["cited"], text, idx)
            if not all(it.get(k) for k in ("label", "body", "credit_implication")):
                errs.append(f"{key}[{i}] ('{st['title'][:40]}'): label, body and credit_implication are required")
            items.append(it)
        d[key] = items
    auth = a.get("filing_signals", [])
    if len(auth) != len(s["signals"]):
        errs.append(f"filing_signals: {len(auth)} authored for {len(s['signals'])} stored")
    else:
        d["filing_signals"] = []
        for i, (st, au) in enumerate(zip(s["signals"], auth)):
            fr = au.get("filings_reveal", st["filings_reveal"])
            it = {"label": au.get("label"), "severity": st["severity"], "classification": st["classification"],
                  "deal_says": au.get("deal_says", st["deal_says"]), "filings_reveal": fr,
                  "sources": a.get("sources_overrides", {}).get(f"filing_signals.{i}") or propose_sources(st["cited"], fr + " " + st["raw_filings_reveal"], idx)}
            if not it["label"]:
                errs.append(f"filing_signals[{i}] ('{st['title'][:40]}'): label is required")
            d["filing_signals"].append(it)
    ca = a.get("capital_structure", {})
    cs = {k: ca.get(k) for k in ("covenant_narrative", "structural_caveat", "target_reference", "leverage_basis")}
    for k, v in cs.items():
        if not v:
            errs.append(f"capital_structure.{k} is required")
    blocks = []
    for b in s["capital"]["blocks"]:
        rows = [list(r) for r in b["rows"]]
        is_target = b["company"] == s["company"]
        if is_target and ca.get("target_rows"):
            rows = ca["target_rows"]
        for e in ca.get("row_edits", []):
            if e["company"] == b["company"]:
                for r in rows:
                    if r[0].startswith(e["facility"]):
                        for j, k in enumerate(("facility", "outstanding", "rate", "maturity", "security", "key_terms")):
                            if k in e and k != "facility":
                                r[j] = e[k]
        src = ca.get("block_sources", {}).get(b["company"]) or ("Deal documents" if is_target else latest_filing(b["company"], idx))
        blocks.append({"company": b["company"], "as_of": ca.get("as_of", {}).get(b["company"], "LTM" if is_target else ""),
                       "rows": rows, "source": src})
        for r in rows:
            if "[REWRITE]" in r[5]:
                errs.append(f"capital structure {b['company']} '{r[0]}': key terms need rewriting (target_rows or row_edits)")
    cs["blocks"] = blocks
    d["capital_structure"] = cs
    if errs:
        print("Assembly problems:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    json.dump(d, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("Assembled", out)


if __name__ == "__main__":
    main(*sys.argv[1:4])
