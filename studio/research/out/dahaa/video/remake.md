---
videomd: 1
part: remake
tokens: 1988
---

## Remake plan

### Step by step

This is a AI story short. Do the steps in this order; the detail for each is in the matching subsection below.

1. **Write the content**: one picture of your own for each of the 16 shots in the shot list
2. **Fill in the prompts**: this run had no image reading, so the shot descriptions in the units are empty; have the agent read the shots first
3. **Generate**: 6 calls (59 s), several shots each. Each shot gets one source frame for composition (subtitles erased, in `remake/refs/`), the swapped-in people, animals and products get reference images, and the prompt lists the shots in order
4. **Adapt the prompts to your model**: the prompts in this report are generic, and every model reads them differently (how shots are split, how references are addressed, how dialogue is written). Before generating, rewrite them following the official prompt guide of the model you actually use, or have the agent refine them with that model's prompting skill; notes for MiniMax H3 / H3 Max at the top of “AI generation”
5. **Voice**: the original is TTS voice-over; record it yourself or use TTS
6. **Edit**: follow the order and lengths in the shot list; the original has 16 shots at 3.7s each
7. **Subtitles and styled text**: timing and style under “Packaging layer”
8. **Put it together and compare**: hand the shots you made to the agent; it places them on the original timeline, keeps the original where yours are missing, and renders a side-by-side comparison with the original

**16 AI video shots → 6 generation units, 6 MiniMax H3 / H3 Max calls**

### Generation units

| Part | Shots | Time | Length | Prepare |
|---|---|---|---|---|
| G1 | #1 | 0.0–12.4s | 12.4s | reference images |
| G2 | #2, #3 | 12.4–27.3s | 14.9s | reference images |
| G3 | #4–#7 | 27.3–35.4s | 8.1s | reference images |
| G4 | #8–#11 | 35.4–42.8s | 7.5s | reference images |
| G5 | #12–#14 | 42.8–51.8s | 9.0s | reference images |
| G6 | #15, #16 | 51.8–59.0s | 7.2s | reference images |

**Why it is split this way**

- Grouping: consecutive shots share a call where they fit, ≤15s per call, ≤4 shots; a long stretch is cut at a scene change first
- Inputs: the model takes no reference video: one source frame per shot (subtitles erased) fixes composition, swapped-in things get their own images
- Audio: the model can generate action sound effects and ambience along with the picture; voice-over is better done as separate TTS and mixed in, so copy and timing stay editable
- Packaging: the text label, styled text, sticker on the generated shots is post-production packaging: keep it out of the prompts (erased from source references) and lay it back on from the packaging timeline after generation

**G1 · shots #1 · 12.4s**

- reference images: source frames of shots #1 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; three-quarter key + fill (standard set-up), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G2 · shots #2, #3 · 14.9s**

- reference images: source frames of shots #2、#3 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; three-quarter key + fill (standard set-up), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 13.0s): (no description: write one in the image review) (composition: @图片2)
```

**G3 · shots #4–#7 · 8.1s**

- reference images: source frames of shots #4、#5、#6、#7 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; three-quarter key + fill (standard set-up), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 1.4s): (no description: write one in the image review) (composition: @图片2)
Shot 3 (from 3.2s): (no description: write one in the image review) (composition: @图片3)
Shot 4 (from 4.0s): (no description: write one in the image review) (composition: @图片4)
```

**G4 · shots #8–#11 · 7.5s**

- reference images: source frames of shots #8、#9、#10、#11 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; three-quarter key + fill (standard set-up), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 1.8s): (no description: write one in the image review) (composition: @图片2)
Shot 3 (from 3.4s): (no description: write one in the image review) (composition: @图片3)
Shot 4 (from 5.3s): (no description: write one in the image review) (composition: @图片4)
```

**G5 · shots #12–#14 · 9.0s**

- reference images: source frames of shots #12、#13、#14 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; three-quarter key + fill (standard set-up), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 2.5s): (no description: write one in the image review) (composition: @图片2)
Shot 3 (from 5.9s): (no description: write one in the image review) (composition: @图片3)
```

**G6 · shots #15, #16 · 7.2s**

- reference images: source frames of shots #15、#16 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; three-quarter key + fill (standard set-up), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background clearly blurred (shallow depth of field / portrait mode). No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 3.6s): (no description: write one in the image review) (composition: @图片2)
```
