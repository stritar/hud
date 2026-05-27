# Bring-up Checklist

Work through this list **in order** when hardware arrives. Each step ends in a verifiable REPL print. Do not skip ahead — debugging three new things at once is the main beginner trap.

Estimated total time: **2–4 evenings**, depending on how much trouble each step gives you.

## Step 0 — Unbox and inspect (15 min)

- [ ] Pico 2 H: confirm headers are soldered on both sides, USB-C port intact, "RP2350" markings on the main chip
- [ ] BNO055: chip in the center reads `BOSCH BNO055` (under a magnifier if necessary). Four pins minimum: VIN/VCC, GND, SDA, SCL
- [ ] BMP280: small metal can in the center labeled `BME280` or `BMP280`. Be aware **BME280** also has humidity — same code works for the pressure half
- [ ] OLED: protective film on the screen, ribbon cable secure, four pins labeled GND/VCC/SCL/SDA on the I²C version

## Step 1 — Flash CircuitPython (20 min)

- [ ] Download the latest **CircuitPython UF2 for Raspberry Pi Pico 2** (not Pico 1, not Pico 2 W): https://circuitpython.org/board/raspberry_pi_pico2/
- [ ] Hold the `BOOTSEL` button on the Pico while plugging it into USB
- [ ] A USB drive named `RPI-RP2` appears on your Mac
- [ ] Drag the downloaded `.uf2` file onto the drive — the Pico reboots and the drive re-mounts as `CIRCUITPY`
- [ ] Open `CIRCUITPY/code.py` in any text editor, replace its contents with `print("hello from pico")`, save
- [ ] Open a REPL: in Terminal run `ls /dev/tty.usbmodem*` to find the port, then `screen /dev/tty.usbmodem<TAB> 115200`. Press Enter — you should see `Adafruit CircuitPython ... >>>`. Press Ctrl-D to soft-reboot and see "hello from pico"
- [ ] To exit `screen`: Ctrl-A then K then Y

## Step 2 — Blink the on-board LED (10 min)

- [ ] Replace `code.py` with:
  ```python
  import board, digitalio, time
  led = digitalio.DigitalInOut(board.LED)
  led.direction = digitalio.Direction.OUTPUT
  while True:
      led.value = not led.value
      time.sleep(0.5)
  ```
- [ ] Save. The on-board green LED should blink at 1 Hz. If not, the Pico isn't running your code — check `CIRCUITPY/boot_out.txt` for errors and read `CIRCUITPY/code.py` to confirm it saved.

## Step 3 — Wire the BNO055 only (15 min)

Power off the Pico first (unplug USB).

- [ ] Pico GP0 (pin 1) → BNO055 SDA
- [ ] Pico GP1 (pin 2) → BNO055 SCL
- [ ] Pico 3V3 (pin 36) → BNO055 VIN/VCC
- [ ] Pico GND (pin 3) → BNO055 GND
- [ ] Plug USB back in

## Step 4 — I²C bus scan (10 min)

- [ ] Replace `code.py` with:
  ```python
  import board, busio, time
  i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
  while not i2c.try_lock(): pass
  print([hex(a) for a in i2c.scan()])
  i2c.unlock()
  time.sleep(5)
  ```
- [ ] Expected output in the REPL: `['0x28']` or `['0x29']`. If you get `[]`, recheck the four wires (most common cause: SDA/SCL swapped).

## Step 5 — Read BNO055 orientation (20 min)

- [ ] Copy `adafruit_bno055.mpy` and `adafruit_bus_device/` folder into `CIRCUITPY/lib/`. Get them from the [Adafruit CircuitPython library bundle](https://circuitpython.org/libraries) — download the bundle for your CircuitPython major version, copy just these from inside.
- [ ] Replace `code.py` with:
  ```python
  import board, busio, time, adafruit_bno055
  i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
  imu = adafruit_bno055.BNO055_I2C(i2c, address=0x28)  # try 0x29 if 0x28 fails
  while True:
      euler = imu.euler
      print(f"heading={euler[0]:.1f} roll={euler[1]:.1f} pitch={euler[2]:.1f}")
      time.sleep(0.1)
  ```
- [ ] Tilt the breadboard by hand. Roll and pitch values should change by ~5° per noticeable tilt. Yaw drifts at startup until the magnetometer self-calibrates — figure-8 motion the device for ~30 s to lock yaw.

## Step 6 — Add BMP280 to the bus (15 min)

Power off.

- [ ] Wire BMP280 in parallel with the BNO055 — same four rails (3V3, GND, SDA, SCL)
- [ ] Power on, re-run the bus scan from Step 4. Expected: `['0x28', '0x76']` (or with `0x29` and `0x77`)

## Step 7 — Read BMP280 altitude (15 min)

- [ ] Copy `adafruit_bmp280.mpy` into `CIRCUITPY/lib/`
- [ ] Replace `code.py` with:
  ```python
  import board, busio, time, adafruit_bmp280
  i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
  bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
  bmp.sea_level_pressure = 1013.25  # adjust later for your location
  ref = None
  while True:
      if ref is None:
          ref = bmp.altitude  # zero relative altitude at startup
      rel = bmp.altitude - ref
      print(f"pressure={bmp.pressure:.2f} hPa, rel_alt={rel*100:.0f} cm")
      time.sleep(0.2)
  ```
- [ ] Lift the breadboard 30 cm; `rel_alt` should jump by roughly 25–35 cm (BMP280 has ±~10 cm noise indoors — that's normal)

## Step 8 — Add the OLED and draw "HELLO" (30 min)

Power off.

- [ ] Wire the OLED in parallel with the other two — same four rails
- [ ] Copy `adafruit_displayio_ssd1306.mpy`, `adafruit_display_text/`, and `adafruit_display_shapes/` into `CIRCUITPY/lib/`
- [ ] Replace `code.py` with:
  ```python
  import board, busio, displayio, terminalio
  from adafruit_display_text import label
  import adafruit_displayio_ssd1306
  displayio.release_displays()
  i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
  bus = displayio.I2CDisplay(i2c, device_address=0x3C)
  display = adafruit_displayio_ssd1306.SSD1306(bus, width=128, height=64)
  group = displayio.Group()
  group.append(label.Label(terminalio.FONT, text="HELLO", x=40, y=32))
  display.root_group = group
  while True: pass
  ```
- [ ] You should see "HELLO" on the OLED. If the screen is upside-down, add `rotation=180` to the SSD1306 constructor.

## Step 9 — First integration: live horizon line (45 min)

This is where the project becomes "real."

- [ ] Combine Steps 5 + 8: read BNO055 roll/pitch, draw a horizon line that tilts and translates accordingly
- [ ] Ask Claude to generate this code from the symbology functions in `simulator/symbology.py`
- [ ] Tilt the breadboard — the horizon line should stay level with the actual ground

## Step 10 — Full HUD (Phase E)

At this point you have all the inputs wired and the display working. From here it's pure software: port the rest of `simulator/symbology.py` to the firmware. See [the plan](../../.claude/plans/i-want-to-build-federated-kazoo.md) Phase E.

---

## When something doesn't work

- **No REPL appears**: Make sure CircuitPython is flashed (drive should be `CIRCUITPY`, not `RPI-RP2`). Make sure your USB cable carries data.
- **I²C scan returns `[]`**: 99% of the time, SDA and SCL are swapped, or one wire isn't fully seated. Wiggle and re-check.
- **`OSError: [Errno 19] No such device`**: the address in code doesn't match the device. Scan first, then use the address it returns.
- **OLED blank but code seems to run**: check `device_address` (0x3C vs 0x3D), check the `width`/`height` match your panel (most 2.42" are 128×64, some are 128×32), and check the rotation.
- **BNO055 readings flatline at zero**: the chip needs ~600 ms to boot. The Adafruit library handles this, but if you constructed the object during a brown-out the chip may be stuck. Power-cycle the whole bus.
