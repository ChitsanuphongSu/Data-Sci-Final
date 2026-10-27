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

## Quick Quiz extension — 27 October 2026
Added 2 sets of 90 original questions, each with 15 questions per chapter (7–12), topic coverage tables, explanations and chapter review links. Correct choices are deterministically shuffled, avoiding a repeating answer-position pattern.

13 additional automated tests cover all 12 chapter/set combinations at full score, blank grading, per-chapter grade invalidation, wrong-only filters, reset cancellation/confirmation, persistence, set isolation, malformed/unavailable storage, JSON export and independently recomputed numerical examples. Existing 20 behavior tests and 31 formula checks remain applicable. Static links/anchors now cover 17 HTML documents.

Browser extension checks: both sets × six chapters × viewport widths 1366/390/320 = 36 cases with no horizontal body overflow. Verified chapter navigation, grading from the bottom control, explanatory feedback and correct-answer highlighting.
