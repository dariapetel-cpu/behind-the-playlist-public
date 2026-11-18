# PLAN: closing the gaps to Assignment 02 (מטלה 02 – הכנת קובץ PDF באמצעות LaTeX)

*Created 2026-11-18 (Prompt 14); **corrected the same day (Prompt 15)** with the lecturer's Moodle announcement (compliance §A′: agents as Skills, separate Detector/Fixer, automated red-team review, incident reports, a dedicated prompts/Skills folder, README screenshots of agents at work) and the user's decisions (compliance §F). Based on `docs/assignment-compliance.md`. Atomic tasks are in [`TODO.md`](TODO.md); requirements and their sources are in the compliance file.*

## Fixed constraints

These hold for every phase.

- **Preserve** (F-1) the approved topic, the content of the abstract and Ch. 1–8, the citations, the author details, and the charcoal `#121212` / green `#1ED760` / pink `#FF2E88` / page `#F2F2F2` design. Keep ≥ 15 pages (target: stay at 20). Keep `book/main.tex`; chapters keep opening on new pages.
- **Iron law (A2 p. 3):** from now on, every rendering or layout fix goes into the **CLS** or a **Skill**, never into chapter text. Content corrections (facts, wording) remain Writer or coordinator edits and are logged as such.
- **History is append-only.** The 5 genuine agent runs (R1, W1, W2, V1, V2) and the coordinator's fixes keep their current descriptions. New work gets new, dated log rows. Nothing is relabelled.
- **Privacy:** the student IDs stay only in `book/main.tex` and the PDF. They are masked in screenshots and redacted in logs, and any archived transcript is redacted defensively.
- **Software installs, agent runs and publishing** need an explicit go-ahead from the user. Each phase below names the decisions it depends on.

## Status (2026-11-18, after Prompt 21)

- **The book PDF is approved:** the 20-page LuaLaTeX build with class v1.0 and Pairing A fonts is now `submission/behind-the-playlist.pdf` (SHA-256 `43608a86…`). The previous XeLaTeX PDF is kept locally as `backups/behind-the-playlist-v1.1-xelatex-2026-11-14.pdf`.
- **QA round 1 done and approved** (`docs/qa/round-01/`). The submission PDF is now class v1.1 + the label offset (SHA-256 `ed844348…`, 20 pp), and the source ZIP was rebuilt and verified. Open: D3-01 (the qa-bidi check of the rotated label).
- **Next:** P6 (README screenshots of agents at work, remaining incident reports) and the ZIP refresh (P8).
- **Pending, by separate user approval:** GitHub publication and the Moodle submission.

## Phases

| Phase | Goal | Main outputs | Done when | Depends on |
|---|---|---|---|---|
| **P0 Audit** *(done)* | Know the gaps | `docs/assignment-compliance.md`, `PLAN.md`, `TODO.md` | User has reviewed the decisions | — |
| **P1 Toolchain** *(done 2026-11-18, except MiKTeX R-1)* | A LuaLaTeX-capable, reproducible toolchain | `biblatex-ieee` (+ any LuaLaTeX Hebrew packages found missing) installed; distribution decision recorded | `lualatex` compiles a one-page Hebrew test with TikZ, IEEE citation and RTL table; glyph checks pass | D1, D2, D6 |
| **P2 CLS** *(done 2026-11-18: class v1.0)* | `book/behind-the-playlist.cls` replaces `style.sty` | Class with `\ProvidesClass{behind-the-playlist}[YYYY/MM/DD vX.Y]`, changelog, command list (the existing WRITER INTERFACE), palette, boxes, footer, IEEE bibliography setup; `main.tex` uses `\documentclass{behind-the-playlist}` | The book builds with LuaLaTeX; page map unchanged or consciously updated; all automated + glyph checks pass; colour audit passes | P1 |
| **P3 Iron-law cleanup** *(done 2026-11-18)* | No layout hacks left in chapter files | The 5 in-chapter layout edits become CLS commands (side-by-side lab layout, comparison-table column type, figure placement, heading-safe English) | `grep "Boss edit"` in `book/chapters/` is empty of layout code; the PDF is unchanged visually | P2 |
| **P4 Skills** *(done 2026-11-18: 11 project Skills, see SKILLS.md)* | **Agents built as Skills (MA-1)** in a **dedicated folder (MA-5)**, plus the QA Skills of A2 §4 step 5, §5 and table 2 | **Role Skills:** `detector` (finds and reports, never edits), `fixer` (edits the CLS/Skills only), `red-team` (adversarial review), plus the existing roles as Skills (researcher, writer, reviewer) for future use. **QA Skills:** `qa-super`, `qa-bidi`, `qa-table`, `qa-img`, `qa-code`, `qa-typeset`, `qa-infra`, `qa-cls-version` (reusing `tools/check_pdf.py` and the glyph checks). `prompts/` with proven prompts. `SKILLS.md` | Each Skill runs on the current PDF and writes a findings report under `docs/qa/` | P2 (qa-cls-version needs the class) |
| **P5 QA loop** *(round 1 done 2026-11-18: D1 → F1 → D2, candidate acceptable, not promoted)* | **Automated red-team review (MA-3)** with **separate Detector and Fixer (MA-2)**: detect → fix → compile → recheck | Loop script that runs the `detector` (qa-super + `red-team`) → the `fixer` → rebuild → the `detector` again, with a log of every iteration; real runs only | A recorded final round with **0 blocking findings** (L04 §11.8 "done") | P4, D5 |
| **P6 Records** | Evidence the lecturer can follow | **`docs/incidents/` (MA-4):** one report per genuine self-found bug (symptom, detection, root cause, fix location, prevention/Skill update, source line); `prompts/` library of proven prompts (extracted from `docs/agents/tasks/`, labelled with origin); README sections for the Skills, the LuaLaTeX build and the QA loop, **with real screenshots of the agents/Skills at work (MA-6)** | Every README link resolves; no ID leaks (package scan) | P4–P5 |
| **P7 Reproducibility** *(partly: bundled fonts + LuaLaTeX Makefile done; deterministic PDF and clean-copy hash test pending)* | "Run lualatex again → identical PDF" (A2 p. 5) | Bundled **open-licence Hebrew+English fonts (F-2)**, chosen after a bold/number/punctuation glyph test, `SOURCE_DATE_EPOCH` + fixed PDF ID, build script with the A2 sequence `lualatex → biber → lualatex → lualatex`, MiKTeX/Windows notes | A clean extracted copy rebuilds to the **same SHA-256** as `submission/behind-the-playlist.pdf` | P2, D1, D2 |
| **P8 Submission** *(book PDF approved 2026-11-18; ZIP refresh, GitHub and Moodle pending)* | A2 §6 package | **Private GitHub repository shared with both students and the lecturer (F-3)**, created at this stage; lecturer PDFs excluded; final PDF; refreshed `submission/project-source.zip`; human sign-off (G §19.5) | Repository contains .tex/.cls/.bib, PRD/PLAN/TODO/README, the PDF and the Skills with their files; the user signs off | All, D3, D4 |

## Decisions

### Decided (Prompt 15)

| # | Decision |
|---|---|
| D1 | **TeX Live** (current installation) for the local LuaLaTeX work. **MiKTeX compatibility is unverified** until it is tested or the lecturer confirms TeX Live is acceptable (open risk R-1) |
| D2 | **Open-licence fonts** with Hebrew + English, adopted only after a bold/number/punctuation glyph test |
| D3 | **Private GitHub repository** shared with both students and the lecturer, created at the submission stage. The IDs stay in `book/main.tex`/PDF inside that private repository |
| D4 | **Topic approval: unconfirmed** (open risk R-2) |
| D5 | Required by the Moodle announcement: **separate Detector and Fixer, built as Skills**, with an automated red-team review. Their runs are logged as new, real runs |
| D7 | **Chapters keep opening on new pages.** Unbreakable short boxes are still allowed via the CLS |
| D8 | **Lecturer PDFs stay local**; they are excluded from the repository and the ZIP |
| D9 | **Keep `book/main.tex`** and state it in the README |

### Still open

| # | Item | Needed for |
|---|---|---|
| D6 | ~~Install `biblatex-ieee`~~: **done** by the user on 2026-11-18; the LuaLaTeX + IEEE smoke test passed (`tests/lualatex-smoke/RESULTS.md`) | — |
| R-1 | MiKTeX compatibility: unverified | P7/P8 |
| R-2 | Topic approval: unconfirmed; ask the lecturer before submission | P8 |
| R-3 | The original Moodle announcement text is not in the project; save it as `docs/moodle-announcement.md` (user) | Audit traceability |
