---
videomd: 1
part: timeline
shots: 16
tokens: 971
---

# Timeline

One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
`story` job in the story and the point · `seen` what is on screen · `act` acting (emotion, strength, face) · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).

```videomd-timeline
#01 0.0-10.0 | camera smooth move | overlay text, styled text | made~ AI-generated video 70% · runner-up AI avatar (talking head) 8% | material~ AI-generated | remake AI generation · G1 | flag to confirm
#02 10.0-11.8 | camera smooth move | made~ AI-generated video 57% · runner-up live action 26% | material~ AI-generated | remake AI generation · G1 | flag low confidence,to confirm
#03 11.8-17.8 | camera smooth move | transition fade through 0.4s | made~ AI-generated video 69% · runner-up 3D render 18% | material~ AI-generated | remake AI generation · G2 | flag to confirm
#04 17.8-25.8 | camera smooth move | transition fade through 0.4s | made~ AI-generated video 70% · runner-up 3D render 18% | material~ AI-generated | remake AI generation · G2 | flag to confirm
#05 25.8-35.8 | camera smooth move | transition fade through 0.4s | overlay title | made~ AI-generated video 70% · runner-up 3D render 15% | material~ AI-generated | remake AI generation · G3 | flag to confirm
#06 35.8-40.0 | camera smooth move | transition fade through 0.4s | made~ AI-generated video 70% · runner-up 3D render 10% | material~ AI-generated | remake AI generation · G4 | flag to confirm
#07 40.0-45.9 | camera smooth move | transition fade through 0.3s | overlay styled text | made~ AI-generated video 70% · runner-up 3D render 14% | material~ AI-generated | remake AI generation · G4 | flag to confirm
#08 45.9-48.9 | camera smooth move | transition fade through 0.4s | overlay title | made~ AI-generated video 70% · runner-up AI avatar (talking head) 7% | material~ AI-generated | remake AI generation · G4 | flag to confirm
#09 48.9-55.8 | camera smooth move | transition blur 0.3s | made~ AI-generated video 70% · runner-up 3D render 9% | material~ AI-generated | remake AI generation · G5 | flag to confirm
#10 55.8-59.8 | camera smooth move | transition fade through 0.4s | made~ AI-generated video 70% · runner-up AI avatar (talking head) 8% | material~ AI-generated | remake AI generation · G5 | flag to confirm
#11 59.8-65.2 | camera smooth move | transition fade through 0.4s | overlay title | made~ AI-generated video 70% · runner-up live action 5% | material~ AI-generated | remake AI generation · G6 | flag to confirm
#12 65.2-71.1 | camera smooth move | overlay subtitle | made~ AI-generated video 70% · runner-up AI avatar (talking head) 8% | material~ AI-generated | remake AI generation · G6 | flag to confirm
#13 71.1-80.3 | camera smooth move | overlay styled text | made~ AI-generated video 70% · runner-up live action 4% | material~ AI-generated | remake AI generation · G7 | flag to confirm
#14 80.3-90.2 | camera smooth move | overlay text, styled text | made~ AI-generated video 47% · runner-up live action 38% | material~ AI-generated | remake AI generation · G8 | flag low confidence,to confirm
#15 90.2-100.3 | camera static (subject moves) | transition fade through 0.3s | made~ AI-generated video 48% · runner-up live action 39% | material~ AI-generated | remake AI generation · G9 | flag low confidence,to confirm
#16 100.3-110.3 | camera smooth move | transition fade through 0.4s | made~ AI-generated video 70% · runner-up 3D render 3% | material~ AI-generated | remake AI generation · G10 | flag to confirm
```
