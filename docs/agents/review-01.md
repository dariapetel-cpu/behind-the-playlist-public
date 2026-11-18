> Author: Reviewer agent · 2026-11-14 · scope: task V1, the full manuscript (`book/chapters/00-abstract.tex` to `08-play.tex`, `book/figures/pipeline.tex`, `book/main.tex`, `book/style.sty`), checked against `docs/agents/research-notes.md`, `book/references.bib`, `figures/data/noa_week.csv` and the rendered pages `build/pages/page-01.png` to `page-20.png`

# Review 01: full manuscript

## Issue table

| # | Severity | File:line or page | Problem | Suggested fix |
|---|---|---|---|---|
| 1 | major | 04-shirim-kmo-ze.tex:43 (hybrid column, "חולשה") | „דורש יותר סוגי נתונים" is presented as a weakness (cost or complexity), and no note supports it. It only follows from the definition in row 1, and as written it reads as a factual claim. | Replace it with „אין לנו מקור שבודק זאת" or a purely definitional „משלב כמה סוגי נתונים" (and then the row no longer states a weakness). The first option is preferred because it is honest about the gap. |
| 2 | major | 04-shirim-kmo-ze.tex:45 (hybrid column, "משתמשת חדשה?") | „תלוי במידע הזמין" is vague and suggests that context or hybrid methods solve the new-user problem. No note supports that. Schedl defines cold start as arising whenever a new user registers, whatever the approach. | „עדיין קשה: אין היסטוריה" (supported by schedl2018current §2.2, the cold-start definition). |
| 3 | major | 04-shirim-kmo-ze.tex:43 (content-based column, "חולשה") | „נשאר קרוב למה שכבר אהבת" is an over-specialisation claim that no research note records. | Use the definitional wording from google2026candidate: „ממליץ רק על מה שדומה למה שכבר אהבת". Or have the Researcher add a note for the claim before keeping it. |
| 4 | major | 06-shmone-tachanot.tex:32 | The Spotify claim about "trends and general tastes" is placed inside block 4 (candidate generation) of the book's own pipeline. That implies Spotify's candidate generation uses trends, but the source does not say at which stage they are used. This works against PRD §5.3 and check 3. | Move the sentence out of the numbered list, or rephrase it as: „לפי \en{Spotify}, האלגוריתמים שלה מתחשבים גם במגמות ובטעם הכללי של המשתמשים, בלי לפרט באיזה שלב \cite{...}". |
| 5 | major | main.tex:76–78; pages 19–20 | The bibliography is typeset in an `english` environment and is fully left-to-right. PRD §6 ("bibliography … read right-to-left") and §8.3 say otherwise. All entries are English, so LTR is defensible typographically, but it does not match the PRD as written. | The Boss decides: either record the deviation in the PRD/README ("English-language references are set LTR"), or set the section RTL with each entry LTR. Either way, the deviation should be documented. |
| 6 | minor | 04-shirim-kmo-ze.tex:44 | „כן: מספיק השמע והמידע עליו" overstates vandenoord2013deep. The paper shows that latent factors *can be predicted* from audio. It does not show that audio is "enough". | „אפשרי: מהשמע ומהמידע עליו". For parallel wording, change the hybrid cell to „אפשרי, דרך התוכן". |
| 7 | minor | 04-shirim-kmo-ze.tex:39, 46 | The column header „היברידי / מבוסס הקשר" merges two different ideas. In row 6, „השיר ש„בחר" יוני" does not match the Ch. 3 scene, where the app recommended a song to Yoni. | Header: „שילוב גישות (כולל הקשר)". Row 6: „השיר שהומלץ ליוני (פרק 3)". |
| 8 | minor | 04-shirim-kmo-ze.tex:36 | The table caption has no `\educational` tag, but Fig. 6.1 does. The labelling is inconsistent. | Append `\educational` to the caption. |
| 9 | minor | 01-boker-tov.tex:22 | „עשרות החלטות" in an hour: at 3–5 minutes per song, one hour holds about 12–20 songs, so "tens" (עשרות) overstates it. | „יותר מעשר החלטות קטנות" or „כתריסר עד עשרים". |
| 10 | minor | 05-hasha.tex:5; TOC page 3 | The chapter title „הפלייליסט יודע מה השעה" states as fact the very claim that the reality-check box says has no source (time of day). | Add a question mark: „הפלייליסט יודע מה השעה?" |
| 11 | minor | 08-play.tex:18 | `\cite{hu2008collaborative}` is attached to the skip interpretation („לא אהבתי / לא עכשיו"). Hu et al. support "positive and negative preference with varying confidence", not anything about skips. | „משוב משתמע מבטא העדפה בדרגות ביטחון שונות \cite{hu2008collaborative}, ולכן דילוג יכול לומר גם „לא עכשיו"". |
| 12 | minor | 08-play.tex:20 | „עוזרת מול בעיית ההתחלה הקרה" is broader than the source, which covers new *songs* only. New users are not covered (see the table row). | „עוזרת לשירים חדשים מול בעיית ההתחלה הקרה". |
| 13 | minor | 08-play.tex:27 | „זו לא אשמתה. זו לולאת המשוב. בעיקר." makes a causal claim from a simulation study (chaney2018algorithmic). It also contradicts line 14 ("what Noa does affects what she hears"). | Soften it, e.g. „אולי זו לולאת המשוב, ואולי פשוט חקירה. ועכשיו היא יודעת להבדיל." |
| 14 | minor | 07-bua.tex:21–23 | The heading „העשירים מתעשרים" and the bridge from popularity bias to Chaney's feedback loop suggest a rich-get-richer dynamic. Kowald measures bias, not dynamics, and Chaney measures homogenisation, not popularity. The Chaney sentence also nearly repeats 06:39. | Retitle to „הטיית פופולריות" (or keep the title as a question). Shorten the Chaney sentence to a back-reference: „גם לולאת המשוב מפרק 6 (בסימולציה) מצביעה על האחדה". |
| 15 | minor | 06-shmone-tachanot.tex:24 | „מערכת המלצה מתחילה מאוסף ענק…" generalises. The source says this is "a common pattern". | „דפוס נפוץ: המערכת מתחילה…". |
| 16 | minor | 06-shmone-tachanot.tex:33 | The ranking question („מה הסיכוי שנועה תשמע עד הסוף") follows straight after a covington citation, so it reads as sourced. | Add „בפישוט שלנו," before it. |
| 17 | minor | 06-shmone-tachanot.tex:34 | „כך לא יתנגנו עשרה שירים…" is definite, but the source says only "can help ensure diversity". | „כך אפשר למנוע…". |
| 18 | minor | 06-shmone-tachanot.tex:29 | Continuity: Ch. 4 never shows Noa saving the indie song. The Ch. 6 scene happens at 21:00 but refers to the 23:00 skip as something that already happened. | „שמירה של שיר האינדי, אילו נועה הייתה שומרת אותו" or drop it. „הדילוג של 23:00 אתמול". |
| 19 | minor | 03-anashim-kmotech.tex:81–85; 04:22 | „גורמים נסתרים" (latent factors) appears only in the Ch. 3 heading and is never defined in the body. Ch. 4 then refers back to „אותם גורמים מפרק 3". | Add one sentence in Ch. 3: „הצירים של המרחב הזה נקראים \term{גורמים נסתרים}{latent factors}". |
| 20 | minor | 02:14 („דירוג מפורש"), 03:23 („הדירוגים"), 06:33–34 („דירוג", „דירוג מחדש") | Term clash: „דירוג" is used both for *rating* and for *ranking*. | Keep „דירוג" for ranking. For ratings use „ציון / ציונים" (e.g. 02:14 „בניגוד לציון מפורש", 03:23 „לפי הציונים שנתנו אחרים"). |
| 21 | minor | 05-hasha.tex:23 | „רצף האזנה רציף" is redundant, and „המלצה רציפה" mistranslates *sequential*. „הדילוג של 23:00 מספר אפוא…" does not follow from the skip-correlation finding, because that skip came after one song. | „רצף האזנה כזה נקרא סשן"; „המלצה סדרתית". End with: „הדילוג של 23:00 מספר אפוא יותר על ההקשר מאשר על השיר" (linking back to Schedl's point on context). |
| 22 | minor | 02-kol-dilug.tex:14 | „באופן סביל" is grammar terminology (passive voice) and sounds unnatural here. | „באופן פסיבי" or „בלי שנבקש מהם". |
| 23 | minor | 06:39 and 07:23 | „האחידה את התנהגות" is correct but stiff. | „הפכה את התנהגות המשתמשים לאחידה יותר". |
| 24 | minor | 07-bua.tex:8; 07:31 | „כמות האנשים" should be „מספר האנשים" (countable). „להשתיק" (mute) for *snooze* is inaccurate. | „פחות ממספר האנשים…"; „להשהות שיר ל-30 יום". |
| 25 | minor | 07-bua.tex:27 | „בהערכה שלהם" leaves out that the evaluation was counterfactual (offline). Readers may take it as a live test. | „בהערכה קונטרפקטואלית (על נתונים קיימים, לא בניסוי חי)". |
| 26 | minor | 00-abstract.tex:4; 01-boker-tov.tex:38 | „לאורך יום של האזנה" and „לרגע אחר ביום שלה" do not fit the chapters, which happen on a Friday, a Wednesday and in late December. | „לאורך הימים שלה עם המוזיקה" / „לרגע אחר בחיים שלה". |
| 27 | minor | 02:16, 02:43, 06:29; 02:22 and 05:23; 06:39 and 07:23 | Repetition between chapters: the Spotify signals sentence appears 3 times, the "160 million sessions" figure twice, and the Chaney sentence twice. | Keep the first full statement and use short back-references („כפי שראינו בפרק 2") elsewhere. |
| 28 | minor | 08-play.tex:4 | `% Boss edit…` comments out `\label{ch:8}`, so the label is never defined. Nothing references it yet. | Move `\label{ch:8}` before the comment. |
| 29 | minor | page 13 | Near-empty page: only the Ch. 5 reality-check and „בקצרה" boxes (about 30% of the page). | Tighten Ch. 5 (e.g. issue 21), or let the boxes start on p. 12. |
| 30 | minor | pages 14–15 | Fig. 6.1 floats into the middle of list item 8. „מובילה לפחות המלצות דומות [17]" continues below the figure on p. 15. | Place the figure before „התחנות, בערב של נועה" (`[h]` or `[!t]` after the first section), so the list is not split. |
| 31 | minor | pages 10–11 | Table 4.1 floats to the top of p. 11, above the section heading that introduces it, and leaves blank space at the bottom of p. 10. | Put `\begin{table}` after the section's first paragraph, or use `[h!]`. |
| 32 | minor | pages 4–5 | The Ch. 1 reality-check box breaks across pages; its second question opens p. 5. | Acceptable. If space allows, keep the box whole (`unbreakable`). |
| 33 | minor | page 6 | The term gloss „(implicit / feedback)" breaks across lines inside the parenthesis. | Use an unbreakable space inside the gloss for two-word terms, or accept it. |
| 34 | minor | pages 19–20 | Bibliography readability: DOIs and URLs break mid-token („10.1 145/…", „192844.19 2905", „research.at spotify.com"). Entry [18] gives the access date twice (note plus "visited on"). Entry [11] uses "et al." while the others list all authors. | Raise the break penalties for DOIs or let DOIs break only at „/" and „.". Drop `note` from spotify2026company because `urldate` already covers it. Set `maxbibnames=7`, or accept "et al." as consistent with biblatex. |
| 35 | minor | style.sty:151–158; e.g. page 4 | The fictional scene box and the "רגע, זה אמיתי?" fact box both have a peach background and a coral right border. Fiction and fact-check look alike, and only the small tag tells them apart. | Change the scene border to `muted` or give it a dashed rule, so fiction and fact-check differ at a glance. |
| 36 | minor | page 1; main.tex:9–13 | The cover shows placeholders for author, course, lecturer, institution and date. PRD §5.1 requires these details. | Not a Writer fix: the user supplies them (per Prompt 9). Track as open. |

Counts: **0 blocker · 5 major · 31 minor.**

---

## 1. Citation support

Every `\cite` was checked against its research-notes entry:

- **Ch. 1:** spotify2026company (catalog and user figures, "accessed Nov 2026") ✓; schedl2018current (tens of millions of items; 3–5 min; sequential and background use) ✓; schwartz2004paradox (presented as an argument) ✓; spotify2026understanding (personalisation; editors) ✓. The uncited estimate at line 22 is overstated (issue 9).
- **Ch. 2:** hu2008collaborative (implicit feedback definition; positive and negative preference with varying confidence) ✓ at abstract level; spotify2026understanding (search/listen/skip/save) ✓; brost2019music (two forms of implicit feedback; graded skips; correlation within a session; 160M sessions) ✓.
- **Ch. 3:** goldberg1992using (name and year only) ✓; resnick1994grouplens ✓; google2026candidate (CF definition; cosine quote; embeddings) ✓; koren2009matrix (MF beats neighbourhood methods; implicit feedback, temporal effects, confidence) ✓ at abstract level; hu2008collaborative (factor model for implicit feedback) ✓.
- **Ch. 4:** schedl2018current (cold start; acoustic features; context) ✓; vandenoord2013deep (CF cold start; predicting latent factors from audio; CNNs outperform; MSD) ✓; google2026candidate ✓; spotify2026understanding (genre, release date, podcast category, AI signals) ✓. Table cells: see §6.
- **Ch. 5:** schedl2018current ✓; spotify2026understanding (device, language, location; precise location only with opt-in) ✓; brost2019music ✓; mcinerney2018explore (definitions, bandit framework, research result explicitly marked as not a production system) ✓.
- **Ch. 6:** google2026overview (three stages; re-ranking) ✓ but generalised (issue 15) and overstated (issue 17); covington2016deep ✓ (presented as YouTube 2016); chaney2018algorithmic (marked as a simulation) ✓; spotify2026understanding: block 1 ✓, block 8 ✓, block 4 badly placed (issue 4).
- **Ch. 7:** anderson2020algorithmic (association, not causation; organic shift; retention; randomized experiment) ✓, and the text adds a good "correlation ≠ causation" caveat; kowald2020unfairness ✓; schedl2018current ✓; chaney ✓ (issue 14); mehrotra2018towards ✓ (issue 25); spotify2026understanding (controls; snooze 30 days; Discovery Mode) ✓.
- **Ch. 8:** spotify2026understanding (taste profile) ✓; recap citations ✓, except issues 11 and 12.

No wrong keys were found. No factual sentence is uncited, apart from those the book explicitly labels as its own framing (Ch. 6 blocks 2, 3 and 7; the bandit analogy).

## 2. Research limitations ("Gaps / unverified")

| Gap | Status |
|---|---|
| No spectrograms | ✓ the word does not appear; "audio signal" is used instead |
| Repeats or playlist adds not named as signals | ✓ the signal lists are search/listen/skip/save only; Ch. 1:22 "enjoy again" is a property of music (Schedl), not a signal |
| No skip percentage from a source | ✓ Ch. 2 reality-check box says so explicitly; 28.8% is fictional and labelled |
| No time-of-day platform claim | ✓ in the body (Ch. 5:19, 5:32). The chapter title implies one (issue 10) |
| No Daily Mix / Discover / radio internals | ✓ "מיקס הבוקר" and the year-end summary are fictional scene details with no mechanics described |
| Goldberg only for name and year | ✓ Ch. 3:23 (no "coined", no mechanics) |
| Hu and Koren at abstract level | ✓ |
| Schwartz as an argument | ✓ Ch. 1:26 ("כטיעון של שוורץ, ולא כחוק טבע מוכח") |
| Spotify figures with "accessed" | ✓ Ch. 1:18 („נבדק בנובמבר 2026") |
| Eight blocks as the book's own simplification | ✓ Ch. 6:24, caption, „בקצרה" box |

## 3. Platform vs. general

- Platform claims are consistently introduced with "לפי Spotify" or "Spotify מציינת". Spotify-authored papers are framed as "חוקרים מ-Spotify" and research results, not as production systems (Ch. 2:22, 5:29, 7:17). ✓
- Ch. 1 reality-check box, abstract:10 and Ch. 6:24 all state that no company's real algorithm is described. ✓
- Exception: Ch. 6:32 (issue 4).
- The Ch. 6 diagram is clearly presented as an educational simplification: caption plus `\educational` tag, section title „מפה לימודית, לא שרטוט של מפעל", and the source comment in pipeline.tex. ✓

## 4. Mathematics (recomputed)

- **Ch. 1, 570 years:** 100M × 3 min = 3×10⁸ min = 5×10⁶ h = 208,333 days ≈ 570.4 years. "יותר מ-570" ✓.
- **Ch. 3, cosine:** n·y = 20+6+0 = 26; ‖n‖ = √30 ≈ 5.477; ‖y‖ = 5; 26/27.386 = 0.9494 ≈ 0.95 ✓. n·m = 5+0+5 = 10; ‖m‖ = √26 ≈ 5.099; √780 ≈ 27.928; 10/27.928 = 0.358 ≈ 0.36 ✓. Doubling Yoni leaves the cosine unchanged ✓. "0 iff no shared song" holds for non-negative vectors ✓.
- **Ch. 2, against `noa_week.csv`:** plays = 245, skips = 99, total = 344 ✓; 99/344 = 28.78% → 28.8% ✓. Bus, hours 7–8: skips 15+19 = 34, total 48+34 = 82, 41.5% → 41% ✓. Gym, hours 17–18: 6+5 = 11 of 46+11 = 57, 19.3% → 19% ✓. Study, hours 22–23: 3+2 = 5 of 40+5 = 45, 11.1% → 11% ✓. The "30 seconds" definition matches the CSV header and the caption ✓.

## 5. Fictional-data labels

- All 8 scenes use the `scene` box, which carries the auto-tag „בדיוני" (verified on pages 4, 6, 8, 10, 12, 14, 16, 18). ✓
- Fig. 2.1: `\fictional` in the caption, in-figure tag „נתונים בדיוניים", text tag, reality-check box, and the CSV header. ✓
- Ch. 3 lab: auto-tag „דוגמה לימודית", plus the "educational formula" sentence and `\fictional` on the table. ✓
- Fig. 6.1: `\educational`. ✓
- Table 4.1: labelled "סיכום לימודי ומפושט" in words only, without a tag (issue 8).
- Fictional scene numbers ("40 אמנים", 18:00/23:00) sit inside scene boxes. Ch. 5:19 also states this outright. ✓

## 6. Ch. 4 comparison table: cell-by-cell ruling

| Row | Collaborative filtering | Content-based | Hybrid / context |
|---|---|---|---|
| במה משתמשים | Supported (resnick1994grouplens; google2026candidate) | Supported (schedl2018current acoustic features; spotify2026understanding genre and release date, as an example) | Definitional, plus schedl2018current (context) ✓ |
| יתרון | Supported (resnick1994grouplens) | Supported (vandenoord2013deep: "when they cannot be obtained from usage data") | Definitional, illustrated by vandenoord2013deep ✓ |
| חולשה | Supported (vandenoord2013deep; schedl2018current) | **Unsupported** → issue 3 | **Unsupported** („דורש יותר סוגי נתונים") → issue 1 |
| שיר חדש? | Supported (vandenoord2013deep) | Partly supported, overstated („מספיק") → issue 6 | Definitional (hybrid includes content); acceptable, reword to „אפשרי" |
| משתמשת חדשה? | Supported (schedl2018current cold-start definition) | Definitional (google2026candidate: "similar to what the user likes") ✓ | **Unsupported** („תלוי במידע הזמין") → issue 2 |
| רגע ביום של נועה | Fictional pointer; wording → issue 7 | Fictional pointer ✓ | Fictional pointer ✓ |

## 7. Hebrew and consistency

The prose is fluent, warm and well suited to the PRD audience. The humour in the scenes works („אולי האפליקציה היא אמא של המתופף"). Points to fix:

- Phrasing and grammar: issues 21–24.
- Terminology: „דירוג" clash (issue 20); „גורמים נסתרים" undefined (issue 19); „השמעות" and „האזנות" are used interchangeably (acceptable).
- Repetition between chapters: issue 27.
- Continuity and timeline: issues 18 and 26.

## 8. PRD §8 acceptance criteria

| # | Criterion | Status |
|---|---|---|
| 1 | Clean build, one command, no errors | Not checkable now (no build log in scope) |
| 2 | 18–24 pages; title, abstract, TOC, chapters, bibliography in that order | **Pass** (20 pages, order correct) |
| 3 | RTL everywhere, including the bibliography; mixed text in correct order | **Fail as written**: body, TOC and captions pass visually, but the bibliography is LTR (issue 5) |
| 4 | Graph, table, formula with symbols and a worked example | **Pass** |
| 5 | Eight-block TikZ diagram | **Pass** (vector TikZ source, 8 labelled blocks plus a loop) |
| 6 | Every chapter cites; every bib entry is cited; no unverifiable citation | **Pass** (18/18 keys cited; Ch. 1–8 each cite; Goldberg and Schwartz are used within their limits) |
| 7 | Fictional data and educational formulas labelled; no illustrative model is presented as Spotify's | **Pass with fixes** (issues 4, 8, 10) |
| 8 | Consistent colours, fonts and boxes (Reviewer sign-off) | **Pass with reservations**: one palette and style file; sign-off held until issue 35 is addressed or waived |
| 9 | README with screenshots | Not checkable now (out of scope) |
| 10 | prompts.md verbatim; agent log with real outputs | Not checkable now (out of scope) |

## 9. Layout (page images)

- No reversed text, missing glyphs or clipping visible on any page. Hebrew, numbers, `[n]` citations and English terms appear in the correct order. The diagram, graph and cover look correct, and the Boss has verified them at glyph level.
- Chapter openers, headers, the footer progress bar and box styles are uniform across chapters.
- Issues: near-empty p. 13 (29); list split by the figure on pp. 14–15 (30); table above its section on p. 11 (31); box split on pp. 4–5 (32); gloss line break on p. 6 (33); bibliography token breaks (34); scene and fact boxes look alike (35); cover placeholders (36).
- The bibliography is legible, with a clear numeric style and consistent fields, apart from issue 34 and the direction question in issue 5.

---

## Verdict: **CHANGES REQUESTED**

There are no blockers. Fix the five major issues before sign-off: the three unsupported cells in Table 4.1 (issues 1–3), the placement of the Spotify trends claim in Ch. 6 (issue 4), and a documented decision on the bibliography's direction (issue 5). The minor issues can be handled in a single Writer and Boss pass.
