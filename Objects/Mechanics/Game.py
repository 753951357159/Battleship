"""
Mechanics.py

PURPOSE:
Creates and hosts a game of Battleship.
"""
from __future__ import annotations
from typing import List, Tuple, Optional
from Objects.Vessels.Vessel import TraditionalVessel
from Objects.Mechanics.ActivityLog import TraditionalLog
from Objects.Mechanics.Order import TraditionalOrder
from Objects.Mechanics.Player import Player


class BattleshipGame:
    """
    Consists of 2 players and their respective grids. Keeps track of whose turn
    it currently is and statistics about the game / players. Announces the
    winner when the game is over.

    Attribute(s):
     - player1: The first user
     - player2: The second user / CPU
     - current_player: The player who is currently having their turn
     - current_turn_number: The current turn number

     - player1_backup: A copy of player1 before major changes occur
     - player2_backup: A copy of player2 before major changes occur

     - battles: The number of battles that need to be played
     - current_battle: The current battle number that is being played

     - nations_joined: List of currently joined nations in this game
     - log: The Activity Log with all important information for each player
     - current_orders: List of orders the current player is planning
    """
    player1: Player
    player2: Player
    current_player: Player
    current_turn_number: int

    player1_backup: Player
    player2_backup: Player

    battles: int
    current_battle: int

    log: TraditionalLog
    current_orders: List[TraditionalOrder]

    def __init__(self, p1: Player, p2: Player, battles: int) -> None:
        """Initializes a new game of Battleship."""
        self.player1 = p1
        self.player2 = p2
        self.current_player = self.player1
        self.current_turn_number = 1

        self.player1_backup = self.player1.__copy__()
        self.player2_backup = self.player2.__copy__()

        self.battles = battles
        self.current_battle = 1

        self.log = TraditionalLog()
        self.current_orders = []

    # Player related methods
    def reset_p1(self) -> None:
        """Resets Player 1 by making it a copy of Player 1's backup."""
        self.player1 = self.player1_backup.__copy__()

    def reset_p2(self) -> None:
        """Resets Player 2 by making it a copy of Player 2's backup."""
        self.player2 = self.player2_backup.__copy__()

    def update_p1_backup(self) -> None:
        """Brings Player 1's backup up-to-date."""
        self.player1_backup = self.player1.__copy__()

    def update_p2_backup(self) -> None:
        """Brings Player 2's backup up-to-date."""
        self.player2_backup = self.player2.__copy__()

    def check_winner(self) -> Tuple[bool, Optional[Player]]:
        """Checks to see if a winner is found."""
        if self.player1.forfeit:
            return True, self.player2
        elif self.player2.forfeit:
            return True, self.player1
        elif self.player1.battle_total == 0:
            return True, self.player2
        elif self.player2.battle_total == 0:
            return True, self.player1
        return False, None

    def other_player(self) -> Player:
        """Returns the player that is not having their current turn."""
        if self.current_player == self.player1:
            return self.player2
        elif self.current_player == self.player2:
            return self.player1

    def enemy_sunk(self, vessel: TraditionalVessel, player: Player) -> None:
        """
        Updates all player, vessel, grid, and node attributes to reflect the
        changes taking place.

        Parameter(s):
         - vessel: The vessel that has been sunk
         - player: The player (enemy) who owns that vessel
        """
        # Change vessel attributes
        vessel.hp = 0
        vessel.sunk = True
        vessel.update_health_color()

        # Change player attributes
        ves_dict = {'BB': player.bb_curr, 'CC': player.cc_curr,
                    'DD': player.dd_curr, 'FF': player.ff_curr,
                    'SM': player.sm_curr, 'CV': player.cv_curr}
        index_dict = {'BB': 0, 'CC': 1, 'DD': 2, 'FF': 3, 'SM': 4, 'CV': 5}

        index = index_dict[vessel.abbrev]
        vessel_lst = ves_dict[vessel.abbrev]

        for i, ves in enumerate(vessel_lst):
            if ves.pennant == vessel.pennant:
                player.battle_sunk[index].append(vessel_lst.pop(i))
                player.battle_total -= 1
                player.battle_id[index].remove(ves.pennant)

                # Update Activity Logs
                self.log.ally_sunk(vessel, self.other_player().number,
                                   self.current_turn_number)
                self.log.enemy_sunk(vessel, self.current_player.number,
                                    self.current_turn_number)

        # Change grid / node attributes
        player.personal.ally_sunk(vessel)
        self.current_player.traditional.enemy_sunk(vessel)
