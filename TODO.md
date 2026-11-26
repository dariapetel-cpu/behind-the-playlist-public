# TODO: remaining work for Assignment 02

*Created 2026-11-18 (Prompt 14); corrected the same day (Prompt 15) for the Moodle announcement (MA-1…MA-6) and the user's decisions. Updated after Prompt 21: **the LuaLaTeX book (20 pp) is approved and is now `submission/behind-the-playlist.pdf`**; the previous XeLaTeX PDF is backed up in `backups/`.*

**➡ Next pending tasks (after QA round 1, 2026-11-18):**
1. The users decide whether to promote the candidate (class v1.1, only p.20 differs) to `submission/`.
2. Optionally decide on D1-04 (the diagram label offset).
3. Refresh the source ZIP (D1-01).
4. P6: README screenshots of agents at work (MA-6) and the remaining incident reports. Phases and decisions are in [`PLAN.md`](PLAN.md); the requirement sources are in [`docs/assignment-compliance.md`](docs/assignment-compliance.md).*

**Owner** is who will do the task:

| Owner | Meaning |
|---|---|
| **B** | Boss / coordinator |
| **U** | User |
| **S** | QA Skill |
| **F** | Fixer Skill (MA-2) |
| **R** | Reviewer agent |

**⛔ Dn** means the task is blocked by decision Dn.

## P0 Audit
- [x] Read the 3 lecturer PDFs (A2 rendered page by page) and write `docs/assignment-compliance.md` (B, 2026-11-18)
- [x] Create `PLAN.md` and `TODO.md` (B, 2026-11-18)
- [x] Correct the audit, PLAN and TODO for the Moodle announcement; record the decisions F-1…F-4 (B, 2026-11-18)
- [ ] Save the original Moodle announcement text as `docs/moodle-announcement.md` (U)
- [ ] Remaining open items: D6 (sudo install), R-1 MiKTeX unverified, R-2 topic approval unconfirmed (U)

## P1 Toolchain
- [x] Install `biblatex-ieee` (v1.4g), done by the user on 2026-11-18 (U)
- [ ] Record in PRD §10: TeX Live for local builds; MiKTeX compatibility unverified (B)
- [x] Font candidates (open licence, Hebrew + English): glyph test of regular/bold, digits, ״ ׳ ־ – „ " ( ) [ ] % : before choosing; add the fonts and licence files (B) — done: Pairing A chosen by the user (Prompt 18), bundled in `book/fonts/` (2026-11-18)
- [x] LuaLaTeX smoke test in `tests/lualatex-smoke/` with IEEE: passed 2026-11-18; see `tests/lualatex-smoke/RESULTS.md` (B)
- [x] Fix the open smoke findings in the CLS: bibliography list shifted 22 pt into the left margin; Hebrew „מקורות" heading (B) — done: babel `layout=lists`; heading via `\printbookbibliography` (2026-11-18)

## P2 CLS
- [x] Create `book/behind-the-playlist.cls` from `book/style.sty`: `\ProvidesClass` with version, changelog block, command list (B) — done: class v1.0 (2026-11-18)
- [x] Port the RTL rules to LuaLaTeX: replace `\beginR…\endR` in `heb` and `\hebcolor`, and re-test the white-text and LTR-paragraph incidents (B) — done: babel `layout=graphics.lists.tabular`; `\hebcolor`/`heb` kept as compatibility no-ops; colours verified (2026-11-18)
- [x] Switch the bibliography to `style=ieee`; keep the Hebrew heading and the LTR English entries; keep DOI-only printing for DOI entries (B) — done (2026-11-18)
- [x] `main.tex` uses `\documentclass{behind-the-playlist}`; delete `style.sty` once it is unused (B) — done; `style.sty` kept as a retired file because it is the source of the old submission PDF (2026-11-18)
- [x] Rebuild; compare the page map with `docs/screenshots/pagemap.json`; run all automated, glyph and colour checks (B) — done: 20 pp, chapter starts identical, all checks pass (2026-11-18)

## P3 Iron law: move in-chapter layout edits into the CLS
- [x] `03-anashim-kmotech.tex:43`: side-by-side data table + intro becomes a CLS command (B) — done: class command (2026-11-18)
- [x] `04-shirim-kmo-ze.tex:34,37`: float placement and ragged flush-right column become a CLS column type / table environment (B) — done: class command (2026-11-18)
- [x] `06-shmone-tachanot.tex:20`: figure placement becomes a CLS figure policy or environment (B) — done: class command (2026-11-18)
- [x] `08-play.tex:4`: `\enhead` becomes CLS heading handling of Latin words (B) — done: class command (2026-11-18)
- [x] Verify the PDF is visually unchanged, and that no layout code is left in `book/chapters/` (B) — done: no layout code left in `book/chapters/`; same page map (2026-11-18)

## P4 Skills: agents as Skills (MA-1) in a dedicated folder (MA-5), plus the QA Skills (A2 §4 step 5, §5, table 2)
- [x] Dedicated folder layout for Skills and prompts (MA-5), linked from the README (B) — `.claude/skills/` + `prompts/`, listed in `SKILLS.md` (2026-11-18, QA round 1)
- [x] `detector` Skill: runs the QA Skills and the red team, writes findings, **never edits** (B) — done; ran D1 and D2 (2026-11-18, QA round 1)
- [x] `fixer` Skill: applies fixes **only** in the CLS/Skills and logs each fix against its finding (B) — done; ran F1 (2026-11-18, QA round 1)
- [x] `red-team` Skill: adversarial review of facts/citations, BiDi, layout and privacy (ID leaks) (B) — covered by the detector Skill's red-team pass (no separate Skill) (2026-11-18, QA round 1)
- [ ] Researcher, writer and reviewer roles as Skills, for future use. Their earlier runs as subagents stay recorded as such (B)
- [x] `qa-super`: the orchestrator; runs the others, merges the findings and outputs a pass/fail summary (B) — done (2026-11-18, QA round 1)
- [x] `qa-bidi`: glyph-order checks for Hebrew words, digits, brackets, TikZ labels and graph labels (reuse the existing checks) (B) — done (2026-11-18, QA round 1)
- [x] `qa-table`: column order RTL, cell alignment by x-positions, no overflow (B) — done (2026-11-18, QA round 1)
- [x] `qa-img`: figures present, captions, `\fictional` / `\educational` tags, crops inside the page (B) — done (2026-11-18, QA round 1)
- [x] `qa-code`: code-box checks; reports "no code boxes" honestly if none (B) — done (2026-11-18, QA round 1)
- [x] `qa-typeset`: log errors, missing glyphs, overfull/underfull boxes, undefined references (wrap `tools/check_pdf.py`) (B) — done (2026-11-18, QA round 1)
- [x] `qa-infra`: required files (A2 §3.3), folder structure, README links, ID-leak scan (B) — done (2026-11-18, QA round 1)
- [x] `qa-cls-version`: the CLS version in the PDF/log matches the version in `behind-the-playlist.cls` and the changelog (B) — done (2026-11-18, QA round 1)
- [x] `SKILLS.md`: list every Skill, its purpose, its files and the dates it actually ran (B) — done (2026-11-18, QA round 1)
- [x] Run each Skill on the current PDF; save the reports to `docs/qa/` (S) — done: `docs/qa/round-01/` (2026-11-18, QA round 1)

## P5 Automated red-team QA loop (MA-2, MA-3; G §19.1; L04 §11.8)
- [x] Loop script: detector (qa-super + red-team) → fixer → rebuild → detector; stop at 0 blocking (B) — done as a coordinator-orchestrated agent chain D1 → F1 → D2, with no user step; the stop rule was met (0 actionable template/skill defects left) (2026-11-18, QA round 1)
- [ ] Optional Reviewer pass on content, if there are any content changes (R)
- [x] Log every iteration (who detected, who fixed, what changed, recheck result) in `docs/agents/log.md` and `docs/qa/` (B) — done: `docs/agents/log.md` rows 6–8, `docs/qa/round-01/README.md` (2026-11-18, QA round 1)

## QA follow-ups (from QA round 1)
- [x] D3-01: The automated check locates the rotated label on page 14. Regression tests verify that deleting the label fails even when the same words remain on page 15.
- [x] D1-04 label gap: the users decided on a ≈2 mm gap; done and approved (Prompt 25)
- [x] Promote the QA candidate (class v1.1 + label offset) to `submission/`: approved and done (Prompt 25)

## QA round 2 (2026-11-25, `docs/qa/round-02/`)
- [x] Reproduce the harness failures (Detector D4)
- [x] Fix them in the tools and Skills (Fixer F2) and add `tests/test_qa_mutations.py`
- [x] Targeted fixes 1, 2, 3 and 7 (privacy, logs, stale results, unprotected tests): coordinator, 88 focused tests OK
- [x] INC-003 incident report
- [ ] Independent verification: D5 was stopped without a report; only the coordinator verified the targeted fixes
- [ ] Complete one full test run of the final code: the last run stopped for low memory (69 pass, 0 fail, 72 not run)
- [ ] Issue 4 (tiny covers), issue 5 (incomplete iron-law and code lists), issue 6 (false alarms on nine-digit numbers)
- [ ] Run the log checks on a **real** LaTeX and biber log; run on Linux/macOS and on the submission edition
- [ ] Approve `expectations.json`, `visual_baseline.json` and the two chapter 2 layout exceptions (U)
- [ ] Review, commit and push (U)

## P6 Records
- [x] `docs/incidents/` started: index + INC-001 (reversed TikZ labels, found by Daria) (B, 2026-11-18)
- [ ] `docs/incidents/` (MA-4): remaining reports, one per genuine self-found bug (symptom, detection, root cause, fix location, prevention/Skill update, source line), e.g. the tlmgr hang, TikZ word order, `[heb]` + colour white text, matplotlib double bidi, LTR-flipped tag paragraph, commented-out `;`, black text in floats, the false PASS on an image-only check (B)
- [ ] `prompts/`: reusable prompts copied from `docs/agents/tasks/*.md` and proven Boss prompts, each with its origin and date (B)
- [ ] README screenshots of agents/Skills at work, from real runs only, IDs masked (MA-6) (B)
- [ ] README (Hebrew): Skills section, LuaLaTeX build, QA-loop evidence, links to `docs/qa/`, `docs/incidents.md` and `SKILLS.md`; keep the ID masking (B)
- [ ] PRD: update §6 (engine, CLS, IEEE), §8 and §11 (B)

## P7 Reproducibility (A2 p. 5)
- [x] Build script / Makefile runs `lualatex → biber → lualatex → lualatex` (A2 sample) (B) — done: `make pdf` / `make submission` use LuaLaTeX via latexmk; README shows the manual A2 sequence (2026-11-18)
- [ ] Deterministic output: `SOURCE_DATE_EPOCH`, fixed `/ID`, no absolute paths in the PDF (B)
- [ ] Clean-copy test: extract the ZIP to a temporary folder, build, and compare the SHA-256 with the submission PDF (B)
- [ ] MiKTeX/Windows build notes, marked **unverified** until tested or accepted by the lecturer (R-1) (B)

## P8 Submission (A2 §6)
- [x] Public GitHub copy prepared in `public-release/behind-the-playlist/` with `tools/make_public.py`: no student IDs, no submission-date row on the cover; public PDF `pdf/behind-the-playlist.pdf` (Prompt 26)
- [ ] **Waiting for the user's approval:** publish the public copy on GitHub (U)
- [x] Submission date removed from the entire public copy: placeholder „[תאריך ההגשה הושמט]” in the prompt log, transcripts, QA reports and expectations; date row masked in the 3 old QA cover renders; the originals stay in the project (Prompt 27)
- [x] `qa_lib.py --edition public`: public cover phrases plus a blocker check for IDs, dates and ID/date labels on the cover (Prompt 27)
- [ ] Keep the lecturer PDFs local: exclude them from the repository and ZIP (B)
- [ ] Topic approval is **unconfirmed**; ask the lecturer before submission (U)
- [x] Final book PDF approved and copied to `submission/` (identical to the reviewed preview, SHA-256 43608a86…); README screenshots regenerated from it, IDs masked (2026-11-18, Prompt 21)
- [x] Regenerate `submission/project-source.zip` with the approved PDF and current sources; the old ZIP is backed up in `backups/` (B, Prompt 25)
- [ ] Run `qa-infra` on the extracted copy of the new ZIP (S); currently fails as D1-01 (stale ZIP)
- [ ] **Keep pending until the user decides:** GitHub publication and Moodle submission (U)
- [ ] Human sign-off (G §19.5): read the abstract, page through the PDF (U)
