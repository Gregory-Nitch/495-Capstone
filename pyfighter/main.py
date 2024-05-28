"""
PyFighter game in python with pygame! Blast away skip!
Authors:
    - Fandel, Jacob
    - Hart, Hope
    - Lozano, Zaid
    - Nitch, Gregory
    - Wheeler, Jack
"""

import math
import time
import pygame
from constants import IMG_OFFSETS, IMG_PATHS
from models.hud import HUD
from models.player import Player

# Globals
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 828
PLAYER_BUFFER = 150
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
BG_IMG = pygame.image.load(IMG_PATHS["background"]).convert()
PLYR_IMG = pygame.image.load(IMG_PATHS["player"]).convert_alpha()
HUD_HEIGHT = 60


def draw_background():
    """Draws the background of the game and the HUD base."""
    pygame.draw.rect(SCREEN, "black", (0, 0, SCREEN.get_width(), HUD_HEIGHT))
    SCREEN.blit(BG_IMG, (0, 60))


def main() -> None:
    """Main game loop"""

    # pygame setup
    pygame.init()
    pygame.font.init()
    running = True
    start_time = time.time()
    dt = 0
    hud_font = pygame.font.SysFont("Comic Sans MS", 30)

    pos = pygame.Vector2((SCREEN.get_width() / 2), (SCREEN.get_height() / 2))
    player = Player(pos, 3, 300, PLYR_IMG, IMG_OFFSETS["player"])
    hud = HUD()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw to screen here back to front
        draw_background()
        player.draw(SCREEN)
        hud.draw(SCREEN, player, hud_font)

        # Perform state change here
        player.score = math.floor(time.time() - start_time)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.pos.y > HUD_HEIGHT + player.offset["y"]:
            player.pos.y -= player.speed * dt
        if (
            keys[pygame.K_DOWN]
            and player.pos.y + player.offset["y"] < SCREEN_HEIGHT - PLAYER_BUFFER
        ):
            player.pos.y += player.speed * dt
        if keys[pygame.K_LEFT] and player.pos.x > 0 + player.offset["x"]:
            player.pos.x -= player.speed * dt
        if keys[pygame.K_RIGHT] and player.pos.x < SCREEN_WIDTH - player.offset["x"]:
            player.pos.x += player.speed * dt

        if keys[pygame.K_ESCAPE]:
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = CLOCK.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
