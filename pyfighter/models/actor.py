"""Base class for actors in the game"""


class Actor:
    """An actor in the game space."""

    def __init__(self, pos, hp, speed, img, offset) -> None:
        self.pos = pos
        self.hp = hp
        self.speed = speed
        self.img = img
        self.offset = offset

    def draw(self, screen) -> None:
        """Draws the actor on the screen"""

        screen.blit(
            self.img, (self.pos.x - self.offset["x"], self.pos.y - self.offset["y"])
        )
