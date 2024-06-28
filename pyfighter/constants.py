"""This file holds all the constant variables used by the program. 
Such as player ship size, asteroid size and contains paths to images."""

# Game settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1084
HUD_HEIGHT = 60
PLAYER_BUFFER = 150
BASE_SPEED = 100  # Used for asteroids and enemies
BASE_LASER_SPEED = 1000
PLAYER_BASE_SPEED = 300
BASE_CANNON_COOLDOWN = 40
BOAT_MISSILE_COOLDOWN = 200
PLAYER_BASE_HULL = 3
BASE_LASER_DMG = 1

# Offset = img width / 2 and img height / 2
# Blue laser y offset is 0 so head of laser collision = hit
IMG_OFFSETS = {
    "player": {"x": 49, "y": 37},
    "meteorB1": {"x": 50, "y": 42},
    "meteorB2": {"x": 60, "y": 49},
    "meteorB3": {"x": 44, "y": 41},
    "meteorB4": {"x": 49, "y": 48},
    "meteorG1": {"x": 50, "y": 42},
    "meteorG2": {"x": 60, "y": 49},
    "meteorG3": {"x": 44, "y": 41},
    "meteorG4": {"x": 49, "y": 48},
    "blueLaser": {"x": 3, "y": 0},
    "blueMissile": {"x": 10, "y": 0},
    "red_missile": {"x": 10, "y": 0},
    "fire_rate": {"x": 17, "y": 16},
    "speed": {"x": 17, "y": 16},
    "missiles": {"x": 17, "y": 16},
    "enemy_fighter": {"x": 46, "y": 42},
    "enemy_boat": {"x": 41, "y": 42},
}

# Note: use convert alpha for images with transparency (not done here)
IMG_PATHS = {
    "player": "./assets/active_sprites/ships/playerShip1_orange.png",
    "background": "./assets/active_sprites/Backgrounds/bg_merged.png",
    "meteorB1": "./assets/active_sprites/Meteors/meteorBrown_big1.png",
    "meteorB2": "./assets/active_sprites/Meteors/meteorBrown_big2.png",
    "meteorB3": "./assets/active_sprites/Meteors/meteorBrown_big3.png",
    "meteorB4": "./assets/active_sprites/Meteors/meteorBrown_big4.png",
    "meteorG1": "./assets/active_sprites/Meteors/meteorGrey_big1.png",
    "meteorG2": "./assets/active_sprites/Meteors/meteorGrey_big2.png",
    "meteorG3": "./assets/active_sprites/Meteors/meteorGrey_big3.png",
    "meteorG4": "./assets/active_sprites/Meteors/meteorGrey_big4.png",
    "blueLaser": "./assets/active_sprites/Lasers/laserBlue07.png",
    "blueMissile": "./assets/active_sprites/Missiles/spaceMissiles_001.png",
    "fire_rate": "./assets/active_sprites/Power-Ups/powerupBlue_star.png",
    "speed": "./assets/active_sprites/Power-Ups/powerupGreen_star.png",
    "missiles": "./assets/active_sprites/Power-Ups/powerupRed_star.png",
    "enemy_fighter": "./assets/active_sprites/Enemies/enemyBlack1.png",
    "enemy_boat": "./assets/active_sprites/Enemies/enemyBlack4.png",
    "red_laser": "./assets/active_sprites/Lasers/laserRed07.png",
    "red_missile": "./assets/active_sprites/Missiles/spaceMissiles_040.png",
    "start_button": "./assets/active_sprites/buttons/start_button.png",
    "exit_button": "./assets/active_sprites/buttons/exit_button.png",
    "continue_button": "./assets/active_sprites/buttons/continue_button.png",
    "restart_button": "./assets/active_sprites/buttons/restart_button.png",
}

SFX_PATHS = {
    "laser": "./assets/zaid_sfx/laser1.wav",
    "explosion": "./assets/zaid_sfx/Explosion_3.wav",
    "laserHit": "./assets/zaid_sfx/Hit_4.wav",
    "music": "./assets/zaid_sfx/music.mp3",
    "powerup_pickup": "./assets/zaid_sfx/powerup.mp3",
    "missile_launch": "./assets/zaid_sfx/missile_launch_sfx.mp3",
}

# Used for random selection
ASTEROID_LIST = [
    "meteorB1",
    "meteorB2",
    "meteorB3",
    "meteorB4",
    "meteorG1",
    "meteorG2",
    "meteorG3",
    "meteorG4",
]

POWERUP_LIST = [
    "fire_rate",
    "speed",
    "missiles",
]

ANI_PATHS = {
    "fighter_death_frames": "./assets/active_sprites/Enemies/enemy_deathani/enemy_death",
    "boat_death_frames": "./assets/active_sprites/Enemies/boat_deathani/boat_death",
    "player_idle_frames": "./assets/active_sprites/ships/player_ani/idle/player_idle-",
    "meteor_explosion_frames": "./assets/active_sprites/Explosions/explosion",
}
