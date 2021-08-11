"""
Node.py

PURPOSE:
Creates the node object for the Grid object. Stores all relevant information
about vessels.
"""
from __future__ import annotations
from typing import Optional
from Settings import \
    DEFAULT, GREEN, PURPLE, BLUE, RED, YELLOW, \
    EMPTY, HIT, MISS, DROP
from Objects.Vessels.Vessel import TraditionalVessel


class Node:
    """
    A node (coordinate) on a Grid; a grid square in traditional Battleship.
    Stores all important information relevant to player vessels.

    Attribute(s):
     - row: The row the node is in
     - col: The column the node is in

     - north: The node directly north of the current node or None if nonexistent
     - south: The node directly south of the current node or None if nonexistent
     - east: The node directly east of the current node or None if nonexistent
     - west: The node directly west of the current node or None if nonexistent

     - occupied: True if there is a vessel located at the node, False otherwise
     - hit: Whether the node has been hit or not by any armament
     - sign: The relevant symbol; hit, miss, etc.
     - color: The color of the symbol when displayed on the grid
     - vessel: The vessel that occupies the node, if any
    """
    row: str
    col: str

    north: Optional[Node]
    south: Optional[Node]
    east: Optional[Node]
    west: Optional[Node]

    occupied: bool
    hit: bool
    sign: str
    color: str
    vessel: Optional[TraditionalVessel]

    def __init__(self, col: str, row: str) -> None:
        """
        Initiates a new Node object.

        Parameter(s):
         - col: The column the node is in
         - row: The row the node is in
        """
        self.row = row
        self.col = col

        self.north = None
        self.south = None
        self.east = None
        self.west = None

        self.occupied = False
        self.hit = False
        self.sign = EMPTY
        self.color = f'{DEFAULT}'
        self.vessel = None

    def __copy__(self) -> Node:
        """Returns a complete copy of a Node"""
        ret = Node(self.col, self.row)

        ret.occupied = self.occupied
        ret.hit = self.hit
        ret.sign = self.sign
        ret.color = self.color
        ret.vessel = self.vessel

        return ret

    def __str__(self) -> str:
        return f'({self.col}, {self.row})'

    def __repr__(self) -> str:
        return f'{self.color}{self.sign}{DEFAULT}'

    # Grid setup ---------------------------------------------------------------
    def occupy(self, vessel: TraditionalVessel, sign: str) -> None:
        """
        Changes attributes when vessel occupies the node.

        Parameter(s):
         - vc: The vessel's class abbreviation
         - v_id: The vessel's pennant number
         - sign: The sign that is being displayed at the node
        """
        self.occupied = True
        self.vessel = vessel
        self.sign = f'{sign}'
        self.color = f'{GREEN}'

    def vacant(self) -> None:
        """
        Resets the attributes for a node.

        Parameter(s):
         - sign: The default sign to use
        """
        self.occupied = False
        self.vessel = None
        self.sign = EMPTY
        self.color = f'{DEFAULT}'

    # Planning -----------------------------------------------------------------
    def target_and_drop(self) -> None:
        """
        Changes attributes when vessel is targeting the node and also represents
        where the armament will "drop" into the water. Applies to only radar and
        sonar grids (or the traditional grid).
        """
        self.sign = f'{DROP}'
        self.color = f'{PURPLE}'

    def not_target_and_drop(self, ) -> None:
        """
        Reverses changes caused by method target_and_drop().
        """
        self.sign = f'{EMPTY}'
        self.color = f'{DEFAULT}'

    # After shooting -----------------------------------------------------------
    def miss(self) -> None:
        """Changes sign to miss for all grids."""
        self.sign = f'{MISS}'
        self.color = f'{BLUE}'
        self.hit = True

    def damaged(self) -> None:
        """Changes sign to damaged on radar / sonar grids."""
        self.sign = f'{HIT}'
        self.color = f'{YELLOW}'
        self.hit = True

    def personal_damaged(self) -> None:
        """Changes sign to damaged on personal grids."""
        self.sign = f'{self.sign}'
        self.color = f'{YELLOW}'
        self.hit = True

    def destroyed(self) -> None:
        """Changes sign to destroyed on radar / sonar grids."""
        self.sign = f'{HIT}'
        self.color = f'{RED}'
        self.hit = True

    def personal_destroyed(self) -> None:
        """Changes sign to destroyed on personal grids."""
        self.sign = f'{self.sign}'
        self.color = f'{RED}'
        self.hit = True
