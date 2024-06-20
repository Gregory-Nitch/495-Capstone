"""This AITrackingModule class changes behavoir based on the passed string
identifying the type of AI to implement. 
('fighter', 'left_boat', 'right_boat')"""

import math
import random
from pygame import Vector2
from pygame.sprite import Group
from pygame.surface import Surface
from models.actor import Actor


class AITrackingModule:
    """Class to give to enemy AI instances for player tracking."""

    def __init__(self, ai_obj: Actor, logic_type: str):
        self.ai_obj = ai_obj
        self.target_offset = Vector2(0, 0)

        # Object used for pathing collision detection
        self.path_obj = Actor(
            Vector2(0, 0), 0, 0, ai_obj.img, ai_obj.img_mask, ai_obj.offset
        )

        # Fighter seeks to 100px behind player
        if logic_type == "fighter":
            self.target_offset.y += 200
        # Boats offset left and right of player
        elif logic_type == "left_boat":
            self.target_offset.x -= 300
        elif logic_type == "right_boat":
            self.target_offset.x += 300

    def seek_target(
        self, target_pos: Vector2, delta_time: int, asteroids: Group, screen: Surface
    ) -> None:
        """Checks if AI is at target dest, if not calls for neighboring states
        and moves toward the choosen state."""

        # Check if target reached (prevents image vibration)
        dir_x = (target_pos.x + self.target_offset.x) - self.ai_obj.pos.x
        dir_y = (target_pos.y + self.target_offset.y) - self.ai_obj.pos.y
        distance = math.hypot(dir_x, dir_y)
        if distance < 1:
            return

        # Otherwise get next best path (only checks immediate neighbor states)
        path = self.set_path(target_pos, asteroids, screen)
        dir_x = path.x - self.ai_obj.pos.x
        dir_y = path.y - self.ai_obj.pos.y
        distance = math.hypot(dir_x, dir_y)

        if distance < 1:  # On target, avoids / by 0
            return

        dir_x = dir_x / distance
        dir_y = dir_y / distance

        self.ai_obj.pos.x += dir_x * self.ai_obj.speed * delta_time
        self.ai_obj.pos.y += dir_y * self.ai_obj.speed * delta_time

    def set_path(
        self, target_pos: Vector2, asteroids: Group, screen: Surface
    ) -> Vector2:
        """Checks all the neighboring states in a grid like form and returns
        the Vector 2 that represents that state. If is no valid state found
        this returns the current AI's state (does nothing)."""

        # Init neighboor states of AI object
        n_offset = 25  # Looks at states 20px away
        # AI is allowed 300px outside of the screen prevents getting stuck off screen
        ai_allowance_buffer = 300
        states = [
            Vector2(self.ai_obj.pos.x, self.ai_obj.pos.y - n_offset),  # Up
            Vector2(
                self.ai_obj.pos.x + n_offset,
                self.ai_obj.pos.y - n_offset,
            ),  # Up right
            Vector2(self.ai_obj.pos.x + n_offset, self.ai_obj.pos.y),  # Right
            Vector2(
                self.ai_obj.pos.x + n_offset, self.ai_obj.pos.y + n_offset
            ),  # Down Right
            Vector2(self.ai_obj.pos.x, self.ai_obj.pos.y + n_offset),  # Down
            Vector2(
                self.ai_obj.pos.x - n_offset, self.ai_obj.pos.y + n_offset
            ),  # Down Left
            Vector2(self.ai_obj.pos.x - n_offset, self.ai_obj.pos.y),  # Left
            Vector2(
                self.ai_obj.pos.x - n_offset, self.ai_obj.pos.y - n_offset
            ),  # Up Left
        ]

        path = (None, None)  # Vec2 to return, set in following loop
        path_idx = 0  # Path held at this index
        cost_idx = 1
        # Search all neighbooring states
        for state in states:
            if (  # Elimnate those states that are out of screen bounds +- buffer
                state.x < -ai_allowance_buffer
                or state.x > screen.get_width() + ai_allowance_buffer
                or state.y < -ai_allowance_buffer
                or state.y > screen.get_height() + ai_allowance_buffer
            ):
                continue
            for a in asteroids:  # or that would collide with an asteroid
                self.path_obj.pos = state
                if Actor.resolve_collision(self.path_obj, a):
                    continue

            # Else calculate the distance from state to target
            dis_x = (target_pos.x + self.target_offset.x) - state.x
            dis_y = (target_pos.y + self.target_offset.y) - state.y
            distance = math.hypot(dis_x, dis_y)
            canadite = (state, distance)
            # Pick shortest distance
            if not path[path_idx] or canadite[cost_idx] < path[cost_idx]:
                path = canadite
            # Else if equal cost -> choose random direction
            elif path[cost_idx] == canadite[cost_idx]:
                path = random.choice([path, canadite])

        return (
            path[path_idx] if path[path_idx] else self.ai_obj.pos
        )  # Only Vec2 needs to be returned, if there was no path found return current state
