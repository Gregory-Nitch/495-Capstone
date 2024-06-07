""""""

from models.actor import Actor
from models.player import Player


class PowerUp(Actor):
    """"""

    # Power-up object for the game

    def __init__(self, pos, speed, img, img_mask, offset, power_type):
        super().__init__(pos, 0, speed, img, img_mask, offset)
        self.power_type = power_type

    def resolve_powerup_collision(self, player: Player) -> bool:
        """"""

        # +5 is for image offset tuning
        offset_x = (player.pos.x - player.offset["x"] + 5) - (
            self.pos.x - self.offset["x"]
        )
        offset_y = (player.pos.y - player.offset["y"]) - (self.pos.y - self.offset["y"])
        return self.img_mask.overlap(player.img_mask, (offset_x, offset_y)) is not None

    def pickup(self, player: Player) -> None:
        """"""

        # TODO check the rest of the powerup types below
        if self.power_type == "fire_rate":
            player.cooldown_threshold -= 2
