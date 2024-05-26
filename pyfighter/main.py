"""
PyFighter game in python with pygame! Blast away skip!
Authors:
    - Fandel, Jacob
    - Hart, Hope
    - Lozano, Zaid
    - Nitch, Gregory
    - Wheeler, Jack
"""

# Example file showing a basic pygame "game loop"
import pygame

# Globals
SCREEN = pygame.display.set_mode((1280, 828))
CLOCK = pygame.time.Clock()
BG_IMAGE = pygame.image.load(
    "./pyfighter/assets/kenney_space-shooter-redux/Backgrounds/bg_merged.png"
).convert()


def draw_background():
    """Draws the background of the game and the HUD base."""
    pygame.draw.rect(SCREEN, "black", (0, 0, SCREEN.get_width(), 60))
    SCREEN.blit(BG_IMAGE, (0, 60))


def main():
    """Main game loop"""

    # pygame setup
    pygame.init()
    running = True
    dt = 0

    player_pos = pygame.Vector2(SCREEN.get_width() / 2, SCREEN.get_height() / 2)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with background to wipe away anything from last frame
        draw_background()

        pygame.draw.circle(SCREEN, "red", player_pos, 40)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_DOWN]:
            player_pos.y += 300 * dt
        if keys[pygame.K_LEFT]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_RIGHT]:
            player_pos.x += 300 * dt

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = CLOCK.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
