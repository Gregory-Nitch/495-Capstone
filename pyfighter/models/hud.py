"""HUD object to display game state information to player"""


class HUD:
    """HUD for game display"""

    def __init__(self):  # TODO move magic numbers up here (from draw)
        self.score_pos = 0
        self.hp_pos = 0
        self.speed_pos = 0
        self.fire_rate_pos = 0
        self.missile_count_pos = 0

    def draw(self, screen, player, hud_font, control_font) -> None:
        """Draws the HUD on the display"""
        score_surface = hud_font.render(f"Score: {player.score}", True, (255, 255, 255))
        stats_surface = hud_font.render(
            f"Hull: {player.hp}  Thrust: {player.speed} "
            + f" Cannon Cooldown: {player.base_cooldown}  Missiles: {player.missile_count}",
            True,
            (255, 255, 255),
        )
        control_label_surface = hud_font.render("Controls:", True, (255, 255, 255))
        move_surface = control_font.render(
            "Movement: Arrow Keys",
            True,
            (255, 255, 255),
        )
        fire_surface = control_font.render("Cannon: Space", True, (255, 255, 255))
        missile_surface = control_font.render("Missile: L-Alt", True, (255, 255, 255))
        screen.blit(score_surface, (10, 15))
        screen.blit(stats_surface, (420, 15))
        screen.blit(control_label_surface, (1010, 15))
        screen.blit(move_surface, (1110, 3))
        screen.blit(fire_surface, (1110, 20))
        screen.blit(missile_surface, (1110, 37))
