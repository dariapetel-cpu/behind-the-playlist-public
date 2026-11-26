# QA round 2: pre-commit review prompt

*Origin: verbatim user prompt (Roni Sagi), 2026-11-25.*

```text
Perform the final pre-commit review of the current changes.

1. Review expectations.json and visual_baseline.json and verify that no QA requirements were weakened.
2. Run the existing test suite once using python -m unittest discover -s tests.
3. Report the exact number of passed, failed and skipped tests.
4. Verify that the original book content and PDF remain unchanged.
5. Check all changed and new files for personal information, credentials, secrets, and unnecessary generated files before publication.
6. Confirm that all remaining limitations and unverified checks are documented accurately.
7. Propose logical commit groups for the completed contributions.

Do not launch additional agents, broad audits, or unrelated improvements. If a test fails, report it instead of starting another lengthy repair cycle.

Do not commit or push yet.

Provide a concise summary in Hebrew.
```
