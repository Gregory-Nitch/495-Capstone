"""Base class for actors in the game, all other sprites will inherit from this
class."""

from pygame.sprite import Sprite
from pygame import Vector2
from pygame.mask import Mask


class Actor(Sprite):
    """An actor in the game space."""

    def __init__(
        self,
        pos: Vector2,
        hp: int,
        speed: int,
        img,
        img_mask: Mask,
        offset: dict,
    ):
        super().__init__()
        self.pos = pos
        self.hp = hp
        self.speed = speed
        self.img = img
        self.img_mask = img_mask
        self.offset = offset

    def draw(self, screen) -> None:
        """Draws the actor on the screen, image offsets handled internally."""

        # Using an offset allows the image to be centered at the draw location
        screen.blit(
            self.img, (self.pos.x - self.offset["x"], self.pos.y - self.offset["y"])
        )

    @classmethod
    def resolve_collision(cls, obj1, obj2) -> bool:
        """Resolves collision between two Actor objects by returning a bool if
        they are touching. Offsets handled internally. Not tied to a class
        instance."""

        offset_x = (obj2.pos.x - obj2.offset["x"]) - (obj1.pos.x - obj1.offset["x"])
        offset_y = (obj2.pos.y - obj2.offset["y"]) - (obj1.pos.y - obj1.offset["y"])
        return obj1.img_mask.overlap(obj2.img_mask, (offset_x, offset_y)) is not None
