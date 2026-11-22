---
videomd: 1
part: remake
tokens: 2544
---

## Remake plan

### Step by step

This is a AI story short. Do the steps in this order; the detail for each is in the matching subsection below.

1. **Write the content**: one picture of your own for each of the 16 shots in the shot list
2. **Fill in the prompts**: this run had no image reading, so the shot descriptions in the units are empty; have the agent read the shots first
3. **Generate**: 10 calls (110 s), several shots each. Each shot gets one source frame for composition (subtitles erased, in `remake/refs/`), the swapped-in people, animals and products get reference images, and the prompt lists the shots in order; the original's dialogue was generated with the picture, so the lines go in the prompt
4. **Adapt the prompts to your model**: the prompts in this report are generic, and every model reads them differently (how shots are split, how references are addressed, how dialogue is written). Before generating, rewrite them following the official prompt guide of the model you actually use, or have the agent refine them with that model's prompting skill; notes for MiniMax H3 / H3 Max at the top of “AI generation”
5. **Edit**: follow the order and lengths in the shot list; the original has 16 shots at 6.9s each; 11 transitions under “Edit”
6. **Subtitles and styled text**: timing and style under “Packaging layer”
7. **Music**: find a track at the same tempo and mood (source: to confirm, about 132 BPM, F major)
8. **Put it together and compare**: hand the shots you made to the agent; it places them on the original timeline, keeps the original where yours are missing, and renders a side-by-side comparison with the original

**16 AI video shots → 10 generation units, 10 MiniMax H3 / H3 Max calls**

### Generation units

| Part | Shots | Time | Length | Prepare |
|---|---|---|---|---|
| G1 | #1, #2 | 0.0–11.8s | 11.8s | reference images |
| G2 | #3, #4 | 11.8–25.8s | 14.1s | reference images |
| G3 | #5 | 25.8–35.8s | 10.0s | reference images |
| G4 | #6–#8 | 35.8–48.9s | 13.1s | reference images |
| G5 | #9, #10 | 48.9–59.8s | 10.8s | reference images |
| G6 | #11, #12 | 59.8–71.1s | 11.3s | reference images |
| G7 | #13 | 71.1–80.3s | 9.2s | reference images |
| G8 | #14 | 80.3–90.2s | 10.0s | reference images |
| G9 | #15 | 90.2–100.3s | 10.1s | reference images |
| G10 | #16 | 100.3–110.3s | 9.9s | reference images |

**Why it is split this way**

- Grouping: consecutive shots share a call where they fit, ≤15s per call, ≤4 shots; a long stretch is cut at a scene change first
- Inputs: the model takes no reference video: one source frame per shot (subtitles erased) fixes composition, swapped-in things get their own images
- Audio: the model can generate action sound effects and ambience along with the picture; the voice was recorded by a person: record it separately and mix it in rather than having the video model speak, so copy and timing stay editable
- Packaging: the text label, styled text on the generated shots is post-production packaging: keep it out of the prompts (erased from source references) and lay it back on from the packaging timeline after generation

**G1 · shots #1, #2 · 11.8s**

- reference images: source frames of shots #1、#2 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; soft frontal light (flat light), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background slightly soft. No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 10.0s): (no description: write one in the image review) (composition: @图片2)
```

**G2 · shots #3, #4 · 14.1s**

- reference images: source frames of shots #3、#4 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; soft frontal light (flat light), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background slightly soft. No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 6.1s): (no description: write one in the image review) (composition: @图片2)
```

**G3 · shots #5 · 10.0s**

- reference images: source frames of shots #5 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; soft frontal light (flat light), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background slightly soft. No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G4 · shots #6–#8 · 13.1s**

- reference images: source frames of shots #6、#7、#8 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; soft frontal light (flat light), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background slightly soft. No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 4.2s): (no description: write one in the image review) (composition: @图片2)
Shot 3 (from 10.0s): (no description: write one in the image review) (composition: @图片3)
```

**G5 · shots #9, #10 · 10.8s**

- reference images: source frames of shots #9、#10 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; soft frontal light (flat light), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background slightly soft. No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 6.9s): (no description: write one in the image review) (composition: @图片2)
```

**G6 · shots #11, #12 · 11.3s**

- reference images: source frames of shots #11、#12 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; soft frontal light (flat light), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background slightly soft. No subtitles, captions or watermarks in the picture.
Shot 1 (from 0.0s): (no description: write one in the image review) (composition: @图片1)
Shot 2 (from 5.4s): (no description: write one in the image review) (composition: @图片2)
```

**G7 · shots #13 · 9.2s**

- reference images: source frames of shots #13 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; soft frontal light (flat light), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background slightly soft. No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G8 · shots #14 · 10.0s**

- reference images: source frames of shots #14 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; soft frontal light (flat light), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background slightly soft. No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G9 · shots #15 · 10.1s**

- reference images: source frames of shots #15 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; soft frontal light (flat light), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background slightly soft. No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```

**G10 · shots #16 · 9.9s**

- reference images: source frames of shots #16 (subtitles erased)

Draft prompt (generic; rewrite it in MiniMax H3 / H3 Max's format into remake/prompts.json before generating):

```text
Generate the shots below in order in one go, hard cuts between them; each shot takes composition, size and camera from its source frame image. Vertical 9:16; soft frontal light (flat light), soft light (wide lit-to-shadow ramp), warm (about 3000–4000K), background slightly soft. No subtitles, captions or watermarks in the picture.
(no description: write one in the image review) (composition: @图片1)
```
