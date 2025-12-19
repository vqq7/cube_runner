# helpers.py
import pygame
from config import *

def draw_dino(surf, dino):
    r = dino.rect
    pygame.draw.rect(surf, (50, 50, 50), r, border_radius=8)
    pygame.draw.circle(surf, (250, 250, 250), (r.x + r.w - 12, r.y + 12), 3)

def draw_ground_details(surf, offset):
    # линия поверхности (тонкая)
    pygame.draw.line(surf, (90, 90, 90), (0, GROUND_Y), (W, GROUND_Y), 2)

    # камушки
    for i in range(0, W, 40):
        x = int((i - offset) % W)
        pygame.draw.circle(surf, (140, 140, 140), (x, GROUND_Y + 10), 2)