# Everyday CBT

A complete draft introduction to cognitive behavioural therapy through twelve
original stories, visual explanations, recorded narration, and practical labs.

**Draft v0.1.0.** Introductory skills education, not diagnosis, individual treatment,
or professional clinical training. No qualified practitioner review, learner
pilot, or clinical outcome study has taken place.

- [Open the course](https://snowch.github.io/everyday-cbt/)
- [Practice workbook](https://snowch.github.io/everyday-cbt/workbook.html) · [PDF](https://snowch.github.io/everyday-cbt/workbook.pdf)
- [Complete reading edition](https://snowch.github.io/everyday-cbt/reading.html) · [PDF](https://snowch.github.io/everyday-cbt/course.pdf)
- [Offline course](https://snowch.github.io/everyday-cbt/everyday-cbt-offline.zip)
- [Guidance, scope, and chapter sources](https://snowch.github.io/everyday-cbt/about.html)

## What is included

- 12 chapters with 8 pages each: story, initial decision, two explanations, worked
  example, transfer decision, recall, and lab.
- 24 decisions with explanatory feedback for all 72 options.
- 24 recall prompts with suggested reasoning; 12 labs with worked responses.
- 24 concept diagrams and original illustrations of the recurring characters.
- Concise key-message bullets beside illustrations, with full explanations in
  the recording transcripts and reading edition.
- Three independent cases, including a final unfamiliar case and self-assessment.
- 96 recorded Kokoro `af_heart` clips, with transcripts and adjustable playback speed.
- Printable workbook with all labs and cases, complete reading edition, and offline ZIP.

Allow about 20–30 minutes per chapter, plus field practice and the independent
cases. This is a design estimate, not timing established in a learner pilot.

Progress records pages viewed and practices tried in the current browser.
Written responses remain on the current chapter, workbook or case page until
the learner reloads or leaves it. Learners can download their responses as text. The course works without
browser storage. The reading edition includes all feedback without JavaScript.

## Build and preview

Python 3.10 or newer is enough for normal builds; all runtime assets are bundled.

```sh
python3 build.py --require-audio
python3 scripts/package_offline.py
python3 -m http.server 8877 --directory dist
```

Open <http://localhost:8877>. No package installation or speech synthesis is needed
to build or use the course. Extract the offline ZIP before opening `index.html`;
linked source readings require an internet connection.

## Authoring and source

- `content.py`: original story, teaching, question, feedback, lab, and case authoring.
- `course.json`: canonical generated course data used by the build.
- `build.py`: validation, diagrams, illustrations, chapter and companion rendering.
- `site/`: templates, styling, and browser interactions.
- `assets/fonts/`, `licenses/`: unchanged fonts, provenance, and full OFL notices.
- `audio/`, `production/narration.json`: final recordings and production provenance.
- `scripts/`: narration text, optional speech generation, PDF export, and packaging.
- `qa/`: browser and audio checks, with a retained verification summary.

After editing `content.py`, run `python3 content.py`. If visible narration text
changes, regenerate affected recordings and update the PDFs before publishing.
`build.py --require-audio` rejects stale scripts and mismatched audio hashes.
See [narration production](production/README.md).

## Verification

With Playwright and Chromium installed, run against the local preview:

```sh
python3 qa/check_site.py
python3 qa/check_audio.py
python3 qa/check_offline.py
```

The audio check also requires FFmpeg. The browser check exercises every lesson and
feedback option, six screen widths, playback, keyboard navigation, exports,
progress, writing privacy, unavailable storage, and the reading edition without
JavaScript. These are technical checks, not an expert content or listening review.

To regenerate companions (Playwright required), run the local preview, then:

```sh
python3 scripts/export_pdfs.py
python3 build.py --require-audio
python3 scripts/package_offline.py
```

## GitHub Pages

GitHub Actions validates and builds pushes to `main`, packages the offline course,
and deploys the artifact using the official Pages actions. Pull requests build
without deploying. The workflow can also be run manually.

## Design and sources

[Common Ground](https://github.com/snowch/common-ground-social-psychology) supplies
the requested visual direction and learning format. Stories, lesson text, diagrams,
illustrations, and implementation here are original. Further reading links to NHS,
Centre for Clinical Interventions, and NICE resources; those organisations have not
reviewed or endorsed this course. See [design notes](docs/design.md),
[course design](docs/course-plan.md), and [third-party notices](THIRD-PARTY-NOTICES.txt).
