"""Main module to run the game from."""
import pygame

from cell import Cell
from board import Board

SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH

NUM_OF_CELLS = 3
NUM_MINES = 3


def main():
    """Main function to run the game from."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Minesweeper')

    clock = pygame.time.Clock()

    board = Board(
        NUM_OF_CELLS,
        NUM_OF_CELLS,
        NUM_MINES,
        SCREEN_HEIGHT,
        SCREEN_WIDTH,
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                board.uncover(mouse_pos)

        screen.fill((200, 200, 200))

        board.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
