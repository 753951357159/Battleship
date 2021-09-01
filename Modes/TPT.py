"""
TPA.py

PURPOSE:
Runs the entire Two Player Arcade game mode.
"""
from typing import List, Tuple, Optional
from Modes.General import _setup_player, _setup_grid, _confirm_grid, \
    parallel_print, print_log, remove_order, congratulate_p1, congratulate_p2
from Settings import DEFAULT, PURPLE, RED, GREEN, BLACK, BLUE, \
    COL_ICON, ROW_ICON
from Objects.Mechanics.Game import BattleshipGame
from Objects.Mechanics.Player import Player
from Objects.Mechanics.Order import TraditionalOrder
from Objects.Mechanics.ActivityLog import TraditionalLog
from Objects.Vessels.Vessel import TraditionalVessel
from Objects.Vessels.Battleship import TraditionalBattleship
from Objects.Vessels.Cruiser import TraditionalCruiser
from Objects.Vessels.Destroyer import TraditionalDestroyer
from Objects.Vessels.Frigate import TraditionalFrigate
from Objects.Vessels.Submarine import TraditionalSubmarine
from Objects.Vessels.Carrier import TraditionalCarrier


def main() -> None:
    # First time setup
    p1, p2 = _setup_player()
    full_game = BattleshipGame(p1, p2, 1)

    # Create player fleets
    _setup_fleet(full_game.player1)
    full_game.update_p1_backup()

    _setup_fleet(full_game.player2)
    full_game.update_p2_backup()

    # Setup Player 1 grid
    space = '\n'
    input(f'{space * 67}{PURPLE}{full_game.player1.name}{DEFAULT}, '
          f'you will now begin setting up your fleet grid. '
          f'Press {GREEN}ENTER{DEFAULT} to continue: ')

    confirmation = False
    final = False
    while (not confirmation) or (not final):
        while not confirmation:
            confirmation = _setup_grid(full_game.player1)
        final = _confirm_grid(full_game.player1)
        if not final:
            full_game.reset_p1()
            confirmation = False
    full_game.update_p1_backup()
    print('')

    # Setup Player 2 grid
    space = '\n'
    input(f'{space * 67}{PURPLE}{full_game.player2.name}{DEFAULT}, '
          f'you will now begin setting up your fleet grid. '
          f'Press {GREEN}ENTER{DEFAULT} to continue: ')

    confirmation = False
    final = False
    while (not confirmation) or (not final):
        while not confirmation:
            confirmation = _setup_grid(full_game.player2)
        final = _confirm_grid(full_game.player2)
        if not final:
            full_game.reset_p2()
    full_game.update_p2_backup()
    print('')

    # Starting game, with Player 1 going first
    winner = full_game.check_winner()
    while not winner[0]:
        _print_screen(full_game.current_player, full_game.other_player(),
                      full_game.current_orders, full_game.log)
        response = input(f'{PURPLE}Command{DEFAULT}: ')
        check = _check_command(response, full_game.current_player,
                               full_game.current_orders)
        while not check[0]:
            if check[1] == -1:
                _print_screen(full_game.current_player,
                              full_game.other_player(),
                              full_game.current_orders, full_game.log)
                response = input(f'{RED}Invalid Format{DEFAULT}; '
                                 f'{PURPLE}Command{DEFAULT}: ')
            elif check[1] == -2:
                _print_screen(full_game.current_player,
                              full_game.other_player(),
                              full_game.current_orders, full_game.log)
                response = input(f'{RED}Invalid Command{DEFAULT}; '
                                 f'{PURPLE}Command{DEFAULT}: ')
            elif check[1] == -3:
                _print_screen(full_game.current_player,
                              full_game.other_player(),
                              full_game.current_orders, full_game.log)
                response = input(f'{RED}Invalid Coordinate{DEFAULT}; '
                                 f'{PURPLE}Command{DEFAULT}: ')
            elif check[1] == -4:
                _print_screen(full_game.current_player,
                              full_game.other_player(),
                              full_game.current_orders, full_game.log)
                response = input(f'{RED}Max Orders Received Already{DEFAULT}; '
                                 f'{PURPLE}Command{DEFAULT}: ')
            else:  # check[1] == -5
                _print_screen(full_game.current_player,
                              full_game.other_player(),
                              full_game.current_orders, full_game.log)
                response = input(f'{RED}Invalid Order{DEFAULT}; '
                                 f'{PURPLE}Command{DEFAULT}: ')
            check = _check_command(response, full_game.current_player,
                                   full_game.current_orders)

        # Response is valid, ending turn
        if check[1] == 1:
            _end_turn(full_game)
            winner = full_game.check_winner()

        # Response is valid, printing full Activity Log
        elif check[1] == 2:
            print_log(full_game)

        # Response is valid, adding order
        elif check[1] == 3:
            _add_order(full_game, (check[2][1], check[2][2]))

        # Response if valid, removing order
        elif check[1] == 4:
            remove_order(full_game, check[2][1])

        # Response is valid, player quitting the game
        else:
            full_game.current_player.forfeit = True
            winner = full_game.check_winner()

    if winner[1] == full_game.player1:
        congratulate_p1()
    else:
        congratulate_p2()


# Setup ------------------------------------------------------------------------
def _setup_fleet(player: Player) -> None:
    """
    Sets up the fleet for the specified player.

    Parameter(s):
     - player: The player that the fleet is currently being setup for
     - player_num: Either 1 / 2, representing the player
    """
    vessels = [TraditionalBattleship, TraditionalCruiser, TraditionalDestroyer,
               TraditionalFrigate, TraditionalSubmarine, TraditionalCarrier]
    for i in range(6):
        player.add_vessel(vessels[i])


# Confirmation -----------------------------------------------------------------
def _check_command(phrase: str, player: Player,
                   orders: List[TraditionalOrder]) -> \
        Tuple[bool, int, Optional[list]]:
    """
    Checks to see whether the order given is valid or not. If it is
    valid, create an Order object and append to current list of orders.
    If it is invalid, return error message.

    Valid format:
    <command>, <col>, <row>
    <command>, <order_id>

    Parameter(s):
     - phrase: The user input being checked
     - player: The player that is currently having their turn
     - orders: The current list of orders that the player has created
    """
    # Check if phrase is one of the special commands
    if phrase.lower().strip() == '\\execute':
        return True, 1, None  # Player is finishing turn
    elif phrase.lower().strip() == '\\log':
        return True, 2, None  # Player wants to see full activity log
    elif phrase.lower().strip() == '\\forfeit':
        return True, 5, None  # Player quitting game
    elif ',' not in phrase:
        return False, -1, None  # Invalid format

    # Check phrase for each individual command
    lst = phrase.split(',')
    lst[0] = str(lst[0]).strip().lower()

    # If player attempting to add an order
    if len(lst) == 3:
        for _ in range(2):
            lst[_ + 1] = str(lst[_ + 1]).strip().upper()

        if lst[0] != '\\add':
            return False, -2, None  # Invalid command
        elif (lst[1] not in COL_ICON) or (lst[2] not in ROW_ICON):
            return False, -3, None  # Invalid coordinate

        # Check if this order will exceed max amount of orders
        if len(orders) == player.battle_total:
            return False, -4, None  # Max orders received

        # Check if order is already in the list of orders
        coord = (lst[1], lst[2])
        for order in orders:
            if order.coordinate == coord:
                return False, -5, None  # Invalid order

        # Check if node is valid and not hit
        grid = player.traditional
        row = ROW_ICON.index(lst[2])
        col = COL_ICON.index(lst[1])
        if grid.grid[row][col].hit:
            return False, -3, None  # Invalid coordinate
        return True, 3, lst

    # If player attempting to remove an order
    elif len(lst) == 2:
        if lst[0] != '\\remove':
            return False, -2, None  # Invalid command
        elif int(lst[1]) > len(orders):
            return False, -5, None  # Invalid order
        return True, 4, lst

    return False, 1, None  # Invalid format


# Game modification ------------------------------------------------------------
def _add_order(game: BattleshipGame, coord: Tuple[str, str]) -> None:
    """
    Adds a valid order to the list of current player's orders.
    """
    # Add order
    order_id = len(game.current_orders) + 1
    order = TraditionalOrder(order_id, coord)
    game.current_orders.append(order)

    # Change grid characteristics
    grid = game.current_player.traditional
    row = ROW_ICON.index(coord[1])
    col = COL_ICON.index(coord[0])

    grid.grid[row][col].target_and_drop()


def _end_turn(game: BattleshipGame) -> None:
    """
    Ends the current player's turn and updates all game attributes.

    Parameter(s):
     - game: The current game taking place
    """
    traditional_grid = game.current_player.traditional
    personal_grid = game.other_player().personal
    for order in game.current_orders:

        # Get affected node
        row = ROW_ICON.index(order.coordinate[1])
        col = COL_ICON.index(order.coordinate[0])
        t_node = traditional_grid.grid[row][col]
        p_node = personal_grid.grid[row][col]

        # If vessel is located at the node
        if p_node.occupied:
            p_node.vessel.hp -= 1
            p_node.vessel.hits_received += 1

            # Vessel is 1 hp, will be destroyed by this order
            if p_node.vessel.hp == 0:
                game.enemy_sunk(p_node.vessel, game.other_player())

            # Vessel still functional
            else:

                # Change grid icons and node attributes for both players
                p_node.personal_damaged()
                t_node.damaged()
                p_node.vessel.hit = True
                p_node.vessel.update_health_color()

                # Create Activity log message
                game.log.ally_hit(
                    p_node.vessel, game.other_player().number, p_node,
                    game.current_turn_number)
                game.log.enemy_hit(
                    p_node.vessel, game.current_player.number, p_node,
                    game.current_turn_number)

        else:  # Node is empty
            p_node.miss()
            t_node.miss()

    game.current_orders = []

    # Switch current player
    game.current_player = game.other_player()
    if game.current_player == game.player1:
        game.current_turn_number += 1


# Display ----------------------------------------------------------------------
def _print_screen(current_player: Player, other_player: Player,
                  orders: List[TraditionalOrder],
                  activity_log: TraditionalLog) -> None:
    """
    Rearranges all information given and neatly prints on the screen.
    Grids are printed in parallel at the top left of the screen.
    Allied and enemy vessel information is printed at the bottom left of
    the screen, with allied vessel information on top, and enemy vessel
    information below. Orders and Activity Log are in column form on
    the right hand side of the screen, printed both in parallel with
    the grids and the vessel information.
    """
    # Helper function(s):
    def _order_list() -> List[str]:
        """
        Returns a list of all the orders that have accumulated for the current
        player's turn.
        """
        lst = []
        for order in orders:
            lst.append(str(order))
        return lst

    def _vessel_info_line(vessel: TraditionalVessel, current: bool) -> str:
        """
        Returns a string containing all information on the vessel to be
        displayed during the game as part of an information chart.

        Parameter(s):
         - vessel: The vessel that the information is taken from
         - current: Whether it is an ally (True) or enemy (False)
        """
        if not current and not vessel.hit:
            name = f'{RED}[--]{DEFAULT} UNKNOWN'
            position = f'{BLACK}---{DEFAULT}'
            health = f'{BLACK}-{DEFAULT}'
            hits = f'{BLACK}-{DEFAULT}'
            line = f'{name:<58}{position:^13}|{health:^23}{hits:^23}'
        elif current and not vessel.sunk:
            name = f'{BLUE}[{vessel.abbrev}]{DEFAULT} ' \
                   f'{vessel.pennant:02d} ' \
                   f'{vessel.name}'
            position = f'{BLUE}{vessel.bow[0][0]},{vessel.bow[0][1]}{DEFAULT}'
            health = f'{vessel.health_color}{vessel.hp}{DEFAULT}'
            hits = f'{vessel.health_color}{vessel.hits_received}{DEFAULT}'
            line = f'{name:<58}{position:^13}|{health:^23}{hits:^23}'
        elif current and vessel.sunk:
            name = f'{BLACK}[{vessel.abbrev}] ' \
                   f'{vessel.pennant:02d} ' \
                   f'{vessel.name}{DEFAULT}'
            position = f'{BLACK}{vessel.bow[0][0]},{vessel.bow[0][1]}{DEFAULT}'
            health = f'{BLACK}{vessel.hp}{DEFAULT}'
            hits = f'{BLACK}{vessel.hits_received}{DEFAULT}'
            line = f'{name:<58}{position:^13}|{health:^23}{hits:^23}'
        elif not current and not vessel.sunk:
            name = f'{RED}[--]{DEFAULT} {vessel.pennant:02d} {vessel.name}'
            position = f'{BLACK}---{DEFAULT}'
            health = f'{BLACK}-{DEFAULT}'
            hits = f'{vessel.health_color}{vessel.hits_received}{DEFAULT}'
            line = f'{name:<58}{position:^13}|{health:^23}{hits:^23}'
        else:  # not current and vessel.sunk
            name = f'{BLACK}[{vessel.abbrev}]{DEFAULT} ' \
                   f'{vessel.pennant:02d} ' \
                   f'{vessel.name}'
            position = f'{BLACK}{vessel.bow[0][0]},{vessel.bow[0][1]}{DEFAULT}'
            health = f'{BLACK}{vessel.hp}{DEFAULT}'
            hits = f'{BLACK}{vessel.hits_received}{DEFAULT}'
            line = f'{name:<58}{position:^13}|{health:^23}{hits:^23}'
        return line

    def _info_chart(player: Player, current: bool) -> List[str]:
        """
        Creates a chart that specifies the position and direction of each
        vessel along with other information within a player's fleet. If the
        chart is for the enemy vessel information, data is determined upon the
        first hit.

        Parameter(s):
         - player: The player that the chart will take information from
         - current: Whether the player is the current player or not
        """
        if current:
            color = f'{BLUE}'
        else:
            color = f'{RED}'

        if current:
            title = f'{color}{"Allied Vessels":^50}{"R|C":^5}|' \
                    f'{"Hitpoints":^15}{"Dam. Sec.":^15}{DEFAULT}'
        else:
            title = f'{color}{"Enemy Vessels":^50}{"R|C":^5}|' \
                    f'{"Hitpoints":^15}{"Dam. Sec.":^15}{DEFAULT}'

        lst = [title]
        vessel_lst = [player.bb_curr, player.cc_curr, player.dd_curr,
                      player.ff_curr, player.sm_curr, player.cv_curr]
        for j in range(len(player.battle_sunk)):
            vessel_lst.append(player.battle_sunk[j])
        for sublist in vessel_lst:
            for vessel in sublist:
                lst.append(_vessel_info_line(vessel, current))
        return lst

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # Display size for 1440p monitor: 68 x 310 char

    # Radar and sonar grids
    grids = [current_player.personal, current_player.traditional]

    # Create chart with allied and enemy information
    ally_info = _info_chart(current_player, True)
    ally_info[0] = f'{ally_info[0]:^162}'  # 154 char + 4/color change
    for i in range(len(ally_info) - 1):
        ally_info[i + 1] = f'{ally_info[i + 1]:^186}'  # 154 char + 4/cc

    enemy_info = _info_chart(other_player, False)
    enemy_info[0] = f'{enemy_info[0]:^162}'
    for i in range(len(enemy_info) - 1):
        enemy_info[i + 1] = f'{enemy_info[i + 1]:^186}'

    white_space = f'{"":^154}'  # How many chars the grids take up / align
    full_info = [white_space]
    full_info.extend(ally_info)
    full_info.append(white_space)
    full_info.extend(enemy_info)
    for i in range(29 - len(full_info)):
        full_info.append(white_space)

    column_space = f''

    # Create list of orders; 76 char + 4/cc
    player_orders = f'{PURPLE}PLAYER ORDERS{DEFAULT}'
    orders_list = [f'{player_orders:^84}', column_space]
    orders_list.extend(_order_list())
    for i in range(len(orders_list) - 2):
        orders_list[i + 2] = f'{orders_list[i + 2]:<84}'

    # Create limited activity log
    log = activity_log.partial_log(current_player.number)
    activity_log = f'{PURPLE}ACTIVITY LOG{DEFAULT}'
    log_list = [f'{activity_log:^84}', column_space]
    log_list.extend(log)
    for i in range(len(log_list) - 2):
        log_list[i + 2] = f'{log_list[i + 2]:<84}'

    # Create text columns and separate upper / lower text
    text = []
    lines = max(len(orders_list), len(log_list))
    for i in range(lines):
        text_line = ''
        try:
            text_line += f'{orders_list[i]}  '
        except IndexError:
            text_line += f'{"":^76}  '
        try:
            text_line += f'{log_list[i]}'
        except IndexError:
            text_line += f'{"":^76}'
        text.append(text_line)

    upper = text[:38]
    lower = text[38::]

    # Fill lower with whitespaces
    fillers = len(full_info) - len(lower)
    for i in range(fillers):
        lower.append('')

    # Grids + upper columns
    ret = parallel_print(grids, upper)
    # Chart information + lower columns
    for i in range(len(full_info)):
        ret += f'{full_info[i]}  {lower[i]}\n'
    print(ret)
