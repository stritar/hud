---
name: wiring
description: Use when discussing or troubleshooting physical wiring of the HUD hardware — Pico 2 pin assignments, I²C bus layout, which breakout connects where, common short-circuit risks, and the I²C address map. Mirrors docs/wiring.md but written as enforceable rules.
---

# Wiring Rules

Load this skill whenever discussing pin assignments, modifying wiring, debugging "no I²C device found" errors, or planning enclosure cable runs.

The full diagram lives in [docs/wiring.md](../../docs/wiring.md). This file states the rules concisely.

## Single I²C bus, four wires from the Pico

All three peripherals (BNO055, BMP280, SSD1309 OLED) share **one** I²C bus on GP0/GP1. Never split them across buses. Full pin map: [docs/wiring.md](../../docs/wiring.md).

In code: `busio.I2C(scl=board.GP1, sda=board.GP0)`. **Always this order — `scl` first, `sda` second** is the CircuitPython signature.

## Power rules

- All three breakouts run on **3V3 only**. Wire to pin 36 (3V3 OUT).
- **Never connect breakouts to VBUS (pin 40) or VSYS (pin 39)** — those are 5V from USB.
- Always disconnect USB before re-wiring. Hot-plugging signal wires is fine; hot-plugging power is the risk.

## Pull-up resistors

All three breakouts include their own I²C pull-ups. **Do not add external pull-ups.** Multiple parallel pull-ups weaken the bus but at breadboard length it still works — just unnecessary.

## I²C addresses

**Never assume an address — always run `i2c.scan()` first.** The clone-vs-original ambiguity (Adafruit BNO055 `0x28` vs clone `0x29`) has caused half the support requests in this project's history (anticipated). Full default/alternative address table: [docs/wiring.md](../../docs/wiring.md).

## Rule: bring up one device at a time

When wiring new hardware, never connect all three devices before testing the bus. Order:

1. Pico only → confirm REPL works
2. + BNO055 → confirm scan shows `0x28` or `0x29`
3. + BMP280 → confirm scan shows two addresses
4. + OLED → confirm scan shows three addresses

If a device disappears from the scan after adding another, suspect a short — power down immediately.

## Common wiring failures

| Symptom | Cause | Fix |
|---|---|---|
| `i2c.scan()` returns `[]` with one device | SDA/SCL swapped | Swap the two data wires |
| Pico LED never blinks, drive doesn't mount | Charge-only USB cable | Try a different USB cable |
| Pico drive mounts as `RPI-RP2`, not `CIRCUITPY` | CircuitPython not flashed yet, or BOOTSEL was held during plug-in | Drop the UF2 onto the drive; if accidental, just unplug-replug |
| One device disappears when another is added | Both devices on the same I²C address | Use the address jumper on one of them to switch to its alternative address |
| Random reboots when USB plugged in | Brown-out from a short — usually 3V3 to GND through a misplaced jumper | Unplug, recheck the rails before rails before re-powering |
| BNO055 returns all zeros / Nones | Bus init happened too soon after power-on, BNO055 hasn't booted | Add `time.sleep(1)` after `busio.I2C(...)` |

## Enclosure cable run (Phase F)

When moving from breadboard to enclosure:

- I²C wires should be **≤ 30 cm** total run length. Beyond that the bus capacitance gets high enough to need external 2.2 kΩ pull-ups.
- Twist SDA and SCL together loosely; keeps capacitance balanced.
- Power and ground separately from signal — don't make a bundle of all four together if longer than 15 cm.

## Strict no-go list

- **Don't connect 5V to a 3V3 breakout.** All three accept 3V3 only. Some clones tolerate 5V via an onboard regulator, but 3V3 is universally safe.
- **Don't tie SDA or SCL to ground "to fix" floating-bus problems.** That breaks the bus. The pull-ups on the breakouts handle floating already.
- **Don't put the OLED on a different I²C bus** to "isolate" its higher traffic — single-bus is the design.
