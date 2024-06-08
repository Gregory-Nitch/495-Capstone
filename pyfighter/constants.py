"""This file holds all the constant variables used by the program. 
Such as player ship size, asteroid size and contains paths to images."""

# Game settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1084
HUD_HEIGHT = 60
PLAYER_BUFFER = 150
BASE_SPEED = 150  # used for asteroids and enemies
BASE_LASER_SPEED = 1000
PLAYER_BASE_SPEED = 300
BASE_CANNON_COOLDOWN = 40
PLAYER_BASE_HULL = 3
BASE_LASER_DMG = 1

# Offset = img width / 2 and img height / 2
# Blue laser y offset is 0 so head of laser collision = hit
IMG_OFFSETS = {  # TODO revisit asteroids (no longer rotating imgs)
    "player": {"x": 49, "y": 37},
    "meteorB1": {"x": 91, "y": 91},
    "meteorB2": {"x": 109, "y": 109},
    "meteorB3": {"x": 85, "y": 85},
    "meteorB4": {"x": 97, "y": 97},
    "meteorG1": {"x": 91, "y": 91},
    "meteorG2": {"x": 109, "y": 109},
    "meteorG3": {"x": 85, "y": 85},
    "meteorG4": {"x": 97, "y": 97},
    "blueLaser": {"x": 3, "y": 0},
    "blueMissile": {"x": 10, "y": 0},
    "fire_rate": {"x": 17, "y": 16},
    "speed": {"x": 17, "y": 16},
    "missiles": {"x": 17, "y": 16},
}

# Note: use convert alpha for images with transparency (not done here)
IMG_PATHS = {
    "player": "./pyfighter/assets/kenney_space-shooter-redux/PNG/playerShip1_orange.png",
    "background": "./pyfighter/assets/kenney_space-shooter-redux/Backgrounds/bg_merged.png",
    "meteorB1": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Meteors/meteorBrown_big1.png",
    "meteorB2": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Meteors/meteorBrown_big2.png",
    "meteorB3": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Meteors/meteorBrown_big3.png",
    "meteorB4": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Meteors/meteorBrown_big4.png",
    "meteorG1": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Meteors/meteorGrey_big1.png",
    "meteorG2": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Meteors/meteorGrey_big2.png",
    "meteorG3": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Meteors/meteorGrey_big3.png",
    "meteorG4": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Meteors/meteorGrey_big4.png",
    "blueLaser": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Lasers/laserBlue07.png",
    "blueMissile": "./pyfighter/assets/kenney_space-shooter-extension/PNG/Sprites/Missiles/spaceMissiles_001.png",
    "fire_rate": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Power-ups/powerupBlue_star.png",
    "speed": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Power-ups/powerupGreen_star.png",
    "missiles": "./pyfighter/assets/kenney_space-shooter-redux/PNG/Power-ups/powerupRed_star.png",
}

SFX_PATHS = {
    "laser": "./pyfighter/assets/zaid_sfx/laser1.wav",
    "explosion": "./pyfighter/assets/zaid_sfx/Explosion_3.wav",
    "laserHit": "./pyfighter/assets/zaid_sfx/Hit_4.wav",
    "music": "./pyfighter/assets/zaid_sfx/music.mp3",
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
