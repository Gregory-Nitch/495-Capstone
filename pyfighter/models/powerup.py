import pygame
import time
from constants import POWERUP_DURATION  

class PowerUp(pygame.sprite.Sprite):
    #Power-up object for the game

    def __init__(self, pos, power_type, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.power_type = power_type
        self.spawn_time = time.time()

    def update(self, delta_time):
        #Updates the power-up position and checks if it should be removed
        self.rect.y += 200 * delta_time  # Move power-up down the screen
        if time.time() - self.spawn_time > POWERUP_DURATION:
            self.kill()  # Remove power-up after duration expires
