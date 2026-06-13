# Project: F-14-Style Desk HUD

Desk ornament that behaves like a real Heads-Up Display via a Pepper's Ghost combiner above an OLED, with live IMU + barometric inputs. Aesthetic: early Grumman F-14 Tomcat HUD — monochrome, sparse.

## Target hardware

- **MCU**: Raspberry Pi Pico 2 H (RP2350, CircuitPython)
- **IMU**: BNO055 — I²C, built-in sensor fusion (quaternion + Euler, no Kalman needed)
- **Altimeter**: BMP280 — I²C, barometric → relative altitude
- **Display**: 2.42" SSD1309 OLED, 128×64, **I²C (not SPI)**
- **Combiner**: 1–2 mm clear acrylic, ~30×30 mm, at 45°

Full part specs + German sources: [docs/shopping-list.md](docs/shopping-list.md).

## I²C bus

All three peripherals share one bus: **SDA=GP0 (pin 1), SCL=GP1 (pin 2), power=3V3(OUT) pin 36**.
Init: `busio.I2C(scl=board.GP1, sda=board.GP0)`.
**Always run `i2c.scan()` first — never assume addresses** (clone BNO055 may be `0x29` not `0x28`).
Full pin map + address table: [docs/wiring.md](docs/wiring.md) (also enforced by the `wiring` skill).

## Software stack

- **CircuitPython** (latest stable for RP2350) on the Pico, NOT MicroPython
- Adafruit libraries: `adafruit_bno055`, `adafruit_bmp280`, `adafruit_displayio_ssd1306` (works for SSD1309 too with the right init), `displayio`
- Editing workflow: the Pico appears as a USB drive `CIRCUITPY`. Edit `code.py` directly; CircuitPython auto-reloads on save. REPL via the USB serial console (`screen /dev/tty.usbmodem*` on macOS, or use Mu Editor)
- Desktop simulator: Pygame, renders at the OLED's exact 128×64 resolution upscaled 8×

## Where things live (single source of truth — don't restate across layers)

- **docs/** = canonical detail, read on demand: full tables, diagrams, runnable code.
- **skills/** = enforceable rules + topic guidance, auto-loaded on topic. Point to docs; never restate tables.
- **CLAUDE.md** (this file) = always-on minimal index + author context + coding conventions + the few safety rules that must be present without reading anything else.

## Project documents to read for context

- [docs/shopping-list.md](docs/shopping-list.md) — German BOM
- [docs/wiring.md](docs/wiring.md) — breadboard layout
- [docs/optics.md](docs/optics.md) — Pepper's Ghost geometry
- [docs/bringup-checklist.md](docs/bringup-checklist.md) — Phase D sequence

## Project-scoped skills (auto-load when relevant)

- `.claude/skills/hud-symbology/SKILL.md` — what the F-14 HUD shows and how to draw it at 128×64
- `.claude/skills/pico-circuitpython/SKILL.md` — CircuitPython workflow, libraries, common gotchas
- `.claude/skills/wiring/SKILL.md` — pin assignments and breadboard layout rules

## Author context

- User is in Berlin, Germany. Source parts from Amazon.de first, Berlin local shops as fallback (Eckstein Components, Modulor). Avoid US suppliers (shipping + customs).
- User has zero hardware/electronics/programming-hardware experience. Explain steps that an experienced hobbyist would skip.
- User writes no firmware by hand — Claude generates all code. Bias toward small, REPL-debuggable changes.

## Coding conventions

- **Simulator**: render functions in `simulator/symbology.py` must be framework-agnostic (take a `Bitmap`-like object with a `set_pixel(x, y, value)` or `draw_line(...)` interface) so they port to CircuitPython's `displayio` later
- **Firmware**: `code.py` is the entry point. Keep it readable — favor one function per HUD element. Avoid floating-point trig in the hot loop; precompute lookup tables for sin/cos if frame rate suffers
- **Coordinates**: top-left origin, x = right, y = down (matches both Pygame and `displayio`)
- **No comments** explaining what well-named code already shows; only comment on hidden constraints (e.g., "BMP280 needs a 2 ms wait between forced-mode reads")
