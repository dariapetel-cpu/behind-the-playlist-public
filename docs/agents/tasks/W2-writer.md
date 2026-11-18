# Task W2: Writer (sent by Boss, 2026-11-14)

Run via Claude Code's built-in Agent tool, `subagent_type: writer` (definition: `.claude/agents/writer.md`). The agent prompt points to this file; the task text is below the line.

---

Task W2 (date 2026-11-14): write **Chapters 5–8** of „מאחורי הפלייליסט". Do not edit the abstract or Ch. 1–4.

Read only:
- `docs/agents/brief.md`
- `docs/outline.md`: the page-plan rows for Ch. 5–8 and "Where the required elements are"
- `docs/agents/research-notes.md`: the Ch. 5–8 sections and "Gaps / unverified"
- the keys in `book/references.bib`
- the WRITER INTERFACE block in `book/style.sty`
- `book/chapters/01-boker-tov.tex` … `04-shirim-kmo-ze.tex`, **for tone, terminology and box usage only** (do not repeat their content; refer back to them, e.g. „בפרק 3")
- `book/figures/pipeline.tex`, to see the eight block labels

Files to write. Each starts with `% Author: Writer agent · 2026-11-14`.

| File | Content | Target length |
|---|---|---|
| `book/chapters/05-hasha.tex` | `\chapter{הפלייליסט יודע מה השעה}\label{ch:5}` | ≈ 450 words, 2 pages |
| `book/chapters/06-shmone-tachanot.tex` | `\chapter{שמונה תחנות בדרך לשיר הבא}\label{ch:6}` + diagram + one short paragraph per block | ≈ 480 words + diagram, 2 pages |
| `book/chapters/07-bua.tex` | `\chapter{בועה עם פסקול}\label{ch:7}` | ≈ 500 words, 2 pages |
| `book/chapters/08-play.tex` | `\chapter{נועה לוחצת Play}\label{ch:8}`. Write "Play" as `\en{Play}` in the body; the chapter title may contain the raw word | ≈ 250 words, 1 page |

Keep the same structure and tone as Ch. 1–4: a `scene` box (Noa, light humor) → explanation with `\section{}` → optional `realitycheck` → closing `inshort`. Ch. 8 may skip the `realitycheck` and instead end with 6 key takeaways (one per Ch. 1–6 or 2–7), plus a last light line.

Content rules (same as W1):
1. Every factual claim cites a verified key with `\cite{}`, at the strength stated in research-notes.md. Respect every item under "Gaps / unverified":
   - Ch. 5: context in general only (schedl2018current); Noa's gym and study times are scene detail, not a platform claim; explore–exploit and bandits from mcinerney2018explore; sessions and sequences from brost2019music. No formula.
   - No Daily Mix, Discover Weekly or radio internals.
   - Ch. 7: cite only what anderson2020algorithmic, kowald2020unfairness, mehrotra2018towards and chaney2018algorithmic support. Present the findings with nuance, not doom. Spotify's user controls and Discovery Mode must be attributed to Spotify (spotify2026understanding).
2. Keep **[PLATFORM CLAIM]** and **[GENERAL METHOD]** apart, as in W1. Never write "this is how Spotify works".
3. Noa and the people in her story are fictional: put scenes in `scene`, put any invented numbers mid-sentence with `\fictional`, and never start a paragraph with `\fictional` or `\educational`.
4. Keep terminology consistent with Ch. 1–4: סינון שיתופי, המלצה מבוססת תוכן, משוב משתמע, בעיית ההתחלה הקרה, דמיון קוסינוס, פירוק מטריצות. Introduce new terms once with `\term{}{}`, e.g. חקירה/ניצול (exploration/exploitation), יצירת מועמדים (candidate generation), דירוג (ranking), לולאת משוב (feedback loop), הטיית פופולריות (popularity bias).

**Ch. 6 diagram (built by the Boss; insert exactly this, near the top of the chapter after the scene):**
```latex
\begin{figure}[t]
  \centering
  \input{figures/pipeline.tex}
  \caption{<Hebrew caption saying this is an educational simplification of the book, not the internal architecture of any platform> \educational}
  \label{fig:pipeline}
\end{figure}
```
Refer to it as `איור~\ref{fig:pipeline}`. The eight blocks, in order:
1. איסוף אותות
2. ניקוי ואיחוד נתונים
3. ייצוג משתמשים ושירים
4. יצירת מועמדים
5. דירוג
6. סינון וגיוון
7. הצגת המלצות
8. משוב ולמידה
The dashed arrow from 8 back to 1 is labelled „לולאת משוב". The colour groups are נתונים (1–3), מודל (4–6), משתמש (7–8).

Requirements for Ch. 6:
- State in the text, and not only in the caption, that the eight-block division is the book's own educational simplification. What the sources support is the general pattern of candidate generation → ranking → re-ranking/filtering (google2026overview, covington2016deep) and the feedback loop (chaney2018algorithmic). Blocks 1–3 are a reasonable framing that no single source lists.
- Explain each block in 1–3 sentences with a running example from Noa's evening. A numbered `enumerate` list is fine; a `description` list is not, as it is untested in RTL.

When done, reply in ≤10 lines: files written, approximate word counts, the keys used, and any claim dropped for lack of a source.
