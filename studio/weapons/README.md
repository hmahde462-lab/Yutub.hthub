# Magic Forest — FPS weapon models (GLB)

Procedural, game-ready weapon models built with Blender (`bpy`) from code.

| File | Moving parts (separate nodes) |
|---|---|
| M4.glb | Magazine, ChargingHandle, BoltCarrier, DustCover, Trigger |
| AK47.glb | Magazine, DustCover, BoltCarrier (+charging handle), Selector, Trigger |
| LMG.glb | FeedCover (hinged at front), AmmoBox (+belt), ChargingHandle, Trigger |
| Sniper.glb | Bolt, Magazine, Trigger |
| Shotgun.glb | Pump (+action bars), Shell (for reload), Trigger |
| SMG.glb | Magazine, ChargingHandle, Selector, Trigger |
| Optic_RedDot.glb / Optic_Scope4x.glb / Optic_SniperScope.glb | Reticle (emissive) |

- `glb/`: 2048px textures. `glb_mobile/`: 1024px textures (use on phones).
- Units: metres, real-world scale. glTF Y-up; **muzzle points to −Z** (camera forward).
- Weapon origin = top of the pistol grip (firing-hand pivot). Each moving part's origin is its own pivot
  (magazine at the mag well, triggers at the pin, LMG cover at its hinge, bolts on the bore axis).
- Sockets (empty nodes): `Socket_Optic` (rail top, attach optic `Socket_Mount` here), `Socket_Muzzle`,
  `Socket_Eject`, `Socket_LeftHand`, `Socket_RightHand`, `Socket_IronSight` (ADS eye line), `Socket_MagWell`.
  Optics have `Socket_Eye` (ADS camera position) and `Socket_Mount`.
- Materials: PBR metal-roughness (albedo, metallic-roughness, normal) — parkerized steel, black-anodized aluminium,
  blued steel, polymer (black/FDE), wood, rubber, knurled grip, brass, glass/lens, emissive reticle.
- Triangles: 5k–10k per weapon, 2k–4k per optic.

Rebuild: `python3 textures.py 2048 && python3 weapons.py --preview --mobile`
