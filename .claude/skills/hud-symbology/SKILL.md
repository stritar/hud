---
name: hud-symbology
description: Use when drawing, editing, or discussing the F-14-style HUD symbology — pitch ladder, heading tape, airspeed/altitude boxes, velocity vector, reticle, bank indicator. Covers the 128×64 1-bit canvas conventions, glyph positions, what each element means in real avionics, and rules for keeping the look authentic.
---

# F-14 HUD Symbology

This skill defines what gets drawn on the HUD and how. Load it whenever editing `simulator/symbology.py`, the firmware draw routines in `firmware/code.py`, or discussing the visual design.

## Canvas conventions

- **Resolution**: 128 × 64 pixels, **1-bit** (each pixel is on or off)
- **Origin**: top-left, x right, y down
- **Center**: (64, 32) — the "boresight" cross goes here
- **Coordinate units in code**: pixels everywhere. Internal HUD physics (pitch in degrees, heading in degrees, altitude in meters) is converted to pixels at the draw call.
- **Color**: in the simulator, render as `(0, 255, 0)` on `(0, 0, 0)` for the green-phosphor look. In `displayio` on the hardware, pixels are just on/off; the green tint comes from the gel filter.

## Glyph positions (canonical layout)

```
 0,0                                                 127,0
  ┌───────────────────────────────────────────────────┐
  │  ◀ 360 010 020 030 ▶                              │  ← heading tape, y=0..6
  │                                                   │
  │                                                   │
  │  ┌────┐                              ┌────┐       │
  │  │ 320│            ─── 10 ───        │ 052│       │  ← airspeed (kts), altitude (units)
  │  │ KTS│       \                /     │ ALT│       │     boxes at y=22..34
  │  └────┘        \   ───────    /      └────┘       │
  │             ─── \      +     /  ───              │  ← center: boresight pipper +
  │                  \          /                     │     plus pitch ladder lines
  │  ┌────┐           \  ─10 ─ /             ⊕        │  ← velocity vector ⊕ (flight path marker)
  │  │  G │                                           │     drifts based on accel
  │  │ 1.0│                                           │  ← g-meter box (optional)
  │  └────┘                                           │
  │                          ▽                        │  ← bank indicator at y=56..63
  │     0    10   20   30   45   30   20   10    0   │
  └───────────────────────────────────────────────────┘
 0,63                                              127,63
```

### Element-by-element

1. **Boresight pipper** — fixed cross at (64, 32). 5 px wide, 5 px tall, plus a small gap in the middle. Never moves. Represents where the aircraft's nose is pointing. **Always drawn last so it's never occluded.**

2. **Pitch ladder** — horizontal lines at every 10° of pitch (5° for fine detail), with the label written in 5×7 font on both ends. Climb angles ("+10", "+20") are solid lines; dive angles ("-10", "-20") are dashed lines (real F-14 convention). The ladder rotates around (64, 32) by the current **roll** angle, and translates vertically by the current **pitch** angle. Conversion: **1° pitch = 2 pixels** vertical translation. This keeps the ladder readable at the small resolution.

3. **Horizon line** — special bolder pitch ladder line at 0°. 100 px wide, thicker (2 px). Same rotation as the rest of the ladder.

4. **Heading tape** — horizontal strip at top, y=0..6, showing the current compass heading. Center tick = current heading; ticks every 10° to the sides with numerical labels every 30°. Range visible at once: ~60° (so labels for current ±30°). Scroll horizontally as heading changes.

5. **Airspeed box** — left side, x=4..22, y=24..34. Three-digit airspeed in knots. Border drawn as 4 corner brackets (┌ ┐ └ ┘), not a full rectangle, to save pixels.

6. **Altitude box** — right side, x=104..124, y=24..34. Four-digit altitude in feet (or meters — pick one, we use feet for F-14 authenticity). Same corner-bracket border style.

7. **Velocity vector / flight path marker** — small circle 5 px diameter with two short "wings" sticking out left and right and a tiny tail down. Floats based on the aircraft's actual flight path angle (different from where the nose points). For the desk version: drift it based on accelerometer-derived motion direction, or fix it at the boresight for the static look.

8. **Bank angle indicator** — bottom of the screen, y=56..63. A static tick scale (0°, 10°, 20°, 30°, 45° marks) and a triangle (▽) that moves left/right to show current bank angle.

9. **Optional G-meter** — small box at x=4..22, y=44..54, showing current G force as one decimal.

## Drawing rules

- **No filled shapes**: the F-14 HUD is line-art only. Every element is strokes, never fills. Filled rectangles will look wrong.
- **Dashed lines for negative pitch**: solid for climb, dashed for dive — this is a real F-14 convention and a quick visual sanity check that you're below the horizon.
- **Always 1 pixel wide except the horizon line** (which is 2). At 128×64, 2 px is already a chunky line.
- **Numbers are 3- or 4-digit only**: pad with leading spaces, not zeros (`"320"` not `"0320"` for airspeed; `"  52"` not `"0052"` for early altitude). Leading zeros look like a calculator, not a HUD.
- **Font**: 5×7 monospace bitmap. The `terminalio.FONT` in CircuitPython is correct. In Pygame, use a 5×7 pixel font (or scale up a fixed-width system font).

## Function signatures (target for `simulator/symbology.py`)

Keep these framework-agnostic — they take a `Canvas` protocol object exposing `set_pixel(x, y)`,
`draw_line(x0, y0, x1, y1, dashed=False)`, and `draw_text(x, y, text)`. Same functions then work in
Pygame (Phase A) and `displayio` (Phase E). This block mirrors the live code in
`simulator/symbology.py` — keep them in sync.

```python
# state is a HudState (plain object): .pitch .roll .heading .airspeed .altitude .g_force
def draw_boresight(canvas) -> None: ...
def draw_pitch_ladder(canvas, pitch, roll) -> None: ...
def draw_heading_tape(canvas, heading) -> None: ...
def draw_airspeed(canvas, knots) -> None: ...
def draw_altitude(canvas, feet) -> None: ...
def draw_bank_indicator(canvas, roll) -> None: ...

def render(canvas, state) -> None:
    """Compose every element. Pipper draws last so nothing occludes it."""
    draw_pitch_ladder(canvas, state.pitch, state.roll)
    draw_heading_tape(canvas, state.heading)
    draw_airspeed(canvas, state.airspeed)
    draw_altitude(canvas, state.altitude)
    draw_bank_indicator(canvas, state.roll)
    draw_boresight(canvas)
```

**Planned, not yet implemented** (described in the diagram above but absent from
`simulator/symbology.py`): `draw_velocity_vector` (flight-path marker) and `draw_g_meter`. Add them
to both the module and `render()` when building them out.

## What "feels like an F-14" and what doesn't

Authentic:
- Sparse, lots of black space
- No anti-aliasing — pixel-perfect strokes
- Dashed lines for negative pitch
- Bracket corners on boxes, not full rectangles
- Numbers update at ~5 Hz, not 60 Hz (helps readability and adds verisimilitude)

Wrong / modern-looking, avoid:
- Filled colored shapes
- Smooth gradients
- Anti-aliased text
- Anything resembling a glass-cockpit MFD (radar arcs, moving maps, color-coded threats)
- Battery icons, Wi-Fi indicators, anything that screams "this is a microcontroller"
