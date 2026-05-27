# HUD — F-14-Style Desk Heads-Up Display

A desk ornament that behaves like a real Heads-Up Display: pick it up, tilt it, lift it, and the symbology reacts. Horizon line stays level with the ground, altitude readout climbs when you raise it, heading swings as you rotate.

The aesthetic is the early Grumman F-14 Tomcat HUD — monochrome, sparse, just a pitch ladder, heading tape, airspeed/altitude readouts, velocity vector, and a reticle.

Optics use the **Pepper's Ghost** combiner-glass trick: a small OLED faces straight up and reflects off a tilted piece of clear acrylic, so the symbology appears to float on the glass — the same physical principle as a real HUD.

## Status

Pre-hardware. Phase A simulator runs on macOS via Pygame at the OLED's exact 128×64 resolution. See [the plan](https://github.com/) (currently in `~/.claude/plans/`) for the full roadmap.

## Layout

```
hud/
├── README.md                    ← this file
├── CLAUDE.md                    ← project context loaded into every Claude session
├── docs/
│   ├── shopping-list.md         ← German BOM with Amazon.de search terms + Berlin fallbacks
│   ├── wiring.md                ← breadboard layout, GPIO map, I²C addresses
│   ├── optics.md                ← Pepper's Ghost combiner geometry
│   └── bringup-checklist.md     ← Phase D step-by-step for when hardware arrives
├── .claude/skills/              ← project-scoped skills auto-loaded by Claude when relevant
│   ├── hud-symbology/
│   ├── pico-circuitpython/
│   └── wiring/
├── simulator/                   ← Phase A: Pygame prototype, no hardware needed
│   ├── hud.py
│   └── symbology.py
└── firmware/                    ← Phase E: CircuitPython for the Pico (added later)
```

## Hardware target

- **MCU**: Raspberry Pi Pico 2 H (pre-soldered headers, no iron needed)
- **IMU**: BNO055 — has built-in sensor fusion, outputs absolute orientation as quaternions
- **Pressure/altimeter**: BMP280
- **Display**: 2.42" SSD1309 white OLED, 128×64, I²C
- **Combiner**: 1–2 mm clear acrylic, mounted at 45°
- **Language**: CircuitPython

Full BOM with German sources: [docs/shopping-list.md](docs/shopping-list.md).

## Running the simulator

```bash
pip install pygame
python simulator/hud.py
```

Drag with the mouse to rotate (pitch + roll); arrow keys change altitude; left/right with Shift adjusts heading.
