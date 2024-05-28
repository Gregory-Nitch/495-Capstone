"""HUD object to display game state information to player"""


class HUD:
    """HUD for game display"""

    def __init__(self) -> None:
        self.score_pos = 0
        self.hp_pos = 0
        self.speed_pos = 0
        self.fire_rate_pos = 0
        self.missile_count_pos = 0

    def draw(self, screen, player, font) -> None:
        """Draws the HUD on the display"""
        score_surface = font.render(f"Score: {player.score}", False, (255, 255, 255))

        screen.blit(score_surface, (10, 10))
