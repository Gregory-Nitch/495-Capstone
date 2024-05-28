"""Class for asteroids in the game"""

import random
import pygame
from models.actor import Actor


class Asteroid(Actor):
    """An asteroid to be randomly generated"""

    def __init__(self, pos, hp, speed, img, offset) -> None:
        super().__init__(pos, hp, speed, img, offset)
        self.img = pygame.transform.rotate(img, random.randrange(0, 359))
