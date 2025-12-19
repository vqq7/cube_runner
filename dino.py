# dino.py
import pygame
from config import *

class Dino:
    def __init__(self):
        self.x = DINO_X
        self.y = GROUND_Y - DINO_H
        self.vy = 0.0
        self.on_ground = True
        self.crouch = False

        self.jumping = False
        self.jump_hold_ms = 0
        self.jump_held = False

    @property
    def rect(self):
        h = DINO_CROUCH_H if (self.crouch and self.on_ground) else DINO_H
        return pygame.Rect(self.x, int(self.y), DINO_W, h)


    def jump(self):
        if self.on_ground:
            self.vy = JUMP_VEL
            self.on_ground = False
            self.jumping = True
            self.jump_hold_ms = 0

    def set_jump_hold(self, held: bool):
        self.jump_held = held

    def set_crouch(self, value: bool):
        self.crouch = value

        # если присели на земле — подгоняем y, чтобы "стоять" на линии пола
        if self.on_ground:
            if self.crouch:
                self.y = GROUND_Y - DINO_CROUCH_H
            else:
                self.y = GROUND_Y - DINO_H

    def update(self, dt):
        g = GRAVITY

        if not self.on_ground:
            # если жмём вниз в воздухе — падаем быстрее
            if self.crouch and self.vy > 0:
                g *= 1.6

            # variable jump (удержание)
            if self.jumping and self.vy < 0:
                if self.jump_held and self.jump_hold_ms < JUMP_HOLD_TIME:
                    g *= JUMP_HOLD_GRAVITY_MUL
                    self.jump_hold_ms += dt
                elif not self.jump_held:
                    g *= JUMP_CUT_GRAVITY_MUL

            self.vy += g
            self.y += self.vy

            # приземление (важно: учитываем разные высоты, если приземлились "в приседе")
            stand_y = GROUND_Y - (DINO_CROUCH_H if self.crouch else DINO_H)
            if self.y >= stand_y:
                self.y = stand_y
                self.vy = 0
                self.on_ground = True
                self.jumping = False
                self.jump_hold_ms = 0
        else:
            # на земле просто удерживаем правильную высоту
            self.y = GROUND_Y - (DINO_CROUCH_H if self.crouch else DINO_H)

