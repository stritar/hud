# Shopping List — German Suppliers

All parts sourced in Germany. Primary path is **Amazon.de** (most are Prime, AZ-Delivery ships from Deggendorf so usually next-day). Berlin local fallback for each item is noted in the notes column.

Budget target: **€60–100**. Actual total below is roughly **€70–85** depending on which OLED and IMU listings you pick.

## Core electronics

- [ ] **Raspberry Pi Pico 2 H** — €7–10
  - Amazon.de search: `Raspberry Pi Pico 2 H` (the "H" suffix = headers pre-soldered, what you want)
  - **Watch out**: Pico 2 **W** is the wireless version, more expensive and you don't need Wi-Fi. Plain **Pico 2 H** is correct.
  - Berlin fallback: [eckstein-shop.de](https://eckstein-shop.de) carries it, ships from Berlin

- [ ] **BNO055 9-DOF IMU breakout** — €15–25
  - Amazon.de search: `BNO055 9DOF Modul` or `BNO055 GY-955`
  - **Watch out**: some listings ship the cheaper MPU-9250 with a misleading title — confirm the chip name "BNO055" appears in product photos
  - **Watch out**: clone modules often have I²C address `0x29` instead of Adafruit's `0x28` — both work, just need to pass the right address in code
  - Berlin fallback: eckstein-shop.de, or berrybase.de
  - Adafruit-original part on Amazon.de runs ~€25; clones ~€15

- [ ] **BMP280 barometric pressure breakout** — €4–8
  - Amazon.de search: `BMP280 Modul I2C` (AZ-Delivery sells a 3-pack ~€8)
  - **Don't accidentally buy BMP180** — older, less sensitive, larger footprint
  - Berlin fallback: berrybase.de

- [ ] **2.42" SSD1309 OLED, 128×64, I²C, white** — €15–22
  - Amazon.de search: `2.42 Zoll OLED I2C 128x64 weiß` or `SSD1309 OLED 2.42`
  - **Watch out — critical**: many 2.42" OLED listings are **SPI**, which uses 4 wires instead of 2. Confirm the title or photos say "I²C" (or "IIC"). If only SPI is available, that works too but the wiring guide needs to change.
  - Pixel color: white reads best through the combiner. Yellow also fine. Avoid blue (poor contrast with green gel filter).
  - Berlin fallback: eckstein-shop.de

## Connectors and breadboard

- [ ] **Half-size solderless breadboard** (~400 pins) — €3–5
  - Amazon.de search: `Breadboard 400 Pin` — AZ-Delivery 3-pack ~€7 is good value
  - Berlin fallback: any electronics shop

- [ ] **Jumper wire set** (M-M + M-F, 20+ each) — €5–8
  - Amazon.de search: `Jumper Kabel Set 120` (a typical 120-piece kit, ~€7)
  - Get a kit with M-M, M-F, and F-F variants — you'll likely use all three

- [ ] **USB-C cable, data-capable** — €0–6
  - You probably already own one. If not, any name-brand USB-C-to-USB-A or USB-C-to-USB-C data cable works. **Avoid "charge-only" cables** — they have no data lines and the Pico won't appear as a drive.

## Optics

- [ ] **Clear acrylic, 1–2 mm thick**, ~30×30 mm offcut — €3–8
  - Amazon.de search: `Acrylglas Zuschnitt 1mm A6` (smallest sizes available there)
  - **Berlin local — recommended**: [Modulor at Moritzplatz](https://www.modulor.de) sells offcuts by weight; ~€2 for a small piece. Smoother edges and you can choose the exact size.
  - Alternative: a microscope slide (Objektträger) works at a pinch — sold cheaply at any biology supply or even Müller.

- [ ] **Optional — green gel filter** — €3–6
  - Amazon.de search: `Farbfolie grün Fotografie` or `Rosco gel green`
  - Cut a 30×30 mm square, lay it over the OLED for that phosphor-green F-14 look
  - **Berlin local — recommended**: Foto Brenner or Foto Lübeck in Mitte sell single sheets

## Optional later additions (Phase F)

- [ ] **Momentary tactile button** — €3 (pack of 10)
  - For cycling display modes ("NAV", "BORESIGHT", "ACM")
  - Amazon.de search: `Taster 6x6 Breadboard` — buy a 10-pack, cheap insurance

- [ ] **3D printing service** or filament — varies
  - Berlin options: Fab Lab Berlin, Modulor's print service, or just keep a cardboard enclosure for v1

## Summary by supplier (typical happy path)

**One Amazon.de order** (€55–75):
- Raspberry Pi Pico 2 H
- BNO055 module
- BMP280 module
- 2.42" SSD1309 OLED I²C
- Breadboard
- Jumper wire set
- USB-C cable (if needed)
- Momentary button pack (if adding now)

**Berlin walk-in** (€5–10):
- Acrylic offcut from Modulor (Moritzplatz, U-Bahn U1/U8)
- Green gel filter from a photo shop

## When everything arrives

Open `docs/bringup-checklist.md` and go through it in order. Do **not** wire all three sensors at once — bring up the bus, then add one device at a time.
