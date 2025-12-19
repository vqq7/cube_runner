import sys
import pygame

from config import *
from dino import Dino
from obstacle import Obstacle
from helpers import draw_dino
from utils import spawn_obstacle, collide
from menu import run_menu


def game_loop(screen, clock, bg_image, ground_image, speed_inc):
    font = pygame.font.SysFont("Arial", 18)
    big_font = pygame.font.SysFont("Arial", 32, bold=True)

    def reset():
        dino = Dino()
        obstacles = [Obstacle("cactus_s", W + 200)]
        speed = START_SPEED
        score = 0.0
        ground_offset = 0.0
        return dino, obstacles, speed, score, ground_offset

    dino, obstacles, speed, score, ground_offset = reset()
    game_over = False

    while True:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if not game_over:
                        dino.set_jump_hold(True)
                        dino.jump()
                    else:
                        dino, obstacles, speed, score, ground_offset = reset()
                        game_over = False

                if event.key in (pygame.K_DOWN, pygame.K_s) and not game_over:
                    dino.set_crouch(True)

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    dino.set_jump_hold(False)
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    dino.set_crouch(False)

        if not game_over:
            keys = pygame.key.get_pressed()
            dino.set_jump_hold(keys[pygame.K_SPACE] or keys[pygame.K_UP])
            dino.set_crouch(keys[pygame.K_DOWN] or keys[pygame.K_s])

            dino.update(dt)

            speed += speed_inc * dt
            score += speed * 0.1
            ground_offset += speed

            for o in obstacles:
                o.update(speed)
                if collide(dino, o):
                    game_over = True

            obstacles = [o for o in obstacles if o.rect.right > -20]

            if obstacles:
                rightmost = max(o.x for o in obstacles)
                if rightmost < W + 260:
                    obstacles.append(spawn_obstacle(rightmost))

        # DRAW
        screen.blit(bg_image, (0, 0))
        screen.blit(ground_image, (0, GROUND_Y))

        for o in obstacles:
            o.draw(screen)
        draw_dino(screen, dino)

        screen.blit(font.render(f"Score: {int(score)}", True, TEXT_COLOR), (10, 10))
        screen.blit(font.render(f"Speed: {speed:.1f}", True, TEXT_COLOR), (10, 32))
        screen.blit(font.render(f"Accel: {speed_inc:.5f}   (ESC = menu)", True, TEXT_COLOR), (10, 54))

        if game_over:
            screen.blit(big_font.render("GAME OVER", True, (0, 0, 0)), (W // 2 - 110, 120))
            screen.blit(font.render("Press SPACE to restart", True, (0, 0, 0)), (W // 2 - 110, 160))

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Cube Runner")
    clock = pygame.time.Clock()

    # загрузка ресурсов (после set_mode!)
    menu_bg = pygame.image.load("assets/menu_bg.png").convert()
    menu_bg = pygame.transform.scale(menu_bg, (W, H))

    bg_image = pygame.image.load("assets/background.png").convert()
    bg_image = pygame.transform.scale(bg_image, (W, GROUND_Y))

    ground_image = pygame.image.load("assets/ground.png").convert()
    ground_image = pygame.transform.scale(ground_image, (W, H - GROUND_Y))

    speed_inc = SPEED_INC  # стартовое значение из config

    state = "menu"
    while True:
        if state == "menu":
            action, new_inc = run_menu(screen, clock, menu_bg, speed_inc)
            if action == "exit":
                pygame.quit()
                sys.exit()
            if action == "start":
                speed_inc = new_inc
                state = "game"

        elif state == "game":
            result = game_loop(screen, clock, bg_image, ground_image, speed_inc)
            if result == "exit":
                pygame.quit()
                sys.exit()
            if result == "menu":
                state = "menu"


if __name__ == "__main__":
    main()
