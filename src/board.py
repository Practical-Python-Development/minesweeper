"""Board class to handle cell management."""

import itertools
from functools import lru_cache
import random

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
        self.place_mines()

    def init_board(self) -> list[list[Cell]]:
        """Initialize the board."""
        return [[Cell(x, y, self.cell_size) for x in range(self.width)] for y in range(self.height)]

    def place_mines(self) -> None:
        """
        Randomly choose num_mines distinct positions on the board
        and set those cells’ is_mine = True.
        """
        all_positions = [(col, row) for row in range(self.height) for col in range(self.width)]
        mine_positions = random.sample(all_positions, self.num_mines)

        for (mx, my) in mine_positions:
            self.cell_at_position(mx, my).is_mine = True

    @property
    @lru_cache
    def cell_size(self) -> tuple[int, int]:
        """Cell size of the board."""
        return self.screen_width // self.width, self.screen_height // self.height

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all cells of the board on the surface."""
        for cell in itertools.chain(*self.board):
            cell.draw(surface)

    def world2grid(self, position: tuple[int, int]) -> tuple[int, int]:
        """Calculate from world position / pixel to grid coordinates."""
        return position[0] // self.cell_size[0], position[1] // self.cell_size[1]

    def cell_at_position(self, x: int, y: int) -> Cell:
        return self.board[y][x]

    def uncover_cell(self, mouse_pos: tuple[int, int]) -> None:
        grid_x, grid_y = self.world2grid(mouse_pos)
        target_cell = self.cell_at_position(grid_x, grid_y)
        target_cell.uncover()

    def toggle_flag_cell(self, mouse_pos: tuple[int, int]) -> None:
        grid_x, grid_y = self.world2grid(mouse_pos)
        target_cell = self.cell_at_position(grid_x, grid_y)
        target_cell.toggle_flag()
