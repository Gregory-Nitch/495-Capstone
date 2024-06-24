"""Contains the enemy missile boat class that fires missiles at the player from
their left and right."""

from pygame import Mask, Vector2
from pygame.mixer import Sound
from models.actor import Actor
from models.player import Player
from pygame.surface import Surface
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
        missile_sfx: Sound,
        death_animation_frames: list[Surface]  # Add this parameter

    ):
        super().__init__(pos, hp, speed, img, img_mask, offset)
        self.tracking_module = AITrackingModule(self, logic_type)
        self.missile_img = missile_img
        self.missile_mask = missile_mask
        self.missile_cooldown_threshold = BOAT_MISSILE_COOLDOWN
        self.missile_cooldown_counter = 0
        self.missile_sfx = missile_sfx
        self.death_animation_frames = death_animation_frames
        self.is_dying = False
        self.current_frame = 0
        self.animation_counter = 0
        self.dead = False

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
            self.missile_sfx.play()
            self.missile_cooldown_counter = 1
            return missile
        else:
            return None

    def start_death_animation(self):
        self.is_dying = True
        self.current_frame = 0
        self.animation_counter = 0
        
    def update_death_animation(self):
        if self.is_dying:
            if self.animation_counter % 5 == 0:  # Adjust the speed of the animation
                self.current_frame += 1
            if self.current_frame >= len(self.death_animation_frames):
                self.dead = True  # Remove the enemy fighter after the animation is done
            else:
                self.img = self.death_animation_frames[self.current_frame]
            self.animation_counter += 1
