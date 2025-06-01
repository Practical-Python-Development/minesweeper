"""Cell class for minesweeper."""

import pygame


class Cell:
    """Cell class for minesweeper."""
    def __init__(self, x: int, y: int):
        """
        A single cell/tile of the board.

        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        """
        self.x = x
        self.y = y
        self.size = 200

    @property
    def rect(self) -> pygame.Rect:
        """Rect of the cell."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surface: pygame.Surface):
        """Draw the cell on the given surface."""
        default_color = pygame.Color(64, 64, 64)
        pygame.draw.rect(surface, default_color, self.rect)
