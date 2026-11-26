"""Shared QA checks for the book (used by the qa-* project Skills in .claude/skills/).

Reuses the project's existing checks:
  - tools/check_pdf.py (typesetting: log, missing glyphs, over/underfull, undefined refs/cites,
    text outside page, faint text), run as a subprocess;
  - glyph-position reading of RTL lines (PRD §6 verification rule; INC-001);
  - diagram-label-inside-block, table-column order/alignment, footer numbers + progress dot
    (Prompts 18-20), ID-leak and README-link scans (Prompts 12-13);
  - rendered visibility, text completeness and a render fingerprint (QA round 2).

Usage:
  .venv/bin/python tools/qa/qa_lib.py --pdf <pdf> (--log <latex log> | --no-log) --checks all|bidi,table,... --out <dir>
  .venv/bin/python tools/qa/qa_lib.py --pdf <approved pdf> --write-visual-baseline --users-approval "<who, when, why>"
Writes <out>/findings.json and prints a one-line summary. Never edits book or Skill files.
Exit codes: 0 = no fail; 1 = at least one fail; 2 = usage error or crash.

Rules of this file (QA round 2):
  - a missing target is a fail, never a skipped check; `min_findings` guards each family;
  - a check that raises becomes a fail finding;
  - a check that cannot run (no log, public edition) reports n/a with the reason, never pass;
  - no ID or date value is ever printed (see redact()).
"""
import argparse, base64, hashlib, json, os, re, subprocess, sys, traceback, unicodedata, zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import unquote
import pymupdf

def remove_stale(argv):
    """A stale result must never survive, not even when arguments or expectations.json are wrong."""
    for i, x in enumerate(argv):
        m = re.match(r"--o(?:ut?)?(?:=(.*))?$", x)        # also the abbreviations that argparse then rejects
        o = m and (m.group(1) if m.group(1) is not None else argv[i + 1] if i + 1 < len(argv) else None)
        if o: (Path(o) / "findings.json").unlink(missing_ok=True)

if __name__ == "__main__": remove_stale(sys.argv[1:])     # before anything below can crash

ROOT = Path(__file__).resolve().parents[2]
EXP = json.loads((ROOT / "tools/qa/expectations.json").read_text(encoding="utf-8"))
BASELINE = ROOT / "tools/qa/visual_baseline.json"
HEB = re.compile(r"[\u0590-\u05FF]")
LTR = re.compile(r"[0-9A-Za-z]")
MIRROR = {"(": ")", ")": "(", "[": "]", "]": "["}
# "submission" (Moodle PDF: IDs + date on the cover) or "public" (GitHub PDF: neither). Set by --edition.
EDITION = EXP.get("edition", "submission")

# ---------- reporting ----------
SEP = r"[ \t\u00a0\u2009\u202f\-\u2010-\u2015\u2212]"
def redact(s):
    """Nothing that could be an ID (9+ digits, also spaced or hyphenated) leaves this program."""
    return re.sub(rf"\d(?:{SEP}?\d){{8,}}", "[number withheld]", str(s))

findings = []
def add(check, status, where, evidence, expected, severity="info", kind="none", name=None):
    """status: pass | fail | n/a.  kind (for fails): template | skill | content | packaging | build.
    name: stable check name, used by tests/test_qa_mutations.py."""
    findings.append(dict(id=f"{check}-{len(findings)+1:02d}", check=check, name=name or check, status=status,
                         where=redact(where), evidence=redact(evidence), expected=expected,
                         severity=severity if status == "fail" else "info",
                         kind=kind if status == "fail" else "none"))

def result(check, name, ok, where, good, bad, expected, severity, kind):
    add(check, "pass" if ok else "fail", where, good if ok else bad, expected, severity, kind, name)

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

def line_text(cs):
    if any(HEB.match(c["c"]) for c in cs): return read_rtl(cs)
    return "".join(c["c"] for c in sorted(cs, key=lambda c: c["origin"][0]))

def page_text_rtl(page, sep=" ", rect=None):
    lines = sorted(page_lines(page), key=lambda t: (round(t[0]["bbox"][1]), -t[0]["bbox"][2]))
    return sep.join(line_text(cs) for l, cs in lines if rect is None or inside(l["bbox"], rect))

def norm(s): return re.sub(r"\s+", "", s).replace("”", "\"").replace("“", "\"")

def inside(b, r, t=1.0): return b[0] >= r[0] - t and b[1] >= r[1] - t and b[2] <= r[2] + t and b[3] <= r[3] + t

def page_of(doc, number):
    """1-based page, or None when the PDF is too short (callers must fail, not skip)."""
    return doc[number - 1] if 1 <= number <= doc.page_count else None

def strip_comments(tex):
    """Remove TeX comments: from an unescaped % (even number of backslashes before it) to the end of the line."""
    return "\n".join(re.sub(r"(?<!\\)((?:\\\\)*)%.*", r"\1", l) for l in tex.splitlines())

def chapters(): return sorted((ROOT / "book/chapters").glob("*.tex"))
def read(p): return Path(p).read_text(encoding="utf-8", errors="replace")

# ---------- rendered visibility (QA round 2) ----------
VIS_DPI = 100
MIN_INK = 60        # approved PDF: the faintest real character changes its pixels by >= 75 of 255
_vis = {}
def visible_chars(doc, i):
    """[(char, bbox, ink)] of page i (0-based). The page is rendered twice, with all text and with the
    text operators removed from a copy in memory; ink = the largest grey difference inside the character's box.
    Text that is covered, transparent, background-coloured or off-page leaves no difference (ink ~ 0)."""
    key = (id(doc), doc.name, i)
    if key in _vis: return _vis[key]
    p = doc[i]
    copy = pymupdf.open(); copy.insert_pdf(doc, from_page=i, to_page=i); q = copy[0]
    q.add_redact_annot(q.rect, fill=False); q.apply_redactions(images=0, graphics=0, text=0)
    if q.get_text().strip(): raise RuntimeError(f"page {i+1}: text could not be removed for the visibility test")
    a = p.get_pixmap(dpi=VIS_DPI, colorspace=pymupdf.csGRAY); b = q.get_pixmap(dpi=VIS_DPI, colorspace=pymupdf.csGRAY)
    A, B, st, k = a.samples, b.samples, a.stride, VIS_DPI / 72
    def ink(x0, y0, x1, y1):
        xa, xb = max(0, int(x0 * k)), min(a.width, int(x1 * k) + 1); m = 0
        for y in range(max(0, int(y0 * k)), min(a.height, int(y1 * k) + 1)):
            u, v = A[y * st + xa:y * st + xb], B[y * st + xa:y * st + xb]
            if u != v: m = max(m, max(abs(s - t) for s, t in zip(u, v)))
        return m
    out = []
    for l, cs in page_lines(p):
        for c in cs:
            if not c["c"].strip() or unicodedata.category(c["c"]) in ("Cf", "Mn"): continue
            x0, y0, x1, y1 = c["bbox"]; m = ink(x0, y0, x1, y1)
            # one glyph for two characters (the "fi" ligature): PyMuPDF splits the box; look one letter wider
            if m < MIN_INK: m = max(m, ink(x0 - 2, y0, x1 + 2, y1))
            out.append((c["c"], (x0, y0, x1, y1), m))
    copy.close()
    _vis[key] = out
    return out

def hidden(doc, i, rect=None):
    cs = [c for c in visible_chars(doc, i) if rect is None or inside(c[1], rect, 2)]
    return len(cs), sum(1 for c in cs if c[2] < MIN_INK)

GRID = (20, 28)     # cells per page (x, y); RGB mean per cell
# Tolerances: calibrated in docs/qa/round-02/fix/fixer-report.md (re-rendering noise vs. smallest mutation).
FP_CELL, FP_MEAN = 4, 0.3
def fingerprint(page, dpi=72):
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csRGB, alpha=False)
    S, st, out = pix.samples, pix.stride, bytearray()
    for gy in range(GRID[1]):
        y0, y1 = gy * pix.height // GRID[1], (gy + 1) * pix.height // GRID[1]
        for gx in range(GRID[0]):
            x0, x1 = gx * pix.width // GRID[0], (gx + 1) * pix.width // GRID[0]
            rows = [S[y * st + 3 * x0:y * st + 3 * x1] for y in range(y0, y1)]
            for ch in range(3):
                out.append(round(sum(sum(r[ch::3]) for r in rows) / ((y1 - y0) * (x1 - x0))))
    return bytes(out)

def fp_diff(a, b):
    d = [abs(x - y) for x, y in zip(a, b)]
    return max(d), sum(d) / len(d)

def check_visual(doc):
    n = doc.page_count
    bad = [(i, p.rotation, [round(x) for x in p.rect]) for i, p in enumerate(doc, 1) if p.rotation or
           any(abs(a - b) > 1 for a, b in zip((p.rect.width, p.rect.height), EXP["page_size"]))]
    result("qa-visual", "visual.page-geometry", not bad, "all pages", f"{n} pages, rotation 0, A4", f"rotated or resized: {bad}",
           "page rotation 0 and A4 on every page", "major", "template")
    ann = [(i, a.type[1]) for i, p in enumerate(doc, 1) for a in p.annots()] + \
          [(i, "Widget") for i, p in enumerate(doc, 1) for _ in (p.widgets() or [])]
    result("qa-visual", "visual.annotations", not ann, "all pages", "no annotations except links", f"annotations: {ann}",
           "no annotations other than links", "major", "template")
    imgs = [(i, len(p.get_images(full=True))) for i, p in enumerate(doc, 1) if p.get_images(full=True)]
    total = sum(k for _, k in imgs)
    result("qa-visual", "visual.raster-images", total == EXP["raster_images"], "all pages",
           f"{total} raster images (the book is fully vector)", f"raster images on pages (page, count): {imgs}",
           f"{EXP['raster_images']} raster images: text inside an image cannot be read, so it could hide an ID", "blocker", "template")
    for i in range(n):
        tot, hid = hidden(doc, i) if not doc[i].rotation else (0, 0)
        result("qa-visual", "visual.contrast", tot > 0 and hid == 0, f"p.{i+1}", f"{tot} characters, all visible in the render",
               "no measurable text (empty or rotated page)" if not tot else f"{hid} of {tot} characters are not visible in the render",
               "every character visibly changes the rendered page at its place", "blocker", "template")
    over = [(p.number + 1, k) for p in doc for k in [overlaps(p)] if k]
    result("qa-visual", "visual.overlap", not over, "all pages", "no text printed over other text",
           f"(page, overlapping characters): {over}", "no line of text overlaps another one", "major", "template")
    for key, r in EXP["regions"].items():
        p = page_of(doc, r["page"]); where = f"p.{r['page']} {key}"
        if p is None:
            add("qa-visual", "fail", where, "page missing", "region present", "blocker", "template", f"visual.region.{key}"); continue
        tot, hid = hidden(doc, r["page"] - 1, r["rect"]); why = []
        if tot < r["min_chars"]: why.append(f"only {tot} characters (minimum {r['min_chars']})")
        if hid: why.append(f"{hid} characters not visible")
        pix = p.get_pixmap(dpi=72, clip=pymupdf.Rect(r["rect"]), colorspace=pymupdf.csRGB, alpha=False); S = pix.samples
        px = Counter(zip(S[0::3], S[1::3], S[2::3])) if pix.stride == pix.width * 3 else Counter()
        for c in r["palette"]:
            k = sum(m for q, m in px.items() if max(abs(x - y) for x, y in zip(q, c["rgb"])) <= 24)
            if k < c["min_px"]: why.append(f"colour {c['rgb']}: {k} pixels (minimum {c['min_px']})")
        result("qa-visual", f"visual.region.{key}", not why, where, f"{tot} characters visible; palette ink present" if r["palette"]
               else f"{tot} characters visible", "; ".join(why), "text and palette of the region visible in the render", "blocker", "template")
    check_fingerprint(doc)

def overlaps(page):
    """Characters whose centre lies inside a character of another line on (nearly) the same baseline."""
    ch = [(id(l), c["bbox"], c["origin"][1]) for l, cs in page_lines(page) if abs(l["dir"][0]) > 0.99 for c in cs if c["c"].strip()]
    rows = {}
    for t in ch:
        h = t[1][3] - t[1][1]; y = t[2] - h * .25; rows.setdefault(int(y // 4), []).append((t[0], t[1], y))
    n = 0
    for k, row in rows.items():
        near = [t for d in (-1, 0, 1) for t in rows.get(k + d, [])]
        for l, b, y in row:
            x = (b[0] + b[2]) / 2
            n += any(l2 != l and b2[0] + 1 < x < b2[2] - 1 and abs(y - y2) < 3 for l2, b2, y2 in near)
    return n

def check_fingerprint(doc):
    exp = "render equals the approved PDF's coarse fingerprint (regenerate only with the users' approval)"
    if not BASELINE.exists():
        add("qa-visual", "fail", "tools/qa/visual_baseline.json", "baseline file missing", exp, "major", "skill", "visual.fingerprint"); return
    b = json.loads(read(BASELINE)); bad = []
    pages = range(1, max(len(b["pages"]), doc.page_count) + 1)
    if b["edition"] != EDITION:
        add("qa-visual", "n/a", "cover", f"baseline is the {b['edition']} edition; the cover differs by design", exp, name="visual.fingerprint-cover")
        pages = pages[1:]
    for i in pages:
        p = page_of(doc, i)
        if p is None or i > len(b["pages"]): bad.append((i, "page missing or extra")); continue
        m, mean = fp_diff(fingerprint(p), base64.b64decode(b["pages"][i - 1]))
        if m > FP_CELL or mean > FP_MEAN: bad.append((i, f"max cell {m}, mean {mean:.2f}"))
    result("qa-visual", "visual.fingerprint", not bad, f"pp. {pages[0]}-{pages[-1]}", f"all pages within max cell {FP_CELL} and mean {FP_MEAN}",
           f"differs from the approved render: {bad}", exp, "major", "template")

def write_baseline(pdf, approval):
    doc = pymupdf.open(pdf)
    data = dict(_comment="Coarse render fingerprint of the approved PDF (20x28 cells, RGB means, base64). Generated only by "
                "qa_lib.py --write-visual-baseline --users-approval ...; never edit by hand.",
                edition=EDITION, sha256=hashlib.sha256(Path(pdf).read_bytes()).hexdigest(), approval=approval,
                grid=GRID, pages=[base64.b64encode(fingerprint(p)).decode() for p in doc])
    BASELINE.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")

# ---------- privacy (QA round 2) ----------
INVISIBLE = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2069\ufeff\u00ad]")
NUM = rf"(?:\d{{9}}|\d{{8}}{SEP}\d|\d{{3}}{SEP}\d{{3}}{SEP}\d{{3}}|\d(?:{SEP}\d){{8}})"
ID_RX = re.compile(rf"(?:(?<![0-9A-Za-z])|(?<=[iI][dD])|(?<=[tT][zZ]))(?<!\d\.)(?<!\d{SEP}){NUM}(?![0-9A-Za-z])(?!{SEP}\d)")
ODD_RX = re.compile(rf"(?<![0-9A-Za-z])(?<!\d\.)(?<!\d{SEP})\d(?:{SEP}?\d){{8}}(?![0-9A-Za-z])(?!{SEP}\d)")
ID_CONTEXT = re.compile(r"student.?id|\bI\.?D\b|ת[\"״']?ז|תעודת זהות|מספר זהות", re.I)

def check_digit_ok(digits):
    """Israeli ID check digit."""
    v = [int(c) * (1 + i % 2) for i, c in enumerate(digits)]
    return sum(x if x < 10 else x - 9 for x in v) % 10 == 0

GAP = r"(?:[ \t]{1,3}|[ \t]*\r?\n[ \t]*|&nbsp;|[./,_])"
LOOSE_RX = re.compile(rf"(?<![0-9A-Za-z])(?<!\d[.,/\-])(?:\d{{3}}{GAP}\d{{3}}{GAP}\d{{3}}|\d{{8}}{GAP}\d|"
                      r"\d{2,7}[ \t]*\r?\n[ \t]*\d{2,7})(?![0-9A-Za-z])(?![.,/\-]\d)")
ALONE_RX = re.compile(r"(?<![0-9A-Za-z.,/\-])\d{9}(?![0-9A-Za-z\-])")   # whole number, whatever stands next to it
WORD_RX = re.compile(r"[0-9A-Za-z]+")
BASE64_RX = re.compile(r"[0-9A-Za-z+/]{60,}")       # encoded images in transcripts: not words

def loose_spans(text):
    """Forms that also occur in ordinary numbers, so a valid Israeli check digit (about 1 in 10 by chance) or an
    ID word before them is required: dots, slashes, commas, underscores, &nbsp;, several spaces, a line break,
    neighbouring numbers, letters glued to the number. Missed: an ID after a decimal point or in a longer digit
    run, glued letters that are all a-f (looks like a hash) or inside 60+ base64 characters, and any of these forms with a wrong check digit."""
    out = set()
    def take(s, e):
        d = "".join(c for c in text[s:e] if c.isdigit())
        ctx = ID_CONTEXT.search(text[max(0, s - 40):s])
        if len(d) == 9 and len(set(d)) > 2 and (check_digit_ok(d) or ctx): out.add((s, e))
    for rx in (LOOSE_RX, ALONE_RX):
        for m in rx.finditer(text): take(*m.span())
    for m in WORD_RX.finditer(BASE64_RX.sub(lambda b: " " * len(b.group()), text)):
        if len(m.group()) < 10 or re.fullmatch(r"[0-9a-fA-F]+", m.group()): continue
        runs = list(re.finditer(r"\d+", m.group()))
        if len(runs) == 1 and len(runs[0].group()) == 9: take(m.start() + runs[0].start(), m.start() + runs[0].end())
    return out

def id_spans(text):
    """Spans of ID-like numbers: the strict forms below plus the loose forms of loose_spans(). Nine digits as such, d8-d1, d3-d3-d3 or fully spaced are always reported.
    Any other grouping only with a valid check digit or an ID word within 40 characters before it, because
    lists of ordinary numbers look the same. Hexadecimal runs (hashes, UUIDs) are not IDs."""
    out = {m.span() for m in ID_RX.finditer(text)} | loose_spans(text)
    for m in ODD_RX.finditer(text):
        d = "".join(c for c in m.group() if c.isdigit())
        if (ID_CONTEXT.search(text[max(0, m.start() - 40):m.start()]) or
                (check_digit_ok(d) and len(re.findall(SEP, m.group())) <= 2 and len(set(d)) > 2
                 and not re.match(r"\d{4}-\d{2}-\d{2}", m.group()))):
            out.add(m.span())
    return out

def clean(text): return INVISIBLE.sub("", re.sub(r"(?<!\\)\\[nrt]", " ", text))

def count_ids(text, rel=""):
    t = clean(text); n = 0
    for s, e in id_spans(t):
        if not any(rel.startswith(a["file"]) and t[:s].endswith(a["before"]) for a in EXP["privacy_allowed"]): n += 1
    return n

def name_has_id(part):
    """File and folder names: any run of exactly nine digits (or a separated ID), except hexadecimal hash names."""
    stem = part.split(".")[0]
    if re.fullmatch(r"[0-9a-f]{32,}", stem): return False
    return bool(re.search(r"(?<!\d)\d{9}(?!\d)", part) or id_spans(clean(part.replace("_", " "))))

def decode(data):
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"): return data.decode("utf-16", "replace")
    if data[:4000].count(0) > len(data[:4000]) * 0.2:     # UTF-16 without BOM
        odd = data[1:4000:2].count(0) >= data[0:4000:2].count(0)
        return data.decode("utf-16-le" if odd else "utf-16-be", "replace")
    return data.decode("utf-8", "replace")

def pdf_strings(doc, skip_cover=False):
    """(label, text) of everything textual in a PDF: both glyph-order and raw page text, metadata, XMP, bookmarks,
    link targets, annotations, form fields and attachment names. Text inside raster images cannot be read."""
    yield "metadata", "\n".join(str(v) for v in (doc.metadata or {}).values())
    yield "XMP", doc.get_xml_metadata() or ""
    yield "bookmarks", "\n".join(t for _, t, _ in doc.get_toc())
    info = doc.xref_get_key(-1, "Info")
    if info[0] == "xref":
        x = int(info[1].split()[0])
        yield "document info keys", "\n".join(f"{k} {doc.xref_get_key(x, k)[1]}" for k in doc.xref_get_keys(x))
    for n in doc.embfile_names():
        yield "attachments", " ".join([n, *(str(doc.embfile_info(n).get(k)) for k in ("filename", "ufilename", "description")), decode(doc.embfile_get(n))])
    for i, p in enumerate(doc, 1):
        if i == 1 and skip_cover: continue
        yield f"p.{i} text", page_text_rtl(p, "\n")
        yield f"p.{i} text", p.get_text()
        yield f"p.{i} links", "\n".join(str(l.get("uri") or l.get("file") or "") for l in p.get_links())
        yield f"p.{i} annotations", "\n".join(" ".join(str(v) for v in a.info.values()) for a in p.annots())
        yield f"p.{i} form fields", "\n".join(f"{w.field_name} {w.field_value}" for w in (p.widgets() or []))

def hidden_content(doc):
    """Places where a PDF can hold text that no page shows. The approved book has none of them."""
    out = []
    if doc.embfile_count(): out.append("attachments")
    if doc.xref_get_key(doc.pdf_catalog(), "OCProperties")[0] != "null": out.append("optional-content layers")
    for x in range(1, doc.xref_length()):
        try: o = doc.xref_object(x, compressed=True)
        except Exception: out.append("unreadable object"); continue
        if re.search(r"/(?:JS|JavaScript)(?![A-Za-z])", o): out.append("JavaScript")
        if re.search(r"/(?:Launch|EmbeddedFile)(?![A-Za-z])", o): out.append("launch action or embedded file")
    return sorted(set(out))

NOT_TEXT = {".png", ".jpg", ".jpeg", ".gif", ".ttf", ".otf", ".luc", ".gz", ".zip", ".pyc"}
def scan_tree():
    """Walk the project without .git and .venv (compared as path parts, so this works on Windows and POSIX)."""
    hits, names, skipped = [], [], 0
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", ".venv", "__pycache__")]
        rel_base = Path(base).relative_to(ROOT)
        names += [f"{rel_base.as_posix()}/(name withheld)" for x in dirs + files if name_has_id(x)]
        for f in files:
            fp = Path(base) / f; rel = (rel_base / f).as_posix()
            if fp.suffix.lower() in NOT_TEXT: skipped += 1; continue
            # In the submission edition the IDs belong in main.tex and in the submission/build PDFs only.
            if EDITION == "submission" and (rel == "book/main.tex" or fp.suffix == ".pdf" and rel.split("/")[0] in ("submission", "build", "backups")): continue
            try:
                if fp.suffix.lower() == ".pdf":
                    with pymupdf.open(fp) as d:
                        n = sum(count_ids(t) for _, t in pdf_strings(d))
                else: n = count_ids(decode(fp.read_bytes()), rel)
            except Exception as e: hits.append(f"{rel} (unreadable: {type(e).__name__})"); continue
            if n: hits.append(f"{rel} ({n})")
    return hits, names, skipped

# ---------------------------------- checks ----------------------------------
def check_typeset(doc, pdf, log, out):
    pages = Path(out) / "pages"
    for old in pages.glob("page-*.png"): old.unlink()          # never leave pages of an earlier PDF
    try:
        r = subprocess.run([sys.executable, str(ROOT / "tools/check_pdf.py"), str(pdf), str(log) if log else "--no-log", str(pages)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
    finally:
        # Privacy: the rendered cover shows the student IDs; overwrite it with the masked render at once.
        mask_renders(doc, pdf, pages)
    lines = r.stdout.strip().splitlines()
    why = "; ".join(l.strip(" -") for l in lines[lines.index("FAIL:") + 1:][:12]) if "FAIL:" in lines else r.stderr.strip()[-300:]
    result("qa-typeset", "typeset.check-pdf", r.returncode == 0 and bool(lines), f"{pdf.name} + {log.name if log else 'no log'}", lines[0] if lines else "",
           f"exit {r.returncode}; {lines[0] if lines else ''}; reasons: {why}",
           "completed log of this PDF, 0 errors, 0 missing glyphs, no overfull >2pt, 0 undefined refs/cites, no text outside page, no faint text",
           "major", "template")
    if not log:
        add("qa-typeset", "n/a", "build log", "--no-log: no build log given, so errors, warnings, glyphs, boxes and references were NOT checked",
            "log-dependent checks need a real build log", name="typeset.log")
    result("qa-typeset", "typeset.pages", doc.page_count == EXP["pages"], "whole PDF", f"{doc.page_count} pages", f"{doc.page_count} pages",
           f"{EXP['pages']} pages", "blocker", "template")
    toc = {t: p for _, t, p in doc.get_toc()}
    diff = {t: (toc.get(t), p) for t, p in EXP["chapter_starts"].items() if toc.get(t) != p}
    result("qa-typeset", "typeset.toc", not diff, "TOC / chapter openings", f"all {len(EXP['chapter_starts'])} start pages match", f"mismatches: {diff}",
           "chapter start pages as approved", "major", "template")
    check_text(doc)

def mask_renders(doc, pdf, pages):
    cover = pages / "page-01.png"; ok, note = True, "cover render masked as expected"
    if cover.exists():
        want = "0" if EDITION == "public" else "2"
        m = subprocess.run([sys.executable, str(ROOT / "tools/screenshots.py"), str(pdf), "mask-cover", str(cover), "--expect-ids", want],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        n = max(len(id_spans(clean(t))) for t in (page_text_rtl(doc[0], "\n"), doc[0].get_text()))
        if m.returncode or n != int(want):
            ok, note = False, f"mask-cover exit {m.returncode}; {n} ID-like numbers on the cover, expected {want}; render deleted"
            cover.unlink()
    for i in range(2, doc.page_count + 1):
        f = pages / f"page-{i:02d}.png"
        if f.exists() and (count_ids(page_text_rtl(doc[i-1], "\n")) or count_ids(doc[i-1].get_text())):
            f.unlink(); ok, note = False, f"ID-like number on p.{i}; render deleted"
    result("qa-typeset", "typeset.cover-mask", ok, "rendered pages", note, note,
           "expected number of IDs masked on the cover render; none on other pages", "blocker", "content")

# ---------- text completeness ----------
def words(t): return Counter(re.findall(r"[א-ת]{2,}|[A-Za-z]{3,}|\d{2,}", t))

def source_words(tex):
    t = strip_comments(tex)
    t = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)|(?<!\\)\$.*?(?<!\\)\$", " ", t, flags=re.S)        # mathematics is set by other rules
    t = re.sub(r"\\(label|ref|cite|input|includegraphics)(\[[^]]*\])?\{[^}]*\}", " ", t)
    t = re.sub(r"\\begin\{tabular\}\{@\{\}\w+@\{\}\}|\{tab:[^}]*\}\{@\{\}\w+@\{\}\}", " ", t)
    t = re.sub(r"\\(begin|end)\{[^}]*\}(\[[^]]*\])?", " ", t)
    t = t.replace("\\fictional", " נתונים בדיוניים ").replace("\\educational", " דוגמה לימודית ")
    t = re.sub(r"\\(term|textbf|emph|en)\{", "", t)          # ב\term{דירוג} is printed as one word
    return words(re.sub(r"\\[a-zA-Z]+\*?", " ", t))

def check_text(doc):
    """Chapter sources vs. PDF text (bags of normalised words). Threshold: 0 missing words, because the approved
    PDF has 0 in every chapter; printed-only words (titles, box labels, figure labels) up to the approved count.
    Misses: word order, punctuation, single letters, formulas, and a deletion made in source and PDF together."""
    for f, (a, b) in EXP["chapter_pages"].items():
        src = ROOT / "book/chapters" / f
        s = source_words(read(src)) if src.exists() else Counter()
        p = words("\n".join(doc[i-1].get_text() for i in range(a, b + 1) if page_of(doc, i)))
        miss, extra = s - p, +Counter({w: k for w, k in (p - s).items() if not w.isdigit()})
        e, lim = sum(extra.values()), EXP["extra_words_max"][f]
        result("qa-typeset", "typeset.text-complete", bool(s) and not miss and e <= lim, f"{f} vs pp. {a}-{b}",
               f"{sum(s.values())} source words all printed; {e} printed-only words (max {lim})",
               f"{sum(s.values())} source words; {sum(miss.values())} not printed ({redact(list(miss)[:5])}); {e} printed-only words (max {lim})",
               "every word of the chapter source is printed on its pages, and nothing unexpected is", "blocker", "content")
    mt = ROOT / "book/main.tex"
    cover = Counter(w for t in re.findall(r"hebcolor\{\w+\}\{([^{}]*)\}", strip_comments(read(mt)) if mt.is_file() else "") for w in words(t).elements())
    miss = cover - words(doc[0].get_text())
    result("qa-typeset", "typeset.cover-text", bool(cover) and not miss, "p.1", f"{sum(cover.values())} title and subtitle words of main.tex printed",
           f"{sum(cover.values())} title and subtitle words in main.tex, not on the cover: {list(miss)}", "title, subtitle and description on the cover", "blocker", "content")
    want = {t: p for t, p in EXP["chapter_starts"].items()}
    toc = norm(page_text_rtl(page_of(doc, 3))) if page_of(doc, 3) else ""
    raw = norm(doc[2].get_text()) if page_of(doc, 3) else ""
    bad = [t for t in want if norm(t) not in toc and norm(t) not in raw]
    result("qa-typeset", "typeset.toc-page", not bad, "p.3", "all chapter titles printed in the contents", f"missing on p.3: {bad}",
           "the printed contents page lists every chapter", "major", "content")

def check_public_cover(doc):
    """Public edition (Prompt 27): the cover must show no student ID, no date and no ID/date labels.
    Checked on both the glyph-order RTL reading and PyMuPDF's raw text, so a reversed digit run is caught too."""
    pub = EXP["cover_public"]; p = doc[0]
    texts = (clean(norm(page_text_rtl(p))), clean(p.get_text()), re.sub(rf"(?<=\d){SEP}(?=\d)", "", clean(p.get_text())))
    bad_l = [l for l in pub["forbidden_labels"] if any(norm(l) in t or l in t for t in texts)]
    bad_p = sorted({m for pat in pub["forbidden_patterns"] for t in texts for m in re.findall(pat, t)})
    result("qa-bidi", "bidi.public-cover", not (bad_l or bad_p), "page 1 (cover, public edition)",
        "no ID or submission-date label and no digit on the cover",
        # values are counted, never printed: a failing report must not itself leak an ID or the date
        f"forbidden labels: {bad_l}; forbidden numbers/dates: {len(bad_p)} found (values withheld)",
        "public cover without student IDs and without the submission date", "blocker", "content")

def check_feedback_label(doc, phrase):
    # Match Figure 6.1 independently of its label. Body text on the next page
    # repeats the phrase and must never satisfy this check (D3-01).
    matched_pages = []
    diagram_pages = []
    for page in doc:
        text = page.get_text()
        if "6.1" not in text or "דוגמה לימודית" not in text:
            continue
        blocks = diagram_blocks(page)
        if len(blocks) != EXP["diagram_blocks"]:
            continue
        diagram_pages.append(page.number + 1)
        top = min(r.y0 for r in blocks)
        bottom = max(r.y1 for r in blocks)
        right = max(r.x1 for r in blocks)
        for line, chars in page_lines(page):
            dx, dy = line["dir"]
            x0, y0, _, y1 = line["bbox"]
            if dy > -0.99 or x0 < right or y0 < top or y1 > bottom:
                continue
            # Read Hebrew against the line direction, using the glyph origins
            # projected onto the rotated baseline. Spaces in TeX may be synthetic.
            ordered = sorted(chars, key=lambda c: dx*c["origin"][0] + dy*c["origin"][1], reverse=True)
            if norm("".join(c["c"] for c in ordered)) == norm(phrase):
                matched_pages.append(page.number + 1)
    ok = len(diagram_pages) == 1 and matched_pages == diagram_pages
    add("qa-bidi", "pass" if ok else "fail", f"Fig. 6.1 on pages {diagram_pages}",
        f"Rotated '{phrase}' in RTL glyph order beside the blocks: {matched_pages}",
        "one occurrence of the rotated feedback label beside the eight diagram blocks", "major", "template", "bidi.feedback-label")


def diagram_blocks(page):
    return [d["rect"] for d in page.get_drawings()
            if 80 < d["rect"].width < 100 and 35 < d["rect"].height < 50]

def block_labels(page):
    """Fig. 6.1 labels in reading order: both rows as drawn (1-4 right to left, then 5-8 left to right)."""
    rects = diagram_blocks(page)
    if not rects: return []
    mid = (min(r.y0 for r in rects) + max(r.y1 for r in rects)) / 2
    order = sorted([r for r in rects if r.y1 < mid], key=lambda r: -r.x0) + sorted([r for r in rects if r.y1 >= mid], key=lambda r: r.x0)
    lines = page_lines(page); out = []
    for r in order:
        ls = sorted([(l["bbox"][1], read_rtl(cs)) for l, cs in lines if inside(l["bbox"], r, 0) and any(HEB.match(c["c"]) for c in cs)])
        out.append(norm("".join(t for _, t in ls)))
    return out

def check_bidi(doc):
    full = {i+1: norm(page_text_rtl(p)) for i, p in enumerate(doc)}
    def region(key):
        r = EXP["regions"][key]; p = page_of(doc, r["page"])
        # 12 pt of slack: cells and labels of the element itself, not the prose around it
        return (r["page"], norm(page_text_rtl(p, rect=[r["rect"][0]-12, r["rect"][1]-6, r["rect"][2]+12, r["rect"][3]+6])) if p else "")
    scope = {"graph": [region("fig-2.1")], "table": [region("table-4.1")], "cover": [(1, full.get(1, ""))]}
    for group in ("diagram", "graph", "table", "mixed", "cover"):
        phrases = EXP["cover_public"]["phrases"] if (group == "cover" and EDITION == "public") else EXP["phrases"][group]
        p14 = page_of(doc, EXP["figures"]["6.1"]["page"])
        labels = block_labels(p14) if group == "diagram" and p14 else []
        for k, ph in enumerate(phrases):
            if group == "diagram" and ph == "לולאת משוב":
                check_feedback_label(doc, ph)
                continue
            if group == "diagram":
                hit = [p14.number + 1] if len(labels) == EXP["diagram_blocks"] and labels[k] == norm(ph) else []
                where, what = f"Fig. 6.1 p.{EXP['figures']['6.1']['page']} block {k+1}", f"'{ph}' is the label of block {k+1}"
            else:
                hit = [pg for pg, t in scope.get(group, full.items()) if norm(ph) in t]
                where = f"pages {hit}" if hit else {"graph": "Fig. 2.1 p.7", "table": "Table 4.1 p.11", "cover": "p.1"}.get(group, "whole PDF")
                what = f"'{ph}' read in RTL order from glyph positions"
            add("qa-bidi", "pass" if hit else "fail", where, what + ("" if hit else ": NOT found in reading order"),
                f"'{ph}' readable right-to-left with Latin/digit runs intact, in its own place", "major", "template", f"bidi.phrase.{group}")
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
    result("qa-bidi", "bidi.citations", not bad, "all pages", "every multi-number citation ascending", f"unsorted: {bad}",
        "citations like [4, 7] ascending", "minor", "template")

def check_table(doc):
    # Table 4.1: first column (היבט) rightmost; X-columns flush right (constant right edges)
    reg = EXP["regions"]["table-4.1"]; tp = page_of(doc, reg["page"])
    lines = [(l, cs) for l, cs in page_lines(tp) if inside(l["bbox"], reg["rect"], 3)] if tp else []
    def x_of(ls, word):
        return next((l["bbox"] for l, cs in ls if norm(line_text(cs)) == norm(word)), None)
    heads = ["היבט", "סינון שיתופי", "מבוסס תוכן", "שילוב גישות (כולל הקשר)"]
    xs = [x_of(lines, h) for h in heads]
    if not all(xs):       # header cells of one row may be joined to one line: read the row, right to left
        top = min((l["bbox"][1] for l, _ in lines), default=0)
        row = [c for l, cs in lines if abs(l["bbox"][1] - top) < 4 for c in cs]
        ok = norm(read_rtl(row)) == norm("".join(heads)) if row else False
    else: ok = all(a[0] > b[2] for a, b in zip(xs, xs[1:]))
    result("qa-table", "table.4.1-columns", ok, f"p.{reg['page']} Table 4.1", f"header row right to left: {heads}",
        "header row of Table 4.1 not found inside the table, or not in order",
        "first column (היבט) on the right, last column on the left (RTL)", "major", "template")
    edges = {}
    for l, cs in lines:
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
    result("qa-table", "table.4.1-edges", ok, f"p.{reg['page']} Table 4.1", f"4 dominant cell right edges (pt:count) {top}", f"4 dominant cell right edges (pt:count) {top}",
        "each column's cells share one right edge (flush right, ragged left)", "minor", "template")
    # Chapter 3 data table: header order and every number in its column
    reg = EXP["regions"]["table-p9"]; p9 = page_of(doc, reg["page"])
    lines = [(l, cs) for l, cs in page_lines(p9) if inside(l["bbox"], reg["rect"], 3)] if p9 else []
    xs = [x_of(lines, h) for h in EXP["p9_header"]]
    ok = all(xs) and all(a[0] > b[2] for a, b in zip(xs, xs[1:]))
    result("qa-table", "table.p9-columns", ok, f"p.{reg['page']} data table", f"header x: {[x and round(x[0]) for x in xs]}",
        f"header cells found (None = missing): {[x and round(x[0]) for x in xs]}", "header right to left: " + ", ".join(EXP["p9_header"]), "major", "template")
    nums = sorted(((round(l["bbox"][1] / 4), -l["bbox"][0], t) for l, cs in lines for t in [norm(line_text(cs))] if t.isdigit()))
    rows = {}
    for y, _, t in nums: rows.setdefault(y, []).append(t)
    got = [rows[y] for y in sorted(rows)]
    result("qa-table", "table.p9-values", got == EXP["p9_rows"], f"p.{reg['page']} data table", f"rows {got}", f"rows {got}",
        f"rows (right to left) {EXP['p9_rows']}", "major", "template")

def caption_text(doc, fig):
    """Text of a figure's own caption: the line that starts with the caption label, and the next 25 pt."""
    out = []
    for p in doc:
        for l, cs in page_lines(p):
            y = l["bbox"][1]
            if norm(line_text(cs)) == norm(f"איור {fig}") and max(c["size"] for c in l["spans"]) < 10.5:
                out.append((p.number + 1, norm(page_text_rtl(p, rect=[0, y - 3, p.rect.width, y + 27]))))
    return out

def check_img(doc):
    n61 = EXP["figures"]["6.1"]["page"]; pg = page_of(doc, n61)
    rects = diagram_blocks(pg) if pg else []
    labels = block_labels(pg) if pg else []
    good = sum(bool(t) for t in labels)
    cs = [c for _, cc in page_lines(pg) for c in cc if HEB.match(c["c"])] if pg else []
    crossing = sum(1 for R in rects for c in cs if R.x0 < (c["bbox"][0] + c["bbox"][2]) / 2 < R.x1
                   and R.y0 < (c["bbox"][1] + c["bbox"][3]) / 2 < R.y1 and not inside(c["bbox"], R, 0.1))
    result("qa-img", "img.blocks", len(rects) == EXP["diagram_blocks"] == good and not crossing, f"p.{n61} Fig. 6.1",
        f"{len(rects)} blocks, {good} with Hebrew label fully inside", f"{len(rects)} blocks, {good} with Hebrew label fully inside, {crossing} characters crossing a border",
        f"{EXP['diagram_blocks']} blocks, every label inside its block", "major", "template")
    for fig, f in EXP["figures"].items():
        caps = caption_text(doc, fig)
        ok = [p for p, t in caps] == [f["page"]] and norm(f["tag"]) in caps[0][1]
        result("qa-img", f"img.caption-{fig}", ok, f"Fig. {fig} p.{f['page']}", "caption + tag found", f"caption lines on pages {[p for p, _ in caps]}; caption or tag missing",
            f"Fig. {fig} captioned and tagged '{f['tag']}' on p.{f['page']}", "major", "content")
    need = EXP["regions"]["fig-2.1"]
    ok = page_of(doc, need["page"]) is not None
    draw = sum(1 for d in doc[need["page"]-1].get_drawings() if pymupdf.Rect(d["rect"]).intersects(pymupdf.Rect(need["rect"]))) if ok else 0
    result("qa-img", "img.fig-2.1-drawing", ok and draw >= 100, f"p.{need['page']} Fig. 2.1", f"{draw} vector drawings inside the figure", f"{draw} vector drawings inside the figure",
        "the vector graph (at least 100 drawing objects) is on its page", "major", "template")
    # Visible-ink check of the side margins (vector drawing rects are unreliable: matplotlib hatch
    # pattern definitions report off-page coordinates but draw nothing there; calibrated 2026-11-18).
    # Round 2: full page height; compared with the expected page colour, not with a pixel of the page itself;
    # the outermost 3 pt are ignored (the background rectangle is antialiased against the page edge).
    x0, x1 = EXP["text_block_x"]; over = []; bg = EXP["page_bg"]
    for i, p in enumerate(doc, 1):
        if i == 1: continue
        pix = p.get_pixmap(dpi=36, colorspace=pymupdf.csRGB, alpha=False); sx = pix.width / p.rect.width; S, st = pix.samples, pix.stride
        xs = list(range(2, int((x0 - 4) * sx))) + list(range(int((x1 + 4) * sx) + 1, pix.width - 2))
        if any(abs(S[y*st+3*x] - bg[0]) + abs(S[y*st+3*x+1] - bg[1]) + abs(S[y*st+3*x+2] - bg[2]) > 12
               for y in range(2, pix.height - 2) for x in xs): over.append(i)
    result("qa-img", "img.margins", not over and doc.page_count > 1, "pp. 2-20 side margins", "no visible ink in the side margins", f"visible ink in the side margins on pages {over}",
        "no figures, boxes or text in the side margins", "minor", "template")

CODE_RX = re.compile(r"\\begin\s*\{\s*(lstlisting|[a-z]*verbatim\*?|Verbatim|minted|alltt|pythonbox|codebox)\s*\}|"
                     r"\\(lstinline|lstinputlisting|inputminted|mintinline|verb|VerbatimInput|verbatiminput)(?![A-Za-z])")
def check_code(doc):
    hits = Counter(f.name for f in chapters() for _ in CODE_RX.finditer(strip_comments(read(f))))
    if not chapters():
        add("qa-code", "fail", "book/chapters", "no chapter sources found, so nothing could be inspected", "chapter sources inspected", "major", "packaging", "code.boxes"); return
    if hits:
        add("qa-code", "fail", "book/chapters", f"code found in {dict(hits)}, but no working code-box check exists",
            "code boxes are checked for background and overflow before the book uses them", "major", "skill", "code.boxes"); return
    add("qa-code", "n/a", "whole book", f"{len(chapters())} chapter sources inspected (comments ignored): the book contains no code boxes (pythonbox/listings)",
        "code boxes, if any, checked for background and overflow", name="code.boxes")

def check_footer(doc):
    tot = EXP["pages"]; bad = []; dots = []; hid = []
    for i in range(2, tot + 1):
        p = page_of(doc, i)
        if p is None: bad.append((i, "page missing")); dots.append(None); hid.append(i); continue
        foot = sorted((round(l["bbox"][0]), "".join(c["c"] for c in sorted(cs, key=lambda c: c["origin"][0]))) for l, cs in page_lines(p) if l["bbox"][1] > 760)
        if not foot or foot[0][1] != str(tot) or foot[-1][1] != str(i): bad.append((i, foot))
        d = [x["rect"] for x in p.get_drawings() if x["rect"].y0 > 760 and x["rect"].width < 8 and x.get("fill") and x["fill"][0] > 0.9 and x["fill"][1] < 0.3]
        dots.append(round(d[0].x0) if d else None)
        n, h = hidden(doc, i - 1, [0, 760, p.rect.width, p.rect.height])
        dot_ok = False
        if d:
            pix = p.get_pixmap(dpi=144, clip=d[0], colorspace=pymupdf.csRGB, alpha=False)
            q = pix.pixel(pix.width // 2, pix.height // 2); dot_ok = q[0] > 200 and q[1] < 110 and 80 < q[2] < 180
        if not n or h or not dot_ok: hid.append(i)
    if doc.page_count != tot: bad.append(("pages", doc.page_count))
    mono = all(a is not None and b is not None and b < a for a, b in zip(dots, dots[1:]))
    result("qa-footer", "footer.numbers", not bad, "pp. 2-20 footers", f"left = total ({tot}), right = page number on every page", f"wrong: {bad}",
        "left number = total pages, right number = current page (LTR digits)", "major", "template")
    p19 = any(i == 19 for i, _ in bad) or 19 in hid
    result("qa-footer", "footer.p19", not p19, "p.19 footer (regression, Prompt 18)", "page 19 footer correct and visible", "page 19 footer wrong, hidden or missing",
        "p.19: '20' left, '19' right, bar not mirrored", "blocker", "template")
    result("qa-footer", "footer.dot", mono and len(dots) == tot - 1, "pp. 2-20 progress dot", f"pink dot x per page: {dots}", f"pink dot x per page: {dots}",
        "dot moves strictly right-to-left as pages advance", "minor", "template")
    result("qa-footer", "footer.visible", not hid, "pp. 2-20 footers", "numbers and pink dot visible in every render", f"footer text or dot not visible on pages {hid}",
        "footer visible in the rendered page", "major", "template")

def check_bib(doc, log):
    # Locate the real chapter heading: a line that is exactly "מקורות" set at heading size (>= 16 pt).
    # This excludes the 8.7 pt running header, the 10.5 pt TOC line and body text (round-01 D1-02).
    want = EXP["chapter_starts"]["מקורות"]
    heads = [p.number + 1 for p in doc for b in p.get_text("dict")["blocks"] for l in b.get("lines", [])
             if "".join(s["text"] for s in l["spans"]).strip() == "מקורות" and max(s["size"] for s in l["spans"]) >= 16]
    labels, xs = set(), []
    for p in list(doc)[max(0, doc.page_count-3):]:
        for b in p.get_text("blocks"):
            m = re.match(r"\s*\[(\d+)\]", b[4])
            if m: labels.add(int(m.group(1))); xs.append(b[0])
    ok = heads == [want] and labels == set(range(1, EXP["bib_entries"] + 1)) and xs and min(xs) >= EXP["text_block_x"][0] - 0.5
    result("qa-typeset", "typeset.bibliography", ok, "bibliography",
        *[f"heading 'מקורות' on p.{heads if len(heads) != 1 else heads[0]}; {len(labels)} entries; min x0={xs and round(min(xs),1)}"] * 2,
        f"heading 'מקורות' on p.{want} only, {EXP['bib_entries']} numbered entries, all inside the margins", "major", "template")
    pdf_words = words(" ".join(p.get_text() for p in doc if p.number + 1 >= want).lower())
    titles = re.findall(r"(?<![A-Za-z])title\s*=\s*\{(.*?)\}\s*,?\s*$", bib_source(), re.M)
    miss = sum(1 for t in titles if any(w not in pdf_words for w in words(re.sub(r"\\&|[{}]", "", t).lower())))
    result("qa-typeset", "typeset.bib-titles", len(titles) == EXP["bib_entries"] and not miss, "bibliography", f"{len(titles)} titles of references.bib printed",
        f"{len(titles)} titles in references.bib, {miss} not fully printed", "the words of every reference title are printed", "major", "content")
    if log is None:
        add("qa-typeset", "n/a", "biber log", "--no-log: the biber log was NOT checked", "0 biber warnings (all 18 sources resolve)", name="typeset.biber"); return
    blg = log.with_suffix(".blg") if log.suffix == ".log" else None
    if blg is None or not blg.is_file():
        add("qa-typeset", "fail", log.name, "the log is not named *.log" if blg is None else f"{blg.name} not found next to the log",
            "a biber log next to the LaTeX log", "major", "build", "typeset.biber"); return
    t = blg.read_text(encoding="utf-8", errors="replace"); w = len(re.findall(r"WARN|ERROR|FATAL", t)); real = "This is Biber" in t and "INFO - Output to " in t
    result("qa-typeset", "typeset.biber", real and not w, blg.name, f"{w} biber warnings/errors", f"{w} biber warnings/errors; completed biber log: {real}",
        "0 biber warnings (all 18 sources resolve)", "major", "build")

def bib_source():
    f = ROOT / "book/references.bib"
    return strip_comments(read(f)) if f.exists() else ""

LAYOUT_RX = re.compile(
    r"\\begin\s*\{\s*(?:minipage|wrapfigure|wraptable|tikzpicture|picture|adjustbox|multicols|center|flushleft|flushright|landscape|tcolorbox|"
    r"tabularx|longtable|(?:figure|table)\*?)\s*\}(?:\s*\[[^]]*\])?"
    r"|\\includegraphics\s*(?:\[[^]]*\])?\s*\{[^}]*\}"
    r"|\\(?:vspace|hspace|vskip|hskip|kern|newpage|clearpage|cleardoublepage|pagebreak|nopagebreak|linebreak|enlargethispage|resizebox|scalebox|"
    r"rotatebox|raisebox|parbox|setlength|addtolength|renewcommand|newcommand|providecommand|renewenvironment|newenvironment|def|let|fontsize|selectfont|"
    r"setstretch|linespread|newgeometry|looseness|hfill|vfill|bigskip|medskip|smallskip|textcolor|color|definecolor|tiny|scriptsize|footnotesize|small|large|"
    r"Large|LARGE|huge|Huge|usepackage|tikz|rule|vbox|hbox|makebox|fbox|mbox|phantom|FloatBarrier)(?![A-Za-z])\*?"
    r"|\\\\\s*\[[-\d.]")
def iron_law():
    bad = []; used = []
    for f in chapters():
        left = Counter({a["code"]: a["max"] for a in EXP["iron_law_allowed"] if a["file"] == f.name})
        for m in LAYOUT_RX.finditer(strip_comments(read(f))):
            code = re.sub(r"\s+", "", m.group())
            if left[code] > 0: left[code] -= 1; used.append(f"{f.name}: {code}")
            else: bad.append(f"{f.name}: {code[:60]}")
    return bad, used

def check_infra(doc, pdf):
    missing = [f for f in EXP["required_files"] if not (ROOT / f).is_file()]
    result("qa-infra", "infra.required-files", not missing, "project root", f"all {len(EXP['required_files'])} required files present", f"missing: {missing}",
        "A2 §3.3 files present (main.tex, chapters, .cls, PRD, PLAN, TODO, README)", "major", "packaging")
    thin = [f for f in EXP["chapter_pages"] if not (ROOT / "book/chapters" / f).is_file()
            or sum(source_words(read(ROOT / "book/chapters" / f)).values()) < 100
            or (not f.startswith("00") and "\\chapter{" not in strip_comments(read(ROOT / "book/chapters" / f)))]
    extra = [f.name for f in chapters() if f.name not in EXP["chapter_pages"]]
    result("qa-infra", "infra.chapters", not thin and not extra, "book/chapters/", f"{len(EXP['chapter_pages'])} chapter files, none empty", f"missing or empty: {thin}; unexpected: {extra}",
        "chapters 00-08 exist, hold text and a \\chapter command", "major", "packaging")
    mt = ROOT / "book/main.tex"; main = strip_comments(read(mt)) if mt.is_file() else ""
    notin = [f for f in EXP["chapter_pages"] if f"chapters/{f[:-4]}" not in main]
    cls_bad = [] if re.search(r"\\documentclass(\[[^]]*\])?\{behind-the-playlist\}", main) else ["documentclass"]
    result("qa-infra", "infra.main", not notin and not cls_bad, "book/main.tex", "loads the class and all nine chapter files", f"not loaded: {notin + cls_bad}",
        "main.tex uses the book class and inputs every chapter", "major", "packaging")
    cf = ROOT / "book/behind-the-playlist.cls"; cls = strip_comments(read(cf)) if cf.is_file() else ""
    undef = [c for c in EXP["class_interface"] if not re.search(r"\\(?:new|renew|provide|DeclareRobust)(?:command|Command|environment|tcolorbox)\s*\{\\?" + c + r"\}", cls)
             and not re.search(r"\\DeclareRobustCommand\{\\" + c + r"\}", cls)]
    if "\\LoadClass" not in cls: undef.append("\\LoadClass")
    result("qa-infra", "infra.class-interface", not undef, "behind-the-playlist.cls", f"all {len(EXP['class_interface'])} interface commands defined", f"not defined: {undef}",
        "the class defines every command of the writer interface", "major", "template")
    bib = bib_source(); keys = re.findall(r"^\s*@(?!comment|string|preamble)\w+\s*\{\s*([^,\s]+)", bib, re.M | re.I)
    cites = {k.strip() for f in chapters() for m in re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]*)\}", strip_comments(read(f))) for k in m.split(",")}
    result("qa-infra", "infra.bib", len(set(keys)) == len(keys) == EXP["bib_entries"] and cites == set(keys), "book/references.bib",
        f"{len(keys)} entries, all cited keys resolve", f"{len(keys)} entries (expected {EXP['bib_entries']}); cited but missing: {sorted(cites - set(keys))}; never cited: {sorted(set(keys) - cites)}",
        f"{EXP['bib_entries']} unique entries, the same set as the \\cite keys", "major", "packaging")
    bad, used = iron_law()
    result("qa-infra", "infra.iron-law", not bad and bool(chapters()), "book/chapters/",
        f"no layout code in chapter files; explicitly allowed and flagged for the users: {used}", f"layout code: {sorted(set(bad))}",
        "layout lives in the class (A2 iron law)", "major", "template")
    rm = ROOT / "README.md"; s = read(rm) if rm.is_file() else ""
    prose = re.sub(r"```.*?```|`[^`]*`", "", s, flags=re.S)
    defs = {k.lower(): u for k, u in re.findall(r"^\s{0,3}\[([^\]]+)\]:\s*<?(\S+?)>?\s*$", prose, re.M)}
    links = re.findall(r"\]\(\s*<?([^)\s>]+)", prose) + re.findall(r"<(?:img|a)\b[^>]*?\b(?:src|href)\s*=\s*[\"']([^\"']+)", prose, re.I) + list(defs.values())
    undef = [r or t for t, r in re.findall(r"\[([^\]\[]+)\]\[([^\]\[]*)\]", prose) if (r or t).lower() not in defs]
    local = [unquote(l.split("#")[0]) for l in links if not re.match(r"[a-z][a-z0-9+.-]*:", l, re.I) and l.split("#")[0]]
    broken = [l for l in local if not (ROOT / l).exists()] + [f"[{u}] undefined" for u in undef]
    result("qa-infra", "infra.readme", len(s.strip()) >= 1000 and bool(local) and not broken, "README.md", f"{len(local)} relative links and images resolve",
        f"{len(s.strip())} characters, {len(local)} relative links and images, broken: {broken}", "README has content and every link, image and reference link resolves", "minor", "packaging")
    hits, names, skipped = scan_tree()
    result("qa-infra", "infra.privacy-files", not hits, "all text files and PDFs of the project",
        f"no ID-like number ({skipped} image/font/archive files cannot be read; text inside raster images is never checked)",
        f"ID-like numbers (file, count; values withheld): {hits}", "no student IDs outside main.tex and the PDF (public edition: nowhere)", "blocker", "packaging")
    result("qa-infra", "infra.privacy-names", not names, "file and folder names", "no ID-like number in a name", f"ID-like names in: {names}",
        "no student ID in a file name", "blocker", "packaging")
    hits = Counter()
    for label, t in pdf_strings(doc, skip_cover=EDITION == "submission"):
        if count_ids(t): hits[label] += 1
    if name_has_id(Path(pdf).name): hits["file name"] += 1
    result("qa-infra", "infra.privacy-pdf", not hits, "checked PDF: text of all pages, metadata, links, annotations",
        "no ID-like number (raster images cannot be read; see visual.raster-images)", f"ID-like numbers in: {sorted(hits)} (values withheld)",
        "no student ID in the PDF (submission edition: cover only)", "blocker", "packaging")
    hc = hidden_content(doc)
    result("qa-infra", "infra.pdf-hidden-content", not hc, "checked PDF", "no attachments, layers, JavaScript or launch actions", f"found: {hc}",
        "nothing in the PDF that no page shows", "blocker", "packaging")
    sub = ROOT / "submission/behind-the-playlist.pdf"
    zp = ROOT / "submission/project-source.zip"
    if EDITION == "public":
        add("qa-infra", "n/a", "submission/", "public edition: the submission PDF and ZIP are not part of the public copy",
            "ZIP freshness is checked on the submission edition only", name="infra.zip")
    elif not zp.exists() or not sub.exists():
        add("qa-infra", "fail", "submission/", "submission PDF or source ZIP missing", "submission PDF and project-source.zip present", "major", "packaging", "infra.zip")
    else:
        with zipfile.ZipFile(zp) as z:
            zn = z.namelist()
            zpdf = next((n for n in zn if n.endswith("submission/behind-the-playlist.pdf")), None)
            same = zpdf and hashlib.sha256(z.read(zpdf)).hexdigest() == hashlib.sha256(sub.read_bytes()).hexdigest()
            has_cls = any(n.endswith(".cls") for n in zn)
        add("qa-infra", "pass" if (same and has_cls) else "fail", "submission/project-source.zip",
            f"ZIP PDF matches submission PDF: {bool(same)}; ZIP contains .cls: {has_cls}",
            "the source package contains the approved PDF and the current sources", "major", "packaging", "infra.zip")

def check_cls_version(log):
    cf = ROOT / "book/behind-the-playlist.cls"; cls = read(cf) if cf.is_file() else ""
    m = re.search(r"^\s*\\ProvidesClass\{behind-the-playlist\}\[(\S+) (v[\d.]+)", cls, re.M)
    cl = re.search(r"%\s+(v[\d.]+)\s+(\d{4}-\d{2}-\d{2})", cls)
    ok = m and cl and (m.group(2), m.group(1).replace("/", "-")) == cl.groups()
    result("qa-cls-version", "cls.source", bool(ok), "behind-the-playlist.cls", *[f"\\ProvidesClass {m and m.group(2)}; CHANGELOG {cl and cl.group(1)}"] * 2,
        "class version and date identical in \\ProvidesClass and CHANGELOG", "major", "template")
    if log is None:
        add("qa-cls-version", "n/a", "build log", "--no-log: the version in the build log was NOT checked", "class version in the build log", name="cls.log"); return
    lg = re.search(r"Document Class: behind-the-playlist (\S+) (v[\d.]+)", log.read_text(encoding="utf-8", errors="replace"))
    result("qa-cls-version", "cls.log", bool(m and lg and m.groups() == lg.groups()), "build log", *[f"\\ProvidesClass {m and m.group(2)}; log {lg and lg.group(2)}"] * 2,
        "class version identical in \\ProvidesClass, CHANGELOG and the build log", "major", "template")

CHECKS = {"typeset": lambda d, a: (check_typeset(d, a.pdf, a.log, a.out), check_bib(d, a.log)),
          "bidi": lambda d, a: check_bidi(d), "table": lambda d, a: check_table(d), "img": lambda d, a: check_img(d),
          "code": lambda d, a: check_code(d), "footer": lambda d, a: check_footer(d),
          "infra": lambda d, a: check_infra(d, a.pdf), "cls-version": lambda d, a: check_cls_version(a.log),
          "visual": lambda d, a: check_visual(d)}

def run_family(name, doc, a):
    """One family; a crash becomes a fail, and fewer findings than declared is a fail too."""
    start = len(findings)
    try: CHECKS[name](doc, a)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        add(f"qa-{name}", "fail", f"qa_lib.py:{tb.lineno}", f"check crashed: {type(e).__name__}: {str(e)[:200]}", "the check runs to its end", "blocker", "skill", f"{name}.crash")
    n = len(findings) - start
    if n < EXP["min_findings"][name]:
        add(f"qa-{name}", "fail", "harness", f"only {n} findings, at least {EXP['min_findings'][name]} declared", "no check is skipped silently", "blocker", "skill", f"{name}.min-findings")

def main(argv=None):
    global EDITION
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"): s.reconfigure(encoding="utf-8", errors="replace")
    argv = sys.argv[1:] if argv is None else argv
    remove_stale(argv)
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument("--pdf", type=Path, required=True); ap.add_argument("--log", type=Path)
    ap.add_argument("--no-log", action="store_true", help="no build log available: log checks are reported n/a")
    ap.add_argument("--checks", default="all"); ap.add_argument("--out", type=Path)
    ap.add_argument("--edition", choices=("submission", "public"), default=EDITION)
    ap.add_argument("--write-visual-baseline", action="store_true"); ap.add_argument("--users-approval", default="")
    a = ap.parse_args(argv); EDITION = a.edition
    if not a.pdf.is_file(): ap.error("--pdf: file not found")
    if a.write_visual_baseline:
        if not a.users_approval.strip(): ap.error("--write-visual-baseline needs --users-approval \"<who, when, why>\"")
        write_baseline(a.pdf, a.users_approval); print("visual baseline written"); return 0
    if a.out is None: ap.error("--out is required")
    if bool(a.log) == a.no_log: ap.error("give exactly one of --log <latex log> and --no-log")
    if a.log and not a.log.is_file(): ap.error("--log: file not found (use --no-log when there is no build log)")
    names = list(CHECKS) if a.checks == "all" else [c.strip() for c in a.checks.split(",")]
    unknown = [c for c in names if c not in CHECKS]
    if unknown: ap.error(f"unknown checks {unknown}; known: {', '.join(CHECKS)}")
    try: doc = pymupdf.open(a.pdf)
    except Exception as e: ap.error(f"--pdf cannot be opened: {type(e).__name__}")
    if doc.needs_pass: ap.error("--pdf is encrypted and cannot be checked")
    if not doc.is_pdf or doc.page_count == 0: ap.error("--pdf is not a PDF with pages")
    a.out.mkdir(parents=True, exist_ok=True)
    for name in names: run_family(name, doc, a)
    full = a.pdf.resolve()
    shown = full.relative_to(ROOT).as_posix() if full.is_relative_to(ROOT) else f"(outside the project) {a.pdf.name}"
    (a.out / "findings.json").write_text(json.dumps(dict(pdf=redact(shown), sha256=hashlib.sha256(a.pdf.read_bytes()).hexdigest(),
        edition=EDITION, log=redact(a.log.name) if a.log else None, findings=findings), ensure_ascii=False, indent=1), encoding="utf-8")
    n = {s: sum(f["status"] == s for f in findings) for s in ("pass", "fail", "n/a")}
    print(redact(f"QA {a.checks} [{EDITION} edition]: {n['pass']} pass, {n['fail']} fail, {n['n/a']} n/a -> {a.out/'findings.json'}"))
    return 1 if n["fail"] else 0

if __name__ == "__main__":
    try: code = main()
    except SystemExit: raise
    except Exception as e:
        print(redact(f"qa_lib crashed: {type(e).__name__}: {e}"), file=sys.stderr); code = 2
    sys.exit(code)
