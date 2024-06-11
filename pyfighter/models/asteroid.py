"""Class for asteroids in the game."""

from pygame import mask
from pygame import Vector2

from models.actor import Actor


class Asteroid(Actor):
    """An asteroid to be randomly generated"""

    def __init__(self, pos: Vector2, hp: int, speed: int, img, offset: dict):
        super().__init__(pos, hp, speed, img, mask.from_surface(img), offset)
        # Above mask is created from the passed image because the img is
        # randomly chosen
