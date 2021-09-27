"""
General.py

PURPOSE:
To recycle code. This file contains methods that are used in all modes
(or majority of them).
"""
from typing import Tuple, List, Optional
from Settings import DEFAULT, PURPLE, RED, GREEN, BLUE, \
    AFFIRMATIVE, NEGATIVE, NATIONS, \
    ROW_ICON, ROW_SEP, COL_ICON, COL_SEP, COL_SPACER, CORNER, \
    EMPTY_FRAME, MDW
from Objects.Mechanics.Game import BattleshipGame
from Objects.Mechanics.Player import Player
from Objects.Mechanics.Grid import Grid


# Setup ------------------------------------------------------------------------
def _setup_player() -> Tuple[Player, Player]:
    """Creates Player 1 and Player 2 basic information."""
    # Helper function(s):
    def _basic_info(number: int) -> Tuple[str, str]:
        """
        Sets up the basic information for a player.

        Parameter(s):
         - number: The player number
        """
        basic_check = False
        while not basic_check:
            name = input(
                f'{PURPLE} >>> Player {number}{DEFAULT} name: ').strip()
            nation = input(f'{PURPLE} >>> Player {number}{DEFAULT} '
                           f'nationality: ').strip().upper()

            # Check if nation is valid
            while (nation in nations_joined) or \
                    (nation not in list(NATIONS.keys())):
                # Get list of valid nations
                valid = list(NATIONS.keys())
                for nation in nations_joined:
                    valid.remove(nation)

                nation = input(f'{PURPLE} >>> {RED}Invalid Nation{DEFAULT} - '
                               f'Select from {valid}: ').strip().upper()

            # Confirm with user that this is what they want
            print(f'\nPLAYER {number} INFORMATION: ')
            print(f'\tName: {name}')
            print(f'\tNationality: {nation}')
            confirm = input(
                f'{PURPLE} >>> Player {number}{DEFAULT}, confirm '
                f'the above is correct (Y/N): ').strip()

            # Check user response is valid
            while confirm not in AFFIRMATIVE and \
                    confirm not in NEGATIVE:
                confirm = input(f'{PURPLE} >>> {RED}'
                                f'Invalid Option{DEFAULT} (Y/N): ')
            if confirm in AFFIRMATIVE:
                return name, nation
            print('')

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    nations_joined = []

    # Create basic Player 1 profile
    p1_name, p1_nation = _basic_info(1)
    p1 = Player(p1_name, p1_nation, 1)
    nations_joined.append(p1_nation)
    print(f'{GREEN}Welcome,{DEFAULT} {p1.name}!\n')

    # Create basic Player 2 profile
    p2_name, p2_nation = _basic_info(2)
    p2 = Player(p2_name, p2_nation, 2)
    nations_joined.append(p2_nation)
    print(f'{GREEN}Welcome,{DEFAULT} {p2.name}!\n')

    return p1, p2


def _setup_grid(player: Player) -> bool:
    """
    Sets up the grid for the specified player.

    Parameter(s):
     - player: The player that the grid is currently being setup for
    """
    # Helper function(s):
    def _add_vessel_list() -> List[str]:
        """Creates a list of all vessel that can be added to the grid.."""
        ret = [f'{BLUE}Currently In Port{DEFAULT}']
        for index in range(6):
            for i in range(len(player.fleet[index])):
                vessel = f'[{player.fleet[index][i].abbrev} ' \
                         f'{player.fleet[index][i].pennant:02d}]    ' \
                         f'{player.fleet[index][i].name}'
                ret.append(vessel)
        return ret

    def _remove_vessel_list() -> List[str]:
        """Creates a list of all vessels removable from grid."""
        ret = [f'{BLUE}Currently On Grid{DEFAULT}']
        possible = [vessel.__copy__() for vessel in player.bb_curr]
        possible.extend([vessel.__copy__() for vessel in player.cc_curr])
        possible.extend([vessel.__copy__() for vessel in player.dd_curr])
        possible.extend([vessel.__copy__() for vessel in player.ff_curr])
        possible.extend([vessel.__copy__() for vessel in player.sm_curr])
        possible.extend([vessel.__copy__() for vessel in player.cv_curr])

        for i in range(len(possible)):
            vessel = f'({possible[i].bow[0][0]}, {possible[i].bow[0][1]})' \
                     f'    [{possible[i].abbrev} ' \
                     f'{possible[i].pennant:02d}]    ' \
                     f'{possible[i].name}'
            ret.append(vessel)
        return ret

    def _check_response(phrase: str) -> Tuple[bool, int, Optional[list]]:
        """
        Checks if the response given by the user is valid.
         - Must have 6 inputs or is equal to a specific command
         - All inputs must match specific criteria

        Valid format:
        <command>, <class>, <pennant #>, <col>, <row>, <direction>

        Parameter(s):
         - phrase: The response being checked
        """
        rem_dict = {'BB': player.bb_curr, 'CC': player.cc_curr,
                    'DD': player.dd_curr, 'FF': player.ff_curr,
                    'SM': player.sm_curr, 'CV': player.cv_curr}
        add_dict = {'BB': 0, 'CC': 1, 'DD': 2, 'FF': 3, 'SM': 4, 'CV': 5}

        # Check if response is the command \complete
        if phrase.lower().strip() == '\\complete':
            return True, -1, None
        elif ',' not in phrase:
            return False, 1, None  # Invalid format

        lst = phrase.split(',')
        lst[0] = str(lst[0]).strip().lower()

        # If player attempting to add vessel to grid
        if len(lst) == 6:
            for i in range(5):
                lst[i + 1] = str(lst[i + 1]).strip().upper()

            if lst[0] != '\\add':
                return False, 2, None  # Invalid command
            elif lst[1] not in ['BB', 'CC', 'DD', 'FF', 'SM', 'CV']:
                return False, 3, None  # Invalid class
            elif int(float(lst[2])) not in player.all_id[add_dict[lst[1]]]:
                return False, 4, None  # Invalid vessel
            elif (lst[3] not in COL_ICON) or (lst[4] not in ROW_ICON):
                return False, 5, None  # Invalid coordinate
            elif lst[5] not in ['N', 'S', 'E', 'W']:
                return False, 6, None  # Invalid direction

            # Phrase is valid; check if vessel can be placed on grid
            for i, vessel in enumerate(player.fleet[add_dict[lst[1]]]):
                if vessel.pennant == int(lst[2]):
                    if not _check_placement(vessel.hp, lst[5],
                                            (lst[3], lst[4])):
                        return False, 7, None  # Invalid node
                    return True, -2, lst  # Player is adding vessel
            return False, 4, None  # Invalid vessel

        # If player attempting to remove vessel from grid
        elif len(lst) == 3:
            for i in range(2):
                lst[i + 1] = str(lst[i + 1]).strip().upper()

            if lst[0] != '\\remove':
                return False, 2, None  # Invalid command
            elif lst[1] not in ['BB', 'CC', 'DD', 'FF', 'SM', 'CV']:
                return False, 3, None  # Invalid class
            elif int(lst[2]) not in player.all_id[add_dict[lst[1]]]:
                return False, 4, None  # Invalid vessel

            # Phrase is valid; check for pennant number
            for i, vessel in enumerate(rem_dict[lst[1]]):
                if vessel.pennant == int(lst[2]):
                    return True, -3, lst  # player is removing vessel
            return False, 4, None  # Invalid vessel
        else:
            return False, 1, None  # Invalid format

    def _check_placement(hp: int, direction: str,
                         coordinate: Tuple[str, str]) -> bool:
        """
        Checks to see if the coordinate and direction given is valid.

        Parameter(s):
         - hp: The hp of the vessel, equal to number of nodes to check
         - direction: The direction the vessel is facing
         - coordinate: The row and column
        """
        col = COL_ICON.index(coordinate[0])
        row = ROW_ICON.index(coordinate[1])
        curr = player.personal.grid[row][col]

        # Check to see if the bow node is already full or not
        if curr.occupied:
            return False

        nodes = hp - 1

        # Check all other nodes
        if direction == 'N':
            while nodes > 0:
                if curr.south is None:
                    return False
                elif curr.south.occupied:
                    return False
                curr = curr.south
                nodes -= 1
        elif direction == 'S':
            while nodes > 0:
                if curr.north is None:
                    return False
                elif curr.north.occupied:
                    return False
                curr = curr.north
                nodes -= 1
        elif direction == 'E':
            while nodes > 0:
                if curr.west is None:
                    return False
                elif curr.west.occupied:
                    return False
                curr = curr.west
                nodes -= 1
        else:
            while nodes > 0:
                if curr.east is None:
                    return False
                elif curr.east.occupied:
                    return False
                curr = curr.east
                nodes -= 1
        return True

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # Print options and base (empty) grid
    vessel_lst = _add_vessel_list()
    vessel_lst.append(' ')
    vessel_lst.extend(_remove_vessel_list())
    print(EMPTY_FRAME)
    print(parallel_print([player.personal], vessel_lst))

    # Ask use for input
    response = input(f'{PURPLE} >>> Command{DEFAULT}: ')
    check = _check_response(response)
    while not check[0]:
        if check[1] == 1:
            response = input(f'{PURPLE} >>> {RED}Invalid Format{DEFAULT}; '
                             f'{PURPLE}Command{DEFAULT}: ')
        elif check[1] == 2:
            response = input(f'{PURPLE} >>> {RED}Invalid Command{DEFAULT}; '
                             f'{PURPLE}Command{DEFAULT}: ')
        elif check[1] == 3:
            response = input(f'{PURPLE} >>> {RED}Invalid Class{DEFAULT}; '
                             f'{PURPLE}Command{DEFAULT}: ')
        elif check[1] == 4:
            response = input(f'{PURPLE} >>> {RED}Invalid Vessel{DEFAULT}; '
                             f'{PURPLE}Command{DEFAULT}: ')
        elif check[1] == 5:
            response = input(f'{PURPLE} >>> {RED}Invalid Coordinate{DEFAULT}; '
                             f'{PURPLE}Command{DEFAULT}: ')
        elif check[1] == 6:
            response = input(f'{PURPLE} >>> {RED}Invalid Direction{DEFAULT}; '
                             f'{PURPLE}Command{DEFAULT}: ')
        elif check[1] == 7:
            response = input(f'{PURPLE} >>> {RED}Invalid Nodes{DEFAULT}; '
                             f'{PURPLE}Command{DEFAULT} ')
        check = _check_response(response)

    # Response is valid, add vessel to grid
    if check[1] == -2:
        player.place_vessel(check[2][1], int(check[2][2]),
                            (check[2][3], check[2][4]), check[2][5])
        return False

    # Response is valid, remove vessel from grid
    elif check[1] == -3:
        player.remove_vessel(check[2][1], int(check[2][2]))
        return False

    # Response is valid, player requesting to complete planning
    else:
        return True


# Confirmation -----------------------------------------------------------------
def _confirm_grid(player: Player) -> bool:
    """
    Final confirmation from player for placing down vessels on grid.

    Parameter(s):
     - player: Player 1 / Player 2
    """
    print(EMPTY_FRAME)
    print(player.personal)
    print(f'{BLUE}CURRENTLY DEPLOYED VESSELS{DEFAULT}')

    battle_lst = [player.bb_curr, player.cc_curr, player.dd_curr,
                  player.ff_curr, player.sm_curr, player.cv_curr]
    for lst in battle_lst:
        for vessel in lst:
            print(f'{BLUE}[{vessel.abbrev}] {DEFAULT}'
                  f'{vessel.pennant:02d}    {vessel.name:35}  |  '
                  f'({vessel.bow[0][0]}, {vessel.bow[0][1]})  |  '
                  f'{vessel.bow[1]}')

    check = input(f'\n{PURPLE} >>> {player.name}{DEFAULT}, '
                  f'FINAL CONFIRMATION (Y/N): ')
    while check not in AFFIRMATIVE and check not in NEGATIVE:
        check = input(f'{PURPLE} >>> {RED}Invalid Option{DEFAULT} (Y/N): ')
    if check in AFFIRMATIVE:
        return True
    print('')
    return False


# Game modification ------------------------------------------------------------
def remove_order(game: BattleshipGame, order_num: str) -> None:
    """
    Removes the specified order based on the given order number and renumbers
    all the remaining orders.

    Parameter(s):
     - orders: The list of current orders
     - order_num: The id of the order that is to be removed
    """
    order = game.current_orders.pop(int(float(order_num)) - 1)
    index = int(float(order_num)) - 1
    for i in range(index, len(game.current_orders)):
        game.current_orders[i].order_id -= 1

    # Adjust grid node
    coord = order.coordinate
    row = ROW_ICON.index(coord[1])
    col = COL_ICON.index(coord[0])

    node = game.current_player.traditional.grid[row][col]
    node.not_target_and_drop()


# Display ----------------------------------------------------------------------
def press_to_continue() -> None:
    """
    A simple method that prompts the user to 'press enter to continue.'

    Parameter(s):
        - mdw: Represents the Max Display Width for a screen.
    """
    input(f'\n{PURPLE}{"Press ENTER to Continue...":^{MDW}}{DEFAULT}')


def print_log(game: BattleshipGame) -> None:
    """
    Prints the entire Activity Log for the current player in the game.

    Parameter(s):
     - game: The current game taking place
    """
    log = game.log.full_log(game.current_player.number)
    ret = ''
    for i in range(len(log)):
        ret += log[i] + '\n'
    print(ret)
    press_to_continue()


def parallel_print(grids: List[Grid], headers: List[str]) -> str:
    """
    Rearranges multiple grids and other statements so it can be neatly
    printed on the screen.

    Parameter(s):
     - grids: A list of grids that are to be printed
     - headers: A list of text that also needs to be printed alongside grids

    Representation Invariant(s):
     - Every grid must have the same size
     - The list of list of statements has maximum number of text equal to
       length of the grid
    """
    row = ROW_ICON[36 - grids[0].size::]
    col = COL_ICON[:grids[0].size]
    ret = ''

    for i in range(len(row)):
        for grid in grids:
            temp = f'{row[i]} {ROW_SEP} '
            for j in range(len(col)):
                temp += f'{grid.grid[i][j].__repr__()} '
            ret += f'{temp.rstrip()}    '
        ret = ret[:-4:]
        try:
            ret += f'  {headers[i]}\n'
        except IndexError:
            ret += f'\n'

    col_lines = ''
    col_lines += f'  {CORNER}' + f'{COL_SPACER}{COL_SEP}' * grids[0].size
    ret += ((col_lines + f'    ') * len(grids)).rstrip()
    try:
        ret += f'  {headers[36]}\n'
    except IndexError:
        ret += f'\n'

    header = '    '
    for k in range(grids[0].size):
        header += col[k] + ' '
    ret += ((header.rstrip() + '    ') * len(grids)).rstrip()
    ret.rstrip()
    try:
        ret += f'  {headers[37]}\n'
    except IndexError:
        pass
    return ret + '\n'


def congratulate_p1() -> None:
    """
    Prints a congratulatory message for player 1 who won the game.
    """
    battle_is_over = [f'██████╗  █████╗ ████████╗████████╗██╗     ███████╗    '
                      f'██╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ ',
                      f'██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝    '
                      f'██║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗',
                      f'██████╔╝███████║   ██║      ██║   ██║     █████╗      '
                      f'██║███████╗    ██║   ██║██║   ██║█████╗  ██████╔╝',
                      f'██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝      '
                      f'██║╚════██║    ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗',
                      f'██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗    '
                      f'██║███████║    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║',
                      f'╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝    '
                      f'╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝']

    victorious = [f'██████╗ ██╗      █████╗ ██╗   ██╗███████╗██████╗      ██╗ '
                  f'   ██╗███████╗    ██╗   ██╗██╗ ██████╗████████╗ ██████╗ ██'
                  f'████╗ ██╗ ██████╗ ██╗   ██╗███████╗',
                  f'██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗    ███║ '
                  f'   ██║██╔════╝    ██║   ██║██║██╔════╝╚══██╔══╝██╔═══██╗██'
                  f'╔══██╗██║██╔═══██╗██║   ██║██╔════╝',
                  f'██████╔╝██║     ███████║ ╚████╔╝ █████╗  ██████╔╝    ╚██║ '
                  f'   ██║███████╗    ██║   ██║██║██║        ██║   ██║   ██║██'
                  f'████╔╝██║██║   ██║██║   ██║███████╗',
                  f'██╔═══╝ ██║     ██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██╗     ██║ '
                  f'   ██║╚════██║    ╚██╗ ██╔╝██║██║        ██║   ██║   ██║██'
                  f'╔══██╗██║██║   ██║██║   ██║╚════██║',
                  f'██║     ███████╗██║  ██║   ██║   ███████╗██║  ██║     ██║ '
                  f'   ██║███████║     ╚████╔╝ ██║╚██████╗   ██║   ╚██████╔╝██'
                  f'║  ██║██║╚██████╔╝╚██████╔╝███████║',
                  f'╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝     ╚═╝ '
                  f'   ╚═╝╚══════╝      ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═'
                  f'╝  ╚═╝╚═╝ ╚═════╝  ╚═════╝ ╚══════╝']

    congratulations = [f' ██████╗ ██████╗ ███╗   ██╗ ██████╗ ██████╗  █████╗ █'
                       f'███████╗██╗   ██╗██╗      █████╗ ████████╗██╗ ██████╗'
                       f' ███╗   ██╗███████╗██╗',
                       f'██╔════╝██╔═══██╗████╗  ██║██╔════╝ ██╔══██╗██╔══██╗╚'
                       f'══██╔══╝██║   ██║██║     ██╔══██╗╚══██╔══╝██║██╔═══██'
                       f'╗████╗  ██║██╔════╝██║',
                       f'██║     ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝███████║ '
                       f'  ██║   ██║   ██║██║     ███████║   ██║   ██║██║   ██'
                       f'║██╔██╗ ██║███████╗██║',
                       f'██║     ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██╔══██║ '
                       f'  ██║   ██║   ██║██║     ██╔══██║   ██║   ██║██║   ██'
                       f'║██║╚██╗██║╚════██║╚═╝',
                       f'╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║██║  ██║ '
                       f'  ██║   ╚██████╔╝███████╗██║  ██║   ██║   ██║╚██████╔'
                       f'╝██║ ╚████║███████║██╗',
                       f' ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ '
                       f'  ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝'
                       f' ╚═╝  ╚═══╝╚══════╝╚═╝']

    ret = '\n' * 23
    for i in range(len(battle_is_over)):
        ret += f'{battle_is_over[i]:^310}\n'
    ret += '\n'
    for i in range(len(victorious)):
        ret += f'{victorious[i]:^310}\n'
    ret += '\n'
    for i in range(len(congratulations)):
        ret += f'{congratulations[i]:^310}\n'
    ret += '\n' * 24
    print(ret)
    press_to_continue()


def congratulate_p2() -> None:
    """
    Prints a congratulatory message for player 2 who won the game.
    """
    battle_is_over = [f'██████╗  █████╗ ████████╗████████╗██╗     ███████╗    '
                      f'██╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ ',
                      f'██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝    '
                      f'██║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗',
                      f'██████╔╝███████║   ██║      ██║   ██║     █████╗      '
                      f'██║███████╗    ██║   ██║██║   ██║█████╗  ██████╔╝',
                      f'██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝      '
                      f'██║╚════██║    ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗',
                      f'██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗    '
                      f'██║███████║    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║',
                      f'╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝    '
                      f'╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝']

    victorious = [f'██████╗ ██╗      █████╗ ██╗   ██╗███████╗██████╗     █████'
                  f'█╗     ██╗███████╗    ██╗   ██╗██╗ ██████╗████████╗ ██████'
                  f'╗ ██████╗ ██╗ ██████╗ ██╗   ██╗███████╗',
                  f'██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗    ╚════'
                  f'██╗    ██║██╔════╝    ██║   ██║██║██╔════╝╚══██╔══╝██╔═══█'
                  f'█╗██╔══██╗██║██╔═══██╗██║   ██║██╔════╝',
                  f'██████╔╝██║     ███████║ ╚████╔╝ █████╗  ██████╔╝     ████'
                  f'█╔╝    ██║███████╗    ██║   ██║██║██║        ██║   ██║   █'
                  f'█║██████╔╝██║██║   ██║██║   ██║███████╗',
                  f'██╔═══╝ ██║     ██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██╗    ██╔══'
                  f'═╝     ██║╚════██║    ╚██╗ ██╔╝██║██║        ██║   ██║   █'
                  f'█║██╔══██╗██║██║   ██║██║   ██║╚════██║',
                  f'██║     ███████╗██║  ██║   ██║   ███████╗██║  ██║    █████'
                  f'██╗    ██║███████║     ╚████╔╝ ██║╚██████╗   ██║   ╚██████'
                  f'╔╝██║  ██║██║╚██████╔╝╚██████╔╝███████║',
                  f'╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚════'
                  f'══╝    ╚═╝╚══════╝      ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════'
                  f'╝ ╚═╝  ╚═╝╚═╝ ╚═════╝  ╚═════╝ ╚══════╝']

    congratulations = [f' ██████╗ ██████╗ ███╗   ██╗ ██████╗ ██████╗  █████╗ █'
                       f'███████╗██╗   ██╗██╗      █████╗ ████████╗██╗ ██████╗'
                       f' ███╗   ██╗███████╗██╗',
                       f'██╔════╝██╔═══██╗████╗  ██║██╔════╝ ██╔══██╗██╔══██╗╚'
                       f'══██╔══╝██║   ██║██║     ██╔══██╗╚══██╔══╝██║██╔═══██'
                       f'╗████╗  ██║██╔════╝██║',
                       f'██║     ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝███████║ '
                       f'  ██║   ██║   ██║██║     ███████║   ██║   ██║██║   ██'
                       f'║██╔██╗ ██║███████╗██║',
                       f'██║     ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██╔══██║ '
                       f'  ██║   ██║   ██║██║     ██╔══██║   ██║   ██║██║   ██'
                       f'║██║╚██╗██║╚════██║╚═╝',
                       f'╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║██║  ██║ '
                       f'  ██║   ╚██████╔╝███████╗██║  ██║   ██║   ██║╚██████╔'
                       f'╝██║ ╚████║███████║██╗',
                       f' ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ '
                       f'  ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝'
                       f' ╚═╝  ╚═══╝╚══════╝╚═╝']

    ret = '\n' * 23
    for i in range(len(battle_is_over)):
        ret += f'{battle_is_over[i]:^310}\n'
    ret += '\n'
    for i in range(len(victorious)):
        ret += f'{victorious[i]:^310}\n'
    ret += '\n'
    for i in range(len(congratulations)):
        ret += f'{congratulations[i]:^310}\n'
    ret += '\n' * 24
    print(ret)
    press_to_continue()
