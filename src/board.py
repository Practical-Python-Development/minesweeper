"""Board class to handle cell management."""

import itertools

import pygame

from cell import Cell

class Board:
    """Board class to handle cell management."""

    def __init__(
        self,
        width: int,
        height: int,
        num_mines: int,
        screen_height: int = 600,
        screen_width: int = 600,
    ):
        """
        Board class to handle cell management.

        :param width: width of the board
        :param height: height of the board
        :param num_mines: number of mines
        :param screen_height: screen height of the board
        :param screen_width: screen width of the board
        """
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.screen_height = screen_height
        self.screen_width = screen_width

        self.board = self.init_board()

    def init_board(self) -> list[list[Cell]]:
        return [[Cell(x, y, self.cell_size) for x in range(self.width)] for y in range(self.height)]

    @property
    def cell_size(self) -> tuple[int, int]:
        return self.screen_width // self.width, self.screen_height // self.height

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all cells of the board on the surface."""
        for cell in itertools.chain(*self.board):
            cell.draw(surface)
