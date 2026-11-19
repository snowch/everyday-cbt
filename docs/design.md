# Visual design

Everyday CBT follows the field-guide styling of
[Common Ground](https://github.com/snowch/common-ground-social-psychology), at the
repository owner's request. This changes presentation, not the proposed curriculum
or its development/review status.

- Paper: `#EDF3F8`; ink and cover: `#19394D`.
- Ocean: `#216B88`; brass: `#D8AC5C`; muted text: `#4B6172`.
- Headings: Libre Baskerville; body and controls: Arimo.
- Rounded dark cover, pale illustration background, thin rules, circular chapter
  numbers, and two-column chapter rows that stack on small screens.
- Course plan immediately follows the cover; learning approach and production
  status follow the curriculum.

Fonts are bundled locally and unchanged, with their complete OFL notices. The
build copies fonts, provenance, and licenses into the published site. It makes no
font service requests. See `assets/fonts/manifest.json`, `FONT-LICENSE.txt`, and
`THIRD-PARTY-NOTICES.txt`.

The existing five-part CBT diagram uses the same blue palette and an arched frame
to reflect the reference cover. It remains a conceptual diagram, with a text
description for assistive technology.

## Lesson player

Lessons use a white teaching panel with a pale blue illustration area, eight numbered
page links, and Previous/Next controls below the lesson. Each page has native recorded-audio
controls and a recording transcript. Decisions use labelled radio inputs and
feedback after checking; recall and lab suggestions use native disclosure controls.
A readable text version replaces the diagram at narrow widths. Wider layouts offer it as an optional disclosure.

Practice writing is kept only in the current document. Download and print controls
provide explicit ways to retain it. Local progress distinguishes pages viewed from
practice attempts, without a mastery score or reward streak. The complete reading
edition supports learning without JavaScript.

## Teaching messages and narration

All 48 illustrated story, concept, and worked-example pages use separately authored
key-message bullets in the teaching panel. The `key_messages` field contains three
or four concise points; `paragraphs` retains the full explanation for narration,
the recording transcript, and the reading edition. Do not substitute full narration
paragraphs into the panel or derive bullets by splitting those paragraphs.

Decision prompts, recall instructions, and lab fields retain their normal formats.
Changing only teaching summaries does not require regenerating unchanged recordings.

## Keep the lesson ending quiet

Page navigation is the end of an ordinary lesson page. A compact Chapter options
disclosure in the heading contains progress, printing, a link to the lab in the workbook,
and a direct link to the chapter’s evidence notes on the guidance page. It closes
on page changes, outside clicks, or Escape.

Response exports and the unsaved-writing note appear with recall and
lab writing. A practice attempt updates the activity count. Decision feedback
explains a choice, and written responses use suggested reasoning for self-checks. Chapter transitions and checkpoint invitations appear on the final
page. The chapter footer contains just guidance and font-license links; the fuller
footer remains on reference and workbook pages.
