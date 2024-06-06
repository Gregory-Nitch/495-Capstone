"""Base class for actors in the game"""

import pygame


class Actor(pygame.sprite.Sprite):
    """An actor in the game space."""

    def __init__(self, pos, hp, speed, img, img_mask, offset):
        super().__init__()
        self.pos = pos
        self.hp = hp
        self.speed = speed
        self.img = img
        self.img_mask = img_mask
        self.offset = offset

    def draw(self, screen) -> None:
        """Draws the actor on the screen"""

        screen.blit(
            self.img, (self.pos.x - self.offset["x"], self.pos.y - self.offset["y"])
        )

    @classmethod
    def resolve_collision(cls, obj1, obj2) -> bool:
        """Resolves collision between two objects by returning a bool if
        they are touching"""

        # +5 is for image offset tuning
        offset_x = (obj2.pos.x - obj2.offset["x"] + 5) - (obj1.pos.x - obj1.offset["x"])
        offset_y = (obj2.pos.y - obj2.offset["y"]) - (obj1.pos.y - obj1.offset["y"])
        return obj1.img_mask.overlap(obj2.img_mask, (offset_x, offset_y)) is not None
