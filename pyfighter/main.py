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
    SFX_PATHS,
)
from models.hud import HUD
from models.player import Player
from models.asteroid import Asteroid
from models.actor import Actor

# Pygame globals, loading of game assets
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
BG_IMG = pygame.image.load(IMG_PATHS["background"]).convert()
PLYR_IMG = pygame.image.load(IMG_PATHS["player"]).convert_alpha()
PLYR_MASK = pygame.mask.from_surface(PLYR_IMG)
BLUE_LASER = pygame.image.load(IMG_PATHS["blueLaser"]).convert_alpha()
BLUE_LASER_MASK = pygame.mask.from_surface(BLUE_LASER)
ASTEROID_IMG_MAP = {}
for ast in ASTEROID_LIST:
    ASTEROID_IMG_MAP[ast] = pygame.image.load(IMG_PATHS[ast]).convert_alpha()


def main_menu():
    """Prints the start screen before the game begins and waits until the
    player clicks the mouse button."""

    title_font = pygame.font.SysFont("comicsans", 50)
    not_ready = True
    while not_ready:
        SCREEN.blit(BG_IMG, (0, 0))
        title_label = title_font.render(
            "Press the mouse button to begin...", 1, (255, 255, 255)
        )
        SCREEN.blit(
            title_label, (SCREEN.get_width() / 2 - title_label.get_width() / 2, 350)
        )

        # Display above font
        pygame.display.update()

        # Until quit or player starts the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_ready = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                return


def main() -> None:
    """Main game loop. Game will continue until the player looses or closes
    the program."""

    # pygame setup
    pygame.init()
    laser_sfx = pygame.mixer.Sound(SFX_PATHS["laser"])
    explosion_sfx = pygame.mixer.Sound(SFX_PATHS["explosion"])
    laser_hit_sfx = pygame.mixer.Sound(SFX_PATHS["laserHit"])
    pygame.mixer.music.load(SFX_PATHS["music"])
    pygame.font.init()
    pygame.mixer.music.play(-1)  # -1 will ensure the song keeps looping

    main_menu()

    running = True
    start_time = time.time()  # Used for score
    delta_time = 0  # Seconds since last frame, used for framerate physics
    hud_font = pygame.font.SysFont("Comic Sans MS", 20)
    control_font = pygame.font.SysFont("Comic Sans MS", 14)

    # Setup player and other Actor containers/HUD
    pos = pygame.Vector2((SCREEN.get_width() / 2), (SCREEN.get_height() / 2))
    player = Player(
        pos,
        PLAYER_BASE_HULL,
        PLAYER_BASE_SPEED,
        PLYR_IMG,
        PLYR_MASK,
        IMG_OFFSETS["player"],
        BLUE_LASER,
        BLUE_LASER_MASK,
        laser_sfx,
        laser_hit_sfx,
        explosion_sfx,
    )
    hud = HUD()
    asteroids = pygame.sprite.Group()

    # Each iteration = 1 frame, game set to 60FPS
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw to screen here back to front
        SCREEN.blit(BG_IMG, (0, 60))  # Background first, 60px down for hud

        # Actors drawn here
        for laser in player.lasers_fired:
            laser.draw(SCREEN)
        player.draw(SCREEN)
        for a in asteroids:
            a.draw(SCREEN)

        # HUD should be last
        pygame.draw.rect(SCREEN, "black", (0, 0, SCREEN.get_width(), HUD_HEIGHT))
        hud.draw(SCREEN, player, hud_font, control_font)

        # Perform state change here
        player.score = math.floor(time.time() - start_time)
        difficulty = player.score * 0.0005  # Difficulty goes up as score increases
        # Use of random produces a percent chance for an asteroid per frame
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

        player.cooldown_cannon()

        # Check player inputs here
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.pos.y > HUD_HEIGHT + player.offset["y"]:
            player.pos.y -= player.speed * delta_time
        if (
            keys[pygame.K_DOWN]
            and player.pos.y + player.offset["y"] < SCREEN_HEIGHT - PLAYER_BUFFER
        ):
            player.pos.y += player.speed * delta_time
        if keys[pygame.K_LEFT] and player.pos.x > 0 + player.offset["x"]:
            player.pos.x -= player.speed * delta_time
        if keys[pygame.K_RIGHT] and player.pos.x < SCREEN_WIDTH - player.offset["x"]:
            player.pos.x += player.speed * delta_time
        if keys[pygame.K_SPACE]:
            player.shoot()
        # ESC key = quit
        if keys[pygame.K_ESCAPE]:
            running = False

        # Resolve events from state change here, kill = remove object
        for a in asteroids:
            if a.pos.y - PLAYER_BUFFER > SCREEN.get_height():
                a.kill()
            elif Actor.resolve_collision(player, a):
                running = False  # TODO show game over
            a.pos.y += a.speed * delta_time

        for laser in player.lasers_fired:
            if laser.pos.y < 0:
                laser.kill()
            player.resolve_hits(laser, asteroids)
            # TODO add enemy ships to list of objs above (asteroids + enemies)
            laser.pos.y -= laser.speed * delta_time

        # Puts work on screen
        pygame.display.flip()

        # limits FPS to 60
        # delta time in seconds since last frame, used for framerate-
        # independent physics.
        delta_time = CLOCK.tick(60) / 1000

    pygame.quit()  # Exited while loop, leaving game


# Only start the main loop if this file was passed to interpreter
if __name__ == "__main__":
    main()
