"""
This module defines the PowerUp class, which represents power-up items in the game.
Power-ups provide various benefits to the player, such as increasing fire rate,
speed, or missile count when picked up.
"""

from models.actor import Actor
from models.player import Player
import pygame


class PowerUp(Actor):
    """Power-up object for the game"""

    def __init__(self, pos, speed, img, img_mask, offset, power_type):
        """Initializes a new instance of the PowerUp class"""
        super().__init__(pos, 0, speed, img, img_mask, offset)
        self.power_type = power_type

    def pickup(self, player: Player) -> None:
        """Applies the power-up effect to the player when picked up"""

        # TODO check the rest of the powerup types below
        if self.power_type == "fire_rate" and player.cooldown_threshold > 0:
            player.cooldown_threshold -= 2
        elif self.power_type == "speed":
            player.speed += 50
        elif self.power_type == "missiles":
            player.missile_count += 1

        # Play pickup sound
        self.play_pickup_sound()

        # Display visual effect
        self.display_pickup_effect(player)

    def play_pickup_sound(self):
        """Plays a sound effect when the power-up is picked up."""
        pickup_sound = pygame.mixer.Sound("./pyfighter/assets/zaid_sfx/powerup.mp3")
        pickup_sound.play()

    def display_pickup_effect(self, player: Player):
        """Displays a visual effect when the power-up is picked up."""

        #$ TODO this is not working correctly - player doesnt retore to original color
        # Example: Add a brief glow effect to the player
        original_color = player.img.get_at((0, 0))
        glow_color = pygame.Color("yellow")
        player.img.fill(glow_color, special_flags=pygame.BLEND_ADD)
        pygame.time.set_timer(pygame.USEREVENT, 200)  # Restore color after 200ms
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                player.img.fill(original_color, special_flags=pygame.BLEND_SUB)
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Disable timer
