"""Cell class for minesweeper."""

import pygame


class Cell:
    """Cell class for minesweeper."""

    class Color:
        DEFAULT = (64, 64, 64)
        REVEALED = (0, 0, 0)
        FLAG = (255, 0, 0)
        MINE = (0, 255, 0)
        TEXT = (0, 0, 255)  # ToDo depending of number of neighbours

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

        self.revealed = False
        self.flagged = False
        self.is_mine = False
        self.num_of_neighbor_mines = -1

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
        if not self.revealed:
            pygame.draw.rect(surface, self.Color.DEFAULT, self.rect)
        else:
            pygame.draw.rect(surface, self.Color.REVEALED, self.rect)
            if self.is_mine:
                pygame.draw.ellipse(surface, self.Color.MINE, self.rect)
            elif self.num_of_neighbor_mines > 0:
                font = pygame.font.Font(pygame.font.get_default_font(), min(self.size))
                text_surface = font.render(
                    str(self.num_of_neighbor_mines), True, self.Color.TEXT
                )
                text_rect = text_surface.get_rect(center=self.rect.center)
                surface.blit(text_surface, text_rect)

        if self.flagged:
            points = [
                (self.rect.left + self.size[0] * 0.3, self.rect.top + self.size[1] * 0.7),
                (self.rect.left + self.size[0] * 0.7, self.rect.top + self.size[1] * 0.5),
                (self.rect.left + self.size[0] * 0.3, self.rect.top + self.size[1] * 0.3),
            ]
            pygame.draw.polygon(surface, self.Color.FLAG, points)

        # draw boarder
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 1)

    def reveal(self):
        """Uncover the cell."""
        self.revealed = True

    def toggle_flag(self):
        """Toggle the flag of the cell."""
        self.flagged = not self.flagged
