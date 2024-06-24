"""Class for asteroids in the game."""

from pygame import mask
from pygame import Vector2

from models.actor import Actor
from models.explosion import Explosion

class Asteroid(Actor):
    """An asteroid to be randomly generated"""

    def __init__(self, pos: Vector2, hp: int, speed: int, img, offset: dict, explosion_frames: list):
        super().__init__(pos, hp, speed, img, mask.from_surface(img), offset)
        self.explosion_frames = explosion_frames
        # Above mask is created from the passed image because the img is
        # randomly chosen

    def explode(self):
        return Explosion(self.pos, self.explosion_frames)