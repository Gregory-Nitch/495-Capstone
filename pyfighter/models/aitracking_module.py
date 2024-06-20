"""This AITrackingModule class changes behavoir based on the passed string
identifying the type of AI to implement. 
('fighter', 'left_boat', 'right_boat')"""

import math
from pygame import Vector2
from models.player import Player
from models.actor import Actor


class AITrackingModule:
    """Class to give to enemy AI instances for player tracking."""

    def __init__(self, ai_obj: Actor, logic_type: str):
        self.ai_obj = ai_obj
        self.target_offset = Vector2(0, 0)
        # Fighter seeks to 100px behind player
        if logic_type == "fighter":
            self.target_offset.y += 200

        # TODO check 'left_boat' && 'right_boat' types

    def seek_target(self, player: Player, delta_time: int) -> None:
        """Calculates the distance and direction to the player, then moves
        the enclosing class instance in that direction."""

        dir_x = (player.pos.x + self.target_offset.x) - self.ai_obj.pos.x
        dir_y = (player.pos.y + self.target_offset.y) - self.ai_obj.pos.y
        distance = math.hypot(dir_x, dir_y)

        # Check if target reached (prevents img vibration)
        if distance < 1:
            return

        dir_x = dir_x / distance
        dir_y = dir_y / distance

        self.ai_obj.pos.x += dir_x * self.ai_obj.speed * delta_time
        self.ai_obj.pos.y += dir_y * self.ai_obj.speed * delta_time
