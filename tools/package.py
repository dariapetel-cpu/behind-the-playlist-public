"""Build submission/project-source.zip (Boss tool). Lecturer PDFs, backups/ and build/ are never packaged.

Usage: python3 tools/package.py
Packs the project under a top-level folder `behind-the-playlist/`, keeping the directory
structure so README's relative links resolve after extraction. Includes only an explicit
allow-list of sources, docs and evidence; excludes .venv, build/, caches, OS junk, LaTeX
aux files and the ZIP itself. Aborts if anything looks like a credential, or if a student
ID (read from book/main.tex) appears anywhere except main.tex and the PDF.
"""
import re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "submission" / "project-source.zip"
TOP = "behind-the-playlist"

INCLUDE = [
    "README.md", "PRD.md", "PLAN.md", "TODO.md", "SKILLS.md", "Makefile", "requirements.txt",
    "book/behind-the-playlist.cls", "book/*.sty", "book/fonts/*/*", "book/fonts/SOURCES.md", "book/fonts/SHA256SUMS",
    ".claude/skills/*/SKILL.md", "tools/qa/*", "prompts/*.md",
    "docs/qa/**/*", "docs/incidents/*.md", "docs/assignment-compliance.md",
    "tests/*/RESULTS.md", "tests/font-compare/*.tex",
    "book/main.tex", "book/style.sty", "book/references.bib",
    "book/chapters/*.tex", "book/figures/pipeline.tex", "book/figures/noa_week.pdf",
    "figures/noa_week.py", "figures/data/noa_week.csv",
    "tools/*.py",
    "docs/prompts.md", "docs/outline.md",
    "docs/screenshots/*.png", "docs/screenshots/pagemap.json",
    "docs/agents/*.md", "docs/agents/tasks/*.md", "docs/agents/transcripts/*",
    ".claude/agents/*.md",
    "tests/*/*.tex",
    "submission/behind-the-playlist.pdf",
]
EXCLUDE = re.compile(r"(^|/)(\.venv|build|__pycache__|\.DS_Store)(/|$)|\.(aux|log|fls|fdb_latexmk|xdv|bbl|bcf|blg|run\.xml|toc|out|zip)$")
# Patterns are assembled from pieces so this file does not match its own scan.
_parts = ["sk" + "-ant-", "MESSAGING" + "_TOKEN", "api[_-]?" + r"key\s*[:=]", "pass" + r"word\s*[:=]",
          "BEGIN (RSA|OPENSSH) " + "PRIVATE KEY"]
SECRET = re.compile("|".join(_parts).encode(), re.I)

files = sorted({p for pat in INCLUDE for p in ROOT.glob(pat) if p.is_file()})
files = [p for p in files if not EXCLUDE.search(p.relative_to(ROOT).as_posix())]

ids = re.findall(r"\\studentid\{(\d{9})\}", (ROOT / "book/main.tex").read_text(encoding="utf-8"))
problems = []
for p in files:
    rel = p.relative_to(ROOT).as_posix(); data = p.read_bytes()
    if SECRET.search(data): problems.append(f"possible credential in {rel}")
    if rel not in ("book/main.tex", "submission/behind-the-playlist.pdf"):
        if any(i.encode() in data for i in ids): problems.append(f"student ID in {rel}")
if problems:
    raise SystemExit("ABORT:\n  " + "\n  ".join(problems))

OUT.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in files:
        z.write(p, f"{TOP}/{p.relative_to(ROOT).as_posix()}")
print(f"{OUT.relative_to(ROOT)}: {len(files)} files, {OUT.stat().st_size/1024:.0f} KiB")
