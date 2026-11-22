---
videomd: 1
name: lawi
description: '“lawi”. Made with (inferred): AI-generated video 74%, still image + pan/zoom 11%, code / template render 6%, 3D render 5%, live action 4%'
source:
  file: lawi.mp4
  sha256: ac0b32113b1ec49b255c3dcf741498ee8f085b94033af1947f503eaaead9afc5
  duration: 240.033
  size: 1280x720
  fps: 30.0
  aspect: '16:9'
shots: 32
lang: en
made_mix:
  ai_video: 0.7444
  still_motion: 0.1065
  code_render: 0.0625
  cg_3d: 0.0501
  live_action: 0.0365
confidence: 0.563
readers:
- tools
open_questions: 31
generator:
  name: rea-video
  version: 0.1.0
---

# lawi.mp4

**Verdict** (inferred): Mixed production: live action or AI, to confirm 74% + still image + pan/zoom 11% + code / template render 6% + 3D render 5% + live action 4% (39% of the duration is live action or AI, to confirm: the platform transcode erased the noise evidence, needs a VLM pass or a human look at the frames); overlays: animated sticker / GIF, styled text, text labels, static graphics, static sticker (composited in code / an editor); real material used: live footage (own footage or a film / drama clip, confirm by looking) (8.8s); audio: voice; packaging: styled text ×2, text labels ×7, stickers / GIFs ×3
**Made with** (inferred, by duration): AI-generated video 74%, still image + pan/zoom 11%, code / template render 6%, 3D render 5%, live action 4%
**Remake**: 21 AI video shots + 3 3D render shots → 19 generation units, 19 MiniMax H3 / H3 Max calls; live action 1 shot → 1 scene, 1 camera setup; code render / screen capture 3 shots → 1 code project (3 parts); still-image move / static frame 4 shots → rebuilt locally
**Real material to collect**: 1 shots (4% of the duration), list in `video/remake.md`

## Next steps

- No VLM ran: if you can see images, review first: `rea-video review <this dir>` → fill `review_answers.json` → `rea-video apply-review <this dir>`
- Remake: Capsule Cinema does the generation, assembly and checks. `rea-video remake <this dir>` hands over to it, does what can be done automatically and keeps the original elsewhere; `remake/status.md` says per shot what is left. Add incoming clips to `remake/mine.json` and run it again
- Code-rendered shots are best rebuilt in an HTML video framework (such as HyperFrames) from the rhythm and key frames in `video/rhythm.md`; `rea-video code-remake <this dir>` only makes a quick draft for particles / data-visualisation pictures
- AI shots: prompts are in the generation units of `video/remake.md`; for automatic generation use Capsule Cinema: `scripts/remake_reference.py prepare <this dir>`, then `run <jobs.json> --dry-run` (paid: ask the user first)

## Open questions

- The VLM did not run (No VLM; live action / AI / 3D are told apart from pixel statistics only, so confidence is limited. An agent that can see images: run rea-vi…
- Shot #1 (0.0–3.7s): code / template render at only 48% confidence, runner-up ai_video
- Shot #2 (3.7–9.7s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC lab…
- Shot #3 (9.7–12.0s): code / template render at only 60% confidence, runner-up cg_3d
- Shot #4 (12.0–18.9s): Live action / stop motion or AI, to confirm: no AIGC label; 24fps-source marks appear in AI video, stop motion and cinema-camera footage a…
- Shot #5 (18.9–29.3s): Live action / stop motion or AI, to confirm: no AIGC label; 24fps-source marks appear in AI video, stop motion and cinema-camera footage a…
- Shot #6 (29.3–34.8s): photo / image: real material or generated, to confirm
- Shot #7 (34.8–40.1s): AI, 24p camera footage or film / TV footage, to confirm: only frame-rate evidence (a 24fps source, which films and TV share) and no AIGC l…
- 23 more, see the `flag` lines in `video/timeline.md`

## Map

Read this page first; for detail, open only the file you need. Each line is `path | ~tokens | what is in it · when to read it`; paths are relative to this directory.

```videomd-map
video/timeline.md | 1759 | Timeline: one line per shot · what a stretch says, which shots need review, how a shot was made
video/moments.md | 134 | Special moments · reveals, twists, climaxes, goofs: times, key frames, clips
video/content.md | 87 | Content and structure · what it says, the narrative line, structure, the script
video/cast.md | 32 | Cast, scenes and props · reference images for characters, first-frame prompts
video/sound.md | 180 | Sound · voice, music, sound effects, beats and sources
video/rhythm.md | 1580 | Rhythm and key frames · when cuts and transitions happen, shot lengths, the change curve, key frames of each shot
video/look.md | 693 | Camera, lighting and editing · for filmed shots: framing, camera, lighting, kit
video/packaging.md | 645 | Packaging · subtitles, styled text, stickers, picture-in-picture: timing and style
video/remake.md | 6358 | Remake plan · generation units, shoots, code builds, real material to collect, acting and emotion
video/shots/*.md | 534 | Per-shot detail, tokens per file on average · checking one shot: what is seen, the inference and its basis, prompts, frames
breakdown.json | 83464 | Full raw data · for programs; a model rarely needs it
shots/ | - | contact sheet, first and last frame of each shot · checking by eye
storyboard.jpg | - | storyboard of the whole video · the whole video at a glance
stems/ | - | voice, music and effects stems · listening, remaking the sound
packaging/ | - | subtitle files, packaging timeline, sticker frames · remaking subtitles and packaging
frames/ | - | picture scenes: full-size frames, the drawn layer cut out and sampled, measurements · remaking rendered pictures
audio.png | - | waveform and beat chart · seeing the rhythm
```

## How to read

- One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
- `story` job in the story and the point · `seen` what is on screen · `act` acting (emotion, strength, face) · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
- Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).
- What is “seen” can be checked against the frames; what is “inferred” is the tools' and image readers' judgement, with the basis in each shot file. When they disagree, trust the frames.
