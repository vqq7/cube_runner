# utils.py
import random
from obstacle import Obstacle
from config import *

def spawn_obstacle(last_x):
    kind = random.choices(
        ["cactus_s", "cactus_l", "ptero"],
        weights=[0.5, 0.35, 0.15]
    )[0]
    gap = random.randint(260, 420)
    return Obstacle(kind, max(W + 40, last_x + gap))

def collide(dino, obs):
    return dino.rect.inflate(-6, -6).colliderect(
        obs.rect.inflate(-4, -4)
    )
