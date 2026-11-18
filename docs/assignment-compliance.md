# Assignment compliance audit

*Boss (coordinator), 2026-11-18 (Prompt 14); **corrected 2026-11-18 (Prompt 15)** with the lecturer's Moodle announcement (section A′) and the user's project decisions (section F).*

*Original note (Prompt 14): This is a read-only audit: no book, build or tool changes were made while writing it. Only `PLAN.md`, `TODO.md`, this file and the prompt log were created or updated.*

## Sources and how they were read

The user referred to `assignment/`, but that folder does not exist. The three PDFs are in the project root (added 2026-11-18 12:10) and were left in place.

| Code | File | What it is | How it was read |
|---|---|---|---|
| **A2** | `BIU26-27-A-ex02-pdf-via-LaTex-print.pdf` (5 pp.) | **The assignment itself:** „מטלה 02 – הכנת קובץ PDF באמצעות LaTeX", Dr. Yoram Segal, November 2026 | The Hebrew text layer is broken (garbled glyph mapping), so **all 5 pages were rendered and read as images** (the p. 2 table at 220 dpi) |
| **L04** | `Multi-Agent-With-Claude.pdf` (4 pp.) | Lesson 4 summary, pp. 34–37 of 43: §11 cross-session communication, mesh check, team work | Text extraction (visual-order Hebrew, readable) |
| **MA** | **Moodle announcement** by the lecturer | **Explicit requirements added to the assignment.** The original text is **not in the project**. This audit uses the user's summary in Prompt 15 (`docs/prompts.md`); TODO P0 asks for the original to be saved as `docs/moodle-announcement.md` | User summary, quoted in A′ |
| **G** | `preparation-report-book.pdf` (97 pp.) | „From Problem to PDF: The Professional Preparatory Report", a guide for a **different course** (research seminar 5523001, a 40-page preparatory report) | Text extraction for the TOC and English prompts; **pages rendered** for §13.1, §13.4, §15.2, §15.5, §18.11 and §19.1–19.5 |

**Classification used below.** These classes come from the documents' own wording.

| Class | Meaning |
|---|---|
| **M** | Mandatory: stated in A2 as a requirement („חובה", „חייבת", „עליכם", the "Minimum" column, the folder and submission lists, the iron law) |
| **X** | Excellence: A2's „הערות למצטיינים / Excellence" column, or items A2 itself marks optional |
| **R** | Recommendation: A2's tips and "recommended" tables, plus guidance from L04 and G |
| **E** | Example: an illustration, not a requirement (e.g. G's sample folder tree, A2's sample compile commands) |

G is written for another course. Its contents count as **recommendations or examples for this assignment**, not as mandatory requirements, unless A2 repeats them.

## A. Requirements stated in the assignment (A2)

Status key:

| Mark | Meaning |
|---|---|
| ✅ | Met |
| ⚠️ | Partial |
| ❌ | Gap |
| ❓ | Needs a decision |

| ID | Requirement (A2 wording, condensed) | Source | Class | Evidence in the project | Status | Necessary action |
|---|---|---|---|---|---|---|
| A2-1 | Produce the PDF with **LuaLaTeX** + LaTeX | p. 1 §1 goal; p. 2 §3.1 "Compiler: LuaLaTeX"; p. 5 tips and sample commands | M | `Makefile` runs `latexmk -xelatex`; `book/style.sty` uses polyglossia + `bidi`, which is XeTeX-only; diagram RTL uses XeTeX's `\beginR…\endR` | ❌ | Port to LuaLaTeX (babel or polyglossia under LuaTeX); replace the TeX–XeT RTL wrappers in TikZ; re-verify all RTL checks (PRD §6 rules) |
| A2-2 | Compiler obtained via **MiKTeX** (https://miktex.org/download) | p. 2 §3.1 | M as written (distribution choice) | macOS with **BasicTeX / TeX Live 2026**; `lualatex` exists (LuaHBTeX 1.24); MiKTeX not installed | ❓ | Decision D1: install MiKTeX for macOS, or keep TeX Live and document the equivalence (same `lualatex`/`biber` commands) and confirm with the lecturer |
| A2-3 | Use a **custom `.cls` template** for reproducibility and uniformity („חובה להשתמש בקובץ cls. מותאם") | p. 1 §1; p. 2 §3.2; p. 2 table "Design: CLS"; p. 3 §3.3; p. 4 §6 | M | None. `book/main.tex` uses `\documentclass{book}` + `\usepackage{style}` (`book/style.sty` holds the whole design) | ❌ | Turn `style.sty` into `book/behind-the-playlist.cls`, with `\ProvidesClass` version, changelog and command list; keep the design and palette |
| A2-4 | Length: **25 pages (English) or 15 pages (Hebrew + mixed English)** | p. 2 table 1 "Length / Minimum" | M | 20 pages, Hebrew with English terms (`docs/screenshots/pagemap.json`) | ✅ | Keep ≥ 15 after the port |
| A2-5 | Content: images, graphs, summaries, texts, tables | p. 2 table 1 "Content / Minimum" | M | Fig. 2.1 graph p. 7; Fig. 6.1 diagram p. 14; Table 4.1 p. 11; data table p. 9; „בקצרה" summary boxes in every chapter | ✅ | — |
| A2-6 | Excellence: at least one image, one table, a math formula (optional) | p. 2 table 1 "Content / Excellence" | X | Graph + TikZ diagram; Table 4.1; cosine formula + worked example pp. 8–9. There is no photographic/raster image, but the vector figures are "images" in the usual sense | ✅ | — |
| A2-7 | Structure: chapters, TOC, **bibliography (IEEE)** | p. 2 table 1 "Structure / Minimum" | M | Chapters 1–8 ✅; TOC p. 3 ✅. The bibliography uses biblatex **`style=numeric`** (`book/style.sty`), not IEEE; `biblatex-ieee` is **not installed** (`tlmgr`: installed: No) | ⚠️ (IEEE ❌) | Switch to `style=ieee` (needs `biblatex-ieee`, a software install by decision D6); keep the Hebrew heading and the LTR English entries; check the 20-page budget |
| A2-8 | Excellence: professional **Footer + Banner** | p. 2 table 1 "Structure / Excellence" | X | Footer: "player" progress bar + page numbers ✅. Header: running title/chapter text only, no banner | ⚠️ | Optional: a slim header banner defined in the CLS |
| A2-9 | Design: CLS; excellence: **perfect BiDi**, Hebrew + English | p. 2 table 1 "Design" | M (CLS) / X (BiDi) | BiDi verified at glyph level (diagram 18/18, graph 6/6, table cells, cover) under XeLaTeX | CLS ❌ / BiDi ✅ (must be re-verified after A2-1) | See A2-3; re-run all glyph checks after the port |
| A2-10 | Topic: recommended practical topics (seminar, professional report, article, business plan, price proposal); **a topic that differs substantially must be approved in advance** | p. 2 box „המלצה על בחירת נושא" | R (choice) / M (approval if different) | The topic is a popular-science Hebrew book on music recommendation. No record of lecturer approval exists in the project | ❓ | Decision D4: confirm whether the lecturer approved the topic. If not, ask now |
| A2-11 | Folder must contain: `main.tex`; extra `.tex` files (e.g. one per chapter); `.cls`; `PRD.md`; `PLAN.md`; `TODO.md`; `README.md` in the project root | p. 3 §3.3 | M | `book/main.tex` ✅; `book/chapters/00–08.tex` ✅; `.cls` ❌; `PRD.md` ✅; `README.md` (root) ✅; **`PLAN.md` and `TODO.md` were missing until this audit** | ⚠️ | `PLAN.md` and `TODO.md` created now (root); add the `.cls` (A2-3). A2 does not say `main.tex` must be at the root (`book/main.tex`); keep unless decision D9 |
| A2-12 | Workflow, 8 steps: folder → PRD → PLAN → TODO (atomic tasks) → **use QA Skills, especially qa-super, qa-BiDi, qa-table, qa-code, qa-img** → precise prompts → **run, check, fix via a Skill or CLS update, never by hand** → save all work files | p. 3 §4 | M (the workflow is prescribed) | Steps 1, 2, 6 and 8 ✅. Steps 3–4: PLAN/TODO only now. **Step 5: no Skills exist** (`.claude/skills/` absent); QA was done by `tools/check_pdf.py`, the Boss and the Reviewer agent. Step 7: see A2-13 | ⚠️ / ❌ | Create the QA Skills and run them for real (TODO S-*); route all future fixes through the CLS or a Skill |
| A2-13 | **Iron law:** never fix a problem directly in the text; every fix goes through the Skill or the CLS | p. 3–4 red box „חוק ברזל: רפרודוקטיביות" | M | Historically, most layout fixes went into `book/style.sty` (template-level, the closest existing equivalent of the CLS). But **5 layout edits sit inside chapter files**: `03-anashim-kmotech.tex:43` (minipage layout), `04-shirim-kmo-ze.tex:34,37` (float placement, ragged column type), `06-shmone-tachanot.tex:20` (float placement), `08-play.tex:4` (`\enhead`). The review-01/02 **wording** fixes were also applied directly in the text by the coordinator | ❌ (history) | Going forward: move the 5 layout edits into CLS commands (a table column type, figure placement policy, heading-safe English, side-by-side layout). Record honestly that past wording fixes were direct coordinator edits; they are content corrections, not a reproducible rendering fix. Do not rewrite that history |
| A2-14 | **Mandatory Skills list:** attach to the repository the list of Skills used in the project, **including the Skill files** | p. 4 §5 | M | None. No Skill was created or used. The project's agents (`.claude/agents/`) and Python tools are not Skills | ❌ | Create real Skills (`.claude/skills/<name>/SKILL.md` + scripts), use them in the QA loop, record each actual run, and list them in README and a `SKILLS.md` |
| A2-15 | Recommended QA Skills: qa-super, qa-BiDi, qa-table, qa-code, qa-img, qa-typeset, qa-infra, qa-cls-version | p. 4 table 2 („סקילים מומלצים") | R (but §4 step 5 names five of them) | None | ❌ | Implement at least the five named in §4 step 5, plus qa-typeset, qa-infra and qa-cls-version. qa-code can honestly report "no code boxes in this book" |
| A2-16 | **Submission:** one **GitHub repository shared with group members**, containing at least: all sources (.tex .cls .bib); docs (PRD, PLAN, TODO, README); the final PDF; the Skills list | p. 4 §6 | M | Not a git repo; nothing on GitHub (by instruction: "do not publish"). `submission/project-source.zip` exists (no .cls, PLAN, TODO or Skills yet) | ❌ | Decision D3: create the repo (private? who has access?); the student IDs are in `book/main.tex` and the PDF |
| A2-17 | **Reproducibility:** the submission contains all work files so that running `lualatex` again gives an **identical PDF** | p. 5 box „חשוב!" | M | All sources + `Makefile` + pinned `requirements.txt`; the graph PDF is pre-built ✅. But the build uses **XeLaTeX** (A2-1) and **macOS-only system fonts** (New Peninim MT, Arial Hebrew, Times New Roman, Arial), so it will not reproduce on the lecturer's MiKTeX/Windows machine. Byte-identical output is not yet controlled (timestamps, IDs) | ❌ | LuaLaTeX build; bundle open-licence fonts (decision D2); `SOURCE_DATE_EPOCH` + fixed PDF ID; a clean-checkout rebuild test comparing hashes |
| A2-18 → MA-5 | Tips: start minimal; run lualatex often; use qa-super; when you find a bug, **update the matching Skill, not the file**; **save examples of prompts that worked** | p. 5 §7 | R | Prompts saved: `docs/prompts.md` (user prompts, verbatim) and `docs/agents/tasks/*.md` (agent prompts). There is no reusable prompt library | ⚠️ | Create `prompts/` with reusable, proven prompts (extracted from the genuine task files, labelled as such) |
| A2-19 | Sample compile sequence `lualatex → biber → lualatex → lualatex` | p. 5 box | E | `latexmk -xelatex` | ⚠️ | After the port, the Makefile/script should run exactly this sequence (or latexmk with `-lualatex`) |

## A′. Requirements from the Moodle announcement (MA), all mandatory

Source: the lecturer's Moodle announcement as summarised by the user (Prompt 15). Where an item overlaps a recommendation in G, the announcement **upgrades it to mandatory**. The affected rows in section B are marked "→ MA-n".

| ID | Requirement | Class | Evidence in the project | Status | Necessary action |
|---|---|---|---|---|---|
| MA-1 | **Agents built as Skills** | M | Agents exist only as `.claude/agents/*.md` subagent definitions (R1, W1, W2, V1, V2 ran this way). No Skill exists | ❌ | Build the project's agent roles as Skills (`.claude/skills/<name>/SKILL.md` + scripts), in the dedicated folder (MA-5). The existing agent definitions and their 5 historical runs stay as they are |
| MA-2 | **Separate Detector and Fixer roles** | M | The Reviewer detected; the **coordinator** fixed. **No Fixer role has ever existed** | ❌ | A Detector Skill (finds and reports, never edits) and a Fixer Skill (edits the CLS/Skills only, never chapter content), with separate logs |
| MA-3 | **Automated red-team review** | M | Two manual Reviewer passes (V1, V2), started by the coordinator; no red-team role; no automation | ❌ | A red-team Skill that attacks the PDF and sources (facts, BiDi, layout, privacy), run automatically inside the detect → fix → recheck loop until 0 blocking findings |
| MA-4 | **Incident analysis for bugs we find ourselves** | M | Genuine self-found bugs are recorded, but scattered across `docs/prompts.md`, PRD and the review responses; there are no incident reports | ⚠️ | `docs/incidents/` with one report per genuine self-found bug (symptom, detection, root cause, fix location, prevention or Skill update, source line). Only real incidents, with no invented ones |
| MA-5 | **A dedicated folder for prompts and Skills** | M | Prompts are spread over `docs/prompts.md` and `docs/agents/tasks/`; there are no Skills | ❌ | A dedicated folder (e.g. `prompts/` + `.claude/skills/`, or a single `agents/` folder holding `prompts/` and `skills/`, decided in P4), linked from the README |
| MA-6 | **README screenshots showing the agents at work** | M | The README has PDF screenshots only; agent evidence is links to transcripts and timelines | ❌ | Real screenshots of Skill/agent runs (terminal output or rendered reports from actual runs in P4/P5), with no staged or recreated images. Mask any IDs |

## B. Relevant guidance from L04 and the guide (G)

| ID | Guidance | Source | Class | Evidence | Status | Action |
|---|---|---|---|---|---|---|
| G-1 | Role table for a large document (source researcher, writer, illustrator, programmer, technical checker, architect, language editor, duplicate remover, quality checker). "You can run each role as a separate agent, **or** ask one model to switch between them" | G p. 75 §18.11 (table 18.2) | R | Researcher, Writer and Reviewer agents ran for real (5 runs, `docs/agents/log.md`). Illustration and quality checks were done by the coordinator | ✅ (meets the R) | Optional: keep |
| G-2 → MA-3 | **QA loop:** detect → fix → compile → recheck; "don't fix everything at once"; exit only when there are **no findings** | G p. 76 §19.1, fig. 19.1 | R (A2 §1 asks for "automatic quality control") | Detect: Reviewer V1 (36 issues) → fix: **coordinator** → recheck: Reviewer V2 (APPROVE WITH MINOR NOTES, 6 new minors) → fix: **coordinator** → **no third recheck**. The loop was manual, never automated, and is not closed | ⚠️ | Build an automated loop: Detector (qa-super running the QA Skills) → Fixer → compile → re-detect, until 0 blocking findings; log every iteration |
| G-3 → MA-2 | **Separate detection and fixing** (the "מזהים" and "מתקנים" steps) | G §19.1; G Prompt C2 "Use the template as the fixer"; L04 §11.8 red team / lead | R | **No Fixer agent ever existed.** All fixes were made by the coordinator (Boss) | ❌ | If approved (D5), add a `fixer` agent (edits the CLS/Skills only, never the content) and a Detector role (QA Skills plus the existing Reviewer). Past coordinator fixes stay described as coordinator fixes |
| G-4 | Nine check families: template version, cover, directions, tables, images, code, pagination, sources, file structure | G p. 77 §19.2 (table 19.1) | R | Covered piecemeal by `tools/check_pdf.py` (errors, glyphs, overfull, white text, out-of-page), the glyph-order checks and the Reviewer | ⚠️ | Map them onto the Skills: template version → qa-cls-version, BiDi → qa-BiDi, etc. |
| G-5 → MA-4 | **Real faults table (symptom → cause → fix)**, i.e. incident records | G p. 78 §19.3 (table 19.2) | E / R | Genuine incidents exist but are scattered across `docs/prompts.md`, PRD §6/§10/§11 and the review responses. Examples: the tlmgr mirror hang; reversed TikZ word order; `[heb]` + colour → white text; matplotlib double bidi; tag pill paragraph flipped to LTR; the commented-out `;` TikZ errors; black text in floats; the false PASS after an image-only check | ⚠️ | Compile `docs/incidents.md` from the existing records only, each entry citing its source line. Nothing invented |
| G-6 | Pagination rules: no heading stranded at the bottom; **no box/table/figure split across pages; no nearly empty pages** | G p. 78 §19.4 | R | The Ch. 1 fact box splits across pp. 4–5; p. 13 is ≈ 28 % full (end of Ch. 5). Both are known and accepted (review-02) | ⚠️ | Through the CLS: unbreakable short boxes; decide on chapter-start policy (D7). Keep 20 pages ≥ 15 |
| G-7 | Pre-submission sign-off list (0 errors, no reversed Hebrew, tables/images OK, every source checked, eyes on every page, **a human read the abstract**) | G p. 79 §19.5 | R | All are met except the human reading, which the agent cannot sign | ⚠️ | A user sign-off line in `TODO.md` |
| G-8 | "Don't trust the model saying 'I checked'": ask for page numbers and findings and open the pages yourselves | G p. 79 | R | The project already verifies with page numbers and glyph checks. One historical false PASS (Prompt 6) is recorded | ✅ | — |
| G-9 | Template should have a version number and changelog from day one, a command list, a README and an example | G p. 69 Prompt C0; §15.2 | R (and needed for qa-cls-version) | `style.sty` has `\ProvidesPackage[2026/11/14]` only | ❌ | Version, `CHANGELOG` section and command list in the CLS |
| G-10 | Don't give the model organisation data or **ID numbers** | G p. 75 red box | R | The user supplied the student IDs and asked for them in the PDF. They live only in `book/main.tex` and the PDF; they are masked or redacted elsewhere | ⚠️ (user-directed) | No action unless the user wants the IDs removed from the source too (D3) |
| G-11 | Sample folder: `report/main.tex, template.cls, references.bib, chapters/, figures/, work/` | G p. 41 §13.1 | E | Similar: `book/main.tex`, `book/references.bib`, `book/chapters/`, `book/figures/` | ✅ | The CLS goes in `book/` |
| G-12 | Team-lead principles: learn first; plan; red team on the plan; task board; questions last; "done" = all checks pass and **the last review round has no blocking finding** | L04 p. 36 §11.8 | R | The plan, outline and reviews exist. `TODO.md` is the task board as of now | ⚠️ | `TODO.md` + a final QA loop with a recorded zero-blocking round |

## C. The specific checks requested (Prompt 14)

| Check | Finding |
|---|---|
| Custom CLS | **Mandatory, missing.** The design lives in `book/style.sty` on the standard `book` class (A2-3) |
| LuaLaTeX | **Mandatory, not used.** The build is XeLaTeX; `lualatex` is installed and usable, but the RTL machinery must be ported (A2-1) |
| MiKTeX vs BasicTeX | A2 says "LuaLaTeX (via MiKTeX)". We have TeX Live 2026 BasicTeX on macOS. **Decided (Prompt 15):** test locally with TeX Live; **MiKTeX compatibility is unverified** until tested or the lecturer accepts TeX Live |
| IEEE bibliography | **Mandatory, not met.** `style=numeric`; `biblatex-ieee` is not installed (A2-7) |
| PLAN.md / TODO.md | **Mandatory; were missing.** Created by this audit (A2-11) |
| Prompt files | **Mandatory: a dedicated folder for prompts and Skills (MA-5).** A2 tip; G ch. 18. User prompts are logged verbatim and agent prompts are saved as task files; a reusable `prompts/` library is missing (A2-18) |
| Actual Skills | **Mandatory, and the agents themselves must be Skills (MA-1)**; none exist and none were used (A2-12, A2-14, A2-15). The agents and Python tools are not Skills, and must not be relabelled as such |
| Separate Detector and Fixer roles | **Mandatory per the Moodle announcement (MA-2)**. *Prompt 14 classed this as a recommendation; corrected in Prompt 15.* Historically the **Reviewer** detected and the **coordinator** fixed; there was never a Fixer agent (G-3) |
| Automated review-fix-recheck workflow | **Mandatory: automated red-team review (MA-3).** A2 §1 asks for QA Skills "for automatic quality control"; G §19.1 gives the loop. It was done manually, with only one recheck and no closing recheck after the last fixes (G-2) |
| Incident investigations | **Mandatory for bugs we find ourselves (MA-4)**; G §19.3 gives the format. Genuine incidents exist in the logs but are not consolidated (G-5) |
| Reproducible builds | **Mandatory** (A2 p. 5). Partly met: the Makefile works on this Mac only. Blocked by XeLaTeX, macOS system fonts and uncontrolled PDF metadata (A2-17) |
| README evidence of agents | **Mandatory: screenshots of the agents at work (MA-6)**, which are missing. Present and genuine today: the agents table, task files, transcripts, action timelines and both reviews, all linked (README §הסוכנים). It does not yet mention Skills (none exist) |

## D. Integrity of the historical record

- **Genuine agent runs, and only these:** R1 Researcher, W1 Writer, W2 Writer, V1 Reviewer, V2 Reviewer (`docs/agents/log.md`, `docs/agents/transcripts/`).
- **All fixes after V1 and V2** were made by the **coordinator (Boss)**, as `review-01-response.md` and `review-02-response.md` state. They must stay described that way. Future Fixer-agent work, if approved, gets new log rows with new dates.
- **No Skill has been run so far.** Skills created later will be recorded from their first real run onward.

## E. Mandatory gaps (summary)

1. Custom **`.cls`** (A2-3, A2-9, A2-11, A2-16)
2. **LuaLaTeX** build (A2-1, A2-17)
3. **IEEE** bibliography (A2-7)
4. **QA Skills**: created, actually used, and listed with their files (A2-12, A2-14)
5. Fix-through-CLS/Skill discipline (**iron law**) for the remaining in-text layout edits and all future fixes (A2-13)
6. **Reproducible** build on a clean machine (A2-17), including fonts
7. **GitHub repository** shared with the group (A2-16), blocked by decision D3
8. *(conditional)* **Topic approval** if the lecturer regards the topic as substantially different (A2-10, D4)
9. **MiKTeX compatibility: unverified** (A2-2; F-4)
10. **Agents as Skills** (MA-1)
11. **Separate Detector and Fixer** (MA-2)
12. **Automated red-team review** (MA-3)
13. **Incident reports** for self-found bugs (MA-4)
14. **Dedicated prompts and Skills folder** (MA-5)
15. **README screenshots of agents at work** (MA-6)

`PLAN.md` and `TODO.md` were mandatory; they now exist.

## F. Project decisions (recorded 2026-11-18, Prompt 15)

| # | Decision | Effect |
|---|---|---|
| F-1 | Preserve the approved green/charcoal/pink design and the Hebrew content. Keep `book/main.tex`. Chapters keep opening on new pages | Closes PLAN D7 (chapter starts) and D9. The near-empty chapter-end page is accepted; short boxes may still become unbreakable via the CLS |
| F-2 | Use **open-licence fonts** supporting Hebrew and English. Check **bold, numbers and punctuation** before choosing | Closes D2 (the direction). Font candidates must pass a glyph test before adoption; the current macOS fonts stay until then |
| F-3 | **Private GitHub repository** shared with both students and the lecturer. **Lecturer PDFs stay local** (not in the repo or ZIP). Repository creation and sharing are left to the submission stage | Closes D3 and D8 |
| F-4 | **Topic approval: unconfirmed.** Use the **current TeX Live** for the local LuaLaTeX test. **MiKTeX compatibility: unverified** until it is tested or the lecturer confirms TeX Live is acceptable | Records D4 and D1 as open risks, not blockers for local work |

