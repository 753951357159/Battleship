"""
Order.py

PURPOSE:
Create the Order object so that players can create orders to command vessels.
"""
from typing import Tuple
from Settings import PURPLE, DEFAULT


class TraditionalOrder:
    """
    The general command class used in Traditional Battleship to plan player
    moves.

    Attribute(s):
     - order_id: The order number
     - coordinate: The node that is being targeted (col, row)
    """
    order_id: int
    coordinate: Tuple[str, str]

    def __init__(self, num: int, coord: Tuple[str, str]) -> None:
        """
        Initializes a new Order.

        Parameter(s):
         - num: The order num
         - coord: The coordinate of the node being targeted (col, row)
        """
        self.order_id = num
        self.coordinate = coord

    def __str__(self) -> str:
        return f'{PURPLE}{self.order_id:02d}{DEFAULT} | ' \
               f'Targeting ({self.coordinate[0]}, {self.coordinate[1]})'
