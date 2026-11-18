# Development Prompt Log

User prompts to the coordinating agent (Boss), recorded verbatim in chronological order.
Agent-to-agent instructions are logged separately (see the agent log once it exists).

---

## Prompt 1 — 2026-11-11 — Project kickoff and environment check

```text
We are starting a new university project in this directory.

Project: “מאחורי הפלייליסט” (“Behind the Playlist”), a visually designed, approximately 20-page Hebrew book explaining how music recommendation systems work. Follow a fictional listener through everyday listening situations, combining accessible explanations with light humor and verified research.

Final requirements:
1. A PDF compiled from LaTeX, with correct Hebrew right-to-left layout.
2. A title page, abstract, table of contents, chapters, and bibliography.
3. At least one graph generated with Python, one table, and one mathematical formula with an explanation and numerical example.
4. An eight-block diagram explaining the recommendation process, created with editable vector objects, preferably TikZ.
5. Consistent colors, typography, emphasis boxes, and readable page layouts.
6. README.md with project instructions and screenshots from the actual final PDF.
7. PRD.md defining the scope, deliverables, design, and acceptance criteria.
8. An accurate development prompt log and evidence of actual work by at least three distinct agents: Researcher, Writer, and Reviewer. You are the coordinating Boss.
Research requirements:
Use verifiable sources and cite them in the book. Clearly label fictional listening data and educational formulas. Do not present an illustrative model as Spotify’s actual algorithm.

Current step:
Inspect the current directory and check whether Python 3, matplotlib, XeLaTeX or LuaLaTeX, a bibliography tool, PDF rendering tools, and Hebrew fonts are available. Do not install anything yet.

Create PRD.md from these requirements and save this prompt verbatim as the first entry in docs/prompts.md. Record later user prompts accurately, without inventing earlier exchanges.

Propose a lightweight way to run and document the three specialist agents using the existing Claude login. Minimize repeated context and unnecessary agent calls. Do not implement an orchestration framework or start writing the book yet.

Report which tools are available, which are missing, and your proposed agent setup. Then wait for my next instruction.
```

**Boss actions:** inspected the (empty) directory and toolchain without installing anything; created `PRD.md` and this log; proposed an agent setup and paused for the user's decision.

---

## Prompt 2 — 2026-11-11 — Toolchain setup, agent definitions, Hebrew test

```text
Proceed with the setup:
1. Install BasicTeX from its official source and the additional packages needed for this project. Verify the package names and dependencies before installing. If macOS requires an administrator password or an installer window, give me clear instructions. Never ask me to paste my password into chat.
2. Create a project-local Python virtual environment named .venv. Install matplotlib, numpy, python-bidi, and PyMuPDF inside it.
3. Create the Researcher, Writer, and Reviewer definitions in .claude/agents/ using the built-in Agent tool approach you proposed. Keep their responsibilities distinct and record their actual executions and outputs. Do not mark an agent as executed merely because its definition file exists.
4. Verify the setup by compiling a one-page Hebrew LaTeX sample with right-to-left text, a heading, a short formula, and a small TikZ diagram. Render the PDF and inspect it for missing characters, reversed text, and clipping.
5. Update PRD.md and append this prompt to docs/prompts.md. Report what you installed, the agent files you created, and whether the Hebrew compilation test passed.
Do not write the full book yet.
```

---

## Prompt 3 — 2026-11-11 — Message sent while setup was running

```text
The installer finished successfully. Continue the setup and verify the Hebrew LaTeX sample.ֿ
```

*(Sent mid-turn after the BasicTeX GUI installer completed. The trailing character after the period is reproduced as received.)*

**Boss actions:** verified the installed TeX files directly with `kpsewhich` (`tlmgr info --only-installed` falsely reported every package as installed), checked the 19 missing package names and their dependencies against the TeX Live 2026 repository, and gave the user one `sudo tlmgr` command to run in Terminal. *Correction:* the Boss's reply at that point said this message was already logged. It was not; it was added here in order, together with Prompt 4.

---

## Prompt 4 — 2026-11-11 — tlmgr install appears stuck

```text
The installation command in the other Terminal tab has shown no new output for over five minutes, and the shell prompt has not returned. The last output was “tlmgr: command log updated” after the self-update. Inspect the running tlmgr and curl processes and the installation logs. Determine whether the package installation is progressing, waiting for input, or stuck on a download. Do not start another installation or stop the existing process yet. Report what you find and give me one clear next step.
```

**Boss actions (Prompt 4):** inspected the processes and logs read-only. The install was stuck on a `curl` download of `texlive.tlpdb` from an unresponsive mirror, and no packages had been installed. Advised Ctrl+C and a rerun pinned to `ctan.mirror.norbert-ruehl.de`.

---

## Prompt 5 — 2026-11-11 — Verify packages and run the Hebrew test

```text
The installation command finished and the shell prompt returned. Verify that all required packages are installed. Then compile the Hebrew sample, render and visually inspect it, and report whether the test passed. Do not write the full book yet.
```

**Boss actions (Prompt 5):** verification failed. None of the 19 packages are on disk, `biber` and `latexmk` are absent, and the TeX tree hasn't changed since the 20:32 self-update. A `--dry-run` with the pinned mirror resolves all 21 items (including the `biber` and `latexmk` darwin binaries), so the mirror and package names are fine. The Hebrew sample was **not compiled**, because its required packages (bidi, tcolorbox) are missing.

**Boss actions (Prompt 5, continued):** the user's install completed at 20:41 (21 packages per `tlmgr.log`), and all required files and tools were then verified. The Hebrew sample was compiled, rendered and inspected. The first build had 7 missing Latin glyphs in math, fixed by setting a Latin-capable main font. The rebuilt sample **passed**. PRD.md was updated to v0.2.

---

## Prompt 6 — 2026-11-11 — Re-verify and open the sample

```text
The installation completed successfully with all 21 packages. Verify the installed packages, compile the Hebrew sample, render it, and visually inspect the Hebrew text, formula, and diagram. Report the result and open the sample PDF for me. Do not write the full book yet.
```

**Boss actions (Prompt 6):** re-verified 20 key style and language files (none missing) and the 21 `install:` entries in `tlmgr.log`. Did a clean rebuild of the sample (exit 0; 0 missing characters, 0 errors, 0 bad boxes), re-rendered it at 300 dpi and re-inspected it: **PASS**, same as the Prompt 5 result. Opened `tests/hebrew-sample/sample.pdf` for the user.

---

## Prompt 7 — 2026-11-11 — Fix RTL inside TikZ nodes; propose the outline

```text
The sample PDF opens and the main Hebrew paragraph looks readable, but the word order inside all three TikZ nodes is reversed.

The labels must read exactly:
איסוף אותות
דירוג מועמדים
הצגת המלצות

Fix the RTL handling inside the TikZ nodes while keeping the Hebrew source text in its natural order. Keep the flow from right to left. Recompile, render, and visually verify all three labels.

Then prepare a proposed 20-page book outline, including the cover, abstract, table of contents, chapters, and bibliography. Identify where the Python graph, comparison table, explained formula, and eight-block diagram will appear.

Save the outline in docs/outline.md and record this prompt in docs/prompts.md. Do not write the full book yet.
```

**Boss actions (Prompt 7, first send, 2026-11-11):** confirmed the bug numerically: in every node the first word lay left of the second. A first fix attempt (`\setRTL` at node start) had no effect, because node text is an `\hbox`. The working fix wraps node text in `\beginR…\endR` through one `every node` style, with the source text unchanged. After recompiling (0 errors, 0 missing characters, 0 bad boxes), word and letter x-positions confirm all three labels and the right-to-left flow, and a 400 dpi close-up was checked. PRD §6/§10 now records the rule and a correction of the earlier wrong PASS. The turn ended before the outline was written.

---

## Prompt 8 — 2026-11-14 — Same text as Prompt 7, sent again

*(Identical to Prompt 7, sent again verbatim; not duplicated here. The TikZ fix was already done; this send produced `docs/outline.md`.)*

---

## Prompt 9 — 2026-11-14 — Approve outline; run the Researcher

```text
I approve Noa as the fictional listener and the proposed 20-page outline. Keep the eight-block diagram in Chapter 6.

Leave missing cover details as clearly marked placeholders. Do not invent the lecturer’s name, submission date, or author details.

Run the Researcher agent now. Verify the candidate sources and replace any that cannot be verified. Prefer accessible academic papers and official technical publications. Save research-notes.md with a clear mapping between claims, chapters, and sources, and create references.bib with verified bibliographic details and URLs.

Distinguish general recommendation methods from documented claims about specific platforms. Label Noa’s story and all simulated data as fictional.

Record the actual Researcher run and its outputs in docs/agents/log.md, preserve available execution evidence, and save this prompt in docs/prompts.md.

After the research, report source coverage and remaining gaps. Do not write the full book yet.
```

**Boss actions (Prompt 9):**
- Marked the outline approved and wrote `docs/agents/brief.md`.
- Ran the **Researcher** agent once, via the built-in Agent tool (task text in `docs/agents/tasks/R1-researcher.md`). It produced `docs/agents/research-notes.md` and `book/references.bib`.
- Checked the outputs independently: a biber compile and a link/DOI/Crossref check.
- Archived the transcript and an action timeline in `docs/agents/transcripts/`, and completed log row 1 in `docs/agents/log.md`.
- No book text was written.
- Adjusted three outline lines (Ch. 2, 4, 5) to match R1 research gaps; page plan unchanged.

---

## Prompt 10 — 2026-11-14 — Run the Writer (abstract + Ch. 1–4); design preview

```text
עכשיו אפשר להדביק את ההנחיה הבאה. סוכן המחקר סיים, ו־Claude מדווח על 18 מקורות ומתעד אילו מהם קרא חלקית.

ההנחיה מפעילה את סוכן הכתיבה לכתיבת התקציר וארבעת הפרקים הראשונים. היא מחייבת אותו להסתמך על המחקר ולשמור על ההבחנה בין הסיפור של נועה לבין עובדות מהמקורות.

הדביקי בחלון של Claude:

Run the Writer agent to write the Hebrew abstract and Chapters 1–4, following PRD.md, docs/outline.md, docs/agents/brief.md, research-notes.md, and references.bib.

Use an engaging, accessible narrative following Noa, with light humor and clear explanations for readers without a technical background. Keep terminology consistent and respect the planned page budget.

Support factual claims with the verified citation keys. Respect all research limitations, including sources read only partially. Omit unsupported factual claims rather than presenting them without citations. Clearly label fictional scenes, simulated data, and educational examples.

Include the explained cosine-similarity formula and worked example, and the comparison table planned for Chapter 4. Check the arithmetic. Coordinate with the main agent on the Python graph planned for Chapter 2.

Save the chapters as LaTeX source files. Record the actual Writer run and preserve its available execution evidence. Log this prompt.

Then compile a preview of the completed sections using the tested Hebrew RTL setup. Apply a cohesive music-inspired design with readable typography, restrained colors, and consistent explanation boxes. Render and inspect the preview for reversed Hebrew, clipping, and layout problems.

Report the files created and open the preview PDF for me. Do not write Chapters 5–8 yet.
```

**Boss actions (Prompt 10):**
- *Ch. 2 graph:* generated the fictional data `figures/data/noa_week.csv` and the script `figures/noa_week.py`, which outputs `book/figures/noa_week.pdf`. Finding: matplotlib 3.11 already lays out RTL text, and python-bidi's `get_display` reversed the letters a second time, so it was removed (verified at glyph level). The dataviz palette validator could not run because Node.js is not installed; the chart uses a teal/coral pair plus a hatch pattern and direct labels instead.
- *Design:* wrote `book/style.sty` (New Peninim MT body ×1.12, Arial Hebrew headings, Times/Arial for Latin; teal/coral/ink palette; "רצועה 0N" chapter openers with equalizer bars; a player progress bar footer; scene, inshort, lab and realitycheck boxes plus tags) and `book/main.tex` (cover with marked placeholders, abstract, TOC, chapters, bibliography). Bugs found and fixed while testing:
  - a `[heb]` node plus any colour renders the text white, so `\hebcolor` was added;
  - a paragraph starting with a TikZ box turns LTR, so tags moved to box title lines;
  - New Peninim has no Latin letters or bullet, so citations use the English font and bullets are drawn;
  - csquotes has no Hebrew style, which caused bold "?" markers;
  - long bibliography URLs caused overfull lines;
  - the title page reset the page number, giving duplicate PDF anchors;
  - cover elements overlapped, so they are now absolutely positioned.
- *Build tools:* added the `Makefile` and `tools/check_pdf.py`.
- *Writer:* ran the **Writer** once (W1, task text in `docs/agents/tasks/W1-writer.md`). It wrote the abstract and Ch. 1–4. The Boss checked the keys, banned terms, arithmetic and sources.
- *Preview:* built `build/behind-the-playlist.pdf` (14 pp). Automated checks PASS; every page inspected visually, with glyph-level checks for "07:30." and the placeholder brackets. Archived the transcript and completed log row 2. Ch. 5–8 not written.

---

## Prompt 11 — 2026-11-14 — Writer Ch. 5–8, diagram, Reviewer, full 20-page build

```text
Continue with the Writer agent for Chapters 5–8, following the approved outline, research notes, and the tone of Chapters 1–4. Preserve evidence of this actual agent run.

Create the eight-block TikZ diagram in Chapter 6, using the tested RTL style. Explain each block and label the diagram as an educational simplification, not a specific platform’s internal architecture.

Then run the Reviewer agent to check the complete manuscript against the PRD and research notes. Check citation support, research limitations, mathematical accuracy, fictional-data labels, and the comparison table’s unsupported descriptions. Have the Reviewer write a report, then address its findings.

Compile the complete book, targeting 20 pages including the cover, abstract, table of contents, and bibliography. Improve the nearly empty page 10 by redistributing meaningful content. Do not pad the book with empty space or shrink text excessively to meet the page count. Keep the bibliography readable.

Render and inspect every page, including Hebrew word order, graph labels, table cells, diagram arrows, citations, and page numbering. Record all actual agent runs and this prompt.

Open the complete PDF and report remaining issues. Keep missing cover details clearly marked until I provide them.
```

**Boss actions (Prompt 11):**
- *Diagram:* built `book/figures/pipeline.tex`, the eight-block TikZ diagram (snake layout right to left, dashed feedback loop 8 → 1, three colour groups). Glyph-checked all 18 labels. Removed digit ranges from the legend ("1–3" displays as "3–1" in RTL) and fitted the width to the text block.
- *Ch. 3 layout:* to fix the near-empty page 10, the cosine data table now sits beside its introduction and the two calculations are side by side. Content and numbers are unchanged, Ch. 3 now fits on pp. 8–9, and „הטבלה הבאה" became „הטבלה שמימין".
- *Writer W2:* ran the **Writer** a second time (task text in `docs/agents/tasks/W2-writer.md`). It wrote Ch. 5–8. Boss checks: keys valid, all 18 bib entries now cited, no banned terms. Boss fix: `\enhead{Play}` in the Ch. 8 title.
- *Reviewer V1:* ran the **Reviewer** once (task text in `docs/agents/tasks/V1-reviewer.md`). Its report, `docs/agents/review-01.md`, has 36 issues (0 blocker, 5 major, 31 minor) and the verdict CHANGES REQUESTED.
- *Review fixes:* the Boss addressed the findings (`docs/agents/review-01-response.md`): 31 applied, 1 partly applied, 2 open, 2 accepted. Also set `sortcites=true` and refined the white-text check, which was regression-tested.
- *Final build:* the complete book is **20 pages**. Automated checks PASS (0 errors, 0 missing glyphs, 0 overfull). Every page inspected visually, with glyph-level checks of the diagram (18/18), graph (6/6), table cells and citation order. Transcripts for W2 and V1 archived; log rows 3–4 completed. PRD v0.3 records the bibliography decision, and the outline has the new Ch. 5 title.

---

## Prompt 12 — 2026-11-14 — Cover details, second review, README, submission

> **Redaction notice:** the two student ID numbers in this prompt are replaced with `[REDACTED: student ID]`, as the user instructed. Nothing else in the prompt was changed. The IDs appear only in the submission PDF and its LaTeX source (`book/main.tex`).

```text
Update the cover with these exact details:
Author: דריה פטל
Student ID: [REDACTED: student ID]
Author: רוני שגיא
Student ID: [REDACTED: student ID]
Course: בינה מלאכותית יוצרת
Lecturer: ד״ר יורם סגל
Submission date: [תאריך ההגשה הושמט]

Place each student ID beside the correct author. Keep the digits left to right and verify Hebrew word order and punctuation. Remove the institution placeholder without inventing a replacement.

Include the IDs in the submission PDF. Omit them from README text and mask them in README screenshots and any prompt logs prepared for public sharing. Record this prompt with the IDs redacted and explicitly label that redaction.

Run a focused second Reviewer pass on the revised manuscript and rendered PDF. Verify the previous findings against review-01.md and review-01-response.md, especially major issues and partially resolved items. Address remaining substantive problems and record the final verdict honestly.

Keep English bibliography entries left to right under the Hebrew heading. Maintain readable typography and the 20-page target without padding pages.

After the final changes, rebuild the PDF and create README.md in Hebrew containing:
A short description of the book and its audience.
A relative link to the submission PDF.
Actual screenshots from the final PDF showing the cover, Python graph, formula, comparison table, and eight-block diagram. Mask student IDs in the cover screenshot.
A requirements checklist with accurate final page numbers.
The three agents’ roles, actual contributions, and links to their execution evidence and review reports.
Reproducible build instructions, dependencies, and project structure.
Links to PRD.md and the development prompt log.
An explanation that Noa and the graph data are fictional.

Update PRD.md to reflect the delivered project. Record the actual Reviewer run and preserve previous logs and reports.

Place the final PDF in submission/behind-the-playlist.pdf. Verify that README links and screenshots match this version, except for the explicitly masked IDs. Do not publish or upload the project.

Report any remaining issues and open the final PDF for me.
```

**Boss actions (Prompt 12):**
- *Cover:* entered the user's details exactly; removed the institution line; nothing invented. Each ID sits on its author's row as a left-to-right unit. Glyph checks confirmed the digit order, Hebrew word order (ת״ז, ד״ר) and the date [תאריך ההגשה הושמט]. Cell alignment was fixed: in this RTL tabular, `r` means flush right (measured).
- *Privacy:* the IDs appear only in `book/main.tex` and the PDFs. They are absent from README text, masked in all screenshots (`tools/screenshots.py` masks every 9-digit number on the cover by pattern), redacted with a label in this log, and absent from every agent transcript (the V2 Reviewer was barred from `main.tex` and given a masked cover). A repository scan confirmed this.
- *Reviewer V2:* ran the **Reviewer** a second time (task text in `docs/agents/tasks/V2-reviewer.md`). Verdict: **APPROVE WITH MINOR NOTES** (`docs/agents/review-02.md`).
- *Review-02 fixes* (`docs/agents/review-02-response.md`):
  - bibliography ragged-right with no stretched URLs, and DOI-only for DOI entries (back to 20 pages, no smaller type);
  - Ch. 8 last line, the Ch. 7 "גם" repetition, the cover date font and tagline dashes;
  - "ציון" kept for user ratings only;
  - ragged, flush-right cells in Table 4.1.
- *README and submission:* created the Hebrew `README.md`, with screenshots generated from the final PDF and verified pixel-identical to a fresh render of `submission/behind-the-playlist.pdf`, and all 34 relative links checked. Added `requirements.txt` and `make submission`.
- *PRD:* updated to v1.0 (delivered state, §11). Nothing was published or uploaded.

---

## Prompt 13 — 2026-11-14 — New palette, final submission package

*(The message began with a standalone line "5" before the pasted text. Both are reproduced as received.)*

```text
5

Apply the following palette consistently throughout the existing book, then prepare the final submission package.

Palette:
Dark charcoal: #121212
Bright green: #1ED760
Neon pink: #FF2E88
Light page background: #F2F2F2

Use dark charcoal for the cover background and body text. Use bright green and neon pink for cover accents, chapter decorations, diagram elements, chart series and the progress footer. Keep reading pages light. Avoid bright green or pink for small text on light backgrounds. Use charcoal text on green or pink fills.

Replace the previous teal, coral and navy palette throughout the LaTeX styles and Python graph. Preserve the content, Hebrew direction, citations, author details and 20-page layout. Do not rewrite the book or run additional agents.

Rebuild and visually inspect the PDF, including the cover, graph, table, formula boxes and eight-block diagram. Check contrast, Hebrew labels, clipping and page count. Save the updated final PDF as submission/behind-the-playlist.pdf.

Regenerate the README screenshots from the updated PDF, preserving the existing masking of ID numbers. Update the design palette in PRD.md and record this prompt in docs/prompts.md.

Create submission/project-source.zip containing the LaTeX sources, Python graph script and data, bibliography, README and its updated screenshots, PRD, development prompt log, agent definitions, agent execution evidence, review reports, build instructions, dependency files and the updated final PDF.

Preserve the project directory structure so that relative README links work after extraction. Exclude .venv, caches, temporary files, credentials and the ZIP itself. Preserve existing ID masking in documentation and screenshots.

Extract the ZIP into a temporary directory and verify that it opens, all required files are present, relative README links resolve and the packaged PDF matches the updated final PDF.

Do not publish or upload anything. Report the exact paths of the final PDF and ZIP, open the updated PDF for my review and show the submission folder in Finder.
```

**Boss actions (Prompt 13):**
- *Palette:* applied charcoal `#121212` / green `#1ED760` / pink `#FF2E88` / page `#F2F2F2` across `book/style.sty`, `book/main.tex` (full charcoal cover), `book/figures/pipeline.tex` and `figures/noa_week.py`. No teal, coral or navy remains.
- *Contrast:* green and pink are used only for fills, rules, bars and dots on light pages; all text there is charcoal or `#555555`. A PDF-wide audit found every text span ≥ 4.5:1 on pages 2–20. Black text inside boxes, captions and floats was fixed by making charcoal LaTeX's default colour.
- *Content:* unchanged. Hebrew labels re-verified at glyph level (diagram 18/18, graph 6/6, table cells). Still 20 pages, with an identical page map.
- *Fixes during the pass:* two TikZ syntax errors I introduced (a `%` comment swallowing a `;`) were found by the build and fixed.
- *Outputs:* updated `submission/behind-the-playlist.pdf`, regenerated the README screenshots (cover IDs still masked), updated the palette in PRD (v1.1) and README, and created `submission/project-source.zip`, verified by extraction.
- *Agents:* no agent was run, as instructed. Nothing was published or uploaded.

---

## Prompt 14 — 2026-11-18 — Audit against the lecturer's updated assignment PDFs

```text
Read the three lecturer PDFs in assignment/ and audit the existing project against the updated assignment requirements.

Preserve the approved book topic, content and green, charcoal and pink design.

Create docs/assignment-compliance.md with each requirement, its source page, existing file evidence, status and necessary action. Distinguish mandatory requirements from recommendations and examples. Inspect the rendered requirement pages when text extraction is ambiguous.

Check specifically:
Custom CLS, LuaLaTeX, the stated MiKTeX requirement versus our BasicTeX installation, IEEE bibliography, PLAN.md, TODO.md, prompt files, actual Skills, separate Detector and Fixer roles, an automated review-fix-recheck workflow, incident investigations, reproducible builds and README evidence of agents working.

Preserve all genuine historical agent records. Do not invent past runs or retroactively describe the coordinator’s fixes as Fixer-agent work.

Create or update PLAN.md and TODO.md for the remaining work. Do not rewrite the book, change the build system, install software, run agents or publish anything during this audit.

Report the mandatory gaps, a minimal implementation sequence and any questions that require our decision. Record this prompt in the development log.
```

**Boss actions (Prompt 14):**
- *Sources:* `assignment/` does not exist; the three lecturer PDFs are in the project root and were left there.
  - The assignment PDF's Hebrew text layer is garbled, so all 5 pages were rendered and read as images.
  - The L04 summary was read from extracted text.
  - Relevant sections of the 97-page guide (§13.1, §13.4, §15.2, §15.5, §18.11, §19.1–19.5) were rendered. The guide belongs to a different course and is treated as recommendations.
- *Read-only checks:*
  - `lualatex` is available (LuaHBTeX 1.24).
  - `biblatex-ieee` is not installed.
  - There is no `.cls`, no Skills, no git repository, and no PLAN/TODO/prompts folder.
  - There are 5 coordinator layout edits inside chapter files.
- *Created:* `docs/assignment-compliance.md` (A2-1…A2-19, G-1…G-12, the requested checks, history integrity, mandatory gaps), `PLAN.md` (phases P0–P8, decisions D1–D9) and `TODO.md`.
- *Not done, as instructed:* no book, build or tool changes; nothing installed; no agents run; nothing published. Historical agent records are unchanged.

---

## Prompt 15 — 2026-11-18 — Moodle announcement, project decisions, LuaLaTeX smoke test

```text
Use the lecturer’s Moodle announcement together with the three PDFs. Correct the audit, PLAN.md and TODO.md: the announcement explicitly requires agents built as Skills, separate Detector and Fixer roles, an automated red-team review, incident analysis for bugs we find ourselves, a dedicated folder for prompts and Skills, and README screenshots showing agents at work.

Record these project decisions:
- Preserve the approved green, charcoal and pink design and Hebrew content. Keep book/main.tex and chapter openings on new pages.
- Use open-license fonts that support Hebrew and English. Check bold text, numbers and punctuation before selecting them.
- Plan for a private GitHub repository shared with both students and the lecturer. Keep the lecturer’s PDFs local. Leave repository creation and sharing for the submission stage.
- Record topic approval as unconfirmed. Use the current TeX Live installation for a local LuaLaTeX test. Record MiKTeX compatibility as unverified until it is tested or the lecturer confirms TeX Live is acceptable.

Now run one isolated test in tests/lualatex-smoke/. Build a one-page PDF with a mixed Hebrew-English sentence, a number in parentheses, a formula, a Hebrew TikZ label and an IEEE citation from our existing bibliography. Use LuaLaTeX and Biber. Render the PDF and inspect the word order, glyphs and citation. If a missing package requires sudo, give me the exact Terminal command and wait.

Keep the current submission PDF intact. Save this prompt in the development log. Report what passed, what remains unverified, and the path to the test PDF. Stop after the test.
```

**Boss actions (Prompt 15, part 1, waiting for the user):**
- *Moodle announcement:* the original text is not in the project. The audit cites the user's summary as source **MA** and asks for the original to be saved (TODO P0, PLAN R-3).
- *Documents:* corrected `docs/assignment-compliance.md` (new §A′ MA-1…MA-6, all mandatory; G-2/G-3/G-5/A2-18 marked "→ MA"; §C and §E corrected; §F records decisions F-1…F-4), `PLAN.md` (decided D1–D5, D7–D9; open D6, R-1 MiKTeX unverified, R-2 topic approval unconfirmed, R-3) and `TODO.md`.
- *Smoke test:* `tests/lualatex-smoke/smoke.tex` (LuaLaTeX + Biber; babel `bidi=basic,layout=graphics` + `onchar=ids fonts`). The submission PDF was not touched (SHA-256 still 5e24a1cd…).
- *Incidents found and isolated in scratch tests:*
  1. **New Peninim MT** under LuaLaTeX: any `\section` makes the following text vanish (blank first page, overfull vbox). This happens with that font only; it was not used further.
  2. **TikZ node labels** under `bidi=basic`: off-origin labels land outside their boxes. Fixed with `layout=graphics`. The language wrappers place the labels correctly but leave the brackets unmirrored.
  3. Without `onchar=ids fonts`, Latin glyphs go missing and brackets aren't mirrored.
  4. Math `cos` used the Hebrew font; fixed with `\setmathrm`.
  5. A stale `.bcf` left an empty `.bbl` in one probe sequence; rerunning biber fixed it.
  6. Two test-harness errors: zsh turned `\e` into an escape character, and an `rm` glob was blocked by the safety check, so a fresh folder was used instead.
- *Preliminary probe with the fallback `numeric` style:* 1 page; 0 errors; 0 missing glyphs; mixed sentence, number in parentheses, formula, TikZ labels and citation all render.
- *IEEE:* `biblatex-ieee` is missing and needs `sudo`. Gave the user the Terminal command and **stopped to wait**, as instructed.

---

## Prompt 16 — 2026-11-18 — IEEE smoke build, README "התפתחות הפרויקט", first incident report

```text
I installed biblatex-ieee. Build tests/lualatex-smoke/smoke.tex with LuaLaTeX, Biber and IEEE style. Inspect the rendered page: verify that the numbered citation matches its bibliography entry, the mixed Hebrew-English sentence and parentheses read correctly, the formula is legible, and both Hebrew labels sit inside their diagram boxes.

Add these sentences under “התפתחות הפרויקט” in the root README:
בנינו אב־טיפוס של הספר על סמך ההנחיות שקיבלנו בשיעור. לאחר שהמרצה פרסם את המפרט המלא, השווינו את הפרויקט לדרישות ועדכנו את תוכנית העבודה בהתאם.

Link the paragraph to the audit and PLAN.md. In the incident log, document how Daria spotted the reversed Hebrew word order in the earlier diagram, why the first review missed it, and how the team verified the correction. Base the account on the existing records. Record today’s test results separately.

Log this prompt and show me the test PDF path, the check results and the files you updated. Keep the submission PDF intact.
```

**Boss actions (Prompt 16):**
- *Smoke test:* `tests/lualatex-smoke/smoke.tex` switched to `style=ieee` (biblatex-ieee v1.4g present). A clean `lualatex → biber → lualatex → lualatex` run passed: 0 errors, 0 missing characters, 0 undefined citations, 0 overfull boxes. At glyph level, the citation `[1]` matches the Hu et al. IEEE entry, the mixed sentence and „(344 שירים)" read correctly, the formula is legible, and both labels sit fully inside their boxes.
- *Open findings:* the bibliography list is shifted 22 pt into the left margin; Arial Hebrew has no italic; the bibliography heading is English. Results are recorded separately in `tests/lualatex-smoke/RESULTS.md`.
- *README:* added „התפתחות הפרויקט" with the user's two sentences verbatim, linked to the audit, PLAN, TODO and the incident log.
- *Incidents:* created `docs/incidents/README.md` (index, template, pending list) and `docs/incidents/INC-001-reversed-tikz-labels.md`, based only on Prompts 5–7, PRD §6/§10, the reviews and `tests/hebrew-sample/sample-nodes.png`. The attribution to Daria comes from the user's statement in this prompt.
- *TODO/PLAN:* updated (D6 done; smoke test done; CLS follow-ups added).
- *Submission PDF:* unchanged.

---

## Prompt 17 — 2026-11-18 — Compare two open-licence font pairings

```text
Test two open-license font pairings for the Hebrew book “מאחורי הפלייליסט”. Match the current design: a Hebrew serif for body text and a sans serif for headings. Use fonts that can be bundled with the project and include their license files and source links.

Create a one-page, side-by-side comparison PDF using LuaLaTeX. Show the same short passage from the book in both columns at the actual reading size. Include a bold Hebrew heading, mixed Hebrew and English text, parentheses, numbers, a TikZ label and an IEEE reference with an italic English title. Use our approved green, charcoal and pink palette.

Inspect the rendered page for word order, missing characters and readability. Recommend one pairing and explain the visible difference in one sentence. Open the comparison PDF in Preview so I can choose. Keep this test separate from the submission PDF and log the prompt and results.
```

**Boss actions (Prompt 17):**
- *Fonts:* downloaded OFL fonts pinned to exact commits/releases into `tests/font-compare/fonts/` (Frank Ruhl Libre, Heebo, Libertinus Serif, Noto Serif/Sans Hebrew, Noto Serif/Sans), each with its `OFL.txt`. Sources are in `fonts/SOURCES.md` and checksums in `fonts/SHA256SUMS`. The Libertinus release zip was moved to the scratchpad after extracting 4 OTFs + OFL.
- *Coverage check (fontTools):* the Noto Hebrew fonts have no digits, Latin or basic punctuation.
- *Comparison:* built `tests/font-compare/comparison.pdf`, one A4-landscape page with the two real column builds at 100% scale.
  - **A** = Frank Ruhl Libre + Heebo + Libertinus; **B** = Noto Serif/Sans Hebrew + Noto Serif/Sans, with a luaotfload fallback.
  - Both builds: 0 errors, 0 missing characters, 0 overfull lines.
  - Glyph-level checks passed: heading, bold, mixed text, brackets, numbers, labels inside their boxes, citations ↔ entries, true italic titles.
- *Issues found and fixed:* the fallback needs the `"[absolute path]"` form; the bibliography labels were clipped by the 22 pt list shift, **fixed by babel `layout=lists`** (this also resolves smoke-test finding 1); a `\makeatletter`-in-hook bug of mine.
- *Recommendation:* pairing A. Results are in `tests/font-compare/RESULTS.md`; the smoke-test RESULTS has an appended update.
- *Opened* `comparison.pdf` in Preview. The submission PDF is unchanged (5e24a1cd…).

---

## Prompt 18 — 2026-11-18 — Font choice (Pairing A); custom class; full LuaLaTeX build

```text
I choose Pairing A: Frank Ruhl Libre for Hebrew body text, Heebo for Hebrew headings, and Libertinus Serif for English text and italics. Use the exact font files and settings that passed the comparison. Bundle the fonts and their licenses.

Implement the custom LaTeX class and use it from book/main.tex. Move the shared design rules and the five layout fixes identified in the audit into the class. Preserve the approved wording, green and pink palette, charcoal cover and playback footer.

Build the full book with LuaLaTeX, Biber and IEEE style. Save the PDF as build/behind-the-playlist-lualatex.pdf for review. Keep the existing submission PDF intact.

Inspect all pages. Check the Hebrew-English word order, the eight diagram blocks, the graph, formula and table. Verify that the bibliography heading reads „מקורות”, its numbered entries fit inside the margins, and all 18 sources resolve. Compare the page count and chapter breaks with the 20-page original. If anything shifts, report where and why.

Record my font choice in the PRD and this prompt in the development log. Open the preview PDF and report the page count and any remaining layout issues.
```

**Boss actions (Prompt 18):**
- *Fonts:* bundled Pairing A in `book/fonts/` (Frank Ruhl Libre, Heebo, Libertinus Serif; OFL texts, `SOURCES.md`, `SHA256SUMS`; byte-identical to the tested files).
- *Class:* created `book/behind-the-playlist.cls` v1.0 from `style.sty`: LuaLaTeX/babel, IEEE via biblatex, the same palette, boxes, chapter openers and playback footer. `book/main.tex` now uses `\documentclass{behind-the-playlist}` and `\printbookbibliography`.
- *The five in-chapter layout edits (audit A2-13) moved into the class:* `\besidetable` and `\sidebyside` (Ch. 3), `comparisontable` (Ch. 4), `herefigure` (Ch. 6), and automatic Latin in headings (Ch. 8, `\enhead` removed). The wording is unchanged. `book/style.sty` is kept, unused, as the source of the XeLaTeX submission v1.1.
- *Build:* added a `make lualatex` target, which writes `build/behind-the-playlist-lualatex.pdf` and leaves `submission/` untouched.
- *Problems found and fixed during review:*
  1. `tabularx` inside a custom environment (fixed with `\table…\endtable`).
  2. Tables were LTR (babel `layout=tabular`).
  3. Cover-detail columns were flush left (new column type `H`; under babel's RTL tables `l`/`r` are swapped).
  4. Running header sides were swapped (fancyhdr L/R are physically reversed under babel).
  5. English words were hyphenated inside Hebrew lines (`hyphenrules=nohyphenation`).
  6. The IEEE style lowercased proper nouns: braced `{Spotify}` and `{Netnews}` in `references.bib` (a bibliography-data fix).
  7. Page 19's footer was built LTR because the page break fell inside the English bibliography (header and footer wrapped in `\inhebrew`).
- *Interruption:* the session ended during the verification build of fix 7. The class edit had already been saved.

---

## Prompt 19 — 2026-11-18 — Resume the interrupted footer fix; finish the review

```text
Resume from the interrupted footer fix on page 19. First inspect book/behind-the-playlist.cls to see whether the edit was saved. Apply any missing part of the fix, then rebuild the LuaLaTeX preview.

Visually verify the page numbers and progress bar on pages 18, 19 and 20. Confirm the preview still has 20 pages, finish any remaining review checks, and report the preview PDF path and any open issues. Keep the existing submission PDF intact.
```

**Boss actions (Prompt 19):**
- Inspected the class. The footer fix (`\inhebrew` around the header, the footer and the plain page style) was saved, and the other Prompt 18 edits were intact.
- The next step (log this prompt + rebuild) was **rejected by the user**. Its rebuild did not run. Its logging part **had already written** the Prompt 19 entry above and a placeholder line for Prompt 18's actions; this was discovered in Prompt 20, and the placeholder was replaced there.

---

## Prompt 20 — 2026-11-18 — Rebuild, verify pages 18–20, then logs and PRD

```text
Rebuild the LuaLaTeX preview using the saved footer fix. Inspect pages 18, 19 and 20 in the rendered PDF and verify the page numbers and progress bar. Report the preview path, total page count and any remaining issues. Then add any missing prompt log entries and record the approved fonts in the PRD. Keep the existing submission PDF intact.
```

**Boss actions (Prompt 20):**
- *Rebuild:* `make lualatex` gave **20 pages**; 0 errors, 0 missing characters, 0 overfull/underfull lines, 0 undefined references or citations.
- *Pages 18–20:* the left footer number is the total "20" and the right is the current page. The green bar fills from the right and the pink dot moves left (x = 141 → 122 → 102 pt). Page 19 is fixed; the footers on pp. 2–20 are all correct.
- *Review checks:* chapter starts are identical to the 20-page original; the bibliography heading is „מקורות", with 18 entries, all inside the margins; 8/8 diagram labels sit inside their blocks; Table 4.1 is RTL; text colours are only charcoal and grey (plus light badge digits).
- *Records:* PRD updated to v1.2 (approved fonts Pairing A, LuaLaTeX engine). The Prompt 18 placeholder was replaced with the full account, and this entry was added.
- *Submission PDF:* unchanged (5e24a1cd…).

---

## Prompt 21 — 2026-11-18 — Approve the LuaLaTeX book as the new submission PDF

```text
I approve the 20-page LuaLaTeX preview as the new book PDF. Keep a local backup of the previous submission PDF, then copy the reviewed preview to submission/behind-the-playlist.pdf. Verify that the two files are identical.

Update the root README with the LuaLaTeX build instructions and regenerate the book screenshots from the approved PDF. Mask student IDs in the README screenshots. Record the approval in the prompt log and update PLAN.md and TODO.md.

Report the final PDF path and the next pending task for the Detector and Fixer agents. Keep GitHub publication and Moodle submission pending.
```

**Boss actions (Prompt 21):**
- *Approval recorded:* the user approved the 20-page LuaLaTeX preview as the new book PDF.
- *Backup:* the previous submission PDF was copied to `backups/behind-the-playlist-v1.1-xelatex-2026-11-14.pdf`, identical to the old file (SHA-256 5e24a1cd…).
- *Submission:* copied `build/behind-the-playlist-lualatex.pdf` to `submission/behind-the-playlist.pdf`. `cmp` reports them byte-identical (SHA-256 43608a86…); 20 pages.
- *README screenshots:* regenerated from the approved PDF, with both cover IDs masked and the page map unchanged. The formula screenshot crop was fixed so it ends above the next heading (`tools/screenshots.py`).
- *README:* LuaLaTeX build instructions (packages including biblatex-ieee, `make pdf` / `make submission`, the manual A2 sequence), bundled OFL fonts, versions, the class in the project structure, MiKTeX marked as untested, and a history note about the retired XeLaTeX build. All 40 links resolve.
- *Makefile:* switched to LuaLaTeX only; checked with a dry run, not a real rebuild, so the approved PDF's checksum stays unchanged.
- *PLAN/TODO:* P1–P3 marked done, P7 partly done, P8 book PDF approved. **Next: P4/P5, the Detector and Fixer Skills.** The ZIP refresh is listed as pending.
- *ID scan:* the IDs appear only in `book/main.tex` (PDFs keep text compressed).
- *Not done, by instruction:* GitHub publication and the Moodle submission remain pending.

---

## Prompt 22 — 2026-11-18 — Red-team QA round: Detector and Fixer agents with project Skills

```text
Run the red-team QA phase from PLAN.md on the approved 20-page LuaLaTeX book. Create separate Detector and Fixer agents with project Skills, and reuse the existing checks for Hebrew/English direction, tables, figures, typesetting, file structure and template version.

Run Detector on the approved PDF and its sources. Have it record each finding with a page or file, evidence, and the expected result. Include the page 19 footer as a regression check.

Pass the report to Fixer automatically. Fixer may edit the template or Skills. If a finding requires a content decision, flag it for us. If Detector finds no actionable defects, record that outcome honestly.

For any fixes, rebuild a separate candidate PDF and have Detector recheck the affected pages and the 20-page count. Preserve the approved submission PDF for comparison.

Save the actual prompts, Skills, run records and a short Hebrew QA summary. Report what each agent did, what passed, and what remains open. Keep this round local.
```

**Boss actions (Prompt 22):**
- *QA machinery:* created `tools/qa/qa_lib.py` + `tools/qa/expectations.json`. They reuse `tools/check_pdf.py`, the glyph-order reading rule, the diagram/table/footer checks, the ID-leak and link scans, and the masked cover render.
- *Project Skills:* created 11 Skills in `.claude/skills/` (detector, fixer, qa-super, qa-typeset, qa-bidi, qa-table, qa-img, qa-code, qa-footer, qa-infra, qa-cls-version) and the agents `.claude/agents/detector.md` and `fixer.md`. Added `make candidate`.
- *Calibration before D1:* the dry run gave 4 harness errors (smoke-test phrase, wrapped table cell, trailing % split, hatch-pattern rects); these were corrected and recorded in `expectations.json` `_calibration`. 1 real failure (stale ZIP).
- *D1 Detector:* ran as a general-purpose subagent bound to the detector definition and Skill, because the agent type was not yet registered. Write scope verified. 55/1/1; findings D1-01…04; p.19 footer PASS.
- *F1 Fixer:* registered type; the report was handed over automatically. Fixed D1-02 (QA bibliography-check bug) and D1-03 (class v1.1 URL break); flagged D1-01 (ZIP) and D1-04 (diagram label). Built candidate `build/behind-the-playlist-candidate.pdf`. The procedure file was read via the shell; no Skill-tool call was recorded.
- *D2 Detector recheck:* registered type. Fixes verified (negative tests in the scratchpad); only p.20 differs; 20 pages; p.19 PASS; **candidate acceptable**.
- *Records:* `docs/qa/round-01/` (README, `summary-he.md`, reports, findings), `SKILLS.md`, `prompts/qa-round-01-*.md`, `docs/agents/tasks/D1/F1/D2`, redacted transcripts + action timelines, `docs/incidents/INC-002`, log rows 6–8, TODO/PLAN.
- *Submission PDF:* unchanged (43608a86…). The candidate was not promoted. Everything stayed local.

---

## Prompt 23 — 2026-11-18 — Show zoomed candidate details; wait for approval

```text
פתח ב־Preview את הקובץ build/behind-the-playlist-candidate.pdf. הראה לי בהגדלה את הכיתוב ״לולאת משוב״ ואת הקו המקווקו לידו בעמוד 14, כדי שאבדוק אם המרווח ביניהם מספיק. אחר כך הראה לי את מקור 13 בעמוד 20, כדי שאראה איפה הקישור עובר לשורה הבאה. חכה לאישור שלי לפני שתעדכן את קובצי ההגשה.
```

**Boss actions (Prompt 23):** opened `build/behind-the-playlist-candidate.pdf` in Preview. Rendered and opened zooms `build/review/p14-loop-label-zoom.png` (600 dpi) and `build/review/p20-ref13-zoom.png` (300 dpi). Measured the gap between the „לולאת משוב" label and the dashed loop line: ≈0.2 pt (≈0.06 mm), i.e. practically touching. Entry [13]: the URL starts on its own line; the only break is after `machine-` (at the hyphen), not inside `https://`. **No submission files were changed; waiting for the user's approval.**

---

## Prompt 24 — 2026-11-18 — Approve ref [13] layout; move the loop label ~2 mm; Detector recheck

```text
אני מאשרת את העימוד של מקור 13 בעמוד 20. בעמוד 14, הזז מעט ימינה את הכיתוב ״לולאת משוב״ כדי להשאיר מרווח של כ־2 מ״מ בינו לבין הקו המקווקו. בנה מחדש את גרסת הבדיקה ובקש מ־Detector לוודא שהכיתוב קריא, שכל שמונת הבלוקים נשארו במקומם ושהספר עדיין כולל 20 עמודים. הצג לי תקריב מעודכן של התרשים וחכה לאישור שלי לפני עדכון קובץ ההגשה וה־ZIP.
```

**Boss actions (Prompt 24):**
- *Edit:* moved the label in `book/figures/pipeline.tex` (the users' decision on D1-04; a coordinator edit, since figures are content files).
- *Two failed attempts* (recorded honestly):
  1. With an `overlay` label alone, the picture narrowed and centring shifted the blocks by about 6 pt.
  2. With an invisible point, the node's inner padding was missing, so the blocks shifted 2.5 pt and one list line moved from p.15 to p.14.
- *Final fix:* a phantom copy of the label at its old place plus the visible label as an overlay. The blocks and dashed line are identical to the approved PDF; gap 2.00 mm (glyph box).
- *Rebuild:* `build/behind-the-playlist-candidate.pdf` (ed844348…), 20 pp, 0 overfull.
- *Detector D3:* verdict **acceptable**; gap 1.86 mm measured by ink; new D3-01 (skill) and D3-02 (0.51 mm overhang).
- *Close-ups* opened in Preview: `build/review/p14-diagram-v2.png`, `build/review/p14-loop-label-zoom-v2.png`.
- **Submission PDF and ZIP not changed; waiting for the user's approval.**

---

## Prompt 25 — 2026-11-18 — Approve the candidate; update submission PDF and ZIP

```text
אני מאשרת את העימוד בעמוד 14 ואת גרסת הספר שבדקת. שמור גיבוי של קובץ ההגשה הקודם, עדכן את קובץ ההגשה ואת ה־ZIP, ובדוק שה־PDF בתוך ה־ZIP זהה לגרסה שאישרתי וכולל 20 עמודים. תעד שהבדיקה הידנית של הכיתוב עברה ושכלי הבדיקה האוטומטי עדיין דורש תיקון. הצג לי את הנתיבים של ה־PDF ושל ה־ZIP. השאר את הפרסום ב־GitHub ואת ההגשה ב־Moodle לאישור נפרד.
```

**Boss actions (Prompt 25):**
- *Backups:* the previous submission PDF went to `backups/behind-the-playlist-v1.2-lualatex-cls1.0-2026-11-18.pdf` (43608a86…) and the old ZIP to `backups/project-source-2026-11-14.zip`.
- *Submission PDF:* `submission/behind-the-playlist.pdf` = the approved candidate, byte-identical by `cmp` (SHA-256 ed844348…), 20 pages.
- *README screenshots:* regenerated from it (IDs masked; page map unchanged).
- *Records:* the manual check of „לולאת משוב" (passed, D3) and the open tool defect D3-01 recorded in `docs/qa/round-01/README.md` and `TODO.md`.
- *ZIP:* `tools/package.py` now also packs PLAN/TODO/SKILLS, the class, fonts and licences, Skills, `tools/qa`, `prompts/`, `docs/qa`, incidents, the audit and test results.
  - Rebuilt `submission/project-source.zip`: 203 files.
  - Verified by extraction: integrity OK; the PDF inside is identical to the approved PDF and has 20 pages; 30/30 required files present; no lecturer PDFs, backups or build files; 40/40 README links resolve; no IDs outside `main.tex`/PDFs.
  - `qa-infra` now passes, so D1-01 is resolved.
- *GitHub and Moodle:* not done; they wait for separate approval.

---

## Prompt 26 — 2026-11-18 — Prepare a public GitHub copy (no IDs, no submission date on the cover); wait before publishing

```text
הכן עותק לפרסום ב־GitHub של הפרויקט ״מאחורי הפלייליסט״. הסר מהעותק הציבורי את מספרי תעודת הזהות ובדוק גם את עמוד השער ב־PDF, קובצי המקור וצילומי המסך. ודא שהקישור לספר מתוך ה־README מוביל לעותק הציבורי. שמור את קובצי ההגשה המקוריים בתיקיית submission. הצג לי אילו קבצים הכנת והמתן לאישור שלי לפני הפרסום.בעותק הציבורי, הסר את השורה ״תאריך הגשה״ מהשער, כולל התאריך עצמו. עדכן את קובץ ה־LaTeX, הפק ממנו את ה־PDF הציבורי ורענן את צילום השער ב־README. בתיקיית ההגשה ל־Moodle שמור את הגרסה המקורית שאישרתי.
```

**Boss actions (Prompt 26):**
- *Script:* created `tools/make_public.py` and a `--expect-ids` option in `tools/screenshots.py`.
- *Public copy:* built `public-release/behind-the-playlist/` (243 files) from the same curated list as the ZIP. It excludes `submission/`, `backups/`, `build/` and the lecturer PDFs, and adds a `.gitignore`.
- *Public `book/main.tex`:* the ID column and the „תאריך הגשה" row are removed from the cover.
- *Public PDF:* `pdf/behind-the-playlist.pdf`, built with LuaLaTeX + Biber: 20 pp, all checks pass, text differs from the approved PDF only on p.1. README screenshots were refreshed from it (cover without IDs or date). The README's book link now points to `pdf/behind-the-playlist.pdf`, with a public-edition note; 40/40 links resolve.
- *Verification:* no student IDs anywhere in the copy (bytes and PDF text); no date on the public cover.
- *Open question for the user:* the date remains in the historical QA cover renders (IDs masked) and in the prompt-log text.
- *Unchanged:* `submission/` (PDF ed844348…, ZIP f93fcd0a…) and the main project. **Nothing published; waiting for approval.**

---

## Prompt 27 — 2026-11-18 — Remove the submission date from the entire public copy; wait before publishing

```text
הסר את תאריך ההגשה [תאריך ההגשה הושמט] מכל העותק הציבורי. בשלושת צילומי השער הישנים, הסתר את שורת תאריך ההגשה. ביומן הפרומפטים, בתמלילי הסוכנים ובדוחות הבדיקה החלף את תאריך ההגשה במילים ״[תאריך ההגשה הושמט]״. התאם גם את הבדיקה האוטומטית לשער הציבורי. שמור את תאריכי העבודה ואת התיעוד המקורי בתיקיית הפרויקט. בסיום, בדוק את הצילומים ואת הקבצים, ודא שכל 40 הקישורים ב־README עובדים, והמתן לאישור שלי לפני הפרסום ב־GitHub.
```

**Boss actions (Prompt 27):**
- *Automated check:* `tools/qa/qa_lib.py` gained `--edition submission|public`, the default coming from `expectations.json`.
  - The public edition reads the four public cover lines (`cover_public` in `tools/qa/expectations.json`).
  - It adds a blocker check that fails if the cover shows a 9-digit number, a date, or the „תאריך הגשה" / „ת״ז" labels. A failure reports counts only, never the values.
  - The cover-masking step expects 0 IDs in the public edition; the ZIP check is n/a there.
  - Tested both ways: the public PDF passes and the submission PDF fails, as intended.
  - Submission edition rerun: 56 pass, 0 fail, 1 n/a.
- *`tools/make_public.py`:* reads the date from the private `main.tex`, so the script never contains it.
  - It replaces the date with „[תאריך ההגשה הושמט]" in every text file of the copy: the prompt log, three agent transcripts (JSONL still valid), three QA `findings.json` files and the expectations.
  - It masks the date row ("date hidden") in the three old QA cover renders; the ID masks are kept, checked visually.
  - It marks the copy's expectations `"edition": "public"`.
- *Verification of the copy* (243 files):
  - no submission date and no student IDs in any file (bytes and PDF text);
  - public cover without date or IDs;
  - 40/40 README links resolve;
  - qa-super on the public edition: 55 pass, 0 fail, 2 n/a (qa-code; ZIP check).
- *Kept in the project:* the original records (with the date) and all work dates. `submission/` is unchanged.
- **Nothing published; waiting for approval.**
