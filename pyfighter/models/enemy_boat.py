""""""

from pygame import Mask, Vector2
from models.actor import Actor
from models.player import Player
from models.aitracking_module import AITrackingModule


class EnemyBoat(Actor):
    """"""

    def __init__(
        self,
        pos: Vector2,
        hp: int,
        speed: int,
        img,
        img_mask: Mask,
        offset: dict,
        player: Player,
    ):
        super().__init__(pos, hp, speed, img, img_mask, offset)
        self.tracking_module = AITrackingModule(player)
