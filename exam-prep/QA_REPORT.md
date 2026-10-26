# Final QA — 27 October 2026

## Passed
- 20 automated behavior tests: grading, reset/restore, malformed or unavailable storage, deadline enforcement, written score limits, search escaping, code copy/wrap/expand, exact source text preservation. See results/qa-tests.json.
- 31 independent numerical/formula/rubric assertions; all 15 HTML documents have valid local links/anchors and unique IDs.
- 48 quiz questions, 24 mock MCQs and 6 written questions; mock total 100 points.
- Re-ran all three Python examples with quiz/requirements.txt dependencies; P01–P05 outputs match displayed results.
- Desktop browser navigation across all 14 categories: no horizontal page overflow or broken images.
- Responsive checks at 390 and 320 px: code labs, quiz, mock exam and chapter 12 have no horizontal page overflow. Mobile menu closes after navigation.
- Real browser clipboard matched the complete highlighted Python source after cache version correction.
- One Dark Pro via Shiki 4.5.0: all 6 code blocks; Python and PowerShell; no runtime dependency.

## Corrections
- Safe restoration of corrupted saved answers/read progress, invalid options and self-scores.
- Expired exams reject late answers between timer ticks; missing deadline recovers safely.
- Fixed code-copy selector after toolbar change; preserve indentation with textContent.
- Versioned CSS/JS URLs to prevent previously cached scripts breaking updated HTML.
- Keyboard escape, hidden mobile menu focus behavior, reduced motion, code wrapping/expansion and print styling.

## Scope and limits
Content review covers the supplied chapter summaries, source explanations, formulas, worked examples and assessment rubrics. Automated checks supplement review; they do not prove every sentence or predict the real exam. Written responses are self-graded. The browser test used the in-app Chromium browser, not every browser/device. Print CSS was inspected; a physical print was not tested. Local file storage varies by browser; GitHub Pages HTTPS is the recommended reading entry point.
