# PRD — „מאחורי הפלייליסט" (Behind the Playlist)

*Status: **v1.2, in progress** · 2026-11-18 · Owner: Boss (coordinating agent)*
*v1.2 (2026-11-18, Prompts 18–20): **fonts approved by the user: Pairing A**; custom class `book/behind-the-playlist.cls` v1.0; LuaLaTeX + Biber + IEEE preview builds at 20 pages (`build/behind-the-playlist-lualatex.pdf`). The submission PDF (v1.1, XeLaTeX) is unchanged until the new build is approved.*
*v1.1: final palette (charcoal / green / pink / light page) applied throughout (§6); submission package `submission/project-source.zip` added (D11).*
*v1.0: project delivered. Cover details supplied by the user (no institution line, by user request; student IDs only in the submission PDF and `book/main.tex`); second Reviewer pass (review-02: APPROVE WITH MINOR NOTES) and its notes addressed; README, submission copy and the delivered state recorded in §11.*
*v0.3: bibliography direction decided (§6, §8.3); full 20-page manuscript built and reviewed (review-01).*
*v0.2: toolchain installed and verified (§10); engine fixed to XeLaTeX; font rule from the Hebrew smoke test (§6); agent definitions created, none run yet (§7).*

## 1. Summary

A visually designed Hebrew book of about 20 pages that explains how music recommendation systems work. The reader follows a fictional listener through everyday listening situations (morning commute, workout, studying, a party, a breakup playlist...). Each situation introduces one mechanism, explained accessibly with light humor and backed by verifiable research.

The book is a university project. Besides the book itself, it must document how it was made: a prompt log and evidence that three specialist agents (Researcher, Writer, Reviewer) worked on it under a coordinating Boss.

## 2. Goals and non-goals

**Goals**
- Explain the main ideas behind music recommendation (collaborative filtering, content and audio features, context and sessions, feedback signals, exploration vs. exploitation, cold start, filter bubbles and diversity) to a non-technical Hebrew reader.
- Ground every factual claim in a verifiable, cited source.
- Produce a polished, consistent, print-quality PDF with correct right-to-left Hebrew layout.
- Make the process reproducible: anyone can rebuild the PDF from source.

**Non-goals**
- Revealing or reconstructing Spotify's (or any company's) actual production algorithm. Illustrative models are always labelled as educational simplifications.
- Training or running a real recommender on real user data.
- A general orchestration framework for agents.

## 3. Audience and tone

- **Audience:** Hebrew-speaking students and curious listeners with no technical or math background beyond high school.
- **Tone:** friendly, lightly humorous, never condescending. Humor lives in the listener's story, not in the facts.
- **Voice:** the fictional listener's scenes, followed by short explanations, then an emphasis box with the key takeaway.

## 4. Deliverables

| # | Deliverable | Location (delivered) | Status |
|---|---|---|---|
| D1 | Compiled book PDF, 20 pages | `submission/behind-the-playlist.pdf` (identical to `build/behind-the-playlist.pdf`) | ✅ |
| D2 | LaTeX source (main file, chapters, style file) | `book/main.tex`, `book/chapters/00–08`, `book/style.sty` | ✅ |
| D3 | Bibliography database | `book/references.bib` (18 verified entries) | ✅ |
| D4 | Python script generating the graph + fictional data file | `figures/noa_week.py`, `figures/data/noa_week.csv` | ✅ |
| D5 | TikZ eight-block recommendation process diagram | `book/figures/pipeline.tex` (Fig. 6.1, p. 14) | ✅ |
| D6 | `README.md` (Hebrew) with build instructions and screenshots from the final PDF | `README.md`, `docs/screenshots/` (cover IDs masked) | ✅ |
| D7 | `PRD.md` (this file) | repo root | ✅ |
| D8 | Development prompt log (verbatim user prompts; student IDs redacted with a label in Prompt 12) | `docs/prompts.md` | ✅ |
| D9 | Agent work evidence: tasks, outputs, transcripts, reviews and the call log | `docs/agents/` (`log.md`, `tasks/`, `transcripts/`, `research-notes.md`, `review-0N.md`, `review-0N-response.md`) | ✅ |
| D10 | Single-command build | `Makefile` (`make submission`) + `tools/` | ✅ |
| D11 | Source package (sources, evidence, README with screenshots, PDF) | `submission/project-source.zip` (verified by extraction) | ✅ |

## 5. Content requirements

### 5.1 Book structure
1. **Title page** — Hebrew title „מאחורי הפלייליסט", subtitle, author/course details, a visual element.
2. **Abstract (תקציר)** — about half a page.
3. **Table of contents.**
4. **Chapters** — roughly 5–7 chapters, each built around one listening situation of the fictional listener. Tentative arc (subject to Researcher findings):
   - Introduction: meet the listener; why recommendation exists at all.
   - Signals: what the system learns from plays, skips, saves, repeats.
   - "People like you": collaborative filtering and similarity.
   - "Songs like this": content/audio features and metadata.
   - Context and sessions: time, activity, sequence.
   - Exploration, cold start, and new artists.
   - Filter bubbles, diversity, fairness, and what the listener can do.
   - Conclusion.
5. **Bibliography (מקורות)** — generated by the bibliography tool from `references.bib`.

### 5.2 Mandatory elements
- **Graph (≥1):** generated by Python/matplotlib from a data file in the repo; Hebrew labels rendered correctly; style matches the book palette. If it uses invented data, the caption says so explicitly.
- **Table (≥1):** e.g. the fictional listener's listening log or a comparison of recommendation approaches.
- **Formula (≥1):** e.g. cosine similarity between listeners or songs, with:
  - a plain-language explanation of every symbol,
  - a fully worked numerical example with small numbers,
  - a label stating it is an educational formula, not a description of any company's system.
- **Eight-block diagram:** the recommendation process (e.g. collect signals → clean/aggregate → represent users & songs → generate candidates → score/rank → filter & diversify → present → collect feedback, looping back). Built in TikZ as editable vector objects, with RTL-correct Hebrew labels.
- **Emphasis boxes:** at least three types, used consistently, e.g. „בקצרה" (key takeaway), „רגע, זה אמיתי?" (fact vs. myth / research note), „מעבדה" (formula or worked example), and a distinct style for fictional-data notices.

### 5.3 Research and honesty rules
- Every factual claim about how recommender systems work, about specific companies, or about research findings cites a source in the bibliography.
- Sources must be verifiable: peer-reviewed papers, books, official engineering/research blogs, or reputable journalism. Each `.bib` entry has a DOI or URL where possible.
- Aim for at least 10 distinct sources, with at least 4 academic.
- Statements about Spotify or other companies are attributed to what that company has publicly said ("according to Spotify's research blog...") and never extrapolated into claims about its actual algorithm.
- All fictional listening data, people, and numbers are marked as fictional in the caption or the box where they appear.
- No invented citations. The Reviewer checks every cited source against the claim it supports.

## 6. Design requirements

- **Engine (from v1.2):** LuaLaTeX + babel (`bidi=basic`, `layout=graphics.lists.tabular`, `onchar=ids fonts`; English `hyphenrules=nohyphenation`), with the custom class `book/behind-the-playlist.cls` v1.0; bibliography biblatex `style=ieee` + Biber. Build: `make lualatex`. *(Until v1.1: XeLaTeX + polyglossia/bidi with `book/style.sty`; that build produced the current submission PDF.)*
- **Font rule (from the smoke test):** Arial Hebrew has no Latin glyphs, and math and Latin text use `\setmainfont`. The main font must therefore cover Latin, and Hebrew runs use `\hebrewfont`. Every build must have **0 "Missing character" lines** in the log.
- **TikZ RTL rule:** TikZ typesets node text in a left-to-right `\hbox`, where `\setRTL` has no effect, so multi-word Hebrew labels come out in reversed word order. All Hebrew TikZ nodes use the `heb` style from `style.sty` (`execute at begin node=\beginR, execute at end node=\endR`). Inside a `heb` node, any colour change (`text=<color>` or `\color`) renders the text **white**, so coloured Hebrew node text uses `\hebcolor{<color>}{<text>}` without `heb`, which keeps the colour outside the RTL segment, and the source text stays in natural order. **Verification rule:** word order in the PDF is checked numerically, from **glyph** x-positions (PyMuPDF `rawdict`; its word-level extraction reorders RTL strings itself), so that in RTL the first word lies to the right of the next, and not by reading a rendered image alone.
- **Direction:** all running text, headings, TOC, captions and lists read right-to-left; embedded English terms and numbers render correctly in LTR. **Bibliography (decision 2026-11-14, review-01 #5):** the heading „מקורות" is RTL, and the entries, which are all English-language sources, are set LTR, as is usual in Hebrew academic texts.
- **Typography:** one Hebrew body font, one Hebrew heading font (or weights of the same family), one Latin companion font; fonts are licensed for this use and named in the README.
- **Approved fonts (user's choice, 2026-11-18, Prompt 18): Pairing A.** All are bundled in `book/fonts/` with their OFL 1.1 licences, pinned sources (`SOURCES.md`) and checksums (`SHA256SUMS`). The files are byte-identical to those that passed `tests/font-compare/`.

  | Role | Font | Scale |
  |---|---|---|
  | Hebrew body | **Frank Ruhl Libre** (Regular, Bold) | 0.96 |
  | Hebrew headings, captions, tags | **Heebo** (Regular, Bold) | 0.97 |
  | English text, italics, math roman | **Libertinus Serif** (Regular, Italic, Bold, BoldItalic) | 1.03 |

  The scales match the previous book's letter heights. These fonts replace the macOS system fonts (New Peninim MT, Arial Hebrew, Times New Roman, Arial). New Peninim MT also failed under LuaLaTeX (text vanished after `\section`; `tests/lualatex-smoke/RESULTS.md`).
- **Color palette (final, Prompt 13, 2026-11-14):** four colours, defined once in `book/style.sty` and mirrored in `figures/noa_week.py`. They replaced the earlier teal/coral/navy palette.

  | Colour | Hex | Use |
  |---|---|---|
  | Dark charcoal | `#121212` | cover background; all body text, headings, captions, box titles and diagram labels |
  | Bright green | `#1ED760` | cover subtitle and waveform; chapter equalizer bars and title rule; „בקצרה" box rule and light fill; data blocks of the diagram; chart series "plays"; footer progress line |
  | Neon pink | `#FF2E88` | cover and equalizer accents; „רגע, זה אמיתי?" box rule and light fill; user blocks and feedback-loop arrow of the diagram; chart series "skips" (hatched); list bullets; footer position dot |
  | Light page background | `#F2F2F2` | every reading page; light text on the cover |

  **Contrast rules (measured, WCAG):**
  - Charcoal on the page is 16.7:1; on green 9.8:1; on pink 5.4:1.
  - Green (1.7:1) and pink (3.1:1) on the page are never used for text, only for fills, rules, bars and dots.
  - Small grey text uses `#555555` (6.7:1).
  - Every fill that carries text gets charcoal text, except the charcoal badges, which use light digits.
  - An audit of all text spans in the final PDF found no text below 4.5:1 on pages 2–20.
- **Layout:** A4 or B5, comfortable margins, line spacing about 1.2–1.4, no overfull lines visible in the PDF, no widows of headings at page bottoms, figures close to their reference.
- **Consistency:** all boxes, captions, and chapter openers share one style defined in a single style file.

## 7. Process and agent roles

| Role | Responsibility | Main outputs |
|---|---|---|
| **Boss** (main session) | Plans, writes briefs, integrates, builds the PDF, keeps logs, talks to the user | PRD, logs, LaTeX integration, build |
| **Researcher** | Finds and verifies sources; writes a fact sheet with claim → source pairs | `docs/agents/research-notes.md`, `book/references.bib` |
| **Writer** | Writes Hebrew chapter text from the outline and fact sheet only | chapter `.tex` files |
| **Reviewer** | Checks facts against sources, labelling of fictional data, Hebrew quality, and the rendered PDF against this PRD | `docs/agents/review-*.md` with issues and verdict |

Agents are defined in `.claude/agents/{researcher,writer,reviewer}.md` and run through Claude Code's built-in Agent tool, using the existing Claude login with no orchestration framework. They hand work to each other through files in `docs/agents/`, not through long prompts. The planned budget is about 5–6 calls in total. A definition file existing does not count as a run.

Every agent call is recorded in `docs/agents/log.md` (date, agent, brief, files read, files produced, outcome). User prompts are recorded verbatim in `docs/prompts.md`; no earlier exchanges are invented.

## 8. Acceptance criteria

The project is done when all of the following hold:

1. `build/behind-the-playlist.pdf` builds from a clean checkout with one documented command and no LaTeX errors.
2. The PDF has 18–24 pages, including a title page, abstract, TOC, chapters, and bibliography in this order.
3. Hebrew text, headings, TOC and captions are right-to-left, and the bibliography follows the §6 decision (RTL heading, LTR English entries); mixed English/numbers render in the correct order (checked visually on every page, with glyph-level checks for diagrams, graph and table).
4. At least one Python-generated graph, one table, and one formula with symbol explanation and a worked numerical example are present.
5. The eight-block diagram is TikZ source in the repo (not a raster image) and shows exactly eight labelled blocks.
6. Every chapter cites at least one source; every bibliography entry is cited at least once; no citation is unverifiable.
7. All fictional data and educational formulas are explicitly labelled; no text claims an illustrative model is Spotify's actual algorithm.
8. Colors, fonts, and box styles are consistent throughout (Reviewer sign-off).
9. `README.md` explains prerequisites, build steps, and project structure, and shows screenshots rendered from the final PDF.
10. `docs/prompts.md` contains all user prompts verbatim; the agent log shows real outputs from Researcher, Writer, and Reviewer.

## 9. Risks and open questions

- **Toolchain:** resolved, see §10.
- **TeX mirrors:** the CTAN redirector once picked an unresponsive mirror and `tlmgr` hung. Future `tlmgr` calls should pin a working mirror with `--repository`.
- **Bibliography in RTL:** biblatex + biber with Hebrew can need tuning; fallback is a manually styled bibliography environment.
- **Hebrew in matplotlib:** matplotlib does not shape RTL text; labels may need reordering (e.g. `python-bidi`) or the graph can use minimal text with Hebrew captions in LaTeX.
- **Font licensing:** macOS system Hebrew fonts are fine for local builds; open fonts (e.g. Google Fonts Hebrew families) would make builds portable.

## 10. Verified environment (2026-11-11)

| Component | Version / detail |
|---|---|
| macOS (Intel x86_64) | 14.8.9 |
| TeX | BasicTeX 2026 (official CTAN `.pkg`, SHA-512 checked, Apple-notarized), XeTeX, LuaTeX |
| Added TeX packages | bidi zref biblatex biber tcolorbox tikzfill pdfcol environ trimspaces titlesec enumitem csquotes footmisc emptypage xstring logreq babel-hebrew hebrew-fonts latexmk (installed via `tlmgr --repository https://ctan.mirror.norbert-ruehl.de/systems/texlive/tlnet`) |
| Already in BasicTeX | fontspec, polyglossia, pgf/TikZ, xcolor, hyperref, geometry, amsmath, fancyhdr, caption, booktabs, setspace |
| Tools | biber 2.22, latexmk 4.89 |
| Python (`.venv`, 3.13.2) | matplotlib 3.11.2, numpy 2.5.4, python-bidi 0.6.12, PyMuPDF 1.28.2 (binary wheel; a source build fails on this Mac) |
| Hebrew fonts (system) | Arial Hebrew, SF Hebrew (+ Rounded), New Peninim MT, Raanana, Corsiva Hebrew, Times New Roman, Arial |

**Hebrew smoke test** (`tests/hebrew-sample/sample.tex`, built with `latexmk -xelatex`): **PASS after two fixes**. *Correction (Prompt 7):* the earlier PASS was wrong about the TikZ labels. The user found their word order reversed (for example „אותות איסוף“), and the Boss's image-only check had missed it. That was fixed with `\beginR…\endR` (§6) and re-verified numerically. The first build had 7 "Missing character" warnings (Latin letters in math with Arial Hebrew as the main font). After the font fix (§6), the build had 0 errors, 0 missing characters and 0 over/underfull boxes. Rendered at 150/300 dpi with PyMuPDF and checked:
- the heading is right-aligned with its number on the right,
- RTL paragraph text, inline English, numbers (30, 1,234, 87%) and the date 11/11/2026 are in the correct order,
- parentheses are mirrored correctly (checked at glyph level),
- the tcolorbox title is on the right,
- the TikZ arrows flow right to left; node labels read „איסוף אותות“, „דירוג מועמדים“, „הצגת המלצות“ (first word right of second, checked by word x-positions),
- all content is inside the margins.

## 11. Delivered state (2026-11-14)

**Page map (from the final PDF):**

| Pages | Content |
|---|---|
| 1 | Cover |
| 2 | Abstract |
| 3 | Table of contents |
| 4–18 | Ch. 1–8 (starting on pp. 4, 6, 8, 10, 12, 14, 16, 18) |
| 19–20 | Bibliography |

Required elements: Python graph Fig. 2.1 on p. 7; cosine formula with symbol explanations and a worked example on pp. 8–9; comparison Table 4.1 on p. 11; eight-block TikZ diagram Fig. 6.1 on p. 14.

**Acceptance criteria (§8):**

| # | Result |
|---|---|
| 1 | Pass: `make submission` builds with 0 errors |
| 2 | Pass: 20 pages, in the required order |
| 3 | Pass: RTL per §6, with LTR English bibliography entries |
| 4 | Pass |
| 5 | Pass |
| 6 | Pass: all 18 entries cited; every chapter cites ≥1 source |
| 7 | Pass |
| 8 | Pass: Reviewer sign-off in review-02 |
| 9 | Pass: Hebrew README; links and screenshots verified against the submission PDF (pixel-identical renders) |
| 10 | Pass: see below |

Criteria 1, 9 and 10 were verified by the Boss after review-02, so the Reviewer did not check them.

**Agent runs (5 in total), each recorded in `docs/agents/log.md`:**

| Run | Agent | Task | Result |
|---|---|---|---|
| R1 | Researcher | sources and research notes | completed |
| W1 | Writer | abstract and Ch. 1–4 | completed |
| W2 | Writer | Ch. 5–8 | completed |
| V1 | Reviewer | full review | CHANGES REQUESTED; 36 issues, 5 major |
| V2 | Reviewer | focused re-review | APPROVE WITH MINOR NOTES |

The Boss addressed every finding and documented the actions in `review-01-response.md` and `review-02-response.md`. No third review pass was run. The N1–N6 fixes after review-02 were verified by the Boss only.

**Design decisions:**

| Decision | Where |
|---|---|
| Bibliography: Hebrew heading, English entries LTR, ragged-right | §6 |
| Entries with a DOI print the DOI only (URL and access date suppressed at print time; still in the `.bib`) | `style.sty` |
| Hebrew TikZ text uses `[heb]` or `\hebcolor` | §6 |
| In RTL tables, `\raggedleft` = flush right | `04-shirim-kmo-ze.tex` |

**Privacy:** the student IDs appear only in `book/main.tex` and the PDFs. A repository scan confirmed they are absent from every other file.

**Known minor issues (accepted):**
- p. 13 is ≈28% full (end of Ch. 5).
- English glosses in parentheses may break across lines.
- The Ch. 1 fact box splits across pp. 4–5.
- The build relies on macOS system fonts.

