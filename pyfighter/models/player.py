"""Player object for the game."""

import actor


class Player(actor.Actor):
    """Player object for the game"""

    def __init__(self, x, y, hp, speed):
        super().__init__(x, y, hp, speed)
        self.fire_rate = 1
        self.missile_cout = 0
        self.score = 0
