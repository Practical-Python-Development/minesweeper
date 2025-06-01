"""Main module to run the game from."""
import pygame

from cell import Cell

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def main():
    """Main function to run the game from."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Minesweeper')

    clock = pygame.time.Clock()

    cell = Cell(5, 5)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((200, 200, 200))

        cell.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
