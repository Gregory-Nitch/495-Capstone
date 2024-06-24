"""HUD object to display game state information to player."""

from pygame.font import SysFont
from models.player import Player


class HUD:
    """HUD for game display, calling draw() will display the hud."""

    def __init__(self):
        self.score_pos = 0
        self.hp_pos = 0
        self.speed_pos = 0
        self.fire_rate_pos = 0
        self.missile_count_pos = 0
        self.text_color = (255, 255, 255)

    def draw(
        self, screen, player: Player, hud_font: SysFont, control_font: SysFont
    ) -> None:
        """Draws the HUD on the display. Includes score, player state, and controls."""

        score_surface = hud_font.render(f"Score: {player.score}", True, self.text_color)
        stats_surface = hud_font.render(
            f"Hull: {player.hp}  Thrust: {player.speed} "
            + f" Cannon Cooldown: {player.cooldown_threshold}  Missiles: {player.missile_count}",
            True,
            self.text_color,
        )
        control_label_surface = hud_font.render("Controls:", True, self.text_color)
        move_surface = control_font.render(
            "Movement: Arrow Keys",
            True,
            self.text_color,
        )
        fire_surface = control_font.render("Cannon: Space", True, self.text_color)
        missile_surface = control_font.render("Missile: L-Alt", True, self.text_color)
        screen.blit(score_surface, (10, 15))
        screen.blit(stats_surface, (420, 15))
        screen.blit(control_label_surface, (1010, 15))
        screen.blit(move_surface, (1110, 3))
        screen.blit(fire_surface, (1110, 20))
        screen.blit(missile_surface, (1110, 37))
