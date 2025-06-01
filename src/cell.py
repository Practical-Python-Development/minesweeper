"""Cell class for minesweeper."""

import pygame


class Cell:
    """Cell class for minesweeper."""
    def __init__(self, x: int, y: int, size: tuple[int, int]):
        """
        A single cell/tile of the board.

        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :param size: size of the cell
        """
        self.x = x
        self.y = y
        self.size = size

        self.is_covered = True

    @property
    def rect(self) -> pygame.Rect:
        """Rect of the cell."""
        return pygame.Rect(
            self.x * self.size[0],
            self.y * self.size[1],
            self.size[0],
            self.size[1],
        )

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the cell on the given surface."""
        default_color = pygame.Color(64, 64, 64)
        uncovered_color = pygame.Color(0, 0, 0)

        color = default_color if self.is_covered else uncovered_color
        pygame.draw.rect(surface, color, self.rect)

    def uncover(self):
        """Uncover the cell."""
        self.is_covered = False
