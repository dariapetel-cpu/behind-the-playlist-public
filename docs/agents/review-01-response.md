# Response to review-01 (Boss, 2026-11-14)

The Reviewer's report: `review-01.md` (verdict CHANGES REQUESTED: 0 blocker, 5 major, 31 minor). The Boss applied the fixes directly, mostly with the Reviewer's own suggested wording, and rebuilt and re-inspected all 20 pages. "Applied" means the edit is in the source and the rebuilt PDF was checked.

| # | Sev. | Action | Where |
|---|---|---|---|
| 1 | major | **Applied.** Hybrid "weakness" → „לא נבדק במקורות שלנו" (honest about the gap) | 04:43 |
| 2 | major | **Applied.** → „עדיין קשה: אין היסטוריה" (cold-start definition, schedl2018current, cited in the paragraph above the table) | 04:45 |
| 3 | major | **Applied.** → „ממליץ רק על מה שדומה למה שכבר אהבת" (content-based definition, google2026candidate) | 04:43 |
| 4 | major | **Applied.** Trend claim rephrased in parentheses: „בנפרד, לפי Spotify … בלי לפרט באיזה שלב" | 06 block 4 |
| 5 | major | **Decided: keep the bibliography LTR.** All 18 entries are English; LTR entries under an RTL Hebrew heading is the usual convention for Hebrew academic texts. PRD §6 and §8.3 updated to say so. | PRD |
| 6 | minor | Applied: „אפשרי: מהשמע ומהמידע עליו", „אפשרי, דרך התוכן" | 04:44 |
| 7 | minor | Applied: header „שילוב גישות (כולל הקשר)"; „השיר שהומלץ ליוני (פרק 3)" | 04:39, 46 |
| 8 | minor | Applied: `\educational` on the table caption | 04:36 |
| 9 | minor | Applied: „כתריסר עד עשרים החלטות קטנות" (60 min ÷ 3–5 min = 12–20) | 01:22 |
| 10 | minor | Applied: title „הפלייליסט יודע מה השעה?" | 05:5 |
| 11 | minor | Applied: the Hu citation now supports "preference with varying confidence"; the skip reading follows from it | 08 |
| 12 | minor | Applied: „עוזרת לשירים חדשים מול בעיית ההתחלה הקרה" | 08 |
| 13 | minor | Applied: „אולי זו לולאת המשוב, ואולי פשוט חקירה. ועכשיו נועה יודעת להבדיל." | 08 |
| 14 | minor | Applied: section retitled „הטיית פופולריות"; the Chaney sentence shortened to a back-reference marked as simulation | 07 |
| 15 | minor | Applied: „בדפוס נפוץ המערכת מתחילה…" | 06:24 |
| 16 | minor | Applied: „בפישוט שלנו, השאלה היא בערך…" | 06 block 5 |
| 17 | minor | Applied: „כך אפשר למנוע מצב שבו…" | 06 block 6 |
| 18 | minor | Applied: „הדילוג של 23:00 אתמול", „ההאזנה לשיר האינדי" (no unshown save) | 06 block 1 |
| 19 | minor | Applied: „הצירים של המרחב הזה נקראים גורמים נסתרים (latent factors)" | 03 |
| 20 | minor | Applied: rating = „ציון", ranking = „דירוג" (02 ×2, 03 ×1) | 02, 03 |
| 21 | minor | Applied: „רצף האזנה כזה נקרא סשן", „המלצה סדרתית", „…יותר על ההקשר מאשר על השיר" + schedl citation | 05 |
| 22 | minor | Applied: „באופן פסיבי" | 02:14 |
| 23 | minor | Applied: „הפכה את התנהגות המשתמשים לאחידה יותר" (06); 07 sentence rewritten under #14 | 06, 07 |
| 24 | minor | Applied: „מספר האנשים"; „להשהות שיר" | 07 |
| 25 | minor | Applied: „בהערכה קונטרפקטואלית (על נתונים קיימים, לא בניסוי חי)" | 07 |
| 26 | minor | Applied: „לאורך הימים שלה עם המוזיקה" / „לרגע אחר בחיים שלה" | 00, 01 |
| 27 | minor | Partly applied: the 160M figure is kept only in Ch. 2 (Ch. 5 refers back); Ch. 6 block 1 refers back to Ch. 2; the Chaney sentence is a back-reference in Ch. 7. The Ch. 2 `inshort` keeps its one-line summary on purpose. | 05, 06, 07 |
| 28 | minor | Fixed (this was a Boss bug): `\label{ch:8}` had been swallowed by a `%` comment | 08:4 |
| 29 | minor | **Not fixed (open).** P. 13 holds the end of Ch. 5 (≈28%). Chapters start on new pages by design; filling it would mean padding or cutting content. See the remaining issues. | p. 13 |
| 30 | minor | Applied: Fig. 6.1 is `[h!]` after the intro section, so the list is no longer split by the figure | 06 |
| 31 | minor | Applied: Table 4.1 is `[h!]` under its section heading | 04 |
| 32 | minor | Accepted as is (the Reviewer agreed it is acceptable) | p. 4–5 |
| 33 | minor | Not applied: an unbreakable gloss caused 2 overfull lines (tested on 2026-11-14), so line breaks inside glosses are accepted | style.sty |
| 34 | minor | Applied: URL/DOI break penalties raised to 9000 (break only when needed); `note` dropped from spotify2026company; `maxbibnames=7` (McInerney now lists all 7 authors). Two long URLs still break mid-word ([1], [18]). | style.sty, bib |
| 35 | minor | Applied: the scene box now has a dashed grey (muted) border and a grey title, distinct from the coral fact-check box | style.sty |
| 36 | minor | Open by user instruction: cover details stay as marked placeholders until the user provides them | main.tex |

Other Boss changes in the same pass: `sortcites=true` (multi-citations were printed as written, e.g. [7, 4]; now ascending), and the checker's white-text rule now samples the background (white digits on the diagram's coloured badges are intended). The rule was regression-tested against the known [heb]+colour bug PDF, which is still caught.
