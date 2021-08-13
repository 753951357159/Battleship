"""
Grid.py

PURPOSE:
Creates the Grid and stores all relevant game information within each node.
"""
from __future__ import annotations
from typing import List, Tuple
from Settings import ROW_ICON, COL_ICON, ROW_SEP, CORNER, COL_SPACER, COL_SEP, \
    BOW, STERN
from Objects.Mechanics.Node import Node
from Objects.Vessels.Vessel import TraditionalVessel


class Grid:
    """
    A grid that players will place vessels on and play with.

    Attribute(s):
     - grid: A list of nodes that form the grid
     - size: The side length of the grid (all grids are square)
    """
    grid: List[List[Node]]
    size: int

    def __init__(self, size: int = 36) -> None:
        """
        Initiates a new Grid object.

        Parameter(s):
        - size: The side length of the grid.

        Precondition(s):
         - size <= 36
        """
        self.grid = []
        self.size = size

        self._create_node()
        self._link_nodes()

    def __copy__(self) -> Grid:
        ret = Grid()
        for i in range(len(ret.grid)):
            for j in range(len(ret.grid)):
                ret.grid[i][j] = self.grid[i][j].__copy__()
        ret._link_nodes()

        return ret

    def __repr__(self) -> str:
        """Used for printing the personal grid."""
        ret = ''
        row = ROW_ICON[36 - self.size::]
        col = COL_ICON[:self.size]

        # Get each row's representation
        for i in range(len(row)):
            temp_row = f'{row[i]} {ROW_SEP} '
            for j in range(len(col)):
                temp_row += f'{repr(self.grid[i][j])} '
            ret += temp_row.rstrip() + f'\n'

        # Create column header and return
        ret += f'  {CORNER}' + f'{COL_SPACER}{COL_SEP}' * self.size

        col_header = f'\n    '
        for i in range(self.size):
            col_header += f'{COL_ICON[i]} '
        ret += col_header.rstrip() + f'\n'

        return ret

    # Helper functions for __init__
    def _create_node(self) -> None:
        """Creates the nodes and basic grid structure."""
        # Get appropriate row and columns
        row = ROW_ICON[36 - self.size::]
        col = COL_ICON[:self.size]

        # Create List[List[Node]]
        for i in range(len(row)):
            temp_row = []
            for j in range(len(col)):
                temp_node = Node(col[j], row[i])
                temp_row.append(temp_node)
            self.grid.append(temp_row)

    def _link_nodes(self) -> None:
        """Links all nodes within the grid together."""
        for index1, row in enumerate(self.grid):
            for index2, node in enumerate(row):
                # North
                try:
                    north_index = index1 - 1
                    if north_index < 0:
                        raise IndexError
                    node.north = self.grid[north_index][index2]
                except IndexError:
                    node.north = None

                # South
                try:
                    south_index = index1 + 1
                    if south_index >= self.size:
                        raise IndexError
                    node.south = self.grid[south_index][index2]
                except IndexError:
                    node.south = None

                # East
                try:
                    east_index = index2 + 1
                    if east_index >= self.size:
                        raise IndexError
                    node.east = self.grid[index1][east_index]
                except IndexError:
                    node.east = None

                # West
                try:
                    west_index = index2 - 1
                    if west_index < 0:
                        raise IndexError
                    node.west = self.grid[index1][west_index]
                except IndexError:
                    node.west = None

    # Player placement (grid setup) --------------------------------------------
    def add_vessel(self, vessel: TraditionalVessel, coordinate: Tuple[str, str],
                   direction: str) -> None:
        """
        Places a vessel on the grid in the specified direction at the specified
        node.

        Parameter(s):
         - vessel: The vessel that is being placed on the grid
         - coordinate: The col and row
         - direction: The direction the bow of the vessel is facing
         - player_num: The assigned player number
        """
        mid = vessel.symbol
        col = COL_ICON.index(coordinate[0])
        row = ROW_ICON.index(coordinate[1])
        leftover = vessel.hp - 1

        node = self.grid[row][col]
        node.occupy(vessel, BOW[direction])

        if direction == 'N':
            while leftover > 1:
                node = node.south
                node.occupy(vessel, mid)
                leftover -= 1
            node.south.occupy(vessel, STERN[direction])
        elif direction == 'S':
            while leftover > 1:
                node = node.north
                node.occupy(vessel, mid)
                leftover -= 1
            node.north.occupy(vessel, STERN[direction])
        elif direction == 'E':
            while leftover > 1:
                node = node.west
                node.occupy(vessel, mid)
                leftover -= 1
            node.west.occupy(vessel, STERN[direction])
        else:
            while leftover > 1:
                node = node.east
                node.occupy(vessel, mid)
                leftover -= 1
                node.east.occupy(vessel, STERN[direction])

    def remove_vessel(self, vessel: TraditionalVessel) -> None:
        """
        Removes a vessel from the grid.

        Parameter(s):
         - vessel: The vessel that is being removed from the grid
        """
        col = COL_ICON.index(vessel.bow[0][0])
        row = ROW_ICON.index(vessel.bow[0][1])

        leftover = vessel.hp - 1
        direction = vessel.bow[1]

        node = self.grid[row][col]
        node.vacant()

        if direction == 'N':
            while leftover > 1:
                node = node.south
                node.vacant()
                leftover -= 1
            node.south.vacant()
        elif direction == 'S':
            while leftover > 1:
                node = node.north
                node.vacant()
                leftover -= 1
            node.north.vacant()
        elif direction == 'E':
            while leftover > 1:
                node = node.west
                node.vacant()
                leftover -= 1
            node.west.vacant()
        else:
            while leftover > 1:
                node = node.east
                node.vacant()
                leftover -= 1
            node.east.vacant()

    def ally_sunk(self, vessel: TraditionalVessel) -> None:
        """
        Converts the signs of the nodes where the sunk vessel is to destroyed on
        personal grids.

        Parameter(s):
         - vessel: The vessel that has been destroyed
        """
        hp_dict = {'BB': 6, 'CC': 5, 'DD': 4, 'FF': 3, 'SM': 4, 'CV': 5}
        row = ROW_ICON.index(vessel.bow[0][1])
        col = COL_ICON.index(vessel.bow[0][0])
        leftover = hp_dict[vessel.abbrev] - 1
        direction = vessel.bow[1]

        node = self.grid[row][col]
        node.personal_destroyed()

        if direction == 'N':
            while leftover > 1:
                node = node.south
                node.personal_destroyed()
                leftover -= 1
            node.south.personal_destroyed()
        elif direction == 'S':
            while leftover > 1:
                node = node.north
                node.personal_destroyed()
                leftover -= 1
            node.north.personal_destroyed()
        elif direction == 'E':
            while leftover > 1:
                node = node.west
                node.personal_destroyed()
                leftover -= 1
            node.west.personal_destroyed()
        else:
            while leftover > 1:
                node = node.east
                node.personal_destroyed()
                leftover -= 1
            node.east.personal_destroyed()

    def enemy_sunk(self, vessel: TraditionalVessel) -> None:
        """
        Converts the signs of the nodes where the sunk vessel is to destroyed on
        radar / sonar (or traditional) grids.

        Parameter(s):
         - vessel: The vessel that has been destroyed
        """
        hp_dict = {'BB': 6, 'CC': 5, 'DD': 4, 'FF': 3, 'SM': 4, 'CV': 5}
        row = ROW_ICON.index(vessel.bow[0][1])
        col = COL_ICON.index(vessel.bow[0][0])
        leftover = hp_dict[vessel.abbrev] - 1
        direction = vessel.bow[1]

        node = self.grid[row][col]
        node.destroyed()

        if direction == 'N':
            while leftover > 1:
                node = node.south
                node.destroyed()
                leftover -= 1
            node.south.destroyed()
        elif direction == 'S':
            while leftover > 1:
                node = node.north
                node.destroyed()
                leftover -= 1
            node.north.destroyed()
        elif direction == 'E':
            while leftover > 1:
                node = node.west
                node.destroyed()
                leftover -= 1
            node.west.destroyed()
        else:
            while leftover > 1:
                node = node.east
                node.destroyed()
                leftover -= 1
            node.east.destroyed()
