# obstacle.py
import random
import pygame
from config import *

class Obstacle:
    def __init__(self, kind: str, x: int):
        self.kind = kind
        self.x = float(x)

        if kind == "cactus_s":
            self.w, self.h = 18, 38
            self.y = GROUND_Y - self.h
        elif kind == "cactus_l":
            self.w, self.h = 26, 52
            self.y = GROUND_Y - self.h
        else:
            self.w, self.h = 46, 24
            self.y = random.choice([GROUND_Y - 90, GROUND_Y - 60])

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, speed):
        self.x -= speed

    def draw(self, surf):
        r = self.rect
        if self.kind.startswith("cactus"):
            pygame.draw.rect(surf, (30, 160, 60), r, border_radius=3)
        else:
            pygame.draw.rect(surf, (90, 90, 90), r, border_radius=6)
