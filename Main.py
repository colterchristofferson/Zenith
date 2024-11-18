import pygame
from game_logic import ZenithGame
from constants import *

pygame.init()

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zenith")
clock = pygame.time.Clock()

# Load assets
background = pygame.image.load("assets/background.jpg")

# Game instance
game = ZenithGame()

# Main loop
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background and game state
        screen.blit(background, (0, 0))
        game.draw_status(screen)  # Assuming you move your draw logic here

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
