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
        self.calculate_neighbor_mines()

        self.game_over = False

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

    def calculate_neighbor_mines(self) -> None:
        """
        For each non-mine cell, count how many of its neighbors contain a mine,
        and set neighbor_mines accordingly.
        """
        for row in range(self.height):
            for col in range(self.width):
                cell = self.cell_at_position(row, col)
                if cell.is_mine:
                    continue
                neighbors = self._get_neighbors(row, col)
                cell.num_of_neighbor_mines = sum(1 for n in neighbors if n.is_mine)

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

    def reveal_cell(self, mouse_pos: tuple[int, int]) -> None:
        grid_x, grid_y = self.world2grid(mouse_pos)
        cell = self.cell_at_position(grid_x, grid_y)

        if cell.revealed or cell.flagged:
            return

        cell.reveal()

        if cell.is_mine:
            self.game_over = True
            return

        if cell.num_of_neighbor_mines == 0:
            self._flood_fill(cell)

    def toggle_flag_cell(self, mouse_pos: tuple[int, int]) -> None:
        grid_x, grid_y = self.world2grid(mouse_pos)
        target_cell = self.cell_at_position(grid_x, grid_y)
        target_cell.toggle_flag()

    def _get_neighbors(self, x: int, y: int) -> list[Cell]:
        """
        Return a list of neighboring Cell objects around (x, y).
        Includes up to 8 neighbors, excluding out‐of‐bounds and (x,y) itself.
        """
        neighbors: list[Cell] = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append(self.cell_at_position(nx, ny))
        return neighbors

    def _flood_fill(self, start_cell: Cell) -> None:
        """
        Reveal all connected trivial cells.

        Reveal all connected cells that have neighbor_mines == 0,
        and their respective neighbours (to show border numbers).
        """
        stack = [start_cell]
        visited = set()

        while stack:
            cur = stack.pop()
            key = (cur.x, cur.y)
            if key in visited:
                continue
            visited.add(key)

            if not cur.revealed:
                cur.reveal()

            if cur.is_mine or cur.num_of_neighbor_mines != 0:
                continue

            for neighbor in self._get_neighbors(cur.x, cur.y):
                if not neighbor.revealed and not neighbor.is_mine:
                    stack.append(neighbor)
