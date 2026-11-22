---
videomd: 1
name: dahaa
description: '“dahaa”. Made with (inferred): AI-generated video 100%'
source:
  file: dahaa.mp4
  sha256: 7f3b9e328054ceec881238d30f06df0fe0d6f7aed13095eff21e0988ece59cfb
  duration: 58.967
  size: 1080x1920
  fps: 30.0
  aspect: '9:16'
shots: 16
lang: en
made_mix:
  ai_video: 1.0
confidence: 0.57
readers:
- tools
open_questions: 18
generator:
  name: rea-video
  version: 0.1.0
---

# dahaa.mp4

**Verdict** (inferred): Mixed production: live action or AI, to confirm 100% (48% of the duration is live action or AI, to confirm: the platform transcode erased the noise evidence, needs a VLM pass or a human look at the frames); overlays: animated sticker / GIF, styled text, text labels, static graphics, static sticker, subtitles (composited in code / an editor); audio: voice; packaging: styled text ×3, text labels ×8, stickers / GIFs ×5
**Made with** (inferred, by duration): AI-generated video 100%
**Remake**: 16 AI video shots → 6 generation units, 6 MiniMax H3 / H3 Max calls

## Next steps

- No VLM ran: if you can see images, review first: `rea-video review <this dir>` → fill `review_answers.json` → `rea-video apply-review <this dir>`
- Remake: Capsule Cinema does the generation, assembly and checks. `rea-video remake <this dir>` hands over to it, does what can be done automatically and keeps the original elsewhere; `remake/status.md` says per shot what is left. Add incoming clips to `remake/mine.json` and run it again
- AI shots: prompts are in the generation units of `video/remake.md`; for automatic generation use Capsule Cinema: `scripts/remake_reference.py prepare <this dir>`, then `run <jobs.json> --dry-run` (paid: ask the user first)

## Open questions

- The VLM did not run (No VLM; live action / AI / 3D are told apart from pixel statistics only, so confidence is limited. An agent that can see images: run rea-vi…
- Shot #1 (0.0–12.4s): Live action / stop motion or AI, to confirm: no AIGC label; 24fps-source marks appear in AI video, stop motion and cinema-camera footage al…
- Shot #2 (12.4–25.4s): Live action / stop motion or AI, to confirm: no AIGC label; 24fps-source marks appear in AI video, stop motion and cinema-camera footage a…
- Shot #3 (25.4–27.3s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- Shot #4 (27.3–28.7s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- Shot #5 (28.7–30.5s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- Shot #6 (30.5–31.3s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- Shot #7 (31.3–35.4s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- 10 more, see the `flag` lines in `video/timeline.md`

## Map

Read this page first; for detail, open only the file you need. Each line is `path | ~tokens | what is in it · when to read it`; paths are relative to this directory.

```videomd-map
video/timeline.md | 971 | Timeline: one line per shot · what a stretch says, which shots need review, how a shot was made
video/moments.md | 106 | Special moments · reveals, twists, climaxes, goofs: times, key frames, clips
video/content.md | 87 | Content and structure · what it says, the narrative line, structure, the script
video/cast.md | 53 | Cast, scenes and props · reference images for characters, first-frame prompts
video/sound.md | 180 | Sound · voice, music, sound effects, beats and sources
video/rhythm.md | 774 | Rhythm and key frames · when cuts and transitions happen, shot lengths, the change curve, key frames of each shot
video/look.md | 458 | Camera, lighting and editing · for filmed shots: framing, camera, lighting, kit
video/packaging.md | 812 | Packaging · subtitles, styled text, stickers, picture-in-picture: timing and style
video/remake.md | 2000 | Remake plan · generation units, shoots, code builds, real material to collect, acting and emotion
video/shots/*.md | 556 | Per-shot detail, tokens per file on average · checking one shot: what is seen, the inference and its basis, prompts, frames
breakdown.json | 45905 | Full raw data · for programs; a model rarely needs it
shots/ | - | contact sheet, first and last frame of each shot · checking by eye
storyboard.jpg | - | storyboard of the whole video · the whole video at a glance
stems/ | - | voice, music and effects stems · listening, remaking the sound
packaging/ | - | subtitle files, packaging timeline, sticker frames · remaking subtitles and packaging
audio.png | - | waveform and beat chart · seeing the rhythm
```

## How to read

- One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
- `story` job in the story and the point · `seen` what is on screen · `act` acting (emotion, strength, face) · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
- Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).
- What is “seen” can be checked against the frames; what is “inferred” is the tools' and image readers' judgement, with the basis in each shot file. When they disagree, trust the frames.
