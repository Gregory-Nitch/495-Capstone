"""Represents an explosion in the game, simply used for animations."""

import pygame
from pygame import Vector2


class Explosion(pygame.sprite.Sprite):
    """Explosion in the game, used for vfx."""

    def __init__(self, pos: Vector2, animation_frames: list):
        super().__init__()
        self.frames = animation_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=pos)
        self.animation_counter = 0

    def update(self):
        """Updates the explosion to the next frame."""
        if self.animation_counter % 5 == 0:  # Adjust this value to change the speed
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.kill()  # Remove the explosion when animation is done
            else:
                self.image = self.frames[self.current_frame]
        self.animation_counter += 1
