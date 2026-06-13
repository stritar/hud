---
name: pico-circuitpython
description: Use when writing or debugging CircuitPython code for the Raspberry Pi Pico 2 in this project. Covers the edit/save/reload workflow on the CIRCUITPY drive, REPL access from macOS, mandatory library imports for BNO055 + BMP280 + SSD1309, memory and frame-rate gotchas, and the structure for the firmware/code.py main loop.
---

# CircuitPython on the Pico 2 — Project Workflow

Apply this skill whenever generating, editing, or debugging code that runs on the device (anything in `firmware/`).

## The device is the filesystem

CircuitPython exposes the Pico 2 as a USB mass-storage device called `CIRCUITPY`. There is no compile step, no flashing for code changes, no toolchain to install. Editing `CIRCUITPY/code.py` and saving auto-reloads the program.

- **Entry point**: `code.py` at the root of `CIRCUITPY`
- **Libraries**: drop `.mpy` files (or whole folders) into `CIRCUITPY/lib/`
- **REPL access on macOS**: `screen /dev/tty.usbmodem<TAB> 115200`. Exit with Ctrl-A, K, Y.
- **Stop the running program** to get an interactive REPL: Ctrl-C in the screen session
- **Soft reboot** (re-runs `code.py`): Ctrl-D

In this repo, the firmware sources live under `firmware/`. The mental model is: those files get copied to `CIRCUITPY` (root for `code.py`, `lib/` for libraries) and run unmodified. Do not write CPython-only constructs.

## Mandatory libraries for this project

Put these in `CIRCUITPY/lib/` (download from the [CircuitPython library bundle](https://circuitpython.org/libraries) matching the installed CircuitPython major version):

- `adafruit_bno055.mpy` — IMU
- `adafruit_bmp280.mpy` — pressure / altitude
- `adafruit_displayio_ssd1306.mpy` — OLED driver (works for SSD1309 with default params)
- `adafruit_display_text/` (folder) — text labels in `displayio`
- `adafruit_display_shapes/` (folder) — lines, rects, circles
- `adafruit_bus_device/` (folder) — I²C transaction helper, required by the others
- `adafruit_register/` (folder) — register helper, required by some sensors

## Bus initialization (use exactly this)

```python
import board, busio
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
```

Pins are GP0 (SDA) / GP1 (SCL) per [docs/wiring.md](../../docs/wiring.md). Do not use the alternate I²C bus on GP2/GP3 — it's reserved for future expansion.

## Main loop structure (target for `firmware/code.py`)

```python
import board, busio, displayio, time
import adafruit_bno055, adafruit_bmp280
import adafruit_displayio_ssd1306
from hud_symbology import render, HudState   # ported from simulator/symbology.py

displayio.release_displays()
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

imu = adafruit_bno055.BNO055_I2C(i2c, address=0x28)
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(bus, width=128, height=64)

ref_alt = bmp.altitude

bitmap = displayio.Bitmap(128, 64, 2)
palette = displayio.Palette(2); palette[0] = 0x000000; palette[1] = 0xFFFFFF
tile = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group(); group.append(tile)
display.root_group = group

while True:
    euler = imu.euler  # (heading, roll, pitch) in degrees; may be (None, None, None) briefly at boot
    if euler[0] is not None:
        state = HudState(
            heading=euler[0],
            roll=euler[1],
            pitch=euler[2],
            altitude=int((bmp.altitude - ref_alt) * 3.281),  # meters → feet
            airspeed=320,   # placeholder until we add a real input
        )
        for y in range(64):
            for x in range(128):
                bitmap[x, y] = 0
        render(BitmapCanvas(bitmap), state)   # BitmapCanvas = thin displayio adapter exposing the Canvas protocol
    time.sleep(0.05)
```

## Gotchas

- **`displayio.release_displays()` at the top**: required every time you reflash, otherwise the second run errors with "Display bus is already in use"
- **`imu.euler` returns `(None, None, None)` for the first ~600 ms** after boot. Always guard with `if euler[0] is not None`.
- **`bmp.altitude` is noisy** at ±10 cm. For HUD use, smooth with a 5-sample rolling average if it's distracting.
- **`time.sleep(0.05)`** = 20 fps. Faster than 30 fps is wasted (the OLED itself updates at ~60 Hz max but I²C transfers are the bottleneck).
- **`bitmap[x, y] = v`** is the per-pixel set. Slow in a hot loop — for 128×64 = 8192 pixels per frame, this is the main perf concern. Two mitigations: (1) only clear the regions you'll redraw, (2) write whole rows via memoryview slicing if perf demands it.
- **Memory**: Pico 2 has 520 KB SRAM, plenty for this. Don't worry about MicroPython-style memory squeezing.
- **`board.GP0` vs `board.D0`**: the Pico 2 uses `GPx` naming. Don't copy `boardD0` examples from random Adafruit tutorials written for Feather boards.

## Sensor calibration notes

- **BNO055**: yaw drifts until the internal magnetometer self-calibrates. Wave the device in a figure-8 motion for ~30 s on first power-on. Pitch and roll work immediately.
- **BMP280**: reports absolute altitude relative to sea-level pressure. For the desk version, zero it at startup by capturing `ref_alt` once and subtracting (see main loop above). For the F-14 aesthetic, scale to feet via `meters × 3.281`.

## Don't do these

- Don't use `MicroPython`-only modules (`machine`, `utime`). CircuitPython uses `time` and `board` instead.
- Don't write blocking sleeps longer than 50 ms in the main loop — input latency for "pick up the device" feel suffers
- Don't add anti-aliasing to draw routines — the panel is 1-bit, AA produces visual noise
- Don't import heavy `numpy`-style libraries; they don't exist on CircuitPython. Use `math.sin` / `math.cos` from the standard library.
