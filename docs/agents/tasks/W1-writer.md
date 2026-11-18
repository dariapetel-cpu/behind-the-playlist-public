# Task W1: Writer (sent by Boss, 2026-11-14)

Run via Claude Code's built-in Agent tool, `subagent_type: writer` (definition: `.claude/agents/writer.md`). The prompt sent is the text below the line.

---

Task W1 (date 2026-11-14): write the Hebrew **abstract** and **Chapters 1–4** of „מאחורי הפלייליסט". Do NOT write Ch. 5–8.

Read only:
- `docs/agents/brief.md`
- `docs/outline.md`: "Frame", the page-plan rows for the abstract and Ch. 1–4, and "Where the required elements are"
- `docs/agents/research-notes.md`, with special attention to "Gaps / unverified"
- the keys in `book/references.bib`
- the WRITER INTERFACE block in `book/style.sty`
- PRD.md §3, §5.3

Files to write (UTF-8, LaTeX body only, no preamble). Each chapter file starts with `% Author: Writer agent · 2026-11-14`.

| File | Content | Target length |
|---|---|---|
| `book/chapters/00-abstract.tex` | Abstract text only (main.tex prints the heading „תקציר"). Describes the whole book (Ch. 1–8, per the outline). States that Noa, her friends and her data are fictional, and that formulas and models are educational simplifications, not any company's algorithm. | 180–220 words |
| `book/chapters/01-boker-tov.tex` | `\chapter{בוקר טוב, נועה}\label{ch:1}` | ≈ 550 words, 2 pages |
| `book/chapters/02-kol-dilug.tex` | `\chapter{כל דילוג נספר}\label{ch:2}` + the graph (below) | ≈ 450 words + figure, 2 pages |
| `book/chapters/03-anashim-kmotech.tex` | `\chapter{אנשים כמוך}\label{ch:3}` + the cosine `lab` box | ≈ 750 words incl. lab, 3 pages |
| `book/chapters/04-shirim-kmo-ze.tex` | `\chapter{שירים כמו זה}\label{ch:4}` + the comparison table | ≈ 450 words + table, 2 pages |

Each chapter is built as: `scene` box (Noa, light humor, ~½ page) → explanation with `\section{}` headings as needed → at most one `realitycheck` where useful → closing `inshort` (2–3 bullets).

Content rules:
1. Every factual claim cites a verified key with `\cite{key}` (or `\cite[postnote]{key}`). Use only claims present in research-notes.md, at the strength stated there. Respect every item under "Gaps / unverified":
   - no spectrograms, no repeats or playlist adds as named signals, no skip percentage from any source, no time-of-day platform claim;
   - no Daily Mix, Discover Weekly or radio internals;
   - Goldberg only for the name Tapestry and the year 1992; Hu and Koren at abstract level only;
   - Schwartz as his argument, not settled science;
   - Spotify figures as "according to Spotify's company page, accessed November 2026".
   If a point has no verified source, leave it out. Do not state it uncited.
2. **[PLATFORM CLAIM]** items must be attributed in the sentence ("לפי Spotify…"). **[GENERAL METHOD]** items are presented as how recommender systems work in general, never as "how Spotify does it".
3. Everything about Noa, Yoni, Maya and their numbers is fictional. Put the scenes in `scene` boxes, tag the data with `\fictional`, and tag educational examples via the `lab` box or `\educational`. Never put `\fictional` or `\educational` as the very first thing in a paragraph (bidi bug); use them mid-sentence or in captions.
4. Terminology: introduce each technical term once with `\term{עברית}{English}`, then use the Hebrew term consistently. Suggested terms: סינון שיתופי, המלצה מבוססת תוכן, משוב מפורש / משוב משתמע, בעיית ההתחלה הקרה, דמיון קוסינוס, פירוק מטריצות.
5. Use English words only via `\en{}`. No new packages and no preamble commands.

**Ch. 2 graph (coordinated with the Boss).** The Boss has already generated `book/figures/noa_week.pdf` from `figures/data/noa_week.csv` (FICTIONAL). Insert exactly:
```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\textwidth]{noa_week.pdf}
  \caption{<your Hebrew caption> \fictional}
  \label{fig:noa-week}
\end{figure}
```
and refer to it as `איור~\ref{fig:noa-week}`. The verified numbers for the text and caption are below; use no others.
- One fictional week: 344 songs started; 245 "plays" (listened past 30 seconds; **our own definition for this chart**, not a platform definition) and 99 skips (28.8%).
- Bus, 07:00–09:00: 34 of 82 songs skipped (41%).
- Gym, 17:00–19:00: 11 of 57 skipped (19%).
- Studying, 22:00–24:00: 5 of 45 skipped (11%).
- Labels in the chart: אוטובוס, חדר כושר, לימודים.

The point of the chapter: a skip is a noisy signal. On the bus Noa skips a lot while hunting for the right song, which does not mean she dislikes those songs. Support this with the verified sources (implicit feedback, skips as signal), not with the fictional numbers.

**Ch. 3 lab box: cosine similarity.** Use `\begin{lab}{דמיון קוסינוס}`.
- The formula: `\[\cos(\theta)=\frac{\mathbf{a}\cdot\mathbf{b}}{\lVert\mathbf{a}\rVert\,\lVert\mathbf{b}\rVert}\]`.
- Explain every symbol in plain Hebrew, as a list.
- Give a worked example with a small fictional table: Noa, Yoni and Maya × 3 songs, small integer play counts.
- Show the dot product, both norms and the result, to 2 decimals, for Noa–Yoni and for Noa–Maya, and conclude who is "more similar".
- Pick integers whose results differ clearly. **Check every number twice.**
- State in the box that this is an educational formula and not the algorithm of any company.
- Cite the source that supports cosine similarity as a standard measure.

**Ch. 4 comparison table.**
```latex
\begin{table}[t]
\centering
\caption{...}\label{tab:approaches}
\begin{tabularx}{\textwidth}{@{}lXXX@{}}
\toprule ... \midrule ... \bottomrule
\end{tabularx}
\end{table}
```
- Columns: aspect | סינון שיתופי | מבוסס תוכן | היברידי / מבוסס הקשר.
- Rows: what it uses; strength; weakness; new song?; new user?; a moment in Noa's day.
- Keep cells short (≤ 8 words). Use only sourced characterisations; cite in the text near the table.

When done, reply in ≤10 lines: files written, approximate word count per file, the cosine numbers you used, and any claim you dropped for lack of a source.
