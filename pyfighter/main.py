"""
PyFighter game in python with pygame! Blast away skip!
Authors:
    - Fandel, Jacob
    - Hart, Hope
    - Lozano, Zaid
    - Nitch, Gregory
    - Wheeler, Jack
"""

# Example file showing a basic pygame "game loop"
import pygame
from models.player import Player
from constants import IMG_PATHS, IMG_OFFSETS

# Globals
SCREEN = pygame.display.set_mode((1280, 828))
CLOCK = pygame.time.Clock()
BG_IMG = pygame.image.load(IMG_PATHS["background"]).convert()


def draw_background():
    """Draws the background of the game and the HUD base."""
    pygame.draw.rect(SCREEN, "black", (0, 0, SCREEN.get_width(), 60))
    SCREEN.blit(BG_IMG, (0, 60))


def main():
    """Main game loop"""

    # pygame setup
    pygame.init()
    running = True
    dt = 0

    pos = pygame.Vector2((SCREEN.get_width() / 2), (SCREEN.get_height() / 2))
    player = Player(pos, 3, 300, IMG_PATHS["player"], IMG_OFFSETS["player"])

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with background to wipe away anything from last frame
        draw_background()
        player.draw(SCREEN)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.pos.y -= player.speed * dt
        if keys[pygame.K_DOWN]:
            player.pos.y += player.speed * dt
        if keys[pygame.K_LEFT]:
            player.pos.x -= player.speed * dt
        if keys[pygame.K_RIGHT]:
            player.pos.x += player.speed * dt

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = CLOCK.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
