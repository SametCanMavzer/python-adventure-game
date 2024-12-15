from pygame import Rect
from game_settings import *

class Player:
    def __init__(self):
        self.rect = Rect(50, HEIGHT - 100, 40, 60)
        self.vx = 0
        self.vy = 0
        self.frame = 0
        self.facing = "right"
        self.jumping = False
        self.animation_timer = 0
        self.health = 3
        self.frames_right = ['hero_walk1', 'hero_walk2', 'hero_walk3', 'hero_walk4']
        self.frames_left = ['hero_walk1_l', 'hero_walk2_l', 'hero_walk3_l', 'hero_walk4_l']

    def update(self):
        self.vy += GRAVITY
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vy = 0
            self.jumping = False

        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.frame = (self.frame + 1) % len(self.frames_right)
            self.animation_timer = 0

class Enemy:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 40, 40)
        self.direction = 1
        self.frame = 0
        self.animation_timer = 0
        self.patrol_start = x
        self.patrol_end = x + 200

    def update(self):
        self.rect.x += 2 * self.direction
        if self.rect.x >= self.patrol_end:
            self.direction = -1
        elif self.rect.x <= self.patrol_start:
            self.direction = 1

        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.frame = (self.frame + 1) % 4
            self.animation_timer = 0