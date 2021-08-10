"""
Settings.py

PURPOSE:
Stores all important information and relevant game settings. If you want to
customize these, feel free to do so.

If the program does not fit your screen, try playing with the MDW (Max Display
Width) variable below.
"""
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
