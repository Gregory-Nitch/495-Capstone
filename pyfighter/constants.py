"""This file holds all the constant variables used by the program. 
Such as player ship size, asteroid size and loads images to use in
main."""

# Game settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1084
HUD_HEIGHT = 60
PLAYER_BUFFER = 150
BASE_SPEED = 150  # used for asteroids and enemies
PLAYER_BASE_SPEED = 300
PLAYER_BASE_HULL = 3
DROP_CHANCE = 0.2

# Offset = img width / 2 and img height / 2 | (Asteroids use averages due to rotation)
IMG_OFFSETS = {
    "player": {"x": 49, "y": 37},
    "meteorB1": {"x": 91, "y": 91},
    "meteorB2": {"x": 109, "y": 109},
    "meteorB3": {"x": 85, "y": 85},
    "meteorB4": {"x": 97, "y": 97},
    "meteorG1": {"x": 91, "y": 91},
    "meteorG2": {"x": 109, "y": 109},
    "meteorG3": {"x": 85, "y": 85},
    "meteorG4": {"x": 97, "y": 97},
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
}

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
