"""Prepare the PUBLIC (GitHub) edition of the project (Boss tool, Prompt 26). Does not publish anything.

Usage: python3 tools/make_public.py
Output: public-release/behind-the-playlist/  (a self-contained folder, ready for `git init` after approval)

Differences from the submission (Moodle) edition:
  - book/main.tex: the student-ID column and the "תאריך הגשה" row are removed from the cover;
  - pdf/behind-the-playlist.pdf: the public PDF, built with LuaLaTeX + Biber from that main.tex;
  - README.md: the book link points to pdf/behind-the-playlist.pdf; cover screenshot refreshed from the public PDF;
  - submission/, backups/, build/ and the lecturer PDFs are NOT copied;
  - (Prompt 27) the submission date is replaced by "[תאריך ההגשה הושמט]" in every text file of the copy
    (prompt log, agent transcripts, QA reports, expectations), and the date row is masked in the old QA cover renders;
    work dates (e.g. 2026-11-18) are kept. tools/qa/expectations.json is marked "edition": "public".
The submission files in submission/ are never touched.
"""
import re, shutil, subprocess, sys, tempfile, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public-release" / "behind-the-playlist"
PY = str(ROOT / ".venv/bin/python")
TEX = "/Library/TeX/texbin"

# the same curated list as tools/package.py, minus submission/
INCLUDE = [
    "README.md", "PRD.md", "PLAN.md", "TODO.md", "SKILLS.md", "Makefile", "requirements.txt",
    "book/main.tex", "book/behind-the-playlist.cls", "book/*.sty", "book/references.bib",
    "book/chapters/*.tex", "book/figures/pipeline.tex", "book/figures/noa_week.pdf",
    "book/fonts/*/*", "book/fonts/SOURCES.md", "book/fonts/SHA256SUMS",
    "figures/noa_week.py", "figures/data/noa_week.csv", "tools/*.py", "tools/qa/*",
    ".claude/agents/*.md", ".claude/skills/*/SKILL.md", "prompts/*.md",
    "docs/prompts.md", "docs/outline.md", "docs/assignment-compliance.md",
    "docs/screenshots/*.png", "docs/screenshots/pagemap.json",
    "docs/agents/*.md", "docs/agents/tasks/*.md", "docs/agents/transcripts/*",
    "docs/qa/**/*", "docs/incidents/*.md",
    "tests/*/*.tex", "tests/*/RESULTS.md",
]
EXCLUDE = re.compile(r"(^|/)(\.venv|build|backups|submission|public-release|__pycache__|\.DS_Store)(/|$)|\.(aux|log|fls|fdb_latexmk|xdv|bbl|bcf|blg|run\.xml|toc|out|zip)$")

def sub1(s, a, b):
    assert s.count(a) == 1, (a[:60], s.count(a)); return s.replace(a, b)

# The submission date is read from the private main.tex, so this script never contains it literally.
_m = re.search(r"\\newcommand\{\\bookdate\}\{[^}]*?(\d{1,2}\.\d{1,2}\.\d{4})", (ROOT / "book/main.tex").read_text(encoding="utf-8"))
if not _m: sys.exit("run from the private project: book/main.tex must define \\bookdate")
DATE = _m.group(1); OMIT = "[תאריך ההגשה הושמט]"
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".tex", ".py", ".txt", ".csv", ".bib", ".cls", ".sty"}

if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)
files = sorted({p for pat in INCLUDE for p in ROOT.glob(pat) if p.is_file()})
files = [p for p in files if not EXCLUDE.search(p.relative_to(ROOT).as_posix())]
for p in files:
    dst = OUT / p.relative_to(ROOT); dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, dst)

# --- 0. submission date -> placeholder in every text file (main.tex is handled in step 1: its row is removed)
replaced = {}
for p in OUT.rglob("*"):
    if p.is_file() and p.suffix in TEXT_SUFFIXES and p != OUT / "book/main.tex":
        t = p.read_text(encoding="utf-8")
        n = t.count(DATE) + t.count(DATE[::-1])
        if n:
            p.write_text(t.replace(DATE, OMIT).replace(DATE[::-1], OMIT), encoding="utf-8"); replaced[p.relative_to(OUT).as_posix()] = n
ex = OUT / "tools/qa/expectations.json"; t = ex.read_text(encoding="utf-8")
assert t.startswith("{\n"); ex.write_text('{\n  "edition": "public",\n' + t[2:], encoding="utf-8"); json.loads(ex.read_text(encoding="utf-8"))

# --- 0b. old QA cover renders (110 dpi, IDs already masked): hide the submission-date row as well
from PIL import Image, ImageDraw
import pymupdf
sub_cover = pymupdf.open(ROOT / "submission/behind-the-playlist.pdf")[0]
row = next(pymupdf.Rect(l["bbox"]) for b in sub_cover.get_text("dict")["blocks"] for l in b.get("lines", [])
           if DATE.replace(".", "") in "".join(sp["text"] for sp in l["spans"]).replace(".", "")
           or DATE[::-1].replace(".", "") in "".join(sp["text"] for sp in l["spans"]).replace(".", ""))
masked = []
for img in sorted(OUT.glob("docs/qa/**/pages/page-01.png")):
    im = Image.open(img).convert("RGB"); k = im.width / sub_cover.rect.width
    box = [int((row.x0 - 3) * k), int((row.y0 - 1.5) * k), int((row.x1 + 3) * k) + 1, int((row.y1 + 1.5) * k) + 1]
    d = ImageDraw.Draw(im); d.rectangle(box, fill=(107, 115, 128))
    d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), "date hidden", fill=(255, 255, 255), anchor="mm")
    im.save(img); masked.append((img.relative_to(OUT).as_posix(), box))

# --- 1. public main.tex: no student IDs, no submission-date row
mt = OUT / "book/main.tex"; s = mt.read_text(encoding="utf-8")
s = re.sub(r"\\newcommand\{\\studentid\}.*\n", "", s)
s = re.sub(r"\\newcommand\{\\bookdate\}.*\n", "", s)
s = sub1(s, "\\begin{tabular}{@{}H@{\\quad}H@{\\qquad}H@{}} % H = flush right in RTL tables (class v1.0)",
         "\\begin{tabular}{@{}H@{\\quad}H@{}} % H = flush right in RTL tables (class v1.0). PUBLIC EDITION: no student IDs, no submission date")
s = re.sub(r"(\\headfont מחבר/ת: & [^&\n]+?) & ת״ז \\studentid\{\d{9}\}", r"\1", s)
s = re.sub(r"  \\headfont קורס: & \\bookcourse &\\\\", r"  \\headfont קורס: & \\bookcourse\\\\", s)
s = re.sub(r"  \\headfont מרצה: & \\booklecturer &\\\\", r"  \\headfont מרצה: & \\booklecturer", s)
s = re.sub(r"\n  \\headfont תאריך הגשה: & \\bookdate &", "", s)
s = s.replace("% Cover details: provided by the user (Prompt 12, 2026-11-14).",
              "% PUBLIC EDITION (Prompt 26): student IDs and the submission date are removed.\n% Cover details: provided by the user (Prompt 12, 2026-11-14).")
assert not re.search(r"\d{9}", s) and "תאריך הגשה" not in s and "studentid" not in s.split("\\begin{document}")[1]
mt.write_text(s, encoding="utf-8")

# --- 2. build the public PDF (LuaLaTeX + Biber via latexmk) in a temporary output folder
tmp = Path(tempfile.mkdtemp(prefix="public-build-"))
r = subprocess.run(["latexmk", "-lualatex", "-interaction=nonstopmode", "-halt-on-error", f"-outdir={tmp}", "main.tex"],
                   cwd=OUT / "book", env={"PATH": f"{TEX}:/usr/bin:/bin"}, capture_output=True, text=True)
if r.returncode: sys.exit("public build failed:\n" + r.stdout[-1500:])
(OUT / "pdf").mkdir(exist_ok=True)
shutil.copy2(tmp / "main.pdf", OUT / "pdf/behind-the-playlist.pdf")
chk = subprocess.run([PY, str(ROOT / "tools/check_pdf.py"), str(OUT / "pdf/behind-the-playlist.pdf"), str(tmp / "main.log"), str(tmp / "pages")],
                     capture_output=True, text=True)
print("public PDF checks:", chk.stdout.strip().splitlines()[0], "|", chk.stdout.strip().splitlines()[-1])

# --- 3. README screenshots from the public PDF (cover has no IDs: --expect-ids 0)
subprocess.run([PY, str(ROOT / "tools/screenshots.py"), str(OUT / "pdf/behind-the-playlist.pdf"), "readme",
                str(OUT / "docs/screenshots"), str(OUT / "docs/screenshots/pagemap.json"), "--expect-ids", "0"],
               check=True, capture_output=True, text=True)

# --- 4. README: link to the public PDF; describe the public edition
rd = OUT / "README.md"; s = rd.read_text(encoding="utf-8")
s = sub1(s, "📄 **קובץ ההגשה:** [submission/behind-the-playlist.pdf](submission/behind-the-playlist.pdf)",
         "📄 **הספר (PDF):** [pdf/behind-the-playlist.pdf](pdf/behind-the-playlist.pdf)\n\n"
         "> **מהדורה ציבורית.** בעותק הזה הוסרו מעמוד השער מספרי תעודת הזהות ושורת „תאריך הגשה”. "
         "שאר הספר זהה לגרסה שהוגשה. קובצי ההגשה עצמם אינם חלק מהמאגר הציבורי.")
s = s.replace("בצילום השער **מספרי תעודת הזהות מוסתרים** („ID hidden\"), והם מופיעים רק בקובץ ההגשה.",
              "צילום השער לקוח מהמהדורה הציבורית, שבה אין מספרי תעודת זהות ואין תאריך הגשה.")
s = s.replace("**שער** (עמ' 1, מספרי ת״ז מוסתרים)", "**שער** (עמ' 1, מהדורה ציבורית)")
s = s.replace("- `submission/behind-the-playlist.pdf` (הגרסה המאושרת)", "- `pdf/behind-the-playlist.pdf` (המהדורה הציבורית שבמאגר)")
s = s.replace("submission/      behind-the-playlist.pdf", "pdf/             behind-the-playlist.pdf (public edition: no student IDs, no submission date)")
s = s.replace("- `docs/screenshots/*.png` (מספרי ת״ז מוסתרים)", "- `docs/screenshots/*.png`")
rd.write_text(s, encoding="utf-8")

# --- 5. .gitignore for the public repository
(OUT / ".gitignore").write_text("build/\n.venv/\n__pycache__/\n.DS_Store\nsubmission/\nbackups/\n*.aux\n*.log\n*.bbl\n*.bcf\n*.blg\n*.fls\n*.fdb_latexmk\n*.run.xml\n*.toc\n*.out\n*.xdv\n", encoding="utf-8")

# --- 6. verification
ids = re.findall(r"\\studentid\{(\d{9})\}", (ROOT / "book/main.tex").read_text(encoding="utf-8"))
import pymupdf
leaks = []
for p in OUT.rglob("*"):
    if not p.is_file(): continue
    data = p.read_bytes()
    if any(i.encode() in data for i in ids): leaks.append(str(p.relative_to(OUT)))
    if p.suffix == ".pdf":
        txt = "".join(pg.get_text() for pg in pymupdf.open(p))
        if any(i in txt for i in ids): leaks.append(str(p.relative_to(OUT)) + " (PDF text)")
cover = pymupdf.open(OUT / "pdf/behind-the-playlist.pdf")[0].get_text()
links = [l for l in re.findall(r"\]\(([^)#]+)\)", s) if not l.startswith("http")]
broken = [l for l in links if not (OUT / l).exists()]
print(f"files: {sum(1 for p in OUT.rglob('*') if p.is_file())}")
print("student IDs anywhere in the public copy (bytes + PDF text):", leaks or "none")
print("cover: 'תאריך הגשה' present:", "הגשה" in cover, "| submission date present:", DATE in cover or DATE[::-1] in cover,
      "| 9-digit numbers on cover:", re.findall(r"\d{9}", cover) or "none")
print(f"README: {len(links)} links, broken: {broken or 'none'}; book link -> pdf/behind-the-playlist.pdf: {'pdf/behind-the-playlist.pdf' in links}")
print("public PDF:", pymupdf.open(OUT / "pdf/behind-the-playlist.pdf").page_count, "pages, sha256",
      hashlib.sha256((OUT / "pdf/behind-the-playlist.pdf").read_bytes()).hexdigest()[:16])
date_left = []
for p in OUT.rglob("*"):
    if not p.is_file(): continue
    b = p.read_bytes()
    if DATE.encode() in b or DATE[::-1].encode() in b: date_left.append(p.relative_to(OUT).as_posix())
    if p.suffix == ".pdf" and any(DATE in pg.get_text() or DATE[::-1] in pg.get_text() for pg in pymupdf.open(p)):
        date_left.append(p.relative_to(OUT).as_posix() + " (PDF text)")
print("date replaced by placeholder in:", replaced)
print("old cover renders with the date row masked:", masked)
print("submission date anywhere in the public copy (bytes + PDF text):", date_left or "none")
qa = subprocess.run([PY, str(OUT / "tools/qa/qa_lib.py"), "--pdf", str(OUT / "pdf/behind-the-playlist.pdf"), "--log", str(tmp / "main.log"),
                     "--checks", "all", "--out", str(tmp / "qa")], capture_output=True, text=True, cwd=OUT)
print(qa.stdout.strip() or qa.stderr[-800:])
print("QA failures:", [(f["id"], f["evidence"][:90]) for f in json.loads((tmp / "qa/findings.json").read_text())["findings"] if f["status"] == "fail"] or "none")
print("build folder (log, QA findings):", tmp)
