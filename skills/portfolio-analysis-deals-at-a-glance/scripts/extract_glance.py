"""Pull the Deal At A Glance table and a short company description for each deal
out of saved portfolio_compare results (tile deal_summary_dashboard, section overview).

Usage: python extract_glance.py OUT.json RESULT_FILE [RESULT_FILE ...]

OUT.json is a working file for the build. For each deal it holds the company name,
the currency, the table rows exactly as shown, and the opening of the company
description (used only to choose the GICS sector). Deals whose table is missing
are listed under "missing" so they can be fetched again on their own.
"""
import json, re, sys

def clean(s):
    return re.sub(r"\s*\[[\d,\s]+\]", "", s).strip()

def parse(content):
    cur = re.search(r"\|\s*Currency\s*\|\s*([^|]+?)\s*\|", content)
    glance = []
    m = re.search(r"###\s*Deal at a glance\s*\n(.*?)(?:\n###|\n## |\Z)", content, re.S | re.I)
    if m:
        for line in m.group(1).splitlines():
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2 or cells[0].lower() == "metric" or set(cells[0]) <= {"-", " "}:
                continue
            glance.append([clean(cells[0]), clean(cells[1])])
    d = re.search(r"###\s*Company(?: Overview)?\s*\n(?:#### Narrative\s*\n)?(.*?)(?:\n####|\n###|\Z)", content, re.S | re.I)
    desc = re.sub(r"\*\*|\[[\d,\s]+\]", "", d.group(1)).strip()[:500] if d else ""
    return (cur.group(1) if cur else ""), glance, desc

def main(out, files):
    deals, missing = [], []
    for f in files:
        data = json.load(open(f))["data"]
        for x in data["deals"]:
            cur, glance, desc = parse(x["content"])
            deals.append({"deal": x["company_name"], "project_id": x.get("project_id"), "currency": cur,
                          "glance": glance, "description": desc})
            if not glance:
                missing.append(x["company_name"])
    json.dump({"deals": deals, "missing": missing}, open(out, "w"), indent=1)
    print(f"{len(deals)} deals, {len(missing)} without a Deal At A Glance table: {missing}")
    # Compact review list: this is all that needs to be read to choose each sector.
    for d in deals:
        print(f"- {d['deal']} | {d['currency'] or 'n/d'} | {len(d['glance'])} rows | {' '.join(d['description'].split())[:180]}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
