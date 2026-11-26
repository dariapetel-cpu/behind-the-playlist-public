---
name: qa-infra
description: "QA Skill: project-structure checks (A2 §3.3 required files, all chapters, bibliography, class interface, no layout code in chapter files, README links, student-ID scan of files, names and PDFs, source ZIP freshness)."
---

# qa-infra

Checks the A2 §3.3 required files; chapters 00-08 present, not empty and loaded by `main.tex`; 18 bibliography entries equal to the cited keys; the class still defines the writer interface; README not empty, with every link, image and reference link resolving; and, in the submission edition only, that `submission/project-source.zip` holds the approved PDF and the class.

**Iron law:** a deny-list of layout commands on the chapter sources, comments ignored. Two existing pieces of code in chapter 2 (`\begin{figure}[t]` and its `\includegraphics[width=\textwidth]`) are allowed once each in `expectations.json` (`iron_law_allowed`) and shown in the evidence, flagged for the users.

**Privacy:** every nine-digit number is an ID by pattern, whatever `main.tex` declares: also spaced, hyphenated, with invisible characters, in UTF-16, in file names, and in PDF text, metadata, links and annotations. Dots, slashes, commas, line breaks, `&nbsp;`, neighbouring numbers, letters glued to the number and other unusual groupings count only with a valid Israeli check digit or an ID word before them; hashes and base64 data are not IDs. A plain nine-digit number always fails, also a harmless one. `infra.pdf-hidden-content` fails on attachments, layers, JavaScript and launch actions. The short `privacy_allowed` list is bound to file and context. `.git` and `.venv` are excluded by path part. Values are never printed. **Text inside raster images cannot be read.**

**Run** (from the project root; read-only, never edits project files; Windows: `.venv/Scripts/python.exe`):

```bash
.venv/bin/python tools/qa/qa_lib.py --pdf <pdf> (--log <latex log> | --no-log) --checks infra --out <report dir>
```

- Default inputs (public edition): `--pdf pdf/behind-the-playlist.pdf --no-log`. Submission edition only (these files are not in the public repository): `--edition submission --pdf submission/behind-the-playlist.pdf --log build/lualatex/main.log`.
- `--no-log` reports log-dependent checks as `n/a` with the reason. Never read `n/a` as a pass.
- Exit code: 0 = no fail, 1 = at least one fail, 2 = usage error or crash (no `findings.json` is left). A check that crashes, or a family with fewer findings than `min_findings`, is a fail.
- Writes `<report dir>/findings.json`. Each finding has `id, check, name, status (pass|fail|n/a), where (page or file), evidence, expected, severity, kind`. Read the evidence of passes too.
- `kind` tells the Fixer who may act: `template` / `skill` = Fixer; `content` / `packaging` / `build` = flag for the users.
- Expected values live in `tools/qa/expectations.json`. Change them only with the users' approval.
- Every check has a negative test in `tests/test_qa_mutations.py` (`python -m unittest discover -s tests`).
