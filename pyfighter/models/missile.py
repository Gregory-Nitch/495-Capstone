""""""

from pygame import Mask, Vector2
from models.actor import Actor


class Missle(Actor):
    """"""

    def __init__(
        self,
        pos: Vector2,
        hp: int,
        speed: int,
        img,
        img_mask: Mask,
        offset: dict,
        target: Actor,
    ):
        super().__init__(pos, hp, speed, img, img_mask, offset)
        self.target = target
        pass

    def seek(self):
        """"""
        # TODO
        pass
