"""Player object for the game."""

from models.actor import Actor


class Player(Actor):
    """Player object for the game"""

    def __init__(self, pos, hp, speed, img, offset):
        super().__init__(pos, hp, speed, img, offset)
        self.fire_rate = 1
        self.missile_cout = 0
        self.score = 0
