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
import button
import sys
import math
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
    POWERUP_LIST,
)
from models.hud import HUD
from models.player import Player
from models.asteroid import Asteroid
from models.actor import Actor
from models.powerup import PowerUp
from models.enemy_fighter import EnemyFighter


# Pygame globals, loading of game assets
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
BG_IMG = pygame.transform.scale(pygame.image.load(IMG_PATHS["background"]).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
PLYR_IMG = pygame.image.load(IMG_PATHS["player"]).convert_alpha()
PLYR_MASK = pygame.mask.from_surface(PLYR_IMG)
BLUE_LASER = pygame.image.load(IMG_PATHS["blueLaser"]).convert_alpha()
BLUE_LASER_MASK = pygame.mask.from_surface(BLUE_LASER)
BLUE_MISSILE = pygame.image.load(IMG_PATHS["blueMissile"]).convert_alpha()
BLUE_MISSILE_MASK = pygame.mask.from_surface(BLUE_MISSILE)
E_FIGHER_IMG = pygame.image.load(IMG_PATHS["enemy_fighter"]).convert_alpha()
E_FIGHER_MASK = pygame.mask.from_surface(E_FIGHER_IMG)
RED_LASER = pygame.image.load(IMG_PATHS["red_laser"])
RED_LASER_MASK = pygame.mask.from_surface(RED_LASER)
START_IMG = pygame.transform.scale(pygame.image.load(IMG_PATHS["start_button"]).convert_alpha(), (384, 128))
EXIT_IMG = pygame.transform.scale(pygame.image.load(IMG_PATHS["exit_button"]).convert_alpha(), (384, 128))
CONTINUE_IMG = pygame.transform.scale(pygame.image.load(IMG_PATHS["continue_button"]).convert_alpha(), (384, 128))

ASTEROID_IMG_MAP = {}
for ast in ASTEROID_LIST:
    ASTEROID_IMG_MAP[ast] = pygame.image.load(IMG_PATHS[ast]).convert_alpha()
POWERUP_IMGS = {
    "fire_rate": pygame.image.load(IMG_PATHS["fire_rate"]).convert_alpha(),
    "speed": pygame.image.load(IMG_PATHS["speed"]).convert_alpha(),
    "missiles": pygame.image.load(IMG_PATHS["missiles"]).convert_alpha(),
}
POWERUP_MASKS = {
    "fire_rate": pygame.mask.from_surface(POWERUP_IMGS["fire_rate"]),
    "speed": pygame.mask.from_surface(POWERUP_IMGS["speed"]),
    "missiles": pygame.mask.from_surface(POWERUP_IMGS["missiles"]),
}
START_BUTTON = button.Button(SCREEN.get_width() / 2 - 175, 350, START_IMG, 1)
EXIT_BUTTON = button.Button(SCREEN.get_width() / 2 - 175, 600, EXIT_IMG, 1)
CONTINUE_BUTTON = button.Button(SCREEN.get_width() / 2 - 175, 350, CONTINUE_IMG, 1)


def main_menu() -> None:
    """Prints the start screen before the game begins and waits until the
    player clicks the mouse button."""

    title_font = pygame.font.SysFont("Bauhaus 93", 150)
    not_ready = True
    menu_state = "menu"
    start_time = time.time()
    while not_ready:
        SCREEN.blit(BG_IMG, (0, 0))
        
        elapsed_time = time.time() - start_time
        float_offset = math.sin(elapsed_time * 2) * 10
        
        title_label = title_font.render("PyFighter", 1, (255, 255, 255))
        SCREEN.blit(
            title_label, (SCREEN.get_width() / 2 - title_label.get_width() / 2, 100+ float_offset)
        )

        # Draw the start button
        if START_BUTTON.draw(SCREEN):
            return
        # Draw the exit button
        if EXIT_BUTTON.draw(SCREEN):
            pygame.quit
            sys.exit()
        # Update the display after all elements are drawn
        pygame.display.update()

        # Until quit or player starts the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()

def pause_menu():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
        
        SCREEN.blit(BG_IMG, (0, 0))
        
        # Draw the continue button
        if CONTINUE_BUTTON.draw(SCREEN):
            paused = False
        
        # Draw the exit button
        if EXIT_BUTTON.draw(SCREEN):
            pygame.quit()
            sys.exit()
        
        # Display the pause menu
        title_font = pygame.font.SysFont("Bauhaus 93", 150)
        title_label = title_font.render("Paused", 1, (255, 255, 255))
        SCREEN.blit(title_label, (SCREEN.get_width() / 2 - title_label.get_width() / 2, 100))
        
        pygame.display.update()
        CLOCK.tick(60)
    
    
    
def gameover_screen(lost_font: pygame.font.SysFont, player: Player) -> bool:
    """Displays the game over screen to the player and returns a bool to end
    the main game loop."""

    pygame.time.wait(500)  # wait on loss before moving to game over
    running = False
    SCREEN.blit(BG_IMG, (0, 0))
    lost_label = lost_font.render(
        "Game Over!! Your score was: " + str(player.score), 1, (255, 255, 255)
    )
    SCREEN.blit(lost_label, (SCREEN_WIDTH / 2 - lost_label.get_width() / 2, 350))
    not_ready = True
    while not_ready:
        # Display above font
        pygame.display.update()
        # Until quit or player starts the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                not_ready = False

    return running


def proccess_obj_for_powerup(obj: Actor, player: Player) -> PowerUp:
    """Creates PowerUp class instances with passed object references."""

    spawn_loc = obj.pos
    spawn_loc.x -= obj.offset["x"] / 2
    spawn_loc.y -= obj.offset["y"] / 2
    powerup_key = random.choice(POWERUP_LIST)
    powerup_img = POWERUP_IMGS[powerup_key]
    powerup_mask = POWERUP_MASKS[powerup_key]
    new_powerup = PowerUp(
        spawn_loc,
        BASE_SPEED + player.score,
        powerup_img,
        powerup_mask,
        IMG_OFFSETS[powerup_key],
        powerup_key,
        pygame.mixer.Sound(SFX_PATHS["powerup_pickup"]),
    )
    return new_powerup


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
    lost_font = pygame.font.SysFont("comicsans", 50)

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
        BLUE_MISSILE,
        BLUE_LASER_MASK,
        laser_hit_sfx,
        explosion_sfx,
    )
    hud = HUD()
    asteroids = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    enemy_lasers = pygame.sprite.Group()
    fighter = None
    left_enemy_boat = None
    right_enemy_boat = None

    # Each iteration = 1 frame, game set to 60FPS
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player
        player.update()

        # Draw to screen here back to front
        SCREEN.blit(BG_IMG, (0, 60))  # Background first, 60px down for hud

        # Actors drawn here
        for p in powerups:
            p.draw(SCREEN)
        if fighter:
            fighter.draw(SCREEN)
        for missile in player.missiles_fired:
            missile.draw(SCREEN)
        for laser in player.lasers_fired:
            laser.draw(SCREEN)
        for laser in enemy_lasers:
            laser.draw(SCREEN)
        player.draw(SCREEN)
        for a in asteroids:
            a.draw(SCREEN)

        # HUD should be last
        pygame.draw.rect(SCREEN, "black", (0, 0, SCREEN.get_width(), HUD_HEIGHT))
        hud.draw(SCREEN, player, hud_font, control_font)

        # Perform state change here
        player.score = math.floor(time.time() - start_time)
        difficulty = player.score * 0.0004  # Difficulty goes up as score increases
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

        difficulty = player.score * 0.00002
        if not fighter and random.random() < difficulty:
            fighter = EnemyFighter(
                pygame.Vector2(random.randrange(0, SCREEN_WIDTH), SCREEN_HEIGHT + 100),
                1,
                BASE_SPEED,
                E_FIGHER_IMG,
                E_FIGHER_MASK,
                IMG_OFFSETS["enemy_fighter"],
                RED_LASER,
                RED_LASER_MASK,
                laser_sfx,
            )

        if fighter:
            fighter.cooldown_cannon()
        player.cooldown_cannon()
        player.cooldown_missiles()

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
        if keys[pygame.K_LALT]:
            player.fire_missle([fighter, left_enemy_boat, right_enemy_boat])
        # ESC key = quit
        if keys[pygame.K_ESCAPE]:
            pause_menu()

        # Resolve events from state change here, kill = remove object
        for a in asteroids:
            if a.pos.y - PLAYER_BUFFER > SCREEN.get_height():
                asteroids.remove(a)
            elif Actor.resolve_collision(player, a):
                running = gameover_screen(lost_font, player)
            a.pos.y += a.speed * delta_time

        if fighter:
            fighter.tracking_module.seek_target(player, delta_time)
            if fighter.has_target(player):
                laser = fighter.shoot()
                if laser:
                    enemy_lasers.add(laser)

        for powerup in powerups:
            if powerup.pos.y - PLAYER_BUFFER > SCREEN.get_height():
                powerups.remove(powerup)
            elif Actor.resolve_collision(player, powerup):
                powerup.pickup(player)
                powerups.remove(powerup)
            powerup.pos.y += powerup.speed * delta_time

        objs_to_kill = []

        for laser in enemy_lasers:
            if laser.pos.y < 0:
                enemy_lasers.remove(laser)
            if Actor.resolve_collision(player, laser):
                player.hp -= 1
                laser_hit_sfx.play()
                if player.hp <= 0:
                    explosion_sfx.play()
                    running = gameover_screen(lost_font, player)
                enemy_lasers.remove(laser)
            for a in asteroids:
                if Actor.resolve_collision(a, laser):
                    a.hp -= 1
                    laser_hit_sfx.play()
                    if a.hp <= 0:
                        asteroids.remove(a)
                        objs_to_kill.append(a)
                        explosion_sfx.play()
                    enemy_lasers.remove(laser)
            # TODO move this for (and others, see below) to a method
            for obj in objs_to_kill:
                if player.score % 3 == 1:  # Randomize drop chance from player score
                    new_powerup = proccess_obj_for_powerup(obj, player)
                    powerups.add(new_powerup)
            laser.pos.y -= laser.speed * delta_time

        # Need to empty objs to kill for next iteration
        objs_to_kill.clear()

        for laser in player.lasers_fired:
            if laser.pos.y < 0:
                player.lasers_fired.remove(laser)
            objs_to_kill = player.resolve_hits(laser, asteroids)
            if fighter:
                objs_to_kill += player.resolve_hits(laser, [fighter])
            for obj in objs_to_kill:
                if player.score % 3 == 1:  # Randomize drop chance from player score
                    new_powerup = proccess_obj_for_powerup(obj, player)
                    powerups.add(new_powerup)
            laser.pos.y -= laser.speed * delta_time

        # Need to empty objs to kill for next iteration
        objs_to_kill.clear()

        for missile in player.missiles_fired:
            if (
                missile.pos.y < 0
                or missile.pos.y > SCREEN.get_height()
                or missile.pos.x < 0
                or missile.pos.x > SCREEN.get_width()
            ):
                player.missiles_fired.remove(missile)
            objs_to_kill = player.resolve_missiles(missile, asteroids)
            if fighter:
                objs_to_kill += player.resolve_missiles(missile, [fighter])
            for obj in objs_to_kill:
                if player.score % 3 == 1:  # Randomize drop chance from player score
                    new_powerup = proccess_obj_for_powerup(obj, player)
                    powerups.add(new_powerup)
            if missile.target:
                missile.seek(delta_time)
            else:
                missile.pos.y -= missile.speed * delta_time

        if fighter and fighter.hp <= 0:
            fighter.kill()
            fighter = None

        # Need to empty objs kill list for next frame
        objs_to_kill.clear()

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
