"""Base class for actors in the game"""


class Actor:
    """An actor in the game space."""

    def __init__(self, x, y, hp, speed):
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed
