"""Shared QA checks for the book (used by the qa-* project Skills in .claude/skills/).

Reuses the project's existing checks:
  - tools/check_pdf.py (typesetting: errors, missing glyphs, over/underfull, undefined refs/cites,
    text outside page, white text on light background), run as a subprocess;
  - glyph-position reading of RTL lines (PRD §6 verification rule; INC-001);
  - diagram-label-inside-block, table-column order/alignment, footer numbers + progress dot
    (Prompts 18-20), ID-leak and README-link scans (Prompts 12-13).

Usage:
  .venv/bin/python tools/qa/qa_lib.py --pdf <pdf> --log <latex log> --checks all|bidi,table,... --out <dir>
Writes <out>/findings.json and prints a one-line summary. Never edits project files.
"""
import argparse, json, os, re, subprocess, sys, hashlib, zipfile
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parents[2]
EXP = json.loads((ROOT / "tools/qa/expectations.json").read_text(encoding="utf-8"))
HEB = re.compile(r"[\u0590-\u05FF]")
LTR = re.compile(r"[0-9A-Za-z]")
MIRROR = {"(": ")", ")": "(", "[": "]", "]": "["}
# "submission" (Moodle PDF: IDs + date on the cover) or "public" (GitHub PDF: neither). Set by --edition.
EDITION = EXP.get("edition", "submission")

findings = []
def add(check, status, where, evidence, expected, severity="info", kind="none"):
    """status: pass | fail | n/a.  kind (for fails): template | skill | content | packaging | build"""
    findings.append(dict(id=f"{check}-{len(findings)+1:02d}", check=check, status=status, where=where,
                         evidence=evidence, expected=expected, severity=severity if status == "fail" else "info",
                         kind=kind if status == "fail" else "none"))

# ---------- glyph-level reading of RTL lines (the INC-001 rule) ----------
def page_lines(page):
    out = []
    for b in page.get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            cs = [c for s in l["spans"] for c in s["chars"]]
            if cs: out.append((l, cs))
    return out

def read_rtl(cs):
    """Reading order of a visual line: right-to-left runs, with left-to-right Latin/digit runs kept intact."""
    cs = sorted(cs, key=lambda c: c["origin"][0])
    groups = []
    for i, c in enumerate(cs):
        ch = c["c"]
        is_l = bool(LTR.match(ch))
        if not is_l and ch == "%" and groups and groups[-1][0] and LTR.match(groups[-1][1][-1]):
            is_l = True                                 # trailing percent sign belongs to the number (28.8%)
        if not is_l and ch in " .,:%-/" and groups and groups[-1][0]:
            nxt = next((x["c"] for x in cs[i+1:] if x["c"] != " "), "")
            if LTR.match(nxt): is_l = True            # punctuation/space inside an LTR run (e.g. 28.8, 07:30, explicit feedback)
        if groups and groups[-1][0] == is_l: groups[-1][1].append(ch)
        else: groups.append((is_l, [ch]))
    s = ""
    for is_l, g in reversed(groups):
        s += "".join(g) if is_l else "".join(MIRROR.get(x, x) for x in reversed(g))
    return s

def page_text_rtl(page):
    lines = sorted(page_lines(page), key=lambda t: (round(t[0]["bbox"][1]), -t[0]["bbox"][2]))
    return " ".join(read_rtl(cs) if any(HEB.match(c["c"]) for c in cs) else "".join(c["c"] for c in sorted(cs, key=lambda c: c["origin"][0])) for l, cs in lines)

def norm(s): return re.sub(r"\s+", "", s).replace("”", "\"").replace("“", "\"")

# ---------------------------------- checks ----------------------------------
def check_typeset(doc, pdf, log, out):
    r = subprocess.run([sys.executable, str(ROOT / "tools/check_pdf.py"), str(pdf), str(log), str(Path(out) / "pages")],
                       capture_output=True, text=True)
    ok = r.returncode == 0
    # Privacy: the rendered cover shows the student IDs; overwrite it with the masked render at once.
    pages = Path(out) / "pages"
    if (pages / "page-01.png").exists():
        subprocess.run([sys.executable, str(ROOT / "tools/screenshots.py"), str(pdf), "mask-cover", str(pages / "page-01.png"),
                        "--expect-ids", "0" if EDITION == "public" else "2"],
                       capture_output=True, text=True, check=True)
    add("qa-typeset", "pass" if ok else "fail", f"{pdf.name} + {log.name}", r.stdout.strip().splitlines()[0] if r.stdout else r.stderr[-200:],
        "0 errors, 0 missing glyphs, no overfull >2pt, 0 undefined refs/cites, no text outside page, no white-on-light text",
        "major", "template")
    if doc.page_count == EXP["pages"]:
        add("qa-typeset", "pass", "whole PDF", f"{doc.page_count} pages", f"{EXP['pages']} pages")
    else:
        add("qa-typeset", "fail", "whole PDF", f"{doc.page_count} pages", f"{EXP['pages']} pages", "blocker", "template")
    toc = {t: p for _, t, p in doc.get_toc()}
    diff = {t: (toc.get(t), p) for t, p in EXP["chapter_starts"].items() if toc.get(t) != p}
    add("qa-typeset", "fail" if diff else "pass", "TOC / chapter openings", f"mismatches: {diff}" if diff else "all 10 start pages match",
        "chapter start pages as approved", "major", "template")

def check_public_cover(doc):
    """Public edition (Prompt 27): the cover must show no student ID, no date and no ID/date labels.
    Checked on both the glyph-order RTL reading and PyMuPDF's raw text, so a reversed digit run is caught too."""
    pub = EXP["cover_public"]; p = doc[0]
    texts = (norm(page_text_rtl(p)), p.get_text())
    bad_l = [l for l in pub["forbidden_labels"] if any(norm(l) in t or l in t for t in texts)]
    bad_p = sorted({m for pat in pub["forbidden_patterns"] for t in texts for m in re.findall(pat, t)})
    add("qa-bidi", "fail" if (bad_l or bad_p) else "pass", "page 1 (cover, public edition)",
        # values are counted, never printed: a failing report must not itself leak an ID or the date
        f"forbidden labels: {bad_l}; forbidden numbers/dates: {len(bad_p)} found (values withheld)" if (bad_l or bad_p)
        else "no ID or submission-date label and no 9-digit number or date on the cover",
        "public cover without student IDs and without the submission date", "blocker", "content")

def check_bidi(doc):
    full = {i+1: norm(page_text_rtl(p)) for i, p in enumerate(doc)}
    for group in ("diagram", "graph", "table", "mixed", "cover"):
        phrases = EXP["cover_public"]["phrases"] if (group == "cover" and EDITION == "public") else EXP["phrases"][group]
        for ph in phrases:
            hit = [pg for pg, t in full.items() if norm(ph) in t]
            add("qa-bidi", "pass" if hit else "fail", f"pages {hit}" if hit else "whole PDF",
                f"'{ph}' read in RTL order from glyph positions" + ("" if hit else ": NOT found in reading order"),
                f"'{ph}' readable right-to-left with Latin/digit runs intact", "major", "template")
    if EDITION == "public":
        check_public_cover(doc)
    # multi-number citations ascending (LTR unit)
    bad = []
    for i, p in enumerate(doc, 1):
        for l, cs in page_lines(p):
            t = "".join(c["c"] for c in sorted(cs, key=lambda c: c["origin"][0]))
            for m in re.findall(r"\[(\d+(?:, \d+)+)\]", t):
                n = [int(x) for x in m.split(", ")]
                if n != sorted(n): bad.append((i, m))
    add("qa-bidi", "fail" if bad else "pass", "all pages", f"unsorted: {bad}" if bad else "every multi-number citation ascending",
        "citations like [4, 7] ascending", "minor", "template")

def check_table(doc):
    # Table 4.1: first column (היבט) rightmost; X-columns flush right (constant right edges)
    tp = next((p for p in doc if "שילוב גישות" in p.get_text()), None)
    if not tp:
        add("qa-table", "fail", "whole PDF", "Table 4.1 not found", "Table 4.1 present", "major", "content"); return
    def x_of(page, word):
        for l, cs in page_lines(page):
            t = "".join(c["c"] for c in cs)
            if word in t or word[::-1] in t: return l["bbox"]
    a, b = x_of(tp, "היבט"), x_of(tp, "שילוב")
    ok = a and b and a[0] > b[2]
    add("qa-table", "pass" if ok else "fail", f"p.{tp.number+1} Table 4.1", f"'היבט' x={a and round(a[0])}, 'שילוב גישות' x={b and round(b[0])}",
        "first column (היבט) on the right, last column on the left (RTL)", "major", "template")
    edges = {}
    for l, cs in page_lines(tp):
        if not (150 < l["bbox"][1] < 450): continue
        cs2 = sorted([c for c in cs if c["c"].strip()], key=lambda c: -c["bbox"][2])
        if not cs2: continue
        cell, cells = [cs2[0]], []
        for c in cs2[1:]:
            if cell[-1]["bbox"][0] - c["bbox"][2] > 9: cells.append(cell); cell = []
            cell.append(c)
        cells.append(cell)
        for ce in cells:
            e = round(max(c["bbox"][2] for c in ce)); edges[e] = edges.get(e, 0) + 1
    top = sorted(edges.items(), key=lambda kv: -kv[1])[:4]
    ok = len(top) == 4 and all(n >= 6 for _, n in top)
    add("qa-table", "pass" if ok else "fail", f"p.{tp.number+1} Table 4.1", f"4 dominant cell right edges (pt:count) {top}",
        "each column's cells share one right edge (flush right, ragged left)", "minor", "template")
    # Chapter 3 data table order
    p9 = next((p for p in doc if "מאזין/ה" in p.get_text() or "ה/ןיזאמ" in p.get_text()), None)
    if p9:
        a, b = x_of(p9, "מאזין"), x_of(p9, "שיר ג")
        ok = a and b and a[0] > b[2]
        add("qa-table", "pass" if ok else "fail", f"p.{p9.number+1} data table", f"'מאזין/ה' x={a and round(a[0])}, 'שיר ג' x={b and round(b[0])}",
            "first column on the right", "major", "template")

def check_img(doc):
    pg = next((p for p in doc if "לולאת" in p.get_text() and "ולמידה" in p.get_text()), None)
    if pg:
        rects = [x["rect"] for x in pg.get_drawings() if 80 < x["rect"].width < 100 and 35 < x["rect"].height < 50]
        cs = [c for _, cc in page_lines(pg) for c in cc]
        inside = sum(1 for R in rects if any(R.x0 <= c["bbox"][0] and c["bbox"][2] <= R.x1 and R.y0 <= c["bbox"][1] and c["bbox"][3] <= R.y1 and HEB.match(c["c"]) for c in cs))
        ok = len(rects) == EXP["diagram_blocks"] and inside == len(rects)
        add("qa-img", "pass" if ok else "fail", f"p.{pg.number+1} Fig. 6.1", f"{len(rects)} blocks, {inside} with Hebrew label fully inside",
            f"{EXP['diagram_blocks']} blocks, every label inside its block", "major", "template")
    for fig, tag in (("2.1", "נתונים בדיוניים"), ("6.1", "דוגמה לימודית")):
        p = next((p for p in doc if f"{fig}" in p.get_text() and tag in p.get_text()), None)
        add("qa-img", "pass" if p else "fail", f"Fig. {fig}" + (f" p.{p.number+1}" if p else ""), "caption + tag found" if p else "caption or tag missing",
            f"Fig. {fig} captioned and tagged '{tag}'", "major", "content")
    # Visible-ink check of the side margins (vector drawing rects are unreliable: matplotlib hatch
    # pattern definitions report off-page coordinates but draw nothing there; calibrated 2026-11-18).
    x0, x1 = EXP["text_block_x"]; over = []
    for i, p in enumerate(doc, 1):
        if i == 1: continue
        pix = p.get_pixmap(dpi=36); sx = pix.width / p.rect.width; bg = pix.pixel(2, pix.height // 2)
        for y in range(int(75 * sx), int(755 * sx)):
            for x in list(range(0, int((x0 - 4) * sx))) + list(range(int((x1 + 4) * sx), pix.width)):
                px = pix.pixel(x, y)
                if sum(abs(a - b) for a, b in zip(px, bg)) > 60: over.append(i); break
            if over and over[-1] == i: break
    add("qa-img", "fail" if over else "pass", "pp. 2-20 side margins", f"visible ink in the side margins on pages {over}" if over else "no visible ink in the side margins",
        "no figures, boxes or text in the side margins", "minor", "template")

def check_code(doc):
    add("qa-code", "n/a", "whole book", "the book contains no code boxes (pythonbox/listings)", "code boxes, if any, checked for background and overflow")

def check_footer(doc):
    tot = doc.page_count; bad = []; dots = []
    for i, p in enumerate(doc, 1):
        if i == 1: continue
        foot = sorted((round(l["bbox"][0]), "".join(c["c"] for c in sorted(cs, key=lambda c: c["origin"][0]))) for l, cs in page_lines(p) if l["bbox"][1] > 760)
        if not foot or foot[0][1] != str(tot) or foot[-1][1] != str(i): bad.append((i, foot))
        d = [x["rect"] for x in p.get_drawings() if x["rect"].y0 > 760 and x["rect"].width < 8 and x.get("fill") and x["fill"][0] > 0.9 and x["fill"][1] < 0.3]
        dots.append(round(d[0].x0) if d else None)
    mono = all(a is not None and b is not None and b < a for a, b in zip(dots, dots[1:]))
    add("qa-footer", "fail" if bad else "pass", "pp. 2-20 footers", f"wrong: {bad}" if bad else f"left = total ({tot}), right = page number on every page",
        "left number = total pages, right number = current page (LTR digits)", "major", "template")
    p19 = bad and any(i == 19 for i, _ in bad)
    add("qa-footer", "fail" if p19 else "pass", "p.19 footer (regression, Prompt 18)", "page 19 footer correct" if not p19 else "page 19 footer wrong again",
        "p.19: '20' left, '19' right, bar not mirrored", "blocker", "template")
    add("qa-footer", "pass" if mono else "fail", "pp. 2-20 progress dot", f"pink dot x per page: {dots}",
        "dot moves strictly right-to-left as pages advance", "minor", "template")

def check_bib(doc, log):
    # Locate the real chapter heading: a line that is exactly "מקורות" set at heading size (>= 16 pt).
    # This excludes the 8.7 pt running header, the 10.5 pt TOC line and body text (round-01 D1-02).
    want = EXP["chapter_starts"]["מקורות"]
    heads = [p.number + 1 for p in doc for b in p.get_text("dict")["blocks"] for l in b.get("lines", [])
             if "".join(s["text"] for s in l["spans"]).strip() == "מקורות" and max(s["size"] for s in l["spans"]) >= 16]
    labels, xs = set(), []
    for p in doc[doc.page_count-3:]:
        for b in p.get_text("blocks"):
            m = re.match(r"\s*\[(\d+)\]", b[4])
            if m: labels.add(int(m.group(1))); xs.append(b[0])
    ok = heads == [want] and len(labels) == EXP["bib_entries"] and xs and min(xs) >= EXP["text_block_x"][0] - 0.5
    add("qa-typeset", "pass" if ok else "fail", "bibliography",
        f"heading 'מקורות' on p.{heads if len(heads) != 1 else heads[0]}; {len(labels)} entries; min x0={xs and round(min(xs),1)}",
        f"heading 'מקורות' on p.{want} only, {EXP['bib_entries']} numbered entries, all inside the margins", "major", "template")
    blg = Path(str(log).replace(".log", ".blg"))
    if blg.exists():
        w = len(re.findall(r"WARN|ERROR", blg.read_text(errors="replace")))
        add("qa-typeset", "fail" if w else "pass", blg.name, f"{w} biber warnings/errors", "0 biber warnings (all 18 sources resolve)", "major", "build")

def check_infra(doc, pdf):
    missing = [f for f in EXP["required_files"] if not (ROOT / f).exists()]
    add("qa-infra", "fail" if missing else "pass", "project root", f"missing: {missing}" if missing else "all required files present",
        "A2 §3.3 files present (main.tex, chapters, .cls, PRD, PLAN, TODO, README)", "major", "packaging")
    lay = [l for l in (ROOT / "book/chapters").glob("*.tex") for line in l.read_text(encoding="utf-8").splitlines()
           if re.search(r"\\begin\{minipage\}|\\renewcommand\{\\tabularxcolumn\}|\\begin\{(table|figure)\}\[h!\]", line)]
    add("qa-infra", "fail" if lay else "pass", "book/chapters/", f"layout code found in: {sorted({p.name for p in lay})}" if lay else "no layout code in chapter files",
        "layout lives in the class (A2 iron law)", "major", "template")
    s = (ROOT / "README.md").read_text(encoding="utf-8")
    links = [l for l in re.findall(r"\]\(([^)#]+)\)", s) if not l.startswith("http")]
    broken = [l for l in links if not (ROOT / l).exists()]
    add("qa-infra", "fail" if broken else "pass", "README.md", f"{len(links)} links, broken: {broken}" if broken else f"{len(links)} relative links resolve",
        "every README link resolves", "minor", "packaging")
    ids = re.findall(r"\\studentid\{(\d{9})\}", (ROOT / "book/main.tex").read_text(encoding="utf-8"))
    leak = []
    for base, dirs, files in os.walk(ROOT):
        if any(x in base for x in ("/.venv", "/.git")): continue
        for f in files:
            fp = Path(base) / f
            if fp.suffix in (".pdf", ".zip") or fp == ROOT / "book/main.tex": continue
            try: data = fp.read_bytes()
            except Exception: continue
            if any(i.encode() in data for i in ids): leak.append(str(fp.relative_to(ROOT)))
    add("qa-infra", "fail" if leak else "pass", "all text files", f"IDs found in: {leak}" if leak else "student IDs only in book/main.tex (and PDFs)",
        "no student IDs outside main.tex and the PDF", "blocker", "packaging")
    sub = ROOT / "submission/behind-the-playlist.pdf"
    zp = ROOT / "submission/project-source.zip"
    if EDITION == "public":
        add("qa-infra", "n/a", "submission/", "public edition: the submission PDF and ZIP are not part of the public copy",
            "ZIP freshness is checked on the submission edition only")
    elif zp.exists():
        with zipfile.ZipFile(zp) as z:
            names = z.namelist()
            zpdf = next((n for n in names if n.endswith("submission/behind-the-playlist.pdf")), None)
            same = zpdf and hashlib.sha256(z.read(zpdf)).hexdigest() == hashlib.sha256(sub.read_bytes()).hexdigest()
            has_cls = any(n.endswith(".cls") for n in names)
        add("qa-infra", "pass" if (same and has_cls) else "fail", "submission/project-source.zip",
            f"ZIP PDF matches submission PDF: {bool(same)}; ZIP contains .cls: {has_cls}",
            "the source package contains the approved PDF and the current sources", "major", "packaging")

def check_cls_version(log):
    cls = (ROOT / "book/behind-the-playlist.cls").read_text(encoding="utf-8")
    m = re.search(r"\\ProvidesClass\{behind-the-playlist\}\[(\S+) (v[\d.]+)", cls)
    cl = re.search(r"%\s+(v[\d.]+)\s+(\d{4}-\d{2}-\d{2})", cls)
    lg = re.search(r"Document Class: behind-the-playlist (\S+) (v[\d.]+)", Path(log).read_text(errors="replace"))
    ok = m and cl and lg and m.group(2) == cl.group(1) == lg.group(2)
    add("qa-cls-version", "pass" if ok else "fail", "behind-the-playlist.cls + build log",
        f"\\ProvidesClass {m and m.group(2)}; CHANGELOG {cl and cl.group(1)}; log {lg and lg.group(2)}",
        "class version identical in \\ProvidesClass, CHANGELOG and the build log", "major", "template")

CHECKS = {"typeset": lambda d, a: (check_typeset(d, a.pdf, a.log, a.out), check_bib(d, a.log)),
          "bidi": lambda d, a: check_bidi(d), "table": lambda d, a: check_table(d), "img": lambda d, a: check_img(d),
          "code": lambda d, a: check_code(d), "footer": lambda d, a: check_footer(d),
          "infra": lambda d, a: check_infra(d, a.pdf), "cls-version": lambda d, a: check_cls_version(a.log)}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", type=Path, required=True); ap.add_argument("--log", type=Path, required=True)
    ap.add_argument("--checks", default="all"); ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--edition", choices=("submission", "public"), default=EDITION)
    a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True); EDITION = a.edition
    doc = pymupdf.open(a.pdf)
    for name in (CHECKS if a.checks == "all" else a.checks.split(",")): CHECKS[name](doc, a)
    (a.out / "findings.json").write_text(json.dumps(dict(pdf=str(a.pdf.relative_to(ROOT)) if a.pdf.is_absolute() else str(a.pdf),
        sha256=hashlib.sha256(a.pdf.read_bytes()).hexdigest(), edition=EDITION, findings=findings), ensure_ascii=False, indent=1), encoding="utf-8")
    n = {s: sum(f["status"] == s for f in findings) for s in ("pass", "fail", "n/a")}
    print(f"QA {a.checks} [{EDITION} edition]: {n['pass']} pass, {n['fail']} fail, {n['n/a']} n/a -> {a.out/'findings.json'}")
