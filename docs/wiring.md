# Wiring

All three peripherals share a single I²C bus. Total wires from the Pico: **2 data (SDA, SCL) + power (3V3, GND)**. Each breakout draws a few mA, well within the Pico 2's 3V3 regulator budget.

## Pico 2 pinout (relevant pins only)

The Pico 2 has the same physical pinout as Pico 1. Pin 1 is at the corner marked with a white dot on the silkscreen.

```
                    ┌──────── USB ────────┐
   GP0  / TX    1 ──┤ ●                   ├── 40  VBUS
   GP1  / RX    2 ──┤                     ├── 39  VSYS
   GND          3 ──┤                     ├── 38  GND
   GP2          4 ──┤                     ├── 37  3V3_EN
   GP3          5 ──┤                     ├── 36  3V3(OUT)   ← power rail
   GP4          6 ──┤                     ├── 35  ADC_VREF
   GP5          7 ──┤                     ├── 34  GP28
   GND          8 ──┤                     ├── 33  GND
        ...                                       ...
                    └──────────────────── ┘
```

## I²C bus assignment

| Signal | Pico 2 GP | Physical pin | Breadboard rail (suggested) |
|---|---|---|---|
| **SDA** | GP0 | 1 | blue column 1 |
| **SCL** | GP1 | 2 | blue column 2 |
| **3V3** | 3V3(OUT) | 36 | red rail (+) |
| **GND** | GND | 3, 8, 13, 18, 23, 28, 33, 38 (pick any) | blue rail (−) |

CircuitPython initializes this bus as:

```python
import board, busio
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
```

## Daisy-chaining the three I²C devices on the breadboard

Every I²C device has the same four pins: VCC, GND, SDA, SCL. They all connect to the **same** bus — they share the wires, distinguished by their unique I²C addresses.

```
   Pico 2          Breadboard rails           Each device
   ──────          ────────────────           ───────────
   3V3 (pin 36) ──→ red (+) rail   ──→ VCC of BNO055, BMP280, OLED
   GND (pin 3)  ──→ blue (−) rail  ──→ GND of BNO055, BMP280, OLED
   GP0 (pin 1)  ──→ SDA column     ──→ SDA of BNO055, BMP280, OLED
   GP1 (pin 2)  ──→ SCL column     ──→ SCL of BNO055, BMP280, OLED
```

**Pull-up resistors**: I²C buses need pull-up resistors on SDA and SCL. **All three breakout boards include their own pull-ups**, so you do not need to add any. Multiple pull-ups in parallel only weakens the effective resistance — fine in practice for short breadboard runs.

## I²C addresses

| Device | Default address | If conflict / alternative |
|---|---|---|
| BNO055 (Adafruit-original) | `0x28` | `0x29` if ADR pin pulled high |
| BNO055 (AliExpress / AZ-Delivery clone) | `0x29` | `0x28` if ADR pulled low |
| BMP280 | `0x76` | `0x77` if SDO pin pulled high |
| SSD1309 OLED 2.42" | `0x3C` | `0x3D` per jumper on rear of module |

These are unique across the bus by default, so no conflicts. Always run an I²C scan as the first integration step:

```python
import board, busio
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
while not i2c.try_lock(): pass
print([hex(a) for a in i2c.scan()])
i2c.unlock()
```

Expected output: `['0x28', '0x3c', '0x76']` (or the alternatives noted above).

## Power notes

- **Powering**: USB-C from your Mac is enough. The Pico 2 regulates 5V from USB down to 3V3 for the rails.
- **Do not connect anything to 5V (VBUS / VSYS) on these breakouts**. All three accept 3V3 only. Some breakouts have an onboard regulator that *accepts* 5V — but 3V3 is universally safe, so stick with that.
- **Always disconnect USB before re-wiring.** Hot-plugging signal wires is fine on logic-level I²C, but a stray 3V3-to-GND short while powered will trip the Pico's regulator and may need a power cycle to recover.

## Physical breadboard layout (suggested)

```
                  Half-size breadboard
   ┌──────────────────────────────────────────────┐
   │ + + + + + + + + + + + + + + + + + + + + + +  │  ← red rail (3V3)
   │ - - - - - - - - - - - - - - - - - - - - - -  │  ← blue rail (GND)
   │                                              │
   │   Pico 2 H spans columns 1–10, both halves   │
   │                                              │
   │       BNO055 ← in columns 15–18              │
   │                                              │
   │       BMP280 ← in columns 22–25              │
   │                                              │
   │       OLED   ← off-board via 4 jumper wires  │
   │                  (it's too big to plug in)   │
   │                                              │
   │ - - - - - - - - - - - - - - - - - - - - - -  │
   │ + + + + + + + + + + + + + + + + + + + + + +  │
   └──────────────────────────────────────────────┘
```

The OLED stays loose on a few jumper wires for now — final mounting happens in Phase F when the enclosure is built.
