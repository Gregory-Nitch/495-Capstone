""""""

from models.actor import Actor
from models.player import Player


class PowerUp(Actor):
    """"""

    # Power-up object for the game

    def __init__(self, pos, speed, img, img_mask, offset, power_type):
        super().__init__(pos, 0, speed, img, img_mask, offset)
        self.power_type = power_type

    def pickup(self, player: Player) -> None:
        """"""

        # TODO check the rest of the powerup types below
        if self.power_type == "fire_rate" and player.cooldown_threshold > 0:
            player.cooldown_threshold -= 2
