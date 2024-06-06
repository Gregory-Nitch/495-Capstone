"""Class for asteroids in the game"""

import pygame
from models.actor import Actor


class Asteroid(Actor):
    """An asteroid to be randomly generated"""

    def __init__(self, pos, hp, speed, img, offset):
        super().__init__(pos, hp, speed, img, pygame.mask.from_surface(img), offset)
