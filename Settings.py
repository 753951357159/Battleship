"""
Settings.py

PURPOSE:
Stores all important information and relevant game settings. If you want to
customize these, feel free to do so.

If the program does not fit your screen, try playing with the MDW (Max Display
Width) variable below.
"""
from Objects.Vessels.Battleship import TraditionalBattleship as Bb
from Objects.Vessels.Cruiser import TraditionalCruiser as Cc
from Objects.Vessels.Destroyer import TraditionalDestroyer as Dd
from Objects.Vessels.Frigate import TraditionalFrigate as Ff
from Objects.Vessels.Submarine import TraditionalSubmarine as Sm
from Objects.Vessels.Carrier import TraditionalCarrier as Cv

# Program information
TITLE = '\u2693  BATTLESHIP  \u2693'
NAME = 'Alexander Feng'
VERSION = 'ver. 1.01'

# The maximum display width of the monitor using PyCharm
MDW = 310  # 182 for a laptop 1080p screen, 310 for a 31 in. 2K monitor

# Clearing screen
EMPTY_FRAME = '\n' * 28

# Color coding
DEFAULT = '\033[m'       # 'Pycharm' normal
GREEN = '\033[32m'       # Green
RED = '\033[31m'         # Red
PURPLE = '\033[35m'      # Purple
BLUE = '\033[34m'        # Blue
BLACK = '\033[30m'       # Black
YELLOW = '\033[33m'      # Yellow
CYAN = '\033[36m'        # Cyan
B_YELLOW = '\033[33;1m'  # 'Bold' Yellow    - Hit
B_BLUE = '\033[34;1m'    # 'Bold' Blue      - Miss
B_RED = '\033[31;1m'     # 'Bold' Red       - Destroyed
B_PURPLE = '\033[35;1m'  # 'Bold' Purple    - Detected

# Confirmations when asking user
AFFIRMATIVE = ['Yes', 'yes', 'Y', 'y']
NEGATIVE = ['No', 'no', 'N', 'n']

# Node symbols
EMPTY = '\u25C7'         # Small diamond
HIT = '\u25CF'           # Filled circle
MISS = '\u25EF'          # Hollow circle
DROP = '+'               # Plus sign

# Grid creation symbols
CORNER = '\u2514'
ROW_SEP = '\u2524'
COL_SEP = '\u252C'
COL_SPACER = '\u2500'
ROW_ICON = ['Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O',
            'N', 'M', 'L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 'D', 'C',
            'B', 'A', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0']
COL_ICON = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
            'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Vessel symbols on grid
BOW = {'N': '\u25B2', 'S': '\u25BC', 'E': '\u25B6', 'W': '\u25C0'}
STERN = {'N': '\u2534', 'S': '\u252C', 'E': '\u251C', 'W': '\u2524'}

# Nations and their respective ranks / symbols
NATIONS = {'DE': ('\u2720', 'Großadmiral'), 'US': ('\u272A', 'Admiral'),
           'RU': ('\u262D', 'Адмирал'), 'FR': ('\u269C', 'Amiral'),
           'UK': ('\u2654', 'Admiral')}

# Maximum number of names available for each vessel class for each nation
PENNANTS = {'DE': {Bb: 49, Cc: 50, Dd: 43, Ff: 16, Sm: 39, Cv: 7},
            'US': {Bb: 49, Cc: 40, Dd: 37, Ff: 38, Sm: 50, Cv: 33},
            'RU': {Bb: 34, Cc: 49, Dd: 60, Ff: 10, Sm: 37, Cv: 8},
            'FR': {Bb: 45, Cc: 25, Dd: 32, Ff: 21, Sm: 20, Cv: 15},
            'UK': {Bb: 43, Cc: 35, Dd: 36, Ff: 38, Sm: 30, Cv: 36}}
FILE_NAMES = {Bb: 'bb', Cc: 'cc', Dd: 'dd', Ff: 'ff', Sm: 'sm', Cv: 'cv'}
