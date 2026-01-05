"""Game module."""

from __future__ import annotations

from abc import ABC, abstractmethod

import pygame

from board import Board
from utils import GameState


class Game(ABC):
    """Generic game class."""

    def __init__(
        self,
        screen: pygame.display,
        clock: pygame.time.Clock,
    ) -> None:
        """Initialise the game class."""
        self.screen = screen
        self.clock = clock

    @abstractmethod
    def run(self, events: list[pygame.event.Event]) -> GameState:
        """Run the game."""


class Minesweeper(Game):
    def __init__(
        self,
        num_mines: int,
        num_cells_x: int,
        num_cells_y: int,
        screen: pygame.display | None = None,
        clock: pygame.time.Clock | None = None,
    ):
        """
        Initialise the game.

        :param num_mines: the number of mines
        :param num_cells_x: the number of cells in a column
        :param num_cells_y: the number of cells in a row
        :param screen: the pygame screen, if None a new one will be created and pygame
            will get initialised.
        :param clock: the pygame clock, if None a new one will be created and pygame
        """
        super().__init__(screen, clock)

        self.board = Board(
            width=num_cells_x,
            height=num_cells_y,
            num_mines=num_mines,
            screen_height=screen.get_height(),
            screen_width=screen.get_width(),
        )

    def run(self, events: list[pygame.event.Event]) -> GameState:
        """Run the game."""

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # left click
                if event.button == 1:
                    self.board.reveal_cell(mouse_pos)
                # right click
                elif event.button == 3:
                    self.board.toggle_flag_cell(mouse_pos)

        self.board.draw(self.screen)

        if self.board.game_over:
            return GameState.WIN if self.board.solved else GameState.LOSS

        pygame.display.flip()
        self.clock.tick(60)

        return GameState.RUNNING


class GameFactory(ABC):
    """Factory class to create minesweepers games."""

    def __init__(
        self,
        screen: pygame.display,
        clock: pygame.time.Clock,
    ):
        """Initialise the factory."""
        self._screen = screen
        self._clock = clock

    @abstractmethod
    def create(self) -> Game:
        """Create the minesweeper game."""
        ...


class MinesweeperEasy(GameFactory):
    """Easy version of minesweeper."""

    def create(self) -> Game:
        return Minesweeper(
            num_mines=10,
            num_cells_x=9,
            num_cells_y=9,
            screen=self._screen,
            clock=self._clock,
        )


class MinesweeperMedium(GameFactory):
    """Medium version of minesweeper."""

    def create(self) -> Game:
        return Minesweeper(
            num_mines=40,
            num_cells_x=16,
            num_cells_y=16,
            screen=self._screen,
            clock=self._clock,
        )


class MinesweeperHard(GameFactory):
    """Hard version of minesweeper."""

    def create(self) -> Game:
        return Minesweeper(
            num_mines=99,
            num_cells_x=30,
            num_cells_y=16,
            screen=self._screen,
            clock=self._clock,
        )
