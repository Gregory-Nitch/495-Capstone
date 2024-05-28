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
import random
import pygame
from constants import (
    IMG_OFFSETS,
    IMG_PATHS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    HUD_HEIGHT,
    PLAYER_BUFFER,
    PLAYER_BASE_SPEED,
    PLAYER_BASE_HULL,
    BASE_SPEED,
    ASTEROID_LIST,
)
from models.hud import HUD
from models.player import Player
from models.asteroid import Asteroid

# Pygame globals
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
BG_IMG = pygame.image.load(IMG_PATHS["background"]).convert()
PLYR_IMG = pygame.image.load(IMG_PATHS["player"]).convert_alpha()
ASTEROID_IMG_MAP = {}
for ast in ASTEROID_LIST:
    ASTEROID_IMG_MAP[ast] = pygame.image.load(IMG_PATHS[ast]).convert_alpha()


def main() -> None:
    """Main game loop"""

    # pygame setup
    pygame.init()
    pygame.font.init()
    running = True
    start_time = time.time()
    dt = 0
    hud_font = pygame.font.SysFont("Comic Sans MS", 20)
    control_font = pygame.font.SysFont("Comic Sans MS", 14)

    pos = pygame.Vector2((SCREEN.get_width() / 2), (SCREEN.get_height() / 2))
    player = Player(
        pos, PLAYER_BASE_HULL, PLAYER_BASE_SPEED, PLYR_IMG, IMG_OFFSETS["player"]
    )
    hud = HUD()
    asteroids = pygame.sprite.Group()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw to screen here back to front
        SCREEN.blit(BG_IMG, (0, 60))  # Background should be first

        # Actors drawn here
        player.draw(SCREEN)
        for a in asteroids:
            a.draw(SCREEN)

        # HUD should be last
        pygame.draw.rect(SCREEN, "black", (0, 0, SCREEN.get_width(), HUD_HEIGHT))
        hud.draw(SCREEN, player, hud_font, control_font)

        # Perform state change here
        player.score = math.floor(time.time() - start_time)
        difficulty = player.score * 0.0005
        if random.random() < difficulty:
            a_pos = pygame.Vector2(random.randrange(0, SCREEN_WIDTH), 0)
            a_key = random.choice(ASTEROID_LIST)
            new_asteroid = Asteroid(
                a_pos,
                3,
                BASE_SPEED + player.score,
                ASTEROID_IMG_MAP[a_key],
                IMG_OFFSETS[a_key],
            )
            asteroids.add(new_asteroid)

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

        for a in asteroids:
            if a.pos.y - PLAYER_BUFFER > SCREEN.get_height():
                a.kill()
            a.pos.y += a.speed * dt

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = CLOCK.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
