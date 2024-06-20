"""This class is used to represent a missile fired from both the player and
AI eneimes and contains all the logic required to track a target."""

import math
import pygame.transform
import pygame.mask
from pygame import Mask, Vector2
from models.actor import Actor


class Missile(Actor):
    """Represents a missile fired by the player or AI enemy."""

    def __init__(
        self,
        pos: Vector2,
        hp: int,
        speed: int,
        img,
        img_mask: Mask,
        offset: dict,
        target: Actor,
        init_heading: float,
    ):
        super().__init__(pos, hp, speed, img, img_mask, offset)
        self.target = target
        self.heading = init_heading
        self.img_rotated = pygame.transform.rotate(self.img, init_heading)
        self.img_mask = pygame.mask.from_surface(self.img)

    def seek(self, delta_time: int):
        """Logic used to track a target, needs to be called on every frame.
        The logic calculates various angles needed to guide a missile to
        its target and allows forward arc movement."""

        # Calculate left or right turn
        dir_x = self.target.pos.x - self.pos.x
        dir_y = self.target.pos.y - self.pos.y
        rads = math.atan2(-dir_y, dir_x)  # dir_y negated due to pygame inverting y
        rads %= 2 * math.pi
        # degrees from direct right on screen counter clockwise
        degs = math.degrees(rads)

        l_degs = degs - self.heading
        if l_degs < 0:
            l_degs += 359  # normailze value from negative number
        r_degs = 359 - l_degs

        # If target is in front of missile follow degs
        if abs(degs - self.heading) < 2:
            self.heading = degs
        # Otherwise turn based on shortest degree angle
        elif l_degs <= r_degs:  # Left turn
            self.heading += 2
        elif l_degs > r_degs:  # Right turn
            self.heading -= 2

        # Normalize heading if needed
        if self.heading > 359:
            self.heading -= 359
        elif self.heading < 0:
            self.heading += 359

        # Turn image and mask
        self.img_rotated = pygame.transform.rotate(self.img, self.heading)
        self.img_mask = pygame.mask.from_surface(self.img)

        # Move forward (calculate forward arc (x,y) from current heading)
        distance = 10
        for_x = distance * math.cos(self.heading * math.pi / 180)
        # negated for pygame y
        for_y = -(distance * math.sin(self.heading * math.pi / 180))

        for_x = for_x / distance
        for_y = for_y / distance

        self.pos.x += for_x * self.speed * delta_time
        self.pos.y += for_y * self.speed * delta_time

    # Overrides Actor.draw()
    def draw(self, screen) -> None:
        """Draws a missile on the screen. Overrides Actor.draw() because
        missile images need to be rotated as their heading changes."""

        screen.blit(
            self.img_rotated,
            (self.pos.x - self.offset["x"], self.pos.y - self.offset["y"]),
        )

    def is_off_screen(self, screen) -> bool:
        """Checks if a missile is off the screen, off screen -> true else
        false."""

        return (
            self.pos.y < 0
            or self.pos.y > screen.get_height()
            or self.pos.x < 0
            or self.pos.x > screen.get_width()
        )

    @classmethod
    def lock(cls, firing_location: Vector2, targets: list) -> Actor:
        """Takes in a list of targets and selects the closest one as the
        missile's locked target. ->(classmethod)<-"""

        # Empty tuple for null return
        lock = (None, 0)

        for target in targets:
            if not target:
                continue
            # Lock onto the nearest target
            dir_x = firing_location.x - target.pos.x
            dir_y = firing_location.y - target.pos.y
            distance = math.hypot(dir_x, dir_y)
            if lock[1] < distance:
                lock = (target, distance)

        # Return None or reference to locked Actor
        return lock[0]
