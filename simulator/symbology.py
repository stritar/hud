"""F-14-style HUD symbology, rendered to a generic Canvas.

Framework-agnostic so the same functions run on Pygame (simulator) and CircuitPython
(`displayio.Bitmap`) on the Pico. Pass anything that implements the Canvas protocol:

    class Canvas:
        width: int                                   # 128 on hardware
        height: int                                  # 64 on hardware
        def set_pixel(self, x, y): ...               # turn one pixel on
        def draw_line(self, x0, y0, x1, y1,
                      dashed=False): ...             # Bresenham, optional dashed pattern
        def draw_text(self, x, y, text): ...         # 5x7-ish monospace at (x, y)

Layout conventions and rationale live in `.claude/skills/hud-symbology/SKILL.md`.
"""

import math


WIDTH = 128
HEIGHT = 64
CX = WIDTH // 2
CY = HEIGHT // 2
PIXELS_PER_DEGREE = 2


class HudState:
    """Plain data container. Avoids dataclasses for CircuitPython portability."""

    def __init__(self, pitch=0.0, roll=0.0, heading=0.0,
                 airspeed=0, altitude=0, g_force=1.0):
        self.pitch = pitch
        self.roll = roll
        self.heading = heading
        self.airspeed = airspeed
        self.altitude = altitude
        self.g_force = g_force


def _rotate(x, y, roll_deg):
    theta = math.radians(-roll_deg)
    c, s = math.cos(theta), math.sin(theta)
    rx = x * c - y * s
    ry = x * s + y * c
    return int(round(rx + CX)), int(round(ry + CY))


def draw_boresight(canvas):
    for dx in (-3, -2, 2, 3):
        canvas.set_pixel(CX + dx, CY)
    for dy in (-3, -2, 2, 3):
        canvas.set_pixel(CX, CY + dy)


def draw_pitch_ladder(canvas, pitch, roll):
    for p in (-30, -20, -10, 10, 20, 30):
        dy = (pitch - p) * PIXELS_PER_DEGREE
        if abs(dy) > HEIGHT:
            continue
        x0, y0 = _rotate(-22, dy, roll)
        x1, y1 = _rotate(-8, dy, roll)
        canvas.draw_line(x0, y0, x1, y1, dashed=(p < 0))
        x0, y0 = _rotate(8, dy, roll)
        x1, y1 = _rotate(22, dy, roll)
        canvas.draw_line(x0, y0, x1, y1, dashed=(p < 0))

    dy = pitch * PIXELS_PER_DEGREE
    if abs(dy) <= HEIGHT:
        x0, y0 = _rotate(-46, dy, roll)
        x1, y1 = _rotate(46, dy, roll)
        canvas.draw_line(x0, y0, x1, y1)
        x0, y0 = _rotate(-46, dy + 1, roll)
        x1, y1 = _rotate(46, dy + 1, roll)
        canvas.draw_line(x0, y0, x1, y1)


def draw_heading_tape(canvas, heading):
    canvas.set_pixel(CX, 0)
    canvas.set_pixel(CX, 1)
    canvas.set_pixel(CX, 2)
    label = "%03d" % (int(round(heading)) % 360)
    canvas.draw_text(CX - 8, 3, label)


def draw_airspeed(canvas, knots):
    canvas.draw_text(4, 28, "%3d" % int(knots))
    for x in range(2, 5):
        canvas.set_pixel(x, 26)
        canvas.set_pixel(x, 38)
    for x in range(20, 23):
        canvas.set_pixel(x, 26)
        canvas.set_pixel(x, 38)


def draw_altitude(canvas, feet):
    canvas.draw_text(100, 28, "%4d" % int(feet))
    for x in range(98, 101):
        canvas.set_pixel(x, 26)
        canvas.set_pixel(x, 38)
    for x in range(124, 127):
        canvas.set_pixel(x, 26)
        canvas.set_pixel(x, 38)


def draw_bank_indicator(canvas, roll):
    y_tick = 60
    for tick_deg in (-45, -30, -20, -10, 0, 10, 20, 30, 45):
        x = CX + int(round(tick_deg * 0.7))
        if 0 <= x < WIDTH:
            canvas.set_pixel(x, y_tick)
            canvas.set_pixel(x, y_tick + 1)
    px = CX + int(round(roll * 0.7))
    px = max(0, min(WIDTH - 1, px))
    canvas.set_pixel(px, y_tick - 4)
    canvas.set_pixel(px - 1, y_tick - 3)
    canvas.set_pixel(px + 1, y_tick - 3)
    canvas.set_pixel(px, y_tick - 2)


def render(canvas, state):
    draw_pitch_ladder(canvas, state.pitch, state.roll)
    draw_heading_tape(canvas, state.heading)
    draw_airspeed(canvas, state.airspeed)
    draw_altitude(canvas, state.altitude)
    draw_bank_indicator(canvas, state.roll)
    draw_boresight(canvas)
