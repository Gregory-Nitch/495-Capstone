"""Player object for the game."""

from pygame.sprite import Group as SpriteGroup
from pygame import Vector2
from models.actor import Actor
from constants import IMG_OFFSETS, BASE_LASER_SPEED


class Player(Actor):
    """Player object for the game"""

    def __init__(
        self,
        pos,
        hp,
        speed,
        ship_img,
        ship_mask,
        offset,
        laser_img,
        laser_mask,
        laser_sfx,
        laser_hit_sfx,
        explosion_sfx,
    ):
        super().__init__(pos, hp, speed, ship_img, ship_mask, offset)
        self.base_cooldown = 40
        self.cooldown_counter = 0
        self.laser_dmg = 1
        self.missile_count = 0
        self.score = 0
        self.laser_img = laser_img
        self.lasers_fired = SpriteGroup()
        self.laser_mask = laser_mask
        self.laser_offset = IMG_OFFSETS["blueLaser"]
        self.laser_sfx = laser_sfx
        self.laser_hit_sfx = laser_hit_sfx
        self.explosion_sfx = explosion_sfx

    def shoot(self):
        """Appends a new laser to the laser list if the player's cannon is not in cooldown."""
        if self.cooldown_counter == 0:
            laser_pos = Vector2((self.pos.x), (self.pos.y - self.offset["y"]))
            laser = Actor(
                laser_pos,
                self.laser_dmg,
                BASE_LASER_SPEED,
                self.laser_img,
                self.laser_mask,
                self.laser_offset,
            )
            self.lasers_fired.add(laser)
            self.laser_sfx.play()
            self.cooldown_counter = 1

    def resolve_hits(self, laser, objs):
        """Resolves player lasers in the game, a hit = -1 on target."""

        for obj in objs:
            if Actor.resolve_collision(laser, obj):
                obj.hp -= 1
                self.laser_hit_sfx.play()
                if obj.hp <= 0:
                    obj.kill()
                    self.explosion_sfx.play()
                self.lasers_fired.remove(laser)

    def cooldown_cannon(self):
        """Ticks trough the player's cooldown timer for their cannon per frame
        displayed."""

        if self.cooldown_counter >= self.base_cooldown:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1
