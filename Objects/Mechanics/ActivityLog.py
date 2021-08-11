"""
ActivityLog.py

PURPOSE:
Creates the Activity Log object which stores what happens at what time for each
player.
"""
from __future__ import annotations
from typing import List
from Settings import RED, PURPLE, GREEN, DEFAULT
from Objects.Mechanics.Node import Node
from Objects.Vessels.Vessel import TraditionalVessel


class Log:
    """
    The general Activity Log class. Stores all information that happens
    in a battle.

    Attribute(s):
     - log1: Player 1's log
     - log2: Player 2's log
    """
    log1: List[str]
    log2: List[str]

    def __init__(self) -> None:
        """Initializes a new Activity Log."""
        self.log1 = []
        self.log2 = []

    def __copy__(self) -> Log:
        """Returns a complete copy of the Activity Log."""
        ret = Log()
        ret.log1 = self.log1.copy()
        ret.log2 = self.log2.copy()

        return ret

    # Display options ----------------------------------------------------------
    def full_log(self, player_num: int) -> List[str]:
        """
        Returns all the events that have occurred in the Activity Log for the
        specified player.

        Parameter(s):
         - player_num: The log's owner, represented by their player number
        """
        if player_num == 1:
            log_lst = self.log1
        else:
            log_lst = self.log2

        lst_1 = log_lst[:64:]
        lst_2 = log_lst[64:128:]
        lst_3 = log_lst[128:192:]
        lst_4 = log_lst[192:256:]

        title = f'{PURPLE}FULL ACTIVITY LOG{DEFAULT}'
        ret = [f'{title:^318}', '']  # 310 char + 4/color change * 2

        for i in range(64):
            temp = ''
            try:
                temp += f'{lst_1[i]:<84}  '  # 76 char + 4/color change * 2
            except IndexError:
                pass
            try:
                temp += f'{lst_2[i]:<84}  '
            except IndexError:
                pass
            try:
                temp += f'{lst_3[i]:<84}  '
            except IndexError:
                pass
            try:
                temp += f'{lst_4[i]:<84}'
            except IndexError:
                pass

            ret.append(temp)
            ret.append('')
        return ret

    def partial_log(self, player_num: int) -> List[str]:
        """
        Returns the most recent events within the Activity Log.

        Parameter(s):
         - player_num: The log's owner, represented by their player number
        """
        if player_num == 1:
            return self.log1[-64::]
        return self.log2[-64::]


class TraditionalLog(Log):
    """The Activity Log for Traditional Battleship."""

    # Possible Messages --------------------------------------------------------
    def ally_sunk(self, vessel: TraditionalVessel,
                  player_num: int, turn_num: int) -> None:
        """
        Creates a message to be added to the activity log stating that an allied
        vessel has been sunk.

        Parameter(s):
         - vessel: The vessel that the message adheres to
         - player_num: The log's owner, represented by their player number
         - turn_num: The current turn number
        """
        temp = f'Turn {turn_num:03d}|{RED}Allied{DEFAULT} {vessel.type} ' \
               f'{vessel.pennant:02d} has been sunk!'

        if player_num == 1:
            self.log1.append(temp)
        else:
            self.log2.append(temp)

    def enemy_sunk(self, vessel: TraditionalVessel,
                   player_num: int, turn_num: int) -> None:
        """
        Creates a message to be added to the activity log stating that an enemy
        vessel has been sunk.

        Parameter(s):
         - vessel: The vessel that the message adheres to
         - player_num: The log's owner, represented by their player number
         - turn_num: The current turn number
         """
        temp = f'Turn {turn_num:03d}|{GREEN}Enemy{DEFAULT} {vessel.type} ' \
               f'{vessel.pennant:02d} has been sunk!'

        if player_num == 1:
            self.log1.append(temp)
        else:
            self.log2.append(temp)

    def ally_hit(self, vessel: TraditionalVessel, player: int,
                 node: Node, turn_num: int) -> None:
        """
        Creates a message to be added to the activity log stating that an allied
        vessel has been hit.

        Parameter(s):
         - vessel: The vessel that the message adheres to
         - player: The player assigned number
         - node: The section of the vessel damaged
         - turn_num: The current turn number
        """
        temp = f'Turn {turn_num:03d}|{RED}Allied{DEFAULT} {vessel.type} ' \
               f'{vessel.pennant:02d} has been damaged at {node!s}!'

        if player == 1:
            self.log1.append(temp)
        else:
            self.log2.append(temp)

    def enemy_hit(self, vessel: TraditionalVessel, player: int,
                  node: Node, turn_num: int) -> None:
        """
        Creates a message to be added to the activity log stating that an enemy
        vessel has been hit.

        Parameter(s):
         - vessel: The vessel that the message adheres to
         - player: The player assigned number
         - node: The section of the vessel damaged
         - turn_num: The current turn number
        """
        temp = f'Turn {turn_num:03d}|{GREEN}Enemy{DEFAULT} vessel ' \
               f'has been damaged at {node!s}!'

        if player == 1:
            self.log1.append(temp)
        else:
            self.log2.append(temp)
