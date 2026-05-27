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
  - **Headers not pre-soldered** on the Adafruit-original — the 10-pin male header strip ships loose in the bag. We're soldering it ourselves; see the **Soldering supplies** section below.
  - Berlin fallback: eckstein-shop.de, or berrybase.de
  - Adafruit-original part on Amazon.de runs ~€25; clones ~€15
  - **Picked**: Minhe GY-BNO055 (Amazon.de, ~€13). Has on-board LDO so VIN tolerates 3–5 V; headers ship loose (we solder them). Verify chip markings on arrival before soldering.

- [ ] **BMP280 barometric pressure breakout** — €4–8
  - Amazon.de search: `BMP280 Modul I2C` (AZ-Delivery sells a 3-pack ~€8)
  - **Don't accidentally buy BMP180** — older, less sensitive, larger footprint
  - Berlin fallback: berrybase.de

- [ ] **2.42" SSD1309 OLED, 128×64, I²C, green** — €15–22
  - Amazon.de search: `2.42 Zoll OLED I2C 128x64 grün` or `SSD1309 OLED 2.42 IIC`
  - **Watch out — critical**: many 2.42" OLED listings are **SPI**, which uses 4 wires instead of 2. Confirm the title or photos say "I²C" (or "IIC"). If only SPI is available, that works too but the wiring guide needs to change.
  - Pixel color: **green is most authentic** — the real F-14 HUD used a green phosphor CRT, so a green OLED gets you closer to the look than white and removes the need for a separate gel filter. White and yellow are fine fallbacks if green is out of stock. Avoid blue (wrong era, wrong feel).
  - **Picked**: Hailege 2.42" SSD1309 IIC Green (Amazon.de, €17.99). Address jumper on back is labeled `0x78`/`0x7A` (8-bit) = `0x3C`/`0x3D` in CircuitPython.
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

- [ ] **Optional — green gel filter** — €3–6 *(skip if you picked the green OLED above)*
  - Amazon.de search: `Farbfolie grün Fotografie` or `Rosco gel green`
  - Only needed if your OLED is white or yellow — cut a 30×30 mm square and lay it over the panel for that phosphor-green F-14 look.
  - **Berlin local — recommended**: Foto Brenner or Foto Lübeck in Mitte sell single sheets

## Soldering supplies

You only need to solder one 10-pin header strip onto the BNO055 — about 10 joints, large pads, ~5 minutes of actual soldering once you're set up. But since this is your first time, get a temperature-controlled iron (not a fixed-temp €10 pencil) — it makes the difference between "easy" and "frustrating".

- [ ] **Temperature-controlled soldering iron, ~60 W** — €25–45
  - Amazon.de search: `Lötkolben Temperaturregelung 60W` — the **TS80P** or **Pinecil V2** are the enthusiast favorites (~€60, USB-C powered, lifetime tool); the cheaper option is an **AZ-Delivery / Tabiger station** at ~€25–35 which is fine for one-off jobs.
  - **Avoid**: the €10 fixed-temperature "pencil" irons — they run too hot, burn pads, and make beginners think they're bad at soldering.
  - Berlin fallback: [eckstein-shop.de](https://eckstein-shop.de) carries Pinecil; Conrad Berlin (Hauptbahnhof) has stations in stock.

- [ ] **Lead-free solder wire, 0.8 mm or 1.0 mm, with rosin core** — €8–12
  - Amazon.de search: `Lötzinn bleifrei 0.8mm Rosin` — a 100 g roll lasts years.
  - **Why lead-free**: EU RoHS rules. Slightly harder to work with than leaded (higher melting point, less shiny joints) but a non-issue at this scale.
  - **Watch out**: avoid "acid core" or plumbing solder — only **rosin/flux core electronics solder**.

- [ ] **Helping hands / PCB holder** — €8–15
  - Amazon.de search: `Helping Hands Lötstation` or `Lötzubehör dritte Hand`
  - You need *something* to hold the board while both your hands are busy with iron and solder. A cheap clamp-with-alligator-clips works; a small vise is nicer.

- [ ] **Solder wick (desoldering braid), 2 mm** — €4–6
  - Amazon.de search: `Entlötlitze 2mm`
  - For when you bridge two pins together (you will, at least once). Press the braid onto the bridge, heat with the iron, the excess solder wicks into the braid.

- [ ] **Flux pen or paste** (optional but recommended for first-timer) — €5–8
  - Amazon.de search: `Flussmittel Stift Elektronik` or `Lötflussmittel No-Clean`
  - A dab of flux on each pad before soldering makes the solder flow cleanly. Strongly reduces "cold joint" frustration.

- [ ] **Safety: work near an open window, or a small fume fan** — €0–15
  - Rosin smoke is mildly irritating, not dangerous in 5-minute sessions, but don't inhale it directly. A USB desk fan blowing the smoke *away from you* costs nothing extra.
  - Optional proper fume extractor: Amazon.de search `Lötrauchabsaugung USB`, ~€15.

- [x] **Heat-resistant work surface** — €0–8
  - A silicone soldering mat (`Lötmatte Silikon`, ~€8) protects the desk. A ceramic tile from any hardware store (€2) works too. **Do not solder directly on wood or plastic.**
  - **Picked**: MMOBIEL Silicone Repair and Soldering Mat, 45×30 cm, heat resistant to 500 °C (Amazon.de, €14.99). Larger than strictly needed but doubles as a general workbench mat.

**Estimated soldering kit total: €40–80** depending on iron choice.

**Berlin walk-in alternative for soldering supplies**: [Eckstein Components](https://eckstein-shop.de) in Pankow stocks irons, solder, wick, and flux — one stop, you can ask the staff for advice.

If this feels like too much spend or hassle for one header strip: any **Berlin makerspace** (Fab Lab Berlin in Kreuzberg, c-base in Mitte) lets you walk in and use their soldering stations for free or a small donation. That gets the BNO055 done in 10 minutes without owning any tools.

## Optional later additions (Phase F)

- [ ] **Momentary tactile button** — €3 (pack of 10)
  - For cycling display modes ("NAV", "BORESIGHT", "ACM")
  - Amazon.de search: `Taster 6x6 Breadboard` — buy a 10-pack, cheap insurance

- [ ] **3D printing service** or filament — varies
  - Berlin options: Fab Lab Berlin, Modulor's print service, or just keep a cardboard enclosure for v1

## Summary by supplier (typical happy path)

**One Amazon.de order** (€95–155):
- Raspberry Pi Pico 2 H
- BNO055 module
- BMP280 module
- 2.42" SSD1309 OLED I²C
- Breadboard
- Jumper wire set
- USB-C cable (if needed)
- Momentary button pack (if adding now)
- Soldering iron + solder + wick + helping hands + flux

**Berlin walk-in** (€5–10):
- Acrylic offcut from Modulor (Moritzplatz, U-Bahn U1/U8)
- Green gel filter from a photo shop
- (alternative) Soldering supplies from Eckstein Components in Pankow if you prefer asking a human

## When everything arrives

Open `docs/bringup-checklist.md` and go through it in order. Do **not** wire all three sensors at once — bring up the bus, then add one device at a time.
