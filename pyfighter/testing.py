"""This file contains all the unit tests for the project. Manually calling the
tests can be done via 'python -m pytest testing.py' from the command line in
the ~/PyFighter/pyfighter/ directory. Note that file paths are different
due to calling pytest from a lower directory, this was done to facilitate
importing of required modules from the game. Also note that sometimes tests 
will play sounds and need to initialze a game screen (your screen may flash).

IMPORTANT: ALL test methods must start with 'test' for pytest to find them

"""

import pygame
from pygame.mixer import Sound
from models.player import Player
from models.actor import Actor


def test_cooldown_toggle():
    """Tests if the player's cannon cooldown counter is properly set after
    firing their cannon."""

    # Setup player and state
    pygame.init()
    test_player = Player(
        pygame.Vector2(0, 0),
        0,
        0,
        None,
        None,
        {"x": 0, "y": 0},
        None,
        None,
        Sound("./assets/zaid_sfx/laser1.wav"),
        None,
        None,
        None,
        None,
    )
    # Test counter
    assert test_player.cooldown_counter == 0
    test_player.shoot()
    assert test_player.cooldown_counter == 1


def test_collision():
    """Tests if collision between two objects is working."""

    # Setup state
    pygame.init()
    pygame.display.set_mode((0, 0))

    # Load an image for masking
    test_img = pygame.image.load(
        "./assets/kenney_space-shooter-redux/PNG/playerShip1_orange.png"
    ).convert_alpha()
    test_mask = pygame.mask.from_surface(test_img)

    # Create mock objects
    test_actor1 = Actor(
        pygame.Vector2(0, 0), 0, 0, test_img, test_mask, {"x": 0, "y": 0}
    )
    test_actor2 = Actor(
        pygame.Vector2(0, 0), 0, 0, test_img, test_mask, {"x": 0, "y": 0}
    )

    # Test collision detection
    assert Actor.resolve_collision(test_actor1, test_actor2) is True


def test_noncollision():
    """Tests collision conditions in the negative state, ie. objects are not
    colliding."""

    # Setup state
    pygame.init()
    pygame.display.set_mode((0, 0))

    # Load images
    test_img = pygame.image.load(
        "./assets/kenney_space-shooter-redux/PNG/playerShip1_orange.png"
    ).convert_alpha()
    test_mask = pygame.mask.from_surface(test_img)

    # Create mock objects 1000px apart
    test_actor1 = Actor(
        pygame.Vector2(1000, 1000), 0, 0, test_img, test_mask, {"x": 0, "y": 0}
    )
    test_actor2 = Actor(
        pygame.Vector2(0, 0), 0, 0, test_img, test_mask, {"x": 0, "y": 0}
    )

    # Test collision detection = negative
    assert Actor.resolve_collision(test_actor1, test_actor2) is False


def test_resolve_hits():
    """Tests that objects hit by lasers are properly having their hp reduced."""

    # Setup state
    pygame.init()
    pygame.display.set_mode((0, 0))

    # Load laser
    test_laser_img = pygame.image.load(
        "./assets/kenney_space-shooter-redux/PNG/Lasers/laserBlue07.png"
    ).convert_alpha()
    test_laser_mask = pygame.mask.from_surface(test_laser_img)

    # Mock player object
    test_player = Player(
        pygame.Vector2(0, 0),
        0,
        0,
        None,
        None,
        {"x": 0, "y": 0},
        test_laser_img,
        test_laser_mask,
        Sound("./assets/zaid_sfx/laser1.wav"),
        None,
        None,
        Sound("./assets/zaid_sfx/Hit_4.wav"),
        None,
    )

    # Load asteroid
    test_asteroid_img = pygame.image.load(
        "./assets/kenney_space-shooter-redux/PNG/Lasers/laserBlue07.png"
    ).convert_alpha()
    test_asteroid_mask = pygame.mask.from_surface(test_asteroid_img)

    # Mock asteroid objects
    test_asteroid1 = Actor(
        pygame.Vector2(0, 0),
        3,
        0,
        test_asteroid_img,
        test_asteroid_mask,
        {"x": 0, "y": 0},
    )
    # 1000px offset to test miss
    test_asteroid2 = Actor(
        pygame.Vector2(1000, 1000),
        3,
        0,
        test_asteroid_img,
        test_asteroid_mask,
        {"x": 0, "y": 0},
    )

    # Mock laser object
    test_laser1 = Actor(
        pygame.Vector2(0, 0), 0, 0, test_laser_img, test_laser_mask, {"x": 0, "y": 0}
    )
    test_laser2 = Actor(
        pygame.Vector2(0, 0), 0, 0, test_laser_img, test_laser_mask, {"x": 0, "y": 0}
    )
    test_player.lasers_fired.add(test_laser1)
    test_player.lasers_fired.add(test_laser2)

    # Hit mock asteroid with mock laser
    test_player.resolve_hits(test_laser1, [test_asteroid1, test_asteroid2])

    # Check asteroid hp is 3 - 1
    assert test_asteroid1.hp == 2
    assert test_asteroid2.hp == 3  # test non hit
