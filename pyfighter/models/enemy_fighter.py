"""Class for the enemy fighters in the game. Attached AITrackingModule performs 
move actions for the AI."""

from pygame import Mask, Vector2
from pygame.surface import Surface
from pygame.mixer import Sound
from models.actor import Actor
from models.player import Player
from models.aitracking_module import AITrackingModule
from constants import IMG_OFFSETS, BASE_LASER_SPEED, BASE_CANNON_COOLDOWN


class EnemyFighter(Actor):
    """An enemy fighter to tail and shoot the player."""

    def __init__(
        self,
        pos: Vector2,
        hp: int,
        speed: int,
        img,
        img_mask: Mask,
        offset: dict,
        laser_img,
        laser_mask: Mask,
        laser_sfx: Sound,
        death_animation_frames: list[Surface]  # Add this parameter

    ):
        super().__init__(pos, hp, speed, img, img_mask, offset)
        self.tracking_module = AITrackingModule(self, "fighter")
        self.cooldown_counter = 0
        self.laser_img = laser_img
        self.laser_mask = laser_mask
        self.laser_sfx = laser_sfx
        self.cooldown_threshold = BASE_CANNON_COOLDOWN
        self.death_animation_frames = death_animation_frames
        self.is_dying = False
        self.current_frame = 0
        self.animation_counter = 0
        self.dead = False

    def has_target(self, player: Player, screen: Surface) -> bool:
        """Checks if the enemy fighter is behind the player and on the
        screen."""

        return (
            player.pos.x > self.pos.x - 25
            and player.pos.x < self.pos.x + 25
            and player.pos.y < self.pos.y - 150
            and self.pos.y < screen.get_height()
        )

    def shoot(self) -> Actor:
        """Method called when the fighter is behind the player, returns an Actor
        object representing a laser. This is not stored in the class as once the
        fighter is destroyed the game would loose reference to the laser objects."""

        # 0 = enemy is ready to fire
        if self.cooldown_counter == 0:
            laser_pos = Vector2((self.pos.x), (self.pos.y - self.offset["y"]))
            laser = Actor(
                laser_pos,
                0,
                BASE_LASER_SPEED,
                self.laser_img,
                self.laser_mask,
                IMG_OFFSETS["blueLaser"],  # Same offset as the blue img
            )
            self.laser_sfx.play()
            # Setting to 1 starts timer (see cooldown_cannon())
            self.cooldown_counter = 1
            return laser
        else:  # Indicates no laser, game logic should check this return
            return None

    def cooldown_cannon(self):
        """Needs to be called on every frame of the game, once the threshold is
        reached the enemy can fire again."""

        # If threshold met, then set counter to 0 (fighter can fire again)
        if self.cooldown_counter >= self.cooldown_threshold:
            self.cooldown_counter = 0
        # Else increase counter (gets closer to threshold)
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1
            
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
