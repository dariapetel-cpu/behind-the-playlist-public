# INC-001 — Reversed Hebrew word order in TikZ diagram labels

| Field | Value |
|---|---|
| Status | **Closed** (fixed 2026-11-11; the rule still applies) |
| Found by | **Daria**, by eye, in the opened sample PDF. The report is user Prompt 7 (`docs/prompts.md`, line 102); the attribution to Daria is the user's statement in Prompt 16 |
| Missed by | The coordinator's (Boss's) own inspection in Prompts 5 and 6. No agent reviewer existed yet: the Reviewer agent first ran on 2026-11-14 |
| Fixed by | The coordinator (Boss), 2026-11-11 (Prompt 7) |
| Affected file | `tests/hebrew-sample/sample.tex` (the XeLaTeX toolchain smoke test). The rule then went into `book/style.sty` and `book/figures/pipeline.tex` |
| Sources | `docs/prompts.md` (Prompts 5, 6 and 7 with their "Boss actions"); `PRD.md` §6 "TikZ RTL rule" and §10 "Correction (Prompt 7)"; `tests/hebrew-sample/sample-nodes.png` (the 400 dpi verification close-up) |

## Symptom

In the one-page Hebrew test PDF, all three diagram boxes showed their two words in reversed order. The source said „איסוף אותות", „דירוג מועמדים" and „הצגת המלצות", but the PDF read „אותות איסוף", „מועמדים דירוג" and „המלצות הצגת". The main Hebrew paragraph on the same page was correct.

## How it was found

Daria opened `tests/hebrew-sample/sample.pdf` after the coordinator reported the test as passed (Prompt 6). She saw that the word order inside every TikZ node was reversed, while the paragraph above read correctly. She asked for a fix that keeps the source text in natural order and the flow right to left (Prompt 7).

## Why the first review missed it

The "first review" was the coordinator's check in Prompts 5 and 6. Both reported **PASS** (`docs/prompts.md` lines 85 and 95). The records show four gaps:

1. **The check was visual only.** The coordinator judged word order from a rendered image. PRD §10 records the correction: "the Boss's image-only check had missed it".
2. **The automated checks could not see this kind of error.** They covered compile errors, missing glyphs, over/underfull boxes and clipping, and all of these were genuinely 0. A reversed label has no missing glyph and no overflow.
3. **Text extraction was misleading for right-to-left lines.** Later records (PRD §6 "Verification rule") note that PyMuPDF's word-level extraction reorders RTL strings by itself. So a string read back from the PDF can look right or wrong independently of what is printed.
4. **There was no expected-text comparison.** The check never asserted "the first word lies to the right of the second" for multi-word labels. Parentheses were checked at glyph level in Prompt 5, but node word order was not.

## Root cause

TikZ typesets node text in a horizontal box (`\hbox`) that runs left to right. Inside that box the paragraph direction does not apply, so XeTeX lays out the words left to right even when each word's letters are right to left.

## Fix

- **First attempt:** `\setRTL` at the start of each node. It had **no effect**, because `\setRTL` changes paragraph direction and node text is a box, not a paragraph.
- **Working fix:** wrap node text in XeTeX's `\beginR … \endR` through one style (`every node/.append style={execute at begin node=\beginR, execute at end node=\endR}`), with the source text left unchanged.
- **Later refinement:** this became the `heb` style in `book/style.sty`. A follow-up finding was that any colour change inside a `heb` node turns the text white, which led to `\hebcolor` (PRD §6).

## How the correction was verified

1. **Numerically, at glyph level.** The coordinator extracted the x-positions of every word and letter. In all three nodes the first word now lay entirely to the right of the second, and letters ran right to left within each word. The node order still flowed right to left.
2. **Visually**, with a 400 dpi close-up of the three nodes (`tests/hebrew-sample/sample-nodes.png`).
3. **Clean rebuild:** 0 errors, 0 missing characters, 0 bad boxes.
4. **Rule recorded** in PRD §6: word order in the PDF is checked from **glyph x-positions**, not from an image alone.
5. **Applied in every later build:**
   - The eight-block diagram's 18 labels passed glyph-level checks on 2026-11-14 (Prompt 11) and after the palette change (Prompt 13).
   - The Reviewer agent's V1 and V2 passes also reported "no reversed text" on every page. Their checks were visual, so the glyph checks remain the authoritative evidence.

## Prevention and lessons

- For right-to-left text, **"looks right" is not evidence**. Assert the order from glyph positions.
- Automated checks must include **content-order assertions**, not only error, glyph and overflow counts. This is planned as the `qa-bidi` Skill (`TODO.md` P4).
- The bug was found by a human reader after the coordinator reported PASS. That is the gap the Detector/red-team Skills must close (`PLAN.md` P4–P5).
- The LuaLaTeX port needs the same assertion. In today's smoke test (`tests/lualatex-smoke/RESULTS.md`), labels are checked inside their boxes at glyph level; under LuaLaTeX the TikZ fix is babel's `layout=graphics`, not `\beginR…\endR`.
