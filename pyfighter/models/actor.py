"""Base class for actors in the game"""


class Actor:
    """An actor in the game space."""

    def __init__(self, pos, hp, speed, img, offset):
        self.pos = pos
        self.hp = hp
        self.speed = speed
        self.img = img
        self.offset = offset

    def draw(self, screen):
        """Draws the actor on the screen"""

        screen.blit(
            self.img, (self.pos.x - self.offset[0], self.pos.y - self.offset[1])
        )
