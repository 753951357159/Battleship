"""
Player.py

PURPOSE:
Creates the Players that participate in a game of Battleship.
"""
from __future__ import annotations
from typing import Tuple, List
from random import randint
from pathlib import Path
from Settings import NATIONS, PENNANTS, FILE_NAMES
from Objects.Mechanics.Grid import Grid
from Objects.Vessels.Vessel import TraditionalVessel
from Objects.Vessels.Battleship import TraditionalBattleship
from Objects.Vessels.Cruiser import TraditionalCruiser
from Objects.Vessels.Destroyer import TraditionalDestroyer
from Objects.Vessels.Frigate import TraditionalFrigate
from Objects.Vessels.Submarine import TraditionalSubmarine


class Player:
    """
    Represents a player participating in a game of Battleship.

    Attribute(s):
     - name: The name of the player
     - nation: The chosen nationality of the player and the respective sign
     - number: The player number; 0 is CPU, 1 is Player1, 2 is Player2
     - forfeit: Whether the player forfeits or not

     - fleet: List of all vessels the player currently owns in port
     - total: The total number of vessels the player owns in port
     - all_id: List of all vessel pennant numbers in port

     - battle_total: The total number of vessels currently in the battle
     - battle_id: List of vessel pennant numbers in the current battle
     - bb_curr: List of Battleships being used in the current battle
     - cc_curr: List of Carriers being used in the current battle
     - dd_curr: List of Destroyers being used in the current battle
     - ff_curr: List of Frigates being used in the current battle
     - sm_curr: List of Submarines being used in the current battle
     - cv_curr: List of Aircraft Carriers being used in the current battle
     - battle_sunk: List of all vessels that were sunk in the current battle

     - personal: The Grid that displays all the positions of your own fleet
     - traditional: The Grid used for the Traditional game mode
    """
    name: str
    nation: Tuple[str, str]  # name, sign
    number: int
    forfeit: bool

    fleet: List[List[TraditionalVessel]]
    total: int
    all_id: List[List[int]]

    battle_total: int
    battle_id: List[List[int]]
    bb_curr: List[TraditionalVessel]
    cc_curr: List[TraditionalVessel]
    dd_curr: List[TraditionalVessel]
    ff_curr: List[TraditionalVessel]
    sm_curr: List[TraditionalVessel]
    cv_curr: List[TraditionalVessel]
    battle_sunk: List[List[TraditionalVessel]]

    personal: Grid
    traditional: Grid

    def __init__(self, name: str, nation: str, number: int) -> None:
        """Initializes a new Player."""
        self.name = f'{NATIONS[nation][1]} {name}'
        self.nation = (nation, NATIONS[nation][0])
        self.number = number
        self.forfeit = False

        self.fleet = [[], [], [], [], [], []]
        self.total = 0
        self.all_id = [[], [], [], [], [], []]

        self.battle_total = 0
        self.battle_id = [[], [], [], [], [], []]
        self.bb_curr = []
        self.cc_curr = []
        self.dd_curr = []
        self.ff_curr = []
        self.sm_curr = []
        self.cv_curr = []
        self.battle_sunk = [[], [], [], [], [], []]

        self.personal = Grid()
        self.traditional = Grid()

    def __copy__(self) -> Player:
        """Returns a complete copy of the player."""
        new_name = self.name.split(' ')

        ret = Player(new_name[1].strip(), self.nation[0], self.number)

        for i in range(len(ret.fleet)):
            ret.fleet[i] = [vessel_class.__copy__() for
                            vessel_class in self.fleet[i]]
        ret.total = self.total
        ret.all_id = [pennant_lst.copy() for pennant_lst in self.all_id]

        ret.battle_total = self.battle_total
        ret.battle_id = [pennant_lst.copy() for pennant_lst in self.battle_id]
        ret.bb_curr = [vessel.__copy__() for vessel in self.bb_curr]
        ret.cc_curr = [vessel.__copy__() for vessel in self.cc_curr]
        ret.dd_curr = [vessel.__copy__() for vessel in self.dd_curr]
        ret.ff_curr = [vessel.__copy__() for vessel in self.ff_curr]
        ret.sm_curr = [vessel.__copy__() for vessel in self.sm_curr]
        ret.cv_curr = [vessel.__copy__() for vessel in self.cv_curr]
        for i in range(len(ret.battle_sunk)):
            ret.battle_sunk[i] = [vessel_class.__copy__() for
                                  vessel_class in self.battle_sunk[i]]

        ret.personal = self.personal.__copy__()
        ret.traditional = self.traditional.__copy__()

        return ret

    def add_vessel(self, vessel_type: type) -> None:
        """
        Creates and adds a vessel to the player's fleet.

        Parameter(s):
         - vessel_type: The vessel class that is to be created
        """
        # Helper function
        def select_id() -> int:
            """Returns correct index for all_id based on vessel class."""
            if vessel_type is TraditionalBattleship:
                return 0
            elif vessel_type is TraditionalCruiser:
                return 1
            elif vessel_type is TraditionalDestroyer:
                return 2
            elif vessel_type is TraditionalFrigate:
                return 3
            elif vessel_type is TraditionalSubmarine:
                return 4
            return 5

        def read_line(filepath: str, line: int) -> str:
            """
            Reads the specified line of a file.

            Parameter(s):
             - filepath: The specified file path
             - line: The line number to read
            """
            with open(filepath, 'r') as f:
                for i, text_line in enumerate(f):
                    if i + 1 == line:
                        return text_line

        # ----------------------------------------------------------------------
        # Check that name is not already being used
        max_pennants = PENNANTS[self.nation[0]][vessel_type]
        index = select_id()

        line_num = randint(1, max_pennants)
        while line_num in self.all_id[index]:
            line_num = randint(1, max_pennants)

        file_path = str(Path().absolute()) + f'/Nations/{self.nation[0]}/' \
                                             f'{FILE_NAMES[vessel_type]}.txt'
        vessel_name = read_line(file_path, line_num).strip()

        # Update player attributes
        self.fleet[index].append(
            vessel_type(self.nation[0], vessel_name, line_num))
        self.all_id[index].append(line_num)
        self.total += 1

    def place_vessel(self, vessel_type: str, pennant: int,
                     coordinate: Tuple[str, str], direction: str) -> None:
        """
        Places a vessel on the personal grid and modifies attributes to
        reflect changes taken place.

        Parameter(s):
         - vessel_type: The class of the vessel
         - pennant: The id number of the vessel
         - direction: The direction the vessel faces
         - coordinate: The coordinate the bow of the vessel is located
        """
        id_dict = {'BB': 0, 'CC': 1, 'DD': 2, 'FF': 3, 'SM': 4, 'CV': 5}
        fleet_dict = {'BB': self.bb_curr, 'CC': self.cc_curr,
                      'DD': self.dd_curr, 'FF': self.ff_curr,
                      'SM': self.sm_curr, 'CV': self.cv_curr}

        for i, vessel in enumerate(self.fleet[id_dict[vessel_type]]):
            if vessel.pennant == pennant:
                self.personal.add_vessel(vessel, coordinate, direction)

                vessel.bow = (coordinate, direction)
                fleet_dict[vessel_type].append(
                    self.fleet[id_dict[vessel_type]].pop(i))
                self.battle_id[id_dict[vessel_type]].append(pennant)
                self.battle_total += 1

    def remove_vessel(self, vessel_type: str, pennant: int) -> None:
        """
        Removes a vessel from the personal grid and modifies attributes to
        reflect changes taken place.

        Parameter(s):
        - vessel_type: The class of the vessel
        - pennant: The id number of the vessel
        """
        id_dict = {'BB': 0, 'CC': 1, 'DD': 2, 'FF': 3, 'SM': 4, 'CV': 5}
        fleet_dict = {'BB': self.bb_curr, 'CC': self.cc_curr,
                      'DD': self.dd_curr, 'FF': self.ff_curr,
                      'SM': self.sm_curr, 'CV': self.cv_curr}

        for i, vessel in enumerate(fleet_dict[vessel_type]):
            if vessel.pennant == pennant:
                self.personal.remove_vessel(vessel)

                popped = fleet_dict[vessel_type].pop(i)
                self.fleet[id_dict[vessel_type]].append(popped)
                self.battle_id[id_dict[vessel_type]].remove(pennant)
                self.battle_total -= 1
                vessel.bow = None
