"""Main module to run the game from."""
import pygame

from cell import Cell

SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH

NUM_OF_CELLS = 3


def main():
    """Main function to run the game from."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Minesweeper')

    clock = pygame.time.Clock()

    cell_size = SCREEN_WIDTH / NUM_OF_CELLS
    cell = Cell(1, 1, cell_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                # ToDo use mouse pos to figure out which cell
                # is pressed
                # mouse_pos = pygame.mouse.get_pos()
                # cell_x = mouse_pos[0] // cell_size
                # cell_y = mouse_pos[1] // cell_size
                cell.uncover()

        screen.fill((200, 200, 200))

        cell.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
