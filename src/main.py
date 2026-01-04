"""Main module to run the game from."""

import pygame

from minesweeper import (
    MinesweeperEasy,
    MinesweeperMedium,
    MinesweeperHard,
    GameFactory,
)
from utils import draw_button, GameState

SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH


class GameHandler:
    def __init__(self, game_selection: list[type[GameFactory]]):
        """Initialize the game handler."""
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.constants.RESIZABLE,
        )
        pygame.display.set_caption("Minesweeper")

        self.clock = pygame.time.Clock()
        self.running = True

        self.game_selection = game_selection
        self._selected_game_factory: GameFactory | None = None

    def run(self):
        """Run the main loop of the game handler."""
        current_game = None
        game_state = GameState.SELECTING
        while self.running:
            events = pygame.event.get()
            if any(event.type == pygame.QUIT for event in events):
                self.running = False
                continue

            if game_state is GameState.SELECTING:
                self._selected_game_factory = self.select_game(events)
                if self._selected_game_factory is not None:
                    game_state = GameState.NEW

            elif game_state is GameState.NEW:
                current_game = self._selected_game_factory.create()
                game_state = GameState.RUNNING

            elif game_state is GameState.RUNNING:
                game_state = current_game.run(events)

            elif game_state in (GameState.WIN, GameState.LOSS):
                game_state = self.game_over_screen(game_state, events)

        pygame.quit()

    def game_over_screen(
        self,
        game_state: GameState,
        events: list[pygame.event.Event],
    ) -> GameState:
        """
        Render the game over screen.

        Additionally, display buttons to either rerun the current Game or go back to the
        main menu.
        :param game_state: The game state to render a corresponding Message.
        :param events: A list of pygame events to react on a button press.
        :return: The Game State. This will either be the current Win/Loss State,
            trigger a new game or go back to the selection menu.
        """
        width, height = self.screen.get_width(), self.screen.get_height()
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # TODO: Make the Text come from the game and not the game_state
        #  it should only represent the game state in the game handler
        msg = "You Win!" if game_state is GameState.WIN else "Game Over!"
        big_font = pygame.font.Font(pygame.font.get_default_font(), 48)
        text_surf = big_font.render(msg, True, (255, 255, 255))
        text_rect = text_surf.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 4)
        )
        self.screen.blit(text_surf, text_rect)

        button_width = int(width * 0.35)
        button_height = int(height * 0.08)

        center_x = width // 2

        replay_button = pygame.Rect(
            center_x - button_width // 2,
            int(height * 0.55),
            button_width,
            button_height,
        )

        menu_button = pygame.Rect(
            center_x - button_width // 2,
            int(height * 0.68),
            button_width,
            button_height,
        )

        mouse_pos = pygame.mouse.get_pos()
        small_font = pygame.font.Font(pygame.font.get_default_font(), 30)
        draw_button(
            self.screen,
            "Replay",
            replay_button,
            small_font,
            (255, 255, 255),
            (70, 130, 180),
            (100, 160, 210),
            mouse_pos,
        )

        draw_button(
            self.screen,
            "Main Menu",
            menu_button,
            small_font,
            (255, 255, 255),
            (180, 70, 70),
            (210, 100, 100),
            mouse_pos,
        )

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    return GameState.NEW

                if menu_button.collidepoint(event.pos):
                    return GameState.SELECTING

        pygame.display.flip()
        self.clock.tick(60)

        return game_state

    def select_game(self, events: list[pygame.event.Event]) -> GameFactory:
        """
        Select the game factory to create the game.

        This function creates a main menu in which a list of given factories is
        displayed and one can choose from with a click of a bottom.
        :param events: pygame event to trigger the press of a bottom.
        :return: the selected game factory.
        """
        title_font = pygame.font.SysFont(None, int(self.height * 0.12))
        button_font = pygame.font.SysFont(None, int(self.height * 0.05))

        button_width = int(self.width * 0.4)
        button_height = int(self.height * 0.08)
        spacing = int(self.height * 0.11)

        center_x = self.width // 2
        start_y = int(self.height * 0.45)

        buttons = []
        for i in range(len(self.game_selection)):
            rect = pygame.Rect(
                center_x - button_width // 2,
                start_y + i * spacing,
                button_width,
                button_height,
            )
            buttons.append(rect)

        mouse_pos = pygame.mouse.get_pos()
        self.screen.fill((25, 25, 25))

        title = title_font.render("Select your Game", True, (240, 240, 240))
        self.screen.blit(
            title, title.get_rect(center=(center_x, int(self.height * 0.25)))
        )

        for i, rect in enumerate(buttons):
            draw_button(
                self.screen,
                self.game_selection[i].__name__,
                rect,
                button_font,
                (255, 255, 255),
                (70, 130, 180),
                (100, 160, 210),
                mouse_pos,
            )

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        return self.game_selection[i](self.screen, self.clock)

        pygame.display.flip()
        self.clock.tick(60)

    @property
    def height(self):
        """The current height of the screen."""
        return self.screen.get_height()

    @property
    def width(self):
        """The current width of the screen."""
        return self.screen.get_width()


def main():
    game_handler = GameHandler([MinesweeperEasy, MinesweeperMedium, MinesweeperHard])
    game_handler.run()


if __name__ == "__main__":
    main()
