#!/usr/bin/env python3
"""Check a comparison build input and render it as a PDF.

Usage: python3 build_pdf.py <build_input.json> <out.pdf>

build_input.json (written fresh each run, never shipped with the skill):
{
  "deal_a": "Name", "deal_b": "Name", "pull_date": "October 23, 2026",
  "notes": {"terms": "...", "structure": "...", "leverage": "...",
            "scorecard": "..."},
  "footnotes": ["...", "..."],
  "datasets": {"headline": [...], "scorecard": [...], "capital_stack": [...],
               "paydown": [...]}
}

Prints PASS (with any warnings) and writes the PDF, or prints FAIL and writes nothing.
Exit code 0 means every check passed; 1 means fix the input and run again.
"""
import json
import os
import re
import sys


COLUMNS = {
    "headline": ["key", "metric", "format", "deal_a", "deal_b"],
    "scorecard": ["lens", "a_score", "a_rating", "a_driver", "b_score", "b_rating", "b_driver"],
    "capital_stack": ["deal", "layer", "amount_mm", "pct_of_cap"],
    "paydown": ["deal", "step", "period", "repaid_pct", "gross_leverage_x"],
    "repayment": ["deal", "read"],
    "screening": ["deal", "tranche", "view", "basis"],
}
FORMATS = {"mm", "x", "pct", "score", "text"}
REQUIRED_HEADLINE_KEYS = ["repaid_final_pct", "gross_leverage_x"]
DEFAULT_NOTES = {
    "terms": "USD unless stated. Each deal is shown at its own anchor period and on its own EBITDA basis, named in the footnotes below.",
    "structure": "Share of total capitalization by layer.",
    "leverage": "Modeled total debt to PF Adjusted Cash EBITDA by projection year. Gross of cash.",
    "scorecard": "Scores run from strongest to weakest as Raven states them. A lens left unscored is shown blank.",
    "creditread": "Raven's repayment read and screening view for each deal, quoted. A basis left blank is not stated on this page.",
}
BANNED = re.compile(r"\b(vault|tile|dashboard|mcp|kpi|prompt id|net leverage|net debt)\b", re.I)
EM_DASH = "—"


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 1
    src, out = argv[1], argv[2]
    with open(src, encoding="utf-8") as fh:
        spec = json.load(fh)
    errors = []

    a, b = spec.get("deal_a", "").strip(), spec.get("deal_b", "").strip()
    if not a or not b or a == b:
        errors.append("deal_a and deal_b must be two different names")
    pull_date = spec.get("pull_date", "").strip()
    if not pull_date:
        errors.append("pull_date is required")

    data = spec.get("datasets", {})
    for ds, cols in COLUMNS.items():
        rows = data.get(ds)
        if not rows:
            errors.append(f"dataset {ds} is empty or missing")
            continue
        for i, r in enumerate(rows):
            missing = [c for c in cols if c not in r]
            if missing:
                errors.append(f"{ds} row {i}: missing columns {missing}")

    # Deal names in row-level datasets must match the two deals exactly.
    for ds in ("capital_stack", "paydown", "repayment", "screening"):
        for i, r in enumerate(data.get(ds, [])):
            if r.get("deal") not in (a, b):
                errors.append(f"{ds} row {i}: deal {r.get('deal')!r} is not {a!r} or {b!r}")
    for deal in (a, b):
        for ds in ("capital_stack", "paydown", "repayment", "screening"):
            if not any(r.get("deal") == deal for r in data.get(ds, [])):
                errors.append(f"{ds} has no rows for {deal}")

    # Headline checks.
    keys = [r.get("key") for r in data.get("headline", [])]
    for k in REQUIRED_HEADLINE_KEYS:
        if k not in keys:
            errors.append(f"headline is missing required key {k}")
    if len(keys) != len(set(keys)):
        errors.append("headline keys must be unique")
    for r in data.get("headline", []):
        if r.get("format") not in FORMATS:
            errors.append(f"headline {r.get('key')}: format must be one of {sorted(FORMATS)}")

    # Ratings are quoted, never blank: a missing rating must read Not rated.
    for i, r in enumerate(data.get("scorecard", [])):
        for side in ("a", "b"):
            if not str(r.get(f"{side}_rating") or "").strip():
                errors.append(f"scorecard row {i} ({r.get('lens')}): {side}_rating is blank; use the Raven rating or the words Not rated")

    # Capital structure shares should add to about 100 for each deal.
    for deal in (a, b):
        tot = sum(r.get("pct_of_cap") or 0 for r in data.get("capital_stack", []) if r.get("deal") == deal)
        if data.get("capital_stack") and abs(tot - 100) > 0.6:
            errors.append(f"capital_stack shares for {deal} add to {tot:.1f}, not 100")

    NETCASH = re.compile(r"\bnet\b(?!\s+(retention|revenue|income|working|interest|new))", re.I)
    for i, r in enumerate(data.get("scorecard", [])):
        for side in ("a", "b"):
            if NETCASH.search(str(r.get(f"{side}_driver") or "")):
                errors.append(f"scorecard row {i} ({r.get('lens')}): {side}_driver mentions a net figure; leave it blank")
    for ds, col in (("repayment", "read"), ("screening", "basis")):
        for i, r in enumerate(data.get(ds, [])):
            if NETCASH.search(str(r.get(col) or "")):
                errors.append(f"{ds} row {i}: {col} mentions a net figure; leave it blank")

    # Series checks: leverage never rises and share repaid never falls, by deal.
    for deal in (a, b):
        pts = sorted((r for r in data.get("paydown", []) if r.get("deal") == deal), key=lambda r: r.get("step", 0))
        lev = [r.get("gross_leverage_x") for r in pts if r.get("gross_leverage_x") is not None]
        rep = [r.get("repaid_pct") for r in pts if r.get("repaid_pct") is not None]
        if any(y > x for x, y in zip(lev, lev[1:])):
            errors.append(f"paydown gross leverage rises between years for {deal}")
        if any(y < x for x, y in zip(rep, rep[1:])):
            errors.append(f"paydown share repaid falls between years for {deal}")

    # Warning only: stated entry leverage against funded debt over anchor EBITDA.
    warnings = []
    hl = {r.get("key"): r for r in data.get("headline", [])}
    if all(k in hl for k in ("funded_debt_mm", "anchor_ebitda_mm", "gross_leverage_x")):
        for side, name in (("deal_a", a), ("deal_b", b)):
            d, e, x = (hl[k].get(side) for k in ("funded_debt_mm", "anchor_ebitda_mm", "gross_leverage_x"))
            if d and e and x and abs(d / e - x) > 0.02:
                warnings.append(f"{name}: stated gross leverage {x:.2f}x but funded debt over anchor EBITDA is {d / e:.2f}x")

    notes = dict(DEFAULT_NOTES)
    notes.update(spec.get("notes", {}))
    footnotes = spec.get("footnotes", [])

    # Language checks on everything a reader will see.
    visible = [a, b, pull_date] + list(notes.values()) + list(footnotes)
    for rows in data.values():
        for r in rows:
            visible += [v for v in r.values() if isinstance(v, str)]
    for text in visible:
        if EM_DASH in text:
            errors.append(f"em dash in: {text[:60]!r}")
        m = BANNED.search(text)
        if m:
            errors.append(f"banned word {m.group(0)!r} in: {text[:60]!r}")

    report = "PASS" if not errors else "FAIL\n" + "\n".join("- " + e for e in errors)
    if warnings:
        report += "\nWARNINGS (report in the reply, keep the deal summary value)\n" + "\n".join("- " + w for w in warnings)
    print(report)
    if errors:
        return 1
    notes_final = notes
    spec["notes"] = notes_final
    render(spec, out)
    print("Wrote", out)
    return 0


def render(d, out):
    import tempfile, os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    tmp = tempfile.mkdtemp()
    STACK, LINES = os.path.join(tmp, "stack.png"), os.path.join(tmp, "lines.png")
    D = d["datasets"]; A, B = d["deal_a"], d["deal_b"]
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "layout.cfg"))
    def cv(sec, key, default):
        return cfg.get(sec, key, fallback=default).strip()
    def cw(key, default):
        return [float(x) for x in cv("tables", key, default).split(",")]
    CA, CB, EQ = cv("colors", "deal_a", "#2F6DB5"), cv("colors", "deal_b", "#D9822B"), cv("colors", "equity", "#7B6AA8")
    HEADC, GRIDC, HFILL = cv("colors", "heading", "#1F4F8A"), cv("colors", "grid", "#BFBFBF"), cv("colors", "header_fill", "#F2F2F2")
    MARG = float(cv("page", "margin_inches", "0.6")) * inch
    BS, NS = float(cv("type", "body_size", "8.5")), float(cv("type", "note_size", "7.5"))
    PAGE = landscape(letter) if cv("page", "orientation", "landscape") == "landscape" else letter
    n1 = lambda v: f"{v:,.1f}"
    F = {"mm": lambda v: "" if v is None else f"${n1(v)}MM", "x": lambda v: "" if v is None else f"{v:.2f}x",
         "pct": lambda v: "" if v is None else f"{v:.1f}%", "score": lambda v: "" if v is None else str(v), "text": lambda v: "" if v is None else str(v)}

    def style(name, **k):
        base = dict(fontName="Helvetica", fontSize=BS, leading=BS * 1.3, textColor=colors.HexColor("#1a1a1a")); base.update(k)
        return ParagraphStyle(name, **base)
    body, small = style("b"), style("s", fontSize=NS, leading=NS * 1.27, textColor=colors.HexColor("#555555"))
    cellr = style("r", alignment=2)
    head = style("h", fontName="Helvetica-Bold")
    headr = style("hr", fontName="Helvetica-Bold", alignment=2)
    h1 = style("h1", fontName="Helvetica-Bold", fontSize=float(cv("type", "title_size", "18")), leading=float(cv("type", "title_size", "18")) * 1.22, spaceAfter=4)
    h2 = style("h2", fontName="Helvetica-Bold", fontSize=float(cv("type", "heading_size", "12")), leading=float(cv("type", "heading_size", "12")) * 1.25, textColor=colors.HexColor(HEADC), spaceBefore=12, spaceAfter=2)
    P = lambda t, s=body: Paragraph(str(t).replace("&", "&amp;").replace("<", "&lt;"), s)

    W = PAGE[0] - 2 * MARG
    def tbl(rows, widths, right=(), muted=(), headrows=1):
        data = []
        for ri, r in enumerate(rows):
            data.append([P(c, (headr if i in right else head) if ri < headrows else (small if i in muted else (cellr if i in right else body))) for i, c in enumerate(r)])
        t = Table(data, colWidths=[w * W for w in widths], repeatRows=headrows)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(GRIDC)), ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (-1, headrows - 1), colors.HexColor(HFILL)), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        return t

    # charts
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
    def fig_stack(path):
        rows = D["capital_stack"]; deals = [A, B]
        fig, ax = plt.subplots(figsize=(10.0, 2.0)); ax.set_xlim(0, 100); ax.set_ylim(-0.6, len(deals) - 0.4); ax.invert_yaxis()
        for i, deal in enumerate(deals):
            own = [r for r in rows if r["deal"] == deal]; debt = [r["layer"] for r in own if "equity" not in r["layer"].lower()]
            acc = 0
            for r in own:
                if "equity" in r["layer"].lower(): c, a = EQ, 1
                else:
                    k = debt.index(r["layer"]); a = 1 - 0.55 * (k / (len(debt) - 1)) if len(debt) > 1 else 1; c = CA
                ax.barh(i, r["pct_of_cap"], left=acc, color=c, alpha=a, edgecolor="white", height=0.55)
                if r["pct_of_cap"] > 5: ax.text(acc + r["pct_of_cap"] / 2, i, f'{r["pct_of_cap"]:.1f}%', ha="center", va="center", color="white", fontsize=8, fontweight="bold")
                acc += r["pct_of_cap"]
            lg = "   ".join(f'{r["layer"]} {r["pct_of_cap"]:.1f}%' for r in own)
            ax.text(0, i + 0.42, lg, fontsize=7, color="#555555", va="top")
        ax.set_yticks(range(len(deals))); ax.set_yticklabels(deals); ax.set_xticks([]); [s.set_visible(False) for s in ax.spines.values()]
        ax.tick_params(length=0); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)
    def fig_lines(path):
        fig, axs = plt.subplots(1, 2, figsize=(10.0, 2.7))
        for ax, field, ttl, fmt in ((axs[0], "repaid_pct", "Debt repaid (share of opening debt)", lambda v: f"{v:.0f}%"), (axs[1], "gross_leverage_x", "Gross leverage (total debt to anchor EBITDA)", lambda v: f"{v:.1f}x")):
            for deal, c in ((A, CA), (B, CB)):
                pts = sorted([r for r in D["paydown"] if r["deal"] == deal and r[field] is not None], key=lambda r: r["step"])
                ax.plot([p["step"] for p in pts], [p[field] for p in pts], color=c, lw=2, marker="o", ms=3.5, label=deal)
                ax.annotate(fmt(pts[-1][field]), (pts[-1]["step"], pts[-1][field]), xytext=(5, -3), textcoords="offset points", fontsize=8, color=c)
            ax.set_title(ttl, fontsize=9, loc="left"); ax.set_xlabel("Projection year (0 is the anchor period)", fontsize=7.5); ax.set_ylim(bottom=0)
            ax.grid(axis="y", color="#e5e5e5"); [ax.spines[s].set_visible(False) for s in ("top", "right")]
            ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _, f=fmt: f(v))); ax.set_xlim(-0.2, 7.0)
        axs[1].legend(frameon=False, fontsize=8, loc="upper right"); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)
    fig_stack(STACK); fig_lines(LINES)

    H = {r["key"]: r for r in D["headline"]}
    story = [P(f"{A} and {B} side by side", h1),
     P(f'Share of debt repaid by the final projection year: {A} {F["pct"](H["repaid_final_pct"]["deal_a"])}, {B} {F["pct"](H["repaid_final_pct"]["deal_b"])}. Entry gross leverage: {A} {F["x"](H["gross_leverage_x"]["deal_a"])}, {B} {F["x"](H["gross_leverage_x"]["deal_b"])}.', style("t", fontSize=10, leading=13)),
     P("Headline terms", h2), P(d["notes"].get("terms", "USD unless stated. Each deal is shown at its own anchor period and on its own EBITDA basis, named in the footnotes below."), small), Spacer(1, 3),
     tbl([["Metric", A, B]] + [[r["metric"], F[r["format"]](r["deal_a"]), F[r["format"]](r["deal_b"])] for r in D["headline"]], cw("headline", "0.34, 0.33, 0.33"), right=(1, 2)),
     P("Capital structure", h2), P("Share of total capitalization by layer.", small), Image(STACK, width=W, height=W * 2.0 / 10.0),
     P("Debt repaid and gross leverage", h2), P(d["notes"]["leverage"], small), Image(LINES, width=W, height=W * 2.7 / 10.0),
     P("Credit assessment by lens", h2), P(d["notes"]["scorecard"], small), Spacer(1, 3)]
    sc = [["Lens", f"{A} score", f"{A} rating", f"{A} driver", f"{B} score", f"{B} rating", f"{B} driver"]] + \
         [[r["lens"], F["score"](r["a_score"]), r["a_rating"], r["a_driver"], F["score"](r["b_score"]), r["b_rating"], r["b_driver"]] for r in D["scorecard"]]
    sc[0] = ["Lens", "Score", "Rating", f"{A} driver", "Score", "Rating", f"{B} driver"]
    story.append(P(f"Left block: {A}. Right block: {B}.", small))
    story.append(tbl(sc, cw("scorecard", "0.10, 0.06, 0.09, 0.26, 0.06, 0.09, 0.34"), right=(1, 4), muted=(3, 6)))
    story += [P("Repayment and screening view", h2), P("Raven's repayment read and screening view for each deal, quoted. A basis left blank is not stated here.", small), Spacer(1, 3),
     tbl([["Deal", "Repayment read"]] + [[r["deal"], r["read"]] for r in D["repayment"]], cw("repayment", "0.22, 0.78")), Spacer(1, 6),
     tbl([["Deal", "Tranche", "Screening view", "Basis"]] + [[r["deal"], r["tranche"], r["view"], r["basis"]] for r in D["screening"]], cw("screening", "0.2, 0.2, 0.15, 0.45")),
     P("Notes", h2), P(f"Source: Raven's analysis of each deal's documents, pulled on {d['pull_date']}. This is a saved copy and does not refresh on its own.", small)] + [P(f, small) for f in d["footnotes"]]

    def footer(c, doc):
        c.saveState(); c.setFont("Helvetica", 7); c.setFillColor(colors.HexColor("#777777"))
        c.drawString(MARG, 0.35 * inch, f"{A} and {B} comparison, pulled {d['pull_date']}"); c.drawRightString(PAGE[0] - MARG, 0.35 * inch, f"Page {doc.page}"); c.restoreState()
    doc = SimpleDocTemplate(out, pagesize=PAGE, leftMargin=MARG, rightMargin=MARG, topMargin=0.55 * inch, bottomMargin=0.6 * inch, title=f"{A} and {B} comparison", author="Raven Risk AI")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
