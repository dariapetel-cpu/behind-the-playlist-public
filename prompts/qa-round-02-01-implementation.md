# QA round 2: implementation prompt

*Origin: verbatim user prompt (Roni Sagi), 2026-11-25, same Claude Code session as the audit ([qa-round-02-00-audit.md](qa-round-02-00-audit.md)). The agent task prompts derived from it are in `prompts/qa-round-02-D4-detector.md`, `-F2-fixer.md` and `-D5-verifier.md`.*

```text
Proceed with recommended contribution #1: strengthening the QA mechanisms and automated mutation testing.

Work strictly according to Assignment 02 requirements and the findings of your independent audit.

1. Create a separate Git branch named roni-qa-improvements.
2. Save the actual audit and implementation prompts in the existing prompts directory.
3. Review and reproduce the identified QA failures before implementing fixes.
4. Improve qa_lib.py and check_pdf.py based on verified findings.
5. Update the relevant QA Skills to prevent recurrence, rather than applying only isolated manual fixes.
6. Implement tests/test_qa_mutations.py with meaningful failure scenarios.
7. Execute the automated tests and verify that valid inputs pass while invalid inputs fail.
8. Create an incident investigation report under docs/incidents/ describing the root cause, why the existing Detector missed the issue, the corrective action and actual verification results.
9. Preserve the original book content and visual design.
10. Document actual test results without fabricating evidence.

Use separate Detector, Fixer and verification agents where supported. Document which agents were actually executed.

Do not commit or push changes yet. I want to review and approve all modifications first.

At the end, provide a Hebrew summary of the modified files, actual test results, unresolved issues and how these improvements satisfy the assignment requirements.
```
