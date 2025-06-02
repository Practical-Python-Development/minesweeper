"""Main module to run the game from."""
import pygame
from pygame.font import get_default_font

from board import Board

SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH

NUM_OF_CELLS = 8
NUM_MINES = 10


def main():
    """Main function to run the game from."""
    while True:  # to start again after win or game-over
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
        repeat = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if board.game_over:  # click to play again
                        repeat = True
                        running = False
                        continue
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
                font_msg = pygame.font.Font(pygame.font.get_default_font(), 48)
                msg_surf = font_msg.render(msg, True, (255, 255, 255))
                msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(msg_surf, msg_rect)

                prompt = "Click to play again."
                font_prompt = pygame.font.Font(pygame.font.get_default_font(), 20)
                prompt_surf = font_prompt.render(prompt, True, (255, 255, 255))
                prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 42))
                screen.blit(prompt_surf, prompt_rect)

            pygame.display.flip()
            clock.tick(60)
        if not repeat:
            break
    pygame.quit()


if __name__ == '__main__':
    main()
