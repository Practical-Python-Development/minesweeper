"""Utilities for minesweeper application."""

from enum import Enum

import pygame


class GameState(Enum):
    """Game state enum."""

    NONE = 0
    RUNNING = 1
    WIN = 2
    LOSS = 3
    SELECTING = 4
    NEW = 5


def draw_button(
    screen, text, rect, font, text_color, button_color, hover_color, mouse_pos
):
    color = hover_color if rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)

    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
