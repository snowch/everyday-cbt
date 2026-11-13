# Technical verification — draft v0.1.0

Run locally on 2026-11-13 with Chromium and Playwright 1.62.0. Machine-readable
results are in `results.json`; source links and relevance are in `source-ledger.json`.

- All 96 lesson pages, 72 choice feedback variants, 24 recall prompts, and 12 labs
  exercised in the browser.
- Layouts checked at 1440, 1024, 768, 620, 390, and 320 pixels on the home page,
  story, decision, concept, recall, lab, workbook, and final case.
- Keyboard navigation, visible page selection, recorded playback, navigation stop,
  rate changes, response export, progress persistence, and editing keys checked.
- Written responses confirmed absent from local storage; reload clears writing.
- Unavailable browser storage and reading without JavaScript checked.
- 506 generated internal references checked, including assets and fragments.
- Axe-core found zero A/AA violations on nine tested pages and lesson types.
- All 96 recordings decoded, with matching script and file hashes, non-silence,
  duration, and broad speaking-rate checks. Total narration: 55.1 minutes.
- Tagged PDFs: 33-page workbook and 73-page reading edition. Text checks cover
  every lab, all three cases, and all 72 feedback explanations.
- Complete offline ZIP extracted and tested with external requests blocked:
  embedded fonts, recorded playback, navigation, feedback, and both PDFs passed.

## Limits

These checks do not establish clinical effectiveness, mastery, complete WCAG
conformance, or suitability for an individual learner. No qualified practitioner
review, learner pilot, independent ASR screen, or human listening review has taken
place. The accessibility screen samples nine pages/types rather than every state.
Managed Chrome blocks file:// navigation; the extracted offline course was tested
through a local HTTP server with no internet access, not by direct file opening.

## Teaching-panel correction — 2026-11-13

The 48 illustrated story, concept, and worked-example panels now show separately
authored key-message bullets. Checked all 48 at 1440, 1024, 768, 390, and 320 pixels
(240 layouts), with no overflow or browser errors. Full prose remains in the
recording transcripts and reading edition. All 96 narration scripts, questions,
answers, and lab prompts are unchanged; the strict build verified the existing
recordings against their script and file hashes. Results: `key-messages-review.json`.
