"""
This module defines the PowerUp class, which represents power-up items in the game.
Power-ups provide various benefits to the player, such as increasing fire rate,
speed, or missile count when picked up.
"""

import pygame
from pygame import Vector2
from pygame.mask import Mask
from models.actor import Actor
from models.player import Player
from constants import SFX_PATHS


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
    ):
        """Initializes a new instance of the PowerUp class"""
        super().__init__(pos, 0, speed, img, img_mask, offset)
        self.power_type = power_type

    def pickup(self, player: Player) -> None:
        """Applies the power-up effect to the player when picked up"""

        # Only decrement if player cooldown is above 0 -> prevents negative cooldown
        if self.power_type == "fire_rate" and player.cooldown_threshold > 0:
            player.cooldown_threshold -= 2
        elif self.power_type == "speed":
            player.speed += 50
        elif self.power_type == "missiles":
            player.missile_count += 1

        # Play a pickup sound
        self.play_pickup_sound()

        # Display visual effect
        player.start_glow_effect()

    def play_pickup_sound(self):
        """Plays a sound effect when the power-up is picked up."""

        pickup_sound = pygame.mixer.Sound(SFX_PATHS["powerup_pickup"])
        pickup_sound.play()

 
