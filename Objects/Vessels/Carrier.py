"""
Carrier.py

PURPOSE:
Creates the Aircraft Carrier class that is usable by players.
"""
from __future__ import annotations
from Objects.Vessels.Vessel import TraditionalVessel


# Due to circular import, cannot import form Settings.py
GREEN = '\033[32m'       # Green
YELLOW = '\033[33m'      # Yellow
RED = '\033[31m'         # Red


class TraditionalCarrier(TraditionalVessel):
    """The Aircraft Carrier vessel class used for Traditional Battleship."""

    def __init__(self, nation: str, name: str, pennant: int) -> None:
        """
        Initializes a new Aircraft Carrier.

        Parameter(s):
         - nation: The affiliated nation
         - name: The name of the vessel
         - pennant: The id number of the vessel
        """
        super().__init__(nation, name, pennant)
        self.type = 'Aircraft Carrier'
        self.abbrev = 'CV'
        self.symbol = 'V'

        self.hp = 6
        self.hits_received = 0
        self.health_color = f'{GREEN}'
        self.enemy_hp_color = f'{RED}'

    def __copy__(self) -> TraditionalCarrier:
        ret = TraditionalCarrier(self.nation, self.name, self.pennant)
        ret.hp = self.hp
        ret.hits_received = self.hits_received
        ret.health_color = self.health_color
        ret.enemy_hp_color = self.enemy_hp_color
        ret.sunk = self.sunk

        ret.bow = self.bow
        ret.hit = self.hit

        return ret

    def update_health_color(self) -> None:
        if self.hp == 6:
            return
        elif self.hp > 1:
            self.health_color = f'{YELLOW}'
            self.enemy_hp_color = f'{YELLOW}'
        else:
            self.health_color = f'{RED}'
            self.enemy_hp_color = f'{GREEN}'
