# Project: F-14-Style Desk HUD

Desk ornament that behaves like a real Heads-Up Display via a Pepper's Ghost combiner above an OLED, with live IMU + barometric inputs. Aesthetic: early Grumman F-14 Tomcat HUD — monochrome, sparse.

## Target hardware

| Role | Part | Notes |
|---|---|---|
| MCU | Raspberry Pi Pico 2 H | RP2350, USB-C, pre-soldered headers, runs CircuitPython |
| IMU | BNO055 (breakout) | I²C, **built-in sensor fusion** — outputs quaternion + Euler directly, no Kalman filter needed |
| Altimeter | BMP280 (breakout) | I²C, barometric pressure → relative altitude |
| Display | 2.42" SSD1309 white OLED, 128×64, **I²C** | NOT SPI — make sure the listing says I²C |
| Combiner | 1–2 mm clear acrylic, ~30×30 mm | Mounted at 45° above the OLED |

## I²C bus assignments

All three peripherals share a single I²C bus on the Pico 2:

| Signal | Pico 2 pin | Pin number |
|---|---|---|
| SDA | GP0 | physical pin 1 |
| SCL | GP1 | physical pin 2 |
| 3V3 | 3V3(OUT) | physical pin 36 |
| GND | any GND | many |

| Device | Default I²C address | Notes |
|---|---|---|
| BNO055 (Adafruit) | `0x28` | |
| BNO055 (AliExpress/AZ-Delivery clone) | `0x29` | ADR pin pulled high by default — confirm with bus scan |
| BMP280 | `0x76` or `0x77` | depends on SDO pin; bus scan to confirm |
| SSD1309 OLED 2.42" | `0x3C` (default) or `0x3D` | depends on jumper on back of module |

Run an I²C bus scan as the very first integration step ([docs/bringup-checklist.md](docs/bringup-checklist.md)) — do not assume addresses.

## Software stack

- **CircuitPython** (latest stable for RP2350) on the Pico, NOT MicroPython
- Adafruit libraries: `adafruit_bno055`, `adafruit_bmp280`, `adafruit_displayio_ssd1306` (works for SSD1309 too with the right init), `displayio`
- Editing workflow: the Pico appears as a USB drive `CIRCUITPY`. Edit `code.py` directly; CircuitPython auto-reloads on save. REPL via the USB serial console (`screen /dev/tty.usbmodem*` on macOS, or use Mu Editor)
- Desktop simulator: Pygame, renders at the OLED's exact 128×64 resolution upscaled 8×

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
