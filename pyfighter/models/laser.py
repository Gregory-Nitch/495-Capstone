"""Contains the laser class used by ships"""

from models.actor import Actor


class Laser(Actor):
    """Represents a laser projectile shot by a ship"""

    def __init__(self, pos, hp, speed, img, img_mask, offset):
        super.__init__(pos, hp, speed, img, img_mask, offset)

    self.dmg = 1
