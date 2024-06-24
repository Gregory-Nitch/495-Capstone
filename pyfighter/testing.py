"""This file contains all the unit tests for the project. Manually calling the
tests can be done via 'python -m pytest testing.py' from the command line in
the ~/PyFighter/pyfighter/ directory. Note that file paths are different
due to calling pytest from a lower directory, this was done to facilitate
importing of required modules from the game. Also note that sometimes tests 
will play sounds and powerup to initialze a game screen (your screen may flash).

IMPORTANT: ALL test methods must start with 'test' for pytest to find them

"""

import pygame
from pygame.mixer import Sound
from models.player import Player
from models.actor import Actor
from models.powerup import PowerUp
from models.enemy_fighter import EnemyFighter
from models.enemy_boat import EnemyBoat


def test_cooldown_counters():
    """Tests if the player's cannon cooldown counter is properly set after
    firing their cannon."""

    # Setup pygame state
    pygame.init()
    pygame.display.set_mode((0, 0))

    # Mock player
    player_img = pygame.image.load(
        "./assets/active_sprites/ships/playerShip1_orange.png"
    ).convert_alpha()
    missile_img = pygame.image.load(
        "./assets/active_sprites/Missiles/spaceMissiles_001.png"
    ).convert_alpha()
    test_player = Player(
        pygame.Vector2(0, 0),
        0,
        0,
        player_img,
        None,
        {"x": 0, "y": 0},
        None,
        None,
        Sound("./assets/zaid_sfx/laser1.wav"),
        missile_img,
        None,
        None,
        None,
        Sound("./assets/zaid_sfx/missile_launch_sfx.mp3"),
        [
            pygame.image.load(
                f"./assets/active_sprites/ships/player_ani/idle/player_idle-{str(i).zfill(3)}.png"
            ).convert_alpha()
            for i in range(0, 20)
        ],
    )

    # Test counters
    assert test_player.cooldown_counter == 0
    test_player.shoot()
    assert test_player.cooldown_counter == 1
    assert test_player.missile_cooldown_counter == 0
    test_player.fire_missle([test_player])
    assert test_player.missile_cooldown_counter == 1


def test_collision():
    """Tests if collision between two objects is working."""

    # Setup state
    pygame.init()
    pygame.display.set_mode((0, 0))

    # Load an image for masking
    test_img = pygame.image.load(
        "./assets/active_sprites/ships/playerShip1_orange.png"
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
        "./assets/active_sprites/ships/playerShip1_orange.png"
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
        "./assets/active_sprites/Lasers/laserBlue07.png"
    ).convert_alpha()
    test_laser_mask = pygame.mask.from_surface(test_laser_img)

    # Mock player object
    player_img = pygame.image.load(
        "./assets/active_sprites/ships/playerShip1_orange.png"
    ).convert_alpha()
    test_player = Player(
        pygame.Vector2(0, 0),
        0,
        0,
        player_img,
        None,
        {"x": 0, "y": 0},
        test_laser_img,
        test_laser_mask,
        Sound("./assets/zaid_sfx/laser1.wav"),
        None,
        None,
        Sound("./assets/zaid_sfx/Hit_4.wav"),
        None,
        Sound("./assets/zaid_sfx/missile_launch_sfx.mp3"),
        [
            pygame.image.load(
                f"./assets/active_sprites/ships/player_ani/idle/player_idle-{str(i).zfill(3)}.png"
            ).convert_alpha()
            for i in range(0, 20)
        ],
    )

    # Load asteroid
    test_asteroid_img = pygame.image.load(
        "./assets/active_sprites/Lasers/laserBlue07.png"
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


def test_powerup_pickup():
    """This tests if the pickups are properly changing player stats."""

    pygame.init()

    # Load image for mock
    powerup_img = pygame.image.load(
        "./assets/active_sprites/Power-Ups/powerupBlue_star.png"
    ).convert_alpha()
    powerup_mask = pygame.mask.from_surface(powerup_img)

    # Mock powerups
    fire_rate_powerup = PowerUp(
        pygame.Vector2(0, 0),
        0,
        powerup_img,
        powerup_mask,
        {"x": 0, "y": 0},
        "fire_rate",
        pygame.mixer.Sound("./assets/zaid_sfx/powerup.mp3"),
    )
    speed_powerup = PowerUp(
        pygame.Vector2(0, 0),
        0,
        powerup_img,
        powerup_mask,
        {"x": 0, "y": 0},
        "speed",
        pygame.mixer.Sound("./assets/zaid_sfx/powerup.mp3"),
    )
    missile_powerup = PowerUp(
        pygame.Vector2(0, 0),
        0,
        powerup_img,
        powerup_mask,
        {"x": 0, "y": 0},
        "missiles",
        pygame.mixer.Sound("./assets/zaid_sfx/powerup.mp3"),
    )

    # Mock player
    player_img = pygame.image.load(
        "./assets/active_sprites/ships/playerShip1_orange.png"
    ).convert_alpha()
    test_player = Player(
        pygame.Vector2(0, 0),
        0,
        300,
        player_img,
        None,
        {"x": 0, "y": 0},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        Sound("./assets/zaid_sfx/missile_launch_sfx.mp3"),
        [
            pygame.image.load(
                f"./assets/active_sprites/ships/player_ani/idle/player_idle-{str(i).zfill(3)}.png"
            ).convert_alpha()
            for i in range(0, 20)
        ],
    )

    fire_rate_powerup.pickup(test_player)
    speed_powerup.pickup(test_player)
    missile_powerup.pickup(test_player)
    assert test_player.cooldown_threshold == 39
    assert test_player.speed == 320
    assert test_player.missile_count == 3


def test_fighter_cooldown_counters():
    """Tests if the enemy's cannon cooldown counter is properly set after
    firing their cannon."""

    # Setup pygame state
    pygame.init()
    pygame.display.set_mode((0, 0))

    # Mock fighter
    fighter_img = pygame.image.load(
        "./assets/active_sprites/Enemies/enemyBlack1.png"
    ).convert_alpha()
    laser_img = pygame.image.load(
        "./assets/active_sprites/Lasers/laserRed07.png"
    ).convert_alpha()
    test_fighter = EnemyFighter(
        pygame.Vector2(0, 0),
        0,
        0,
        fighter_img,
        None,
        {"x": 0, "y": 0},
        laser_img,
        None,
        Sound("./assets/zaid_sfx/laser1.wav"),
        [
            pygame.image.load(
                f"./assets/active_sprites/enemies/enemy_deathani/enemy_death{str(i).zfill(3)}.png"
            ).convert_alpha()
            for i in range(1, 14)
        ],
    )

    # Test counters
    assert test_fighter.cooldown_counter == 0
    laser = test_fighter.shoot()
    assert test_fighter.cooldown_counter == 1
    assert laser is not None
    laser = test_fighter.shoot()
    assert laser is None


def test_boat_cooldown_counters():
    """Tests if the enemy's cannon cooldown counter is properly set after
    firing their cannon."""

    # Setup pygame state
    pygame.init()
    pygame.display.set_mode((0, 0))

    # Mock boat
    boat_img = pygame.image.load(
        "./assets/active_sprites/Enemies/enemyBlack4.png"
    ).convert_alpha()
    missle_img = pygame.image.load(
        "./assets/active_sprites/Missiles/spaceMissiles_040.png"
    ).convert_alpha()
    test_boat = EnemyBoat(
        pygame.Vector2(0, 0),
        0,
        0,
        boat_img,
        None,
        "left_boat",
        {"x": 0, "y": 0},
        missle_img,
        None,
        Sound("./assets/zaid_sfx/missile_launch_sfx.mp3"),
        [
            pygame.image.load(
                f"./assets/active_sprites/enemies/boat_deathani/boat_death{str(i).zfill(3)}.png"
            ).convert_alpha()
            for i in range(1, 13)
        ],
    )

    # Mock player
    player_img = pygame.image.load(
        "./assets/active_sprites/ships/playerShip1_orange.png"
    ).convert_alpha()
    test_player = Player(
        pygame.Vector2(0, 0),
        0,
        0,
        player_img,
        None,
        {"x": 0, "y": 0},
        None,
        None,
        Sound("./assets/zaid_sfx/laser1.wav"),
        None,
        None,
        None,
        None,
        Sound("./assets/zaid_sfx/missile_launch_sfx.mp3"),
        [
            pygame.image.load(
                f"./assets/active_sprites/ships/player_ani/idle/player_idle-{str(i).zfill(3)}.png"
            ).convert_alpha()
            for i in range(0, 20)
        ],
    )

    # Test counters
    assert test_boat.missile_cooldown_counter == 0
    missile = test_boat.launch_missile(test_player)
    assert test_boat.missile_cooldown_counter == 1
    assert missile is not None
    missile = test_boat.launch_missile(test_player)
    assert missile is None
