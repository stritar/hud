"""Phase A simulator: F-14 HUD rendered at the OLED's exact 128x64 resolution,
upscaled 8x on screen for visibility.

Controls:
    mouse drag      - pitch (vertical) and roll (horizontal)
    arrow up/down   - altitude +- 5 ft
    arrow left/right - heading +- 1 deg
    R               - reset state
    Esc / window X  - quit

Run:
    pip install pygame
    python simulator/hud.py
"""

import sys
import pygame

from symbology import HudState, render, WIDTH, HEIGHT


SCALE = 8
WINDOW_W, WINDOW_H = WIDTH * SCALE, HEIGHT * SCALE
FG = (0, 255, 0)
BG = (0, 0, 0)

BLOOM_STRENGTH = 0.7
VIGNETTE_FALLOFF = 0.85
VIGNETTE_FLOOR = 0.25


def make_vignette(window_w, window_h, small=48):
    h = int(small * window_h / window_w)
    surf = pygame.Surface((small, h))
    cx, cy = (small - 1) / 2, (h - 1) / 2
    max_d = (cx * cx + cy * cy) ** 0.5
    for y in range(h):
        for x in range(small):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / max_d
            b = int(255 * max(VIGNETTE_FLOOR, 1.0 - d * VIGNETTE_FALLOFF))
            surf.set_at((x, y), (b, b, b))
    return pygame.transform.smoothscale(surf, (window_w, window_h))


def apply_crt(canvas, vignette):
    sharp = pygame.transform.smoothscale(canvas, (WINDOW_W, WINDOW_H))
    tiny = pygame.transform.smoothscale(canvas, (WIDTH // 2, HEIGHT // 2))
    bloom = pygame.transform.smoothscale(tiny, (WINDOW_W, WINDOW_H))
    bloom.set_alpha(int(255 * BLOOM_STRENGTH))
    sharp.blit(bloom, (0, 0), special_flags=pygame.BLEND_ADD)
    sharp.blit(vignette, (0, 0), special_flags=pygame.BLEND_MULT)
    return sharp


class PygameCanvas:
    def __init__(self, surface, font):
        self.surface = surface
        self.font = font
        self.width = WIDTH
        self.height = HEIGHT

    def set_pixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.surface.set_at((x, y), FG)

    def draw_line(self, x0, y0, x1, y1, dashed=False):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        i = 0
        x, y = x0, y0
        while True:
            if (not dashed) or ((i // 2) % 2 == 0):
                self.set_pixel(x, y)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
            i += 1

    def draw_text(self, x, y, text):
        glyphs = self.font.render(text, False, FG, BG)
        self.surface.blit(glyphs, (x, y))


def main():
    pygame.init()
    pygame.display.set_caption("HUD simulator - 128x64 @ 8x")
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    canvas_surface = pygame.Surface((WIDTH, HEIGHT))
    font = pygame.font.SysFont("Courier", 10, bold=True)
    vignette = make_vignette(WINDOW_W, WINDOW_H)

    state = HudState(pitch=0.0, roll=0.0, heading=90.0,
                     airspeed=320, altitude=5000, g_force=1.0)

    dragging = False
    last_mouse = (0, 0)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                state = HudState(pitch=0.0, roll=0.0, heading=90.0,
                                 airspeed=320, altitude=5000, g_force=1.0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                last_mouse = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - last_mouse[0]
                dy = event.pos[1] - last_mouse[1]
                state.roll += dx * 0.2
                state.pitch += dy * 0.2
                state.pitch = max(-45.0, min(45.0, state.pitch))
                last_mouse = event.pos

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            state.altitude += 5
        if keys[pygame.K_DOWN]:
            state.altitude = max(0, state.altitude - 5)
        if keys[pygame.K_LEFT]:
            state.heading = (state.heading - 1) % 360
        if keys[pygame.K_RIGHT]:
            state.heading = (state.heading + 1) % 360

        canvas_surface.fill(BG)
        render(PygameCanvas(canvas_surface, font), state)

        window.blit(apply_crt(canvas_surface, vignette), (0, 0))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
