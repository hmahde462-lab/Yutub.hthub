---
videomd: 1
part: remake
tokens: 6346
---

## Remake plan

### Step by step

This is a AI story short. Do the steps in this order; the detail for each is in the matching subsection below.

1. **Write the content**: one picture of your own for each of the 32 shots in the shot list
2. **Collect material**: the real material in the picture (live footage) needs the original files, listed under “What to prepare”
3. **Fill in the prompts**: this run had no image reading, so the shot descriptions in the units are empty; have the agent read the shots first
4. **Generate**: 19 calls (191 s), several shots each. Each shot gets one source frame for composition (subtitles erased, in `remake/refs/`), the swapped-in people, animals and products get reference images, and the prompt lists the shots in order
5. **Adapt the prompts to your model**: the prompts in this report are generic, and every model reads them differently (how shots are split, how references are addressed, how dialogue is written). Before generating, rewrite them following the official prompt guide of the model you actually use, or have the agent refine them with that model's prompting skill; notes for MiniMax H3 / H3 Max at the top of “AI generation”
6. **Live shots**: 1 shots to film yourself; camera and light under “Shoot” below
7. **Motion graphics**: have the agent make an editable first version and change the text and pictures on top of it rather than starting from scratch; the first version is only a start, where it differs from the original is under “Code build”
8. **Stills with moves**: swap in your images; the agent moves them the way the original does
9. **Voice**: the original is TTS voice-over; record it yourself or use TTS
10. **Edit**: follow the order and lengths in the shot list; the original has 32 shots at 7.5s each; 11 transitions under “Edit”
11. **Subtitles and styled text**: timing and style under “Packaging layer”
12. **Put it together and compare**: hand the shots you made to the agent; it places them on the original timeline, keeps the original where yours are missing, and renders a side-by-side comparison with the original

**21 AI video shots + 3 3D render shots → 19 generation units, 19 MiniMax H3 / H3 Max calls; live action 1 shot → 1 scene, 1 camera setup; code render / screen capture 3 shots → 1 code project (3 parts); still-image move / static frame 4 shots → rebuilt locally**

### Generation units

| Part | Shots | Time | Length | Prepare |
|---|---|---|---|---|
| G1 | #2, #4 | 3.7–9.7s, 12.0–18.9s | 12.9s | reference images |
| G2 | #5 | 18.9–29.3s | 10.3s | reference images |
| G3 | #7 | 34.8–40.1s | 5.4s | reference images |
| G4 | #9, #10 | 48.9–62.2s | 13.3s | reference images |
| G5 | #11, #12 | 62.2–75.9s | 13.7s | reference images |
| G6 | #13, #14 | 75.9–82.8s | 6.9s | reference images |
| G7 | #15 | 82.8–93.6s | 10.8s | reference images |
| G8 | #16 | 93.6–99.9s | 6.3s | reference images |
| G9 | #17 | 99.9–111.0s | 11.2s | reference images |
| G10 | #18 | 111.0–119.9s | 8.9s | reference images |
| G11 | #19 | 119.9–127.2s | 7.3s | reference images |
| G12 | #20 | 127.2–140.8s | 13.6s | reference images |
| G13 | #21, #22 | 140.8–153.6s | 12.8s | reference images |
| G14 | #23 | 153.6–167.2s | 13.5s | reference images |
| G15 | #24 | 167.2–174.0s | 6.8s | reference images |
| G16 | #25 | 174.0–186.8s | 12.9s | reference images |
| G17 | #26 | 186.8–194.7s | 7.9s | reference images |
| G18 | #29 | 210.5–217.9s | 7.4s | reference images |
| G19 | #31 | 230.0–238.9s | 8.9s | reference images |

**Why it is split this way**

- Grouping: consecutive shots share a call where they fit, ≤15s per call, ≤4 shots; a long stretch is cut at a scene change first
- Inputs: the model takes no reference video: one source frame per shot (subtitles erased) fixes composition, swapped-in things get their own images
- Audio: the model can generate action sound effects and ambience along with the picture; voice-over is better done as separate TTS and mixed in, so copy and timing stay editable
- Packaging: the sticker, text label, styled text on the generated shots is post-production packaging: keep it out of the prompts (erased from source references) and lay it back on from the packaging timeline after generation

**G1 · shots #2, #4 · 12.9s**

- reference images: source frames of shots #2、#4 (subtitles erased)

- these shots are separated by inserts in the cut: generate them together and put the inserts back in the edit

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 6.0s): (no description: write one in the image review) (composition: @图片2)
```

**G2 · shots #5 · 10.3s**

- reference images: source frames of shots #5 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G3 · shots #7 · 5.4s**

- reference images: source frames of shots #7 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G4 · shots #9, #10 · 13.3s**

- reference images: source frames of shots #9、#10 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 9.1s): (no description: write one in the image review) (composition: @图片2)
```

**G5 · shots #11, #12 · 13.7s**

- reference images: source frames of shots #11、#12 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 3.7s): (no description: write one in the image review) (composition: @图片2)
```

**G6 · shots #13, #14 · 6.9s**

- reference images: source frames of shots #13、#14 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 4.0s): (no description: write one in the image review) (composition: @图片2)
```

**G7 · shots #15 · 10.8s**

- reference images: source frames of shots #15 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G8 · shots #16 · 6.3s**

- reference images: source frames of shots #16 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G9 · shots #17 · 11.2s**

- reference images: source frames of shots #17 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G10 · shots #18 · 8.9s**

- reference images: source frames of shots #18 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G11 · shots #19 · 7.3s**

- reference images: source frames of shots #19 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G12 · shots #20 · 13.6s**

- reference images: source frames of shots #20 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G13 · shots #21, #22 · 12.8s**

- reference images: source frames of shots #21、#22 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 7.4s): (no description: write one in the image review) (composition: @图片2)
```

**G14 · shots #23 · 13.5s**

- reference images: source frames of shots #23 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G15 · shots #24 · 6.8s**

- reference images: source frames of shots #24 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G16 · shots #25 · 12.9s**

- reference images: source frames of shots #25 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G17 · shots #26 · 7.9s**

- reference images: source frames of shots #26 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G18 · shots #29 · 7.4s**

- reference images: source frames of shots #29 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G19 · shots #31 · 8.9s**

- reference images: source frames of shots #31 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Horizontal 16:9; soft frontal light (flat light), hard light (sharp shadow edge), cool (daylight / cool-white LED), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

### Shooting scenes

Shoot every shot of one scene before moving to the next; within a scene, shoot the wider sizes first and the close-ups last so the lighting is set only once. Leave about 1s of handle at both ends of every take.

**S1**: shots #8 (8.77s on screen)
- Lighting: three-quarter key + fill (standard set-up), key light frame left, three-quarter front, neutral (about 5000K)
- Setup medium close-up · moving camera (gimbal / handheld pan) · push-in: shots #8, 8.77s on screen, shoot about 10.8s

### Code composition

Rebuild it as one project in an HTML video framework (such as HyperFrames or Remotion): cuts, transitions and each shot's key frames from "Rhythm and key frames", layout, colours and elements from the scenes below. Text and UI are 100% controllable, changing copy is a data change, and an AI coding assistant can write the project.

`rea-video code-remake <breakdown folder>` only makes a quick draft: it renders `code/remake.mp4` from each scene's sampled points / cut-out, motion and background glow and scores it. Particles, point clouds and data visualisations on a dark ground come close; an illustrated character's acting and morph transitions do not.

- Part 1: shots #1 (0.0–3.7s)
- Part 2: shots #3 (9.7–12.0s)
- Part 3: shots #27 (194.7–203.7s)

Remake assets (all in the report folder; hand them over together with the data below to whoever writes the code, or to an LLM):
- `shots/shot_XXX_first.jpg` / `_last.jpg`: first / last frame of each shot at full size, for layout, type size and margins
- `shots/shot_XXX_strip.jpg`: key frames about every 0.5 s, to follow the animation
- `shots/shot_XXX_elements.jpg` and `_el_NN.jpg` / `_st_NN.jpg` / `_ly_NN.jpg`: full-size crop of every element once settled, numbered as in the motion timeline; redraw shapes from them, cut out icons, logos and illustrations that cannot be redrawn
- `packaging/overlays.ass`, `packaging/timeline.json`: timing, position and colour of the text

How to build the pictures (by the measured picture type):
- kinetic type: Word-by-word spring() entrances (offset + scale + opacity), highlight boxes on key words; match font, size and leading from the frame
- particles / point cloud: Three.js particle system (points sampled on the target shape, morph between shapes, bloom), rendered frame by frame with @remotion/three
- vector shapes: SVG shapes + interpolate() / spring() keyframes, positions and timing measured from the frame

Particle shots: what shape the particles form in each shot and how it moves decides whether the remake works; chapter cards, labels and counters go in an HTML layer on top. Build shot by shot from the table below, not one shared background.

| Shot | Time | Build | Picture | Camera | Colours | On-screen text |
|---|---|---|---|---|---|---|
| #1 | 0.0–3.7s | kinetic type | (to fill from the images: what the elements form and how they move) | static | ground #0b1618 · #808e96 #99a3a6 #51606e #1e2928 · drawn #9ca19e #b9bdba #293433 #05080b | 1942 |
| #3 | 9.7–12.0s | particles / point cloud | (to fill from the images: what the elements form and how they move) | static | ground #000204 · #021219 #29323a #19222a #3d474e #515e67 · drawn #69757d #88959f #4a5056 #aebbc5 | — |
| #27 | 194.7–203.7s | vector shapes | (to fill from the images: what the elements form and how they move) | static frame, elements move inside it | ground #5f666d · #666e7d #606b78 #757481 #586775 · drawn #fefaf7 #d6ada7 #c1807f #f5ddce | — |

**Picture scenes** (a new scene whenever what is drawn moves or changes shape as a whole inside a shot. `frames/` holds first / middle / last full-size frames per scene, `scene_XX_layer.png` the drawn layer of the middle frame (background and text removed, alpha by how strongly it stands out), `frames/points/scene_XX.json` samples of that layer, one `x y r g b a` per row with x, y in 0–1. Place particles, trace lines or redraw shapes from these instead of guessing from a description. `track` in `frames/scenes.json` follows the layer's centre and spread over time)

| Scene | Shot | Time | Ground | Background glow | Drawn colours | Pieces | Area (x0 y0 x1 y1) | Motion |
|---|---|---|---|---|---|---|---|---|
| scene_01 | #1 | 0.0–3.7s | #56647a | #081112, centre (0.58, 0.60), radius 0.29 | #a7aeaa #2a3733 #05090a | 30 | 0.03 0.56 0.99 0.74 | near still |
| scene_02 | #3 | 9.7–12.0s | #000000 | #657279, centre (0.55, 0.67), radius 0.24 | #808e95 #56636a #adbbc2 | 548 | 0.04 0.48 0.96 0.95 | near still |
| scene_03 | #27 | 194.7–203.7s | #686e79 | #8c7885, centre (0.51, 0.12), radius 0.19 | #fdfdf9 #f4e4d3 #c3918d | 1 | 0.48 0.29 0.52 0.36 | near still |

When built, score it with `rea-video compare original remake --scenes frames/scenes.json -o dir` (each side's drawn layer is taken against its own ground, so a new ground colour still compares) and fix the lowest-scoring scenes first, from `compare_worst.jpg`.

Per-shot motion timeline (measured: positions in % of frame width / height, colours sampled once the element settles; read together with the key-frame strip)

**Motion #1 0.0–3.7s · 0 events**

- Ground #0b1618; other main colours #808e96 #99a3a6 #51606e #1e2928; drawn layer #9ca19e #b9bdba #293433 #05080b
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: shape / text block · x 0%–67%, y 72%–100% · #060b0f · [crop](shots/shot_001_st_01.jpg)

**Motion #3 9.7–12.0s · 2 events**

- Ground #000204; other main colours #021219 #29323a #19222a #3d474e #515e67; drawn layer #69757d #88959f #4a5056 #aebbc5
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- [crop L1](shots/shot_003_ly_01.jpg) [crop L2](shots/shot_003_ly_02.jpg) · Continuous layer: 52% of the frame moves through the whole shot (x 2%–98%, y 8%–96%), e.g. drifting gradients, particle flow, breathing glow
1. 11.67–11.93s · middle right (x 58%–82%, y 44%–64%) · changes, ease-in-out · #50575d · [crop](shots/shot_003_el_01.jpg)
2. 11.67–11.93s · bottom left (x 2%–27%, y 76%–96%) · changes, moves leftward, ease-in-out · #333a43 · [crop](shots/shot_003_el_02.jpg)

**Motion #27 194.7–203.7s · 0 events**

- Ground #5f666d; other main colours #666e7d #606b78 #757481 #586775; drawn layer #fefaf7 #d6ada7 #c1807f #f5ddce
Element crops (numbers match the motion list below; L = the continuously moving layer mid-shot and at the end, S = elements that never move), full-size files in `shots/`:

- S1. never moves: shape / text block · x 13%–69%, y 52%–72% · #5a6171 · [crop](shots/shot_027_st_01.jpg)
- S2. never moves: shape / text block · x 81%–87%, y 91%–99% · #636062 · [crop](shots/shot_027_st_02.jpg)

### Local rebuild

- #6 still image + pan/zoom 5.5s; #28 still image + pan/zoom 6.8s; #30 still image + pan/zoom 12.1s; #32 still image + pan/zoom 1.2s: one image + the measured zoom / pan parameters, rendered straight from ffmpeg

### Real material in the picture (the original files are needed)

1 shots, 8.77s (4%) contain real material (screen recordings, screenshots, photos, embedded video); a model cannot stand in for them:

- **live footage (own footage or a film / drama clip, confirm by looking)** (whole frame): shots #8, 8.8s in all
