"""
PyFighter game in python with pygame! Blast away skip!
Authors:
    - Fandel, Jacob
    - Hart, Hope
    - Lozano, Zaid
    - Nitch, Gregory
    - Wheeler, Jack
"""

import sys
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
    BASE_CANNON_COOLDOWN,
    BASE_SPEED,
    ASTEROID_LIST,
    SFX_PATHS,
    POWERUP_LIST,
    ANI_PATHS,
)
from models.hud import HUD
from models.player import Player
from models.asteroid import Asteroid
from models.actor import Actor
from models.powerup import PowerUp
from models.enemy_fighter import EnemyFighter
from models.enemy_boat import EnemyBoat
from models.button import Button


# Pygame globals, loading of game assets
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
BG_IMG = pygame.transform.scale(
    pygame.image.load(IMG_PATHS["background"]).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
PLYR_IMG = pygame.image.load(IMG_PATHS["player"]).convert_alpha()
PLYR_MASK = pygame.mask.from_surface(PLYR_IMG)
BLUE_LASER = pygame.image.load(IMG_PATHS["blueLaser"]).convert_alpha()
BLUE_LASER_MASK = pygame.mask.from_surface(BLUE_LASER)
BLUE_MISSILE = pygame.image.load(IMG_PATHS["blueMissile"]).convert_alpha()
BLUE_MISSILE_MASK = pygame.mask.from_surface(BLUE_MISSILE)
E_FIGHER_IMG = pygame.image.load(IMG_PATHS["enemy_fighter"]).convert_alpha()
E_FIGHER_MASK = pygame.mask.from_surface(E_FIGHER_IMG)
E_BOAT_IMG = pygame.image.load(IMG_PATHS["enemy_boat"]).convert_alpha()
E_BOAT_MASK = pygame.mask.from_surface(E_BOAT_IMG)
RED_LASER = pygame.image.load(IMG_PATHS["red_laser"])
RED_LASER_MASK = pygame.mask.from_surface(RED_LASER)
RED_MISSILE = pygame.image.load(IMG_PATHS["red_missile"]).convert_alpha()
RED_MISSILE_MASK = pygame.mask.from_surface(RED_MISSILE)
START_IMG = pygame.transform.scale(
    pygame.image.load(IMG_PATHS["start_button"]).convert_alpha(), (384, 128)
)
EXIT_IMG = pygame.transform.scale(
    pygame.image.load(IMG_PATHS["exit_button"]).convert_alpha(), (384, 128)
)
CONTINUE_IMG = pygame.transform.scale(
    pygame.image.load(IMG_PATHS["continue_button"]).convert_alpha(), (384, 128)
)
RESTART_IMG = pygame.transform.scale(
    pygame.image.load(IMG_PATHS["restart_button"]).convert_alpha(), (384, 128)
)

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
START_BUTTON = Button(SCREEN.get_width() / 2 - 175, 350, START_IMG, 1)
EXIT_BUTTON = Button(SCREEN.get_width() / 2 - 175, 600, EXIT_IMG, 1)
CONTINUE_BUTTON = Button(SCREEN.get_width() / 2 - 175, 350, CONTINUE_IMG, 1)
RESTART_BUTTON = Button(SCREEN.get_width() / 2 - 175, 350, RESTART_IMG, 1)
FIGHTER_DEATH_ANIMATION_FRAMES = [
    pygame.image.load(
        f"{ANI_PATHS['fighter_death_frames']}{str(i).zfill(3)}.png"
    ).convert_alpha()
    for i in range(1, 16)
]
BOAT_DEATH_ANIMATION_FRAMES = [
    pygame.image.load(
        f"{ANI_PATHS['boat_death_frames']}{str(i).zfill(3)}.png"
    ).convert_alpha()
    for i in range(1, 13)
]
PLAYER_IDLE_FRAMES = [
    pygame.image.load(f"{ANI_PATHS['player_idle_frames']}{str(i).zfill(3)}.png").convert_alpha()
    for i in range(0, 20)
]

def main_menu() -> None:
    """Prints the start screen before the game begins and waits until the
    player clicks the mouse button."""

    title_font = pygame.font.SysFont("Bauhaus 93", 150)
    not_ready = True
    start_time = time.time()
    while not_ready:
        SCREEN.blit(BG_IMG, (0, 0))

        elapsed_time = time.time() - start_time
        float_offset = math.sin(elapsed_time * 2) * 10

        title_label = title_font.render("PyFighter", 1, (255, 255, 255))
        SCREEN.blit(
            title_label,
            (SCREEN.get_width() / 2 - title_label.get_width() / 2, 100 + float_offset),
        )

        # Draw the start button
        if START_BUTTON.draw(SCREEN):
            return
        # Draw the exit button
        if EXIT_BUTTON.draw(SCREEN):
            pygame.quit()
            sys.exit()
        # Update the display after all elements are drawn
        pygame.display.update()

        # Until quit or player starts the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def pause_menu() -> float:
    """Contains the logic for the pause menu, prints the menu until user
    requests exit or to continue. Returns the total amount of time spent in the
    pause menu to add to start_time (prevents player score problems during a
    paused state)."""

    paused_time = time.time()
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
        SCREEN.blit(
            title_label, (SCREEN.get_width() / 2 - title_label.get_width() / 2, 100)
        )

        pygame.display.update()
        CLOCK.tick(60)

    return time.time() - paused_time


def gameover_screen(lost_font: pygame.font.SysFont, player: Player) -> bool:
    """Displays the game over screen to the player and returns a bool to end
    the main game loop, or restart it. A True return value means that the game
    state needs to be reset."""

    pygame.time.wait(500)  # Wait on loss before moving to game over
    request_reset = False
    SCREEN.blit(BG_IMG, (0, 0))
    lost_label = lost_font.render(
        "Game Over!! Your score was: " + str(player.score), 1, (255, 255, 255)
    )
    SCREEN.blit(lost_label, (SCREEN_WIDTH / 2 - lost_label.get_width() / 2, 250))
    awaiting_reset = True
    while awaiting_reset:
        # Display above font
        pygame.display.update()

        # Until quit or player starts a new game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if RESTART_BUTTON.draw(SCREEN):
            request_reset = True
            awaiting_reset = False

        if EXIT_BUTTON.draw(SCREEN):
            request_reset = False
            awaiting_reset = False

    return request_reset


def reset_game_state(
    player: Player, sprite_groups: list[pygame.sprite.Group], enemies: list[Actor]
) -> float:
    """Reverts the game state back to its initial settings, this includes
    the player state back to default values, and emptying of all sprite
    groups. Returns start time for the new game."""

    # Reset player state
    player.score = 0
    player.hp = PLAYER_BASE_HULL
    player.speed = PLAYER_BASE_SPEED
    player.pos = pygame.Vector2((SCREEN.get_width() / 2), (SCREEN.get_height() / 2))
    player.missile_count = 2
    player.cooldown_counter = 0
    player.cooldown_threshold = BASE_CANNON_COOLDOWN
    player.missile_cooldown_counter = 0
    player.missile_cooldown_threshold = BASE_CANNON_COOLDOWN
    player.lasers_fired.empty()
    player.missiles_fired.empty()
    player.glow_effect_active = False
    player.glow_effect_end_time = 0

    # Empty all sprite groups
    for group in sprite_groups:
        group.empty()

    # Remove enemies
    for enemy in enemies:
        if enemy:  # Protects against None objects
            enemy.hp = 0  # Needed to set hp to 0 for proper killing of object
            # This results in the killing and nulling of the object in main()

    return time.time()  # Return reset time


def proccess_obj_for_powerup(obj: Actor, player: Player) -> PowerUp:
    """Creates PowerUp class instances with passed object references."""

    spawn_loc = obj.pos
    powerup_key = random.choice(POWERUP_LIST)
    powerup_img = POWERUP_IMGS[powerup_key]
    powerup_mask = POWERUP_MASKS[powerup_key]
    new_powerup = PowerUp(
        spawn_loc,
        BASE_SPEED + player.score * 0.25,
        powerup_img,
        powerup_mask,
        IMG_OFFSETS[powerup_key],
        powerup_key,
        pygame.mixer.Sound(SFX_PATHS["powerup_pickup"]),
    )
    return new_powerup


def player_input(
    player: Player,
    keys: pygame.key,
    fighter: EnemyFighter,
    left_enemy_boat: EnemyBoat,
    right_enemy_boat: EnemyBoat,
    delta_time: float,
) -> bool:
    """Captures player input during a frame, used to carry out player
    comands."""

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


def spawn_asteroids(
    asteroids: list[pygame.sprite.Group], difficulty: float, player: Player
) -> bool:
    """Spawns asteroids at a random rate depending on player score and
    difficulty."""

    if random.random() < difficulty:
        a_pos = pygame.Vector2(random.randrange(50, SCREEN_WIDTH), 0)
        a_key = random.choice(ASTEROID_LIST)
        new_asteroid = Asteroid(
            a_pos,
            3,
            BASE_SPEED + player.score * 0.75,
            ASTEROID_IMG_MAP[a_key],
            IMG_OFFSETS[a_key],
        )
        asteroids.add(new_asteroid)


def asteroid_hp(
    asteroids: list[pygame.sprite.Group],
    incoming: object,
    enemy_fire: list[pygame.sprite.Group],
    objs_to_kill: list[object],
    explosion_sfx: pygame.mixer.Sound,
    laser_hit_sfx: pygame.mixer.Sound,
    projectile_type: int,
) -> bool:
    """Resolves asteroid health actions depending on incoming type of
    projectile."""

    for a in asteroids:
        if Actor.resolve_collision(
            a, incoming
        ):  # determine what projectile is coming, reduce health accordingly
            if projectile_type == 1:
                a.hp -= 3
            else:
                a.hp -= 1
                laser_hit_sfx.play()
            if a.hp <= 0:
                asteroids.remove(a)
                objs_to_kill.append(a)
                explosion_sfx.play()
            enemy_fire.remove(incoming)


def process_killed_objects(
    objs_to_kill: list[object], player: Player, powerups: list[pygame.sprite.Group]
) -> bool:
    """Randomly activates a power up processing action for each object that
    needs to be killed."""

    for obj in objs_to_kill:
        if random.random() < 0.3:  # Randomize drop chance
            new_powerup = proccess_obj_for_powerup(obj, player)
            powerups.add(new_powerup)


def handle_projectile(
    delta_time: int,
    powerups: list[pygame.sprite.Group],
    objs_to_kill: list[object],
    enemy_fire: list[pygame.sprite.Group],
    player: Player,
    asteroids: list[pygame.sprite.Group],
    explosion_sfx: pygame.mixer.Sound,
    laser_hit_sfx: pygame.mixer.Sound,
    projectile_type: int,
    lost_font: pygame.font,
) -> tuple[bool, bool]:
    """Reloves hits against the player and asteroids from enemy projectiles
    based on type. Also calls gameover state logic and returns two booleans
    (reset, running)."""

    reset = False
    running = True
    for fire in enemy_fire:
        if fire.pos.y < 0:
            enemy_fire.remove(fire)
        if Actor.resolve_collision(player, fire):
            player.hp -= 1
            if projectile_type == 0:
                laser_hit_sfx.play()
            else:
                explosion_sfx.play()
            if player.hp <= 0:
                explosion_sfx.play()
                reset = gameover_screen(lost_font, player)
                if not reset:
                    running = False
            enemy_fire.remove(fire)
        asteroid_hp(
            asteroids,
            fire,
            enemy_fire,
            objs_to_kill,
            explosion_sfx,
            laser_hit_sfx,
            projectile_type,
        )
        process_killed_objects(objs_to_kill, player, powerups)
        if projectile_type == 1:
            if fire.target:
                fire.seek(delta_time)
            else:
                fire.pos.y -= fire.speed * delta_time
        else:
            fire.pos.y -= fire.speed * delta_time
    return reset, running


def main() -> None:
    """Main game loop. Game will continue until the player looses or closes
    the program."""

    # pygame setup
    pygame.init()
    laser_sfx = pygame.mixer.Sound(SFX_PATHS["laser"])
    explosion_sfx = pygame.mixer.Sound(SFX_PATHS["explosion"])
    laser_hit_sfx = pygame.mixer.Sound(SFX_PATHS["laserHit"])
    missile_sfx = pygame.mixer.Sound(SFX_PATHS["missile_launch"])
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
        missile_sfx,
        PLAYER_IDLE_FRAMES

    )
    hud = HUD()
    asteroids = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    enemy_lasers = pygame.sprite.Group()
    enemy_missiles = pygame.sprite.Group()
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
        player.update_idle_animation()
        player.update()

        # Draw to screen here back to front
        SCREEN.blit(BG_IMG, (0, 60))  # Background first, 60px down for hud

        # group assets
        sprite_groups = [asteroids, enemy_lasers, enemy_missiles]
        enemies = [fighter, left_enemy_boat, right_enemy_boat]
        # Actors drawn here
        for p in powerups:
            p.draw(SCREEN)
        if fighter:
            fighter.draw(SCREEN)
        if left_enemy_boat:
            left_enemy_boat.draw(SCREEN)
        if right_enemy_boat:
            right_enemy_boat.draw(SCREEN)
        for missile in player.missiles_fired:
            missile.draw(SCREEN)
        for laser in player.lasers_fired:
            laser.draw(SCREEN)
        for laser in enemy_lasers:
            laser.draw(SCREEN)
        for missile in enemy_missiles:
            missile.draw(SCREEN)
        player.draw(SCREEN)
        for a in asteroids:
            a.draw(SCREEN)

        # HUD should be last
        pygame.draw.rect(SCREEN, "black", (0, 0, SCREEN.get_width(), HUD_HEIGHT))
        hud.draw(SCREEN, player, hud_font, control_font)

        # Perform state change here
        player.score = math.floor(time.time() - start_time)
        difficulty = player.score * 0.001  # Difficulty goes up as score increases
        difficulty = min(difficulty, 0.02)  # But is capped at 2% chance per frame
        # Use of random produces a percent chance for an asteroid per frame
        spawn_asteroids(asteroids, difficulty, player)

        difficulty = player.score * 0.000008
        if not fighter and random.random() < difficulty:
            fighter = EnemyFighter(
                pygame.Vector2(random.randrange(50, SCREEN_WIDTH), SCREEN_HEIGHT + 100),
                1,
                BASE_SPEED,
                E_FIGHER_IMG,
                E_FIGHER_MASK,
                IMG_OFFSETS["enemy_fighter"],
                RED_LASER,
                RED_LASER_MASK,
                laser_sfx,
                FIGHTER_DEATH_ANIMATION_FRAMES,
            )

        difficulty = player.score * 0.000002
        if not left_enemy_boat and random.random() < difficulty:
            left_enemy_boat = EnemyBoat(
                pygame.Vector2(-100, random.randrange(0, SCREEN_HEIGHT)),
                1,
                BASE_SPEED,
                E_BOAT_IMG,
                E_BOAT_MASK,
                "left_boat",
                IMG_OFFSETS["enemy_boat"],
                RED_MISSILE,
                RED_MISSILE_MASK,
                missile_sfx,
                BOAT_DEATH_ANIMATION_FRAMES,
            )

        if not right_enemy_boat and random.random() < difficulty:
            right_enemy_boat = EnemyBoat(
                pygame.Vector2(SCREEN_WIDTH + 100, random.randrange(0, SCREEN_HEIGHT)),
                1,
                BASE_SPEED,
                E_BOAT_IMG,
                E_BOAT_MASK,
                "right_boat",
                IMG_OFFSETS["enemy_boat"],
                RED_MISSILE,
                RED_MISSILE_MASK,
                missile_sfx,
                BOAT_DEATH_ANIMATION_FRAMES,
            )

        if fighter:
            fighter.cooldown_cannon()
        if left_enemy_boat:
            left_enemy_boat.cooldown_missiles()
        if right_enemy_boat:
            right_enemy_boat.cooldown_missiles()
        player.cooldown_cannon()
        player.cooldown_missiles()

        # Check player inputs here
        keys = pygame.key.get_pressed()
        player_input(
            player, keys, fighter, left_enemy_boat, right_enemy_boat, delta_time
        )
        # ESC key = quit
        if keys[pygame.K_ESCAPE]:
            start_time += pause_menu()

        # Resolve events from state change here, kill = remove object
        for a in asteroids:
            if a.pos.y - PLAYER_BUFFER > SCREEN.get_height():
                asteroids.remove(a)
            elif Actor.resolve_collision(player, a):
                running = gameover_screen(lost_font, player)
                if running:
                    start_time = reset_game_state(
                        player,
                        [asteroids, enemy_lasers, enemy_missiles],
                        [fighter, left_enemy_boat, right_enemy_boat],
                    )
            if fighter and Actor.resolve_collision(fighter, a):
                fighter.pos.y += (a.speed + fighter.speed) * delta_time
            if left_enemy_boat and Actor.resolve_collision(left_enemy_boat, a):
                left_enemy_boat.pos.y += (a.speed + left_enemy_boat.speed) * delta_time
            if right_enemy_boat and Actor.resolve_collision(right_enemy_boat, a):
                right_enemy_boat.pos.y += (
                    a.speed + right_enemy_boat.speed
                ) * delta_time
            a.pos.y += a.speed * delta_time
        if not running:  # Prevents continuation of frame after a gameover state
            continue

        if fighter:
            if fighter.is_dying:
                fighter.update_death_animation()
            else:
                fighter.tracking_module.seek_target(
                    player.pos, delta_time, asteroids, SCREEN
                )
                if fighter.has_target(player, SCREEN):
                    laser = fighter.shoot()
                    if laser:
                        enemy_lasers.add(laser)
            if fighter.hp <= 0 and not fighter.is_dying:
                fighter.start_death_animation()
            if fighter.dead:
                fighter.kill()
                fighter = None

        if left_enemy_boat:
            if left_enemy_boat.is_dying:
                left_enemy_boat.update_death_animation()
            else:
                left_enemy_boat.tracking_module.seek_target(
                    player.pos, delta_time, asteroids, SCREEN
                )
                if left_enemy_boat.is_on_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    missile = left_enemy_boat.launch_missile(player)
                    if missile:
                        enemy_missiles.add(missile)
            if (
                left_enemy_boat
                and left_enemy_boat.hp <= 0
                and not left_enemy_boat.is_dying
            ):
                left_enemy_boat.start_death_animation()
            if left_enemy_boat.dead:
                left_enemy_boat.kill()
                left_enemy_boat = None

        if right_enemy_boat:
            if right_enemy_boat.is_dying:
                right_enemy_boat.update_death_animation()
            else:
                right_enemy_boat.tracking_module.seek_target(
                    player.pos, delta_time, asteroids, SCREEN
                )
                if right_enemy_boat.is_on_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    missile = right_enemy_boat.launch_missile(player)
                    if missile:
                        enemy_missiles.add(missile)
            if (
                right_enemy_boat
                and right_enemy_boat.hp <= 0
                and not right_enemy_boat.is_dying
            ):
                right_enemy_boat.start_death_animation()
            if right_enemy_boat.dead:
                right_enemy_boat.kill()
                right_enemy_boat = None

        for powerup in powerups:
            if powerup.pos.y - PLAYER_BUFFER > SCREEN.get_height():
                powerups.remove(powerup)
            elif Actor.resolve_collision(player, powerup):
                powerup.pickup(player)
                powerups.remove(powerup)
            powerup.pos.y += powerup.speed * delta_time

        objs_to_kill = []

        # handle lasers
        reset, running = handle_projectile(
            delta_time,
            powerups,
            objs_to_kill,
            enemy_lasers,
            player,
            asteroids,
            explosion_sfx,
            laser_hit_sfx,
            0,
            lost_font,
        )
        if not running:  # Prevents continuation of frame after a gameover state
            continue

        # check for restart
        if reset:
            start_time = reset_game_state(player, sprite_groups, enemies)
        # Need to empty objs to kill for next iteration
        objs_to_kill.clear()

        # handle missiles
        reset, running = handle_projectile(
            delta_time,
            powerups,
            objs_to_kill,
            enemy_missiles,
            player,
            asteroids,
            explosion_sfx,
            laser_hit_sfx,
            1,
            lost_font,
        )
        if not running:  # Prevents continuation of frame after a gameover state
            continue

        # check for restart
        if reset:
            start_time = reset_game_state(player, sprite_groups, enemies)
        # Need to empty objs to kill for next iteration
        objs_to_kill.clear()

        for laser in player.lasers_fired:
            if laser.pos.y < 0:
                player.lasers_fired.remove(laser)
            objs_to_kill = player.resolve_hits(laser, asteroids)
            objs_to_kill += player.resolve_hits(laser, enemy_missiles)
            objs_to_kill += player.resolve_hits(
                laser, [fighter, left_enemy_boat, right_enemy_boat]
            )
            process_killed_objects(objs_to_kill, player, powerups)
            laser.pos.y -= laser.speed * delta_time

        # Need to empty objs to kill for next iteration
        objs_to_kill.clear()

        for missile in player.missiles_fired:
            if missile.is_off_screen(SCREEN):
                player.missiles_fired.remove(missile)
            objs_to_kill = player.resolve_missiles(missile, asteroids)
            objs_to_kill += player.resolve_missiles(
                missile, [fighter, left_enemy_boat, right_enemy_boat]
            )
            process_killed_objects(objs_to_kill, player, powerups)
            if missile.target:
                missile.seek(delta_time)
            else:
                missile.pos.y -= missile.speed * delta_time

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
