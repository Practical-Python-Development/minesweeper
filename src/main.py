"""Main module to run the game from."""
import pygame

from board import Board

SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH

NUM_OF_CELLS = 7
NUM_MINES = 3


def main():
    """Main function to run the game from."""
    pygame.init()
    pygame.font.init()

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
                # left click
                if event.button == 1:
                    board.reveal_cell(mouse_pos)
                # right click
                elif event.button == 3:
                    board.toggle_flag_cell(mouse_pos)

        board.draw(screen)

        if board.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            msg = "You Win!" if board.solved else "Game Over!"
            font = pygame.font.Font(pygame.font.get_default_font(), 48)
            text_surf = font.render(msg, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
