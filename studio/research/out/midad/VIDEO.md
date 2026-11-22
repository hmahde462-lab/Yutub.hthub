---
videomd: 1
name: midad
description: '“midad”. Made with (inferred): AI-generated video 100%'
source:
  file: midad.mp4
  sha256: c51d774b50d83901d39a32661811afbbef19355be5a3253dc6d62c1b752f0fa2
  duration: 110.267
  size: 1080x1920
  fps: 30.0
  aspect: '9:16'
shots: 16
lang: en
made_mix:
  ai_video: 1.0
confidence: 0.656
readers:
- tools
open_questions: 19
generator:
  name: rea-video
  version: 0.1.0
---

# midad.mp4

**Verdict** (inferred): Mixed production: live action or AI, to confirm 100%; overlays: styled text, text labels, subtitles, title (composited in code / an editor); audio: voice + music 132.5BPM (to confirm, leaning stock library music); packaging: styled text ×4, text labels ×12
**Made with** (inferred, by duration): AI-generated video 100%
**Remake**: 16 AI video shots → 10 generation units, 10 MiniMax H3 / H3 Max calls

## Next steps

- No VLM ran: if you can see images, review first: `rea-video review <this dir>` → fill `review_answers.json` → `rea-video apply-review <this dir>`
- Remake: Capsule Cinema does the generation, assembly and checks. `rea-video remake <this dir>` hands over to it, does what can be done automatically and keeps the original elsewhere; `remake/status.md` says per shot what is left. Add incoming clips to `remake/mine.json` and run it again
- AI shots: prompts are in the generation units of `video/remake.md`; for automatic generation use Capsule Cinema: `scripts/remake_reference.py prepare <this dir>`, then `run <jobs.json> --dry-run` (paid: ask the user first)

## Open questions

- The VLM did not run (No VLM; live action / AI / 3D are told apart from pixel statistics only, so confidence is limited. An agent that can see images: run rea-vi…
- Shot #1 (0.0–10.0s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC la…
- Shot #2 (10.0–11.8s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- Shot #3 (11.8–17.8s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- Shot #4 (17.8–25.8s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- Shot #5 (25.8–35.8s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- Shot #6 (35.8–40.0s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- Shot #7 (40.0–45.9s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- 11 more, see the `flag` lines in `video/timeline.md`

## Map

Read this page first; for detail, open only the file you need. Each line is `path | ~tokens | what is in it · when to read it`; paths are relative to this directory.

```videomd-map
video/timeline.md | 986 | Timeline: one line per shot · what a stretch says, which shots need review, how a shot was made
video/moments.md | 138 | Special moments · reveals, twists, climaxes, goofs: times, key frames, clips
video/content.md | 87 | Content and structure · what it says, the narrative line, structure, the script
video/cast.md | 53 | Cast, scenes and props · reference images for characters, first-frame prompts
video/sound.md | 503 | Sound · voice, music, sound effects, beats and sources
video/rhythm.md | 1037 | Rhythm and key frames · when cuts and transitions happen, shot lengths, the change curve, key frames of each shot
video/look.md | 445 | Camera, lighting and editing · for filmed shots: framing, camera, lighting, kit
video/packaging.md | 667 | Packaging · subtitles, styled text, stickers, picture-in-picture: timing and style
video/remake.md | 2556 | Remake plan · generation units, shoots, code builds, real material to collect, acting and emotion
video/shots/*.md | 612 | Per-shot detail, tokens per file on average · checking one shot: what is seen, the inference and its basis, prompts, frames
breakdown.json | 50112 | Full raw data · for programs; a model rarely needs it
shots/ | - | contact sheet, first and last frame of each shot · checking by eye
storyboard.jpg | - | storyboard of the whole video · the whole video at a glance
stems/ | - | voice, music and effects stems · listening, remaking the sound
sfx/ | - | a clip of each sound effect · finding matching effects
packaging/ | - | subtitle files, packaging timeline, sticker frames · remaking subtitles and packaging
audio.png | - | waveform and beat chart · seeing the rhythm
```

## How to read

- One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
- `story` job in the story and the point · `seen` what is on screen · `act` acting (emotion, strength, face) · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
- Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).
- What is “seen” can be checked against the frames; what is “inferred” is the tools' and image readers' judgement, with the basis in each shot file. When they disagree, trust the frames.
