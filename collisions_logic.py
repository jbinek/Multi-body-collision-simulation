import pygame as pg
import numpy as np
from numpy.linalg import norm as Abs
import time
from random import uniform as r
from random import randint as rint
from scipy.constants import g

pg.init()

# Circle Properties
circle_r = 0.025  # m
circle_v_min, circle_v_max = 0.01, 0.2  # m/s, m/s
circle_height, circle_density = 0.5, 480  # m, kg/m^3
px_per_m = 750  # Pixel per meter
circle_quantity = 10
seizure = False

# Window
win_width, win_height = 1050, 750
win_width_temp, win_height_temp = win_width, win_height
win_width_min, win_height_min = 200, 200
info = pg.display.Info()
win = pg.display.set_mode([win_width, win_height], pg.RESIZABLE)
full = False  # Fullscreen

# Time
time_0 = time.time()
time_d = time.time() - time_0

# Mouse
mouse_pos = np.array(pg.mouse.get_pos())
mouse_f_abs = 1

# Gravity
g_toggle = False
g_amp = 1

# Aesthetic
hud = True
font = pg.font.SysFont('trebuchetms', 25)


# Circle
class Circle(object):
    def __init__(self, pos, rad, v):
        # Physical Properties
        self.pos = np.array(pos)
        self.r = rad * px_per_m
        self.v = np.array(v) * px_per_m
        self.m = np.pi * rad ** 2 * circle_height * circle_density

        # Logic
        self.prev_collision = None

        # Aesthetics
        self.color = (rint(10, 255), rint(10, 255), rint(10, 255)) if seizure else (255, 0, 0)

    def circle_collide(self, circle, circle_v):
        # Physics
        c = circle.pos - self.pos
        v_c = (c[0] * self.v[0] + c[1] * self.v[1]) / (
                c[0] ** 2 + c[1] ** 2) * c  # Velocity component in direction of collision
        v_t = self.v - v_c  # Velocity component tangent to direction of collision

        circle_c = self.pos - circle.pos
        circle_v_c = (circle_c[0] * circle_v[0] + circle_c[1] * circle_v[1]) / (
                circle_c[0] ** 2 + circle_c[1] ** 2) * circle_c

        # Calculate new velocity in direction of collision while tangent velocity is preserved:
        v_c_new = ((self.m - circle.m) / (self.m + circle.m)) * v_c + (2 * circle.m / (self.m + circle.m)) * circle_v_c
        self.v = v_c_new + v_t

        # Logic
        self.color = (rint(10, 255), rint(10, 255), rint(10, 255)) if seizure else (255, 0, 0)
        self.prev_collision = circle

    def wall_collide(self):
        # Physics
        if self.r > self.pos[0] or self.pos[0] > win_width - self.r:
            self.pos[0] = self.r if self.r > self.pos[0] else win_width - self.r
            self.v[0] = -self.v[0]
            # Logic
            self.prev_collision = None

        if self.r > self.pos[1] or self.pos[1] > win_height - self.r:
            self.pos[1] = self.r if self.r > self.pos[1] else win_height - self.r
            self.v[1] = -self.v[1]
            # Logic
            self.prev_collision = None

    def vortex(self):
        # Physics
        mouse_dir = mouse_pos - self.pos
        mouse_f = mouse_dir * (mouse_f_abs / Abs(mouse_dir)) * px_per_m
        mouse_a = mouse_f / self.m
        self.v = self.v + mouse_a * time_d
        # Logic
        self.prev_collision = None

    def gravity(self):
        self.v = self.v + np.array([0, g_amp * g]) * time_d * px_per_m

    def move(self):
        self.pos = self.pos + self.v * time_d

    def draw(self):
        draw_pos = np.around(self.pos).astype(int)
        pg.draw.circle(win, self.color, draw_pos, round(self.r))


def rPos():
    return rint(1, win_width), rint(1, win_height)


def rRad():
    return r(circle_r, circle_r)


def rVel():
    return r(circle_v_min, circle_v_max), r(circle_v_min, circle_v_max)