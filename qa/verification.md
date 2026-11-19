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

## Lesson-ending simplification — 2026-11-13

Removed the stack of progress, export/print controls, notices, evidence disclosures,
and between-chapter links from beneath ordinary page navigation. Chapter options
now contains progress and tools; writing pages contain their response export; the
final page contains the next-chapter transition and any checkpoint invitation.
The chapter footer has two quiet links.

Checked all twelve chapters at five widths (60 layouts), menu opening and Escape,
contextual exports, end-of-chapter transitions, and chapter evidence destinations.
The full browser regression passed all 96 pages and 72 feedback variants, including
exports, writing privacy, progress, keyboard navigation, playback, and unavailable
storage. The extracted offline package also passed. Results: `clean-footer-review.json`.

## Learner-facing audit — 2026-11-19

Reviewed all 96 lesson pages and their narration scripts, 72 choice explanations,
24 recall prompts, 12 lab exercises and worked responses, three independent cases,
and the workbook, reading and offline editions against the stated audience of
adults new to psychology. Checked headings, definitions, required actions,
comparison questions, feedback, scope and reading order. All nine distinct chapter
source URLs returned HTTP 200.

Chromium exercised every lesson and choice. Each lab was completed with its five
fields, its worked response, a revised draft and an exact text export. In the
course and workbook, the final case kept the organiser’s message closed until
after the first four tasks, when it could be used to revise the initial account.
Keyboard checks covered choice feedback, recall reveals, the skip link, navigation,
audio rate and closing Chapter options. Layout checks covered six widths at
320–1440 px and both OS colour preferences with the course’s light palette.
Ten sampled views passed the automated axe A/AA screen.

A browser profile created before this update resumed the saved lesson and kept its
practice mark. Separate checks covered blocked reads, failed writes, retry, corrupt
data, canceled or failed removal, successful removal in a second tab, exact draft
exports and writing absent from browser storage. The strict build checked all 96
recordings against the revised scripts; 85 existing recordings kept their original
hashes. The two regenerated tagged PDFs contain all applicable answers and the
workbook preserves the final-case order. The extracted package worked at a local
HTTP address with internet requests blocked. Managed Chromium blocked direct
file navigation.

These are wording and functional checks. Practitioner review, a learner pilot,
human listening review and clinical outcome testing are still pending.
