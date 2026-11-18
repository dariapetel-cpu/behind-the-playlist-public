# Task R1: Researcher (sent by Boss, 2026-11-14 ~15:33 IST)

Run via Claude Code's built-in Agent tool, `subagent_type: researcher` (definition: `.claude/agents/researcher.md`). Exact prompt sent:

```text
Task R1 (date 2026-11-14): verify the sources for the approved book plan and produce the research hand-off files.

Read only: `docs/agents/brief.md`, `docs/outline.md` (sections "Page plan" and "Candidate sources for the Researcher to verify"), and PRD.md §5.3.

Do this:
1. For each of the 12 candidate sources in the outline, open the actual source (publisher page, DOI landing page, arXiv, ACM DL, the authors' PDF, or the official company page) with WebFetch. Confirm authors, title, venue, year, pages, and DOI or URL. If you cannot verify a candidate, or a better accessible source exists for that chapter's claims, replace it and say why.
2. Prefer openly accessible academic papers and official technical publications (e.g. research.atspotify.com, engineering.atspotify.com, newsroom). For platform claims, such as catalog size or what Spotify says about its recommendations, use only the company's own published pages or peer-reviewed papers by its researchers. Record the exact statement and the date accessed.
3. Cover every chapter, Ch. 1–8, with at least one verified claim. Also cover the specific needs:
   - Ch. 2: implicit feedback and skips as signals.
   - Ch. 3: collaborative filtering origins, cosine similarity as a standard similarity measure, matrix factorisation.
   - Ch. 4: content-based audio models and cold start.
   - Ch. 5: context/sessions and explore–exploit.
   - Ch. 6: the generic multi-stage pipeline (candidate generation → ranking), plus anything supporting "filtering/diversification" and the "feedback loop".
   - Ch. 7: diversity effects, popularity bias, artist fairness.
   Target ≥10 verified sources, with ≥4 peer-reviewed.

Write exactly two files:
- `docs/agents/research-notes.md`, using the header and claim-line format from your definition. Group the claims by chapter (Ch. 1–8). Tag every claim as either **[GENERAL METHOD]** or **[PLATFORM CLAIM: <company>]**. Add a "Sources verified / replaced / rejected" table (key, status, how verified: URL opened, date). End with "Gaps / unverified".
- `book/references.bib`: verified entries only, each with `url` (and `doi` where one exists) and `urldate = {2026-11-14}`. Use `@online` for web pages.

Do not write book prose or any Hebrew chapter text. Do not invent quotes, pages or DOIs. If a detail cannot be confirmed, omit it and list it under Gaps.
```
