# Recorded narration

Final recordings are retained in `audio/clips/`, so the course build does not
require synthesis software or network access. `audio/manifest.json` records the
script hash, encoded hash, and duration of each of the 96 clips.

Voice: Kokoro-82M v1.0, `af_heart`, speed 1.0, English (US), via `kokoro-onnx` 0.6.1.
Model and voice-file hashes are pinned in `scripts/generate_audio.py` and recorded
in `narration.json`. The voice is synthetic; no real-person voice cloning was used.
This matches Common Ground's voice selection without copying its recordings.

Narration reads visible lesson text, diagram labels, choices, recall questions,
and lab prompts. Feedback, revealed recall answers, and suggested lab responses
are text-only. The on-page recording transcript and downloadable script reflect
that distinction. There is no automatic advance or autoplay.

## Optional regeneration

Use a separate virtual environment and install `production/requirements.txt`; FFmpeg
must be available. Download the pinned model files from the upstream release:

https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/

```sh
python3 content.py
python3 scripts/generate_audio.py --models /path/to/models --working /path/to/working-audio --workers 2
python3 qa/check_audio.py
python3 build.py --require-audio
```

The generator verifies model hashes, uses two CPU threads per worker, generates
paragraph pauses, and encodes mono 24 kHz AAC at 96 kbps, targeting -16 LUFS and
-1.5 dBTP. A matching working marker avoids regenerating unchanged clips.
Raw WAV files, models, and virtual environments belong outside the repository.

## Review limits

The technical checks verify script hashes, encoded hashes, successful decoding,
non-silence, duration, and broad speaking-rate bounds. No independent ASR screen or
human listening review has taken place. Generated speech can still contain
pronunciation, pacing, or wording problems. Do not describe these checks as
listening approval.
