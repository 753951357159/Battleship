"""
Vessel.py

PURPOSE:
Creates the general vessel class that all vessel types are based on.
"""
from __future__ import annotations
from typing import Tuple, Optional


class TraditionalVessel:
    """
    The general vessel class used for Traditional Battleship.

    Attribute(s):
     - type: The full name of the vessel class
     - abbrev: The abbreviated form of the vessel class
     - symbol: The letter representing the vessel on the Grid

     - nation: The nation (team) the vessel belongs to
     - name: The specific name of the vessel
     - pennant: The specific id number of the vessel

     - bow: The location & direction that the bow of the vessel is located
     - hp: The number of undamaged sections of the vessel (hitpoints)
     - hits_received: The number of damaged sections of the vessel
     - health_color: The color of the vessel hp displayed
     - enemy_hp_color: The color of the vessel hp displayed on the enemy table
     - hit: Whether the vessel has been hit once or not
     - sunk: Whether the vessel is sunk or not
    """
    type: str
    abbrev: str
    symbol: str

    nation: str
    name: str
    pennant: int

    bow: Optional[Tuple[Tuple[str, str], str]]
    hp: int
    hits_received: int
    health_color: str
    enemy_hp_color: str
    hit: bool
    sunk: bool

    def __init__(self, nation: str, name: str, pennant: int) -> None:
        """
        Initializes a Vessel to be placed in a player's fleet.

        Parameter(s):
         - nation: The affiliated nation
         - name: The name of the vessel
         - pennant: The id number of the vessel
        """
        self.type = ''
        self.abbrev = ''
        self.symbol = ''

        self.nation = nation
        self.name = name
        self.pennant = pennant

        self.bow = None
        self.hp = -1
        self.hits_received = -1
        self.health_color = ''
        self.enemy_hp_color = ''
        self.hit = False
        self.sunk = False

    def __copy__(self) -> TraditionalVessel:
        """Returns a complete copy of the vessel."""
        raise NotImplementedError

    def update_health_color(self) -> None:
        """Updates the color of the hp displayed depending on hp left."""
        raise NotImplementedError
