"""
This module defines the PowerUp class, which represents power-up items in the game.
Power-ups provide various benefits to the player, such as increasing fire rate,
speed, or missile count when picked up.
"""

from pygame import Vector2
from pygame.mask import Mask
from pygame.mixer import Sound
from models.actor import Actor
from models.player import Player


class PowerUp(Actor):
    """Power-up object for the game"""

    def __init__(
        self,
        pos: Vector2,
        speed: int,
        img,
        img_mask: Mask,
        offset: dict,
        power_type: str,
        pickup_sfx: Sound,
    ):
        """Initializes a new instance of the PowerUp class"""
        super().__init__(pos, 0, speed, img, img_mask, offset)
        self.power_type = power_type
        self.pickup_sfx = pickup_sfx

    def pickup(self, player: Player) -> None:
        """Applies the power-up effect to the player when picked up"""

        # Only decrement if player cooldown is above 0 -> prevents negative cooldown
        if self.power_type == "fire_rate" and player.cooldown_threshold > 2:
            player.cooldown_threshold -= 1
        elif self.power_type == "speed":
            player.speed += 20
        elif self.power_type == "missiles":
            player.missile_count += 1

        self.pickup_sfx.play()
        player.start_glow_effect()
