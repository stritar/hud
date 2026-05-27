# Optics — The Pepper's Ghost Combiner

A real fighter HUD projects symbology onto a "combiner" — a partially-reflective transparent panel between the pilot and the windscreen. The pilot sees the outside world *through* the combiner with the symbology floating *on* it, focused at infinity.

The desk version uses the same principle, scaled down. **Pepper's Ghost** is the magic-trick name for the same physics: a brightly-lit image source on one axis, a tilted semi-transparent surface, and a viewer on a perpendicular axis. The viewer sees the image apparently floating in space behind the glass.

## Geometry

```
       Side view (cross-section):

       Viewer's eye  ←─────────────────  ┌─────┐
                                          │     │   ← what the viewer perceives:
                                          │ floating symbology behind the combiner
                                          └─────┘

                          ╱
                         ╱   ← combiner acrylic at 45°
                        ╱       (reflects OLED upward, transmits background)
                       ╱
                      ╱
       ┌─────────────┐
       │    OLED     │   ← face-up at the base
       │  (face up)  │
       └─────────────┘
```

**Key rule**: the combiner is at 45° relative to the OLED surface, and the viewer looks at the combiner from the front (perpendicular to the OLED's normal). The reflected image appears to float **behind** the combiner, at the same distance the OLED is *below* the combiner.

## Dimensions for the desk version

- **OLED**: 2.42" diagonal, active area roughly **56 × 28 mm**
- **Combiner**: 30 × 30 mm clear acrylic, 1–2 mm thick
- **Combiner tilt**: exactly 45° from the OLED surface
- **Distance from OLED surface to combiner's lower edge**: ~10–15 mm (just enough that the combiner doesn't physically touch the OLED but stays close enough to capture the image)
- **Viewer distance**: ~30–60 cm (arm's length on a desk)

## Cardboard mockup first

Before committing to a final enclosure, build the geometry from cardboard, a piece of acrylic, and your laptop showing a static white-on-black symbology pattern.

1. Cut a 70×70 mm cardboard base
2. Cut a 40×40 mm cardboard "back wall" — tape it standing up at the rear of the base
3. Cut a 40 mm tall cardboard mount with a slot at 45° to hold the acrylic
4. Tape the acrylic into the slot
5. Lay your phone or the laptop screen face-up at the base, showing a green-text-on-black image
6. Look horizontally at the acrylic — the text should appear floating behind it

If the image is hard to see, troubleshoot in this order:
- **Background**: behind the acrylic, you should be looking at something *dark* (a matte black card, a dark wall). Bright background = washed-out symbology.
- **Brightness**: the OLED is plenty bright at full intensity, but check that nothing dims it (a stray finger over the screen, a green gel filter cutting too much light)
- **Tilt angle**: must be 45°. Off by 10° and the image position shifts dramatically and looks wrong.
- **Acrylic surface quality**: scratches, dust, and protective film all kill the effect. Peel any film off the acrylic.

## Why white OLED + green gel, not green OLED

You can buy 0.96" green-pixel OLEDs, but at 2.42" the standard parts are all white or yellow. The fix: white OLED at full brightness with a thin green photography gel filter (a "Rosco gel" sheet) over it gives:

- The brightness of a white OLED (white pixels emit much more total light than green ones)
- The phosphor-green F-14 aesthetic
- Trivially swappable — peel the gel to test, replace to ship

## Enclosure for the final build (Phase F)

After the cardboard mockup works:

- **3D-printed** (preferred): a simple two-piece print, base + canopy with combiner slot. Black PLA, matte finish. Fab Lab Berlin or any local print service.
- **Laser-cut wood/acrylic**: flat panels glued at right angles. Modulor cuts to order.
- **Hand-cut wood**: a small block of walnut/oak with a slot routed in for the combiner is the most "ornament-like" option, if you have or can borrow basic woodworking tools.

Whatever the material, **the interior must be matte black**. Any reflective surface inside the enclosure will bounce stray light into the combiner and ghost the image. Matte black spray paint, black felt, or black flocking paper all work.

## Optional: focus-at-infinity

A real HUD uses collimating optics so the symbology appears focused at infinity (the pilot doesn't have to refocus between the outside world and the HUD). The desk version skips this — the symbology appears focused at the OLED's apparent distance behind the combiner, which is fine for a desk ornament. Adding a collimating Fresnel lens between the OLED and combiner is a v2 project.
