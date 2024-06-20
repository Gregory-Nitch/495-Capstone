"""Contains the enemy missile boat class that fires missiles at the player from
their left and right."""

from pygame import Mask, Vector2
from models.actor import Actor
from models.player import Player
from models.missile import Missile
from models.aitracking_module import AITrackingModule
from constants import BOAT_MISSILE_COOLDOWN, IMG_OFFSETS


class EnemyBoat(Actor):
    """Represents an enemy ship that fires missiles at the player."""

    def __init__(
        self,
        pos: Vector2,
        hp: int,
        speed: int,
        img,
        img_mask: Mask,
        logic_type: str,
        offset: dict,
        missile_img,
        missile_mask: Mask,
    ):
        super().__init__(pos, hp, speed, img, img_mask, offset)
        self.tracking_module = AITrackingModule(self, logic_type)
        self.missile_img = missile_img
        self.missile_mask = missile_mask
        self.missile_cooldown_threshold = BOAT_MISSILE_COOLDOWN
        self.missile_cooldown_counter = 0

    def is_on_screen(self, screen_width, screen_height) -> bool:
        """Checks if the missile boat is on the screen, used to prevent it from
        firing if it is not on the screen."""

        return (
            self.pos.x > 0
            and self.pos.x < screen_width
            and self.pos.y > 0
            and self.pos.y < screen_height
        )

    def cooldown_missiles(self):
        """Ticks the cooldown for boat missiles, should be called for
        every iteration of the main game loop."""

        if self.missile_cooldown_counter >= self.missile_cooldown_threshold:
            self.missile_cooldown_counter = 0
        elif self.missile_cooldown_counter > 0:
            self.missile_cooldown_counter += 1

    def launch_missile(self, player: Player) -> Missile:
        """Launches a new missile from the boat and returns the missile
        reference for seeking and tracking."""

        if self.missile_cooldown_counter == 0:
            missile_pos = Vector2((self.pos.x), (self.pos.y - self.offset["y"]))
            missile = Missile(
                missile_pos,
                1,
                self.speed,
                self.missile_img,
                self.missile_mask,
                IMG_OFFSETS["red_missile"],
                player,
                90.0,
            )
            self.missile_cooldown_counter = 1
            return missile
        else:
            return None
