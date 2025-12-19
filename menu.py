# menu.py
import pygame
from config import W, H

BTN_COLOR = (30, 30, 30)
BTN_HOVER = (60, 60, 60)
BTN_TEXT = (245, 245, 245)

def _draw_button(screen, rect, text, font, mouse_pos):
    color = BTN_HOVER if rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=12)
    label = font.render(text, True, BTN_TEXT)
    screen.blit(label, (rect.centerx - label.get_width() // 2,
                        rect.centery - label.get_height() // 2))

def run_menu(screen, clock, menu_bg, speed_inc_value):
    """
    Возвращает:
      ("start", new_speed_inc) или ("exit", None)
    """
    title_font = pygame.font.SysFont("Arial", 44, bold=True)
    font = pygame.font.SysFont("Arial", 22)
    small = pygame.font.SysFont("Arial", 18)

    # границы и шаг изменения ускорения
    MIN_INC = 0.00002
    MAX_INC = 0.00200
    STEP    = 0.00005

    speed_inc = float(speed_inc_value)

    # --- Layout (без панели, центрируем по экрану) ---
    # Заголовок
    title_y = 35

    # Кнопки
    start_rect = pygame.Rect(W//2 - 110, 120, 220, 45)
    exit_rect  = pygame.Rect(W//2 - 110, 175, 220, 45)

    # +/- рядом с кнопкой START (по бокам), чтобы выглядело аккуратно
    pm_size = (44, 38)
    minus_rect = pygame.Rect(start_rect.left - 70, start_rect.top + 4, *pm_size)
    plus_rect  = pygame.Rect(start_rect.right + 26, start_rect.top + 4, *pm_size)

    # Скорость снизу
    accel_label_y = 245

    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "exit", None
                if event.key == pygame.K_RETURN:
                    return "start", speed_inc

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_rect.collidepoint(mouse_pos):
                    return "start", speed_inc
                if exit_rect.collidepoint(mouse_pos):
                    return "exit", None

                if minus_rect.collidepoint(mouse_pos):
                    speed_inc = max(MIN_INC, speed_inc - STEP)
                if plus_rect.collidepoint(mouse_pos):
                    speed_inc = min(MAX_INC, speed_inc + STEP)

        # ----- DRAW -----
        screen.blit(menu_bg, (0, 0))
        # Кнопки +/-
        _draw_button(screen, minus_rect, "-", font, mouse_pos)
        _draw_button(screen, plus_rect, "+", font, mouse_pos)

        # Start / Exit
        _draw_button(screen, start_rect, "START", font, mouse_pos)
        _draw_button(screen, exit_rect, "EXIT", font, mouse_pos)

        # SPEED снизу (по центру)
        lbl = small.render("Acceleration (SPEED_INC):", True, (10, 10, 10))
        val = small.render(f"{speed_inc:.5f}", True, (10, 10, 10))

        # лёгкая тень (чтобы читалось на любом фоне)
        lbl_s = small.render("Acceleration (SPEED_INC):", True, (255, 255, 255))
        val_s = small.render(f"{speed_inc:.5f}", True, (255, 255, 255))

        screen.blit(lbl_s, (W//2 - lbl.get_width()//2 + 1, accel_label_y + 1))
        screen.blit(lbl,   (W//2 - lbl.get_width()//2,     accel_label_y))

        screen.blit(val_s, (W//2 - val.get_width()//2 + 1, accel_label_y + 22 + 1))
        screen.blit(val,   (W//2 - val.get_width()//2,     accel_label_y + 22))

        pygame.display.flip()
