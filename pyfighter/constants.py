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
    "player": "./pyfighter/assets/active_sprites/ships/playerShip1_orange.png",
    "background": "./pyfighter/assets/active_sprites/Backgrounds/bg_merged.png",
    "meteorB1": "./pyfighter/assets/active_sprites/Meteors/meteorBrown_big1.png",
    "meteorB2": "./pyfighter/assets/active_sprites/Meteors/meteorBrown_big2.png",
    "meteorB3": "./pyfighter/assets/active_sprites/Meteors/meteorBrown_big3.png",
    "meteorB4": "./pyfighter/assets/active_sprites/Meteors/meteorBrown_big4.png",
    "meteorG1": "./pyfighter/assets/active_sprites/Meteors/meteorGrey_big1.png",
    "meteorG2": "./pyfighter/assets/active_sprites/Meteors/meteorGrey_big2.png",
    "meteorG3": "./pyfighter/assets/active_sprites/Meteors/meteorGrey_big3.png",
    "meteorG4": "./pyfighter/assets/active_sprites/Meteors/meteorGrey_big4.png",
    "blueLaser": "./pyfighter/assets/active_sprites/Lasers/laserBlue07.png",
    "blueMissile": "./pyfighter/assets/active_sprites/Missiles/spaceMissiles_001.png",
    "fire_rate": "./pyfighter/assets/active_sprites/Power-ups/powerupBlue_star.png",
    "speed": "./pyfighter/assets/active_sprites/Power-ups/powerupGreen_star.png",
    "missiles": "./pyfighter/assets/active_sprites/Power-ups/powerupRed_star.png",
    "enemy_fighter": "./pyfighter/assets/active_sprites/Enemies/enemyBlack1.png",
    "enemy_boat": "./pyfighter/assets/active_sprites/Enemies/enemyBlack4.png",
    "red_laser": "./pyfighter/assets/active_sprites/Lasers/laserRed07.png",
    "red_missile": "./pyfighter/assets/active_sprites/Missiles/spaceMissiles_040.png",
    "start_button": "./pyfighter/assets/active_sprites/buttons/start_button.png",
    "exit_button": "./pyfighter/assets/active_sprites/buttons/exit_button.png",
    "continue_button": "./pyfighter/assets/active_sprites/buttons/continue_button.png",
    "restart_button": "./pyfighter/assets/active_sprites/buttons/restart_button.png",
}

SFX_PATHS = {
    "laser": "./pyfighter/assets/zaid_sfx/laser1.wav",
    "explosion": "./pyfighter/assets/zaid_sfx/Explosion_3.wav",
    "laserHit": "./pyfighter/assets/zaid_sfx/Hit_4.wav",
    "music": "./pyfighter/assets/zaid_sfx/music.mp3",
    "powerup_pickup": "./pyfighter/assets/zaid_sfx/powerup.mp3",
    "missile_launch": "./pyfighter/assets/zaid_sfx/missile_launch_sfx.mp3",
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
    "fighter_death_frames": "./pyfighter/assets/active_sprites/enemies/enemy_deathani/enemy_death",
    "boat_death_frames": "./pyfighter/assets/active_sprites/enemies/boat_deathani/boat_death",
    "player_idle_frames": "./pyfighter/assets/active_sprites/ships/player_ani/idle/player_idle-"


}