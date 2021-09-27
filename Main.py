"""
Main.py

PURPOSE:
To start the entire program and will not exit without confirmation. The program
will terminate only when the user decides to exit the program.
"""
from Settings import TITLE, NAME, VERSION, MDW, DEFAULT, GREEN, RED, PURPLE
from Modes.TPT import main as tpt_main


def header(mdw: int) -> None:
    """
    The header of the program. Appears only once during start up. Displays the
    title, name, and version of the program.
    """
    print(f'{TITLE:^{mdw}}')
    print(f'{NAME:^{mdw}}')
    print(f'{VERSION!s:^{mdw}}', f'\n')


def menu() -> bool:
    """
    The main menu of the program. The following are the valid options:
     - Single Player [Arcade]
     - Single Player [Realistic]
     - Single Player [Competitive]
     - Two Player [Traditional]
     - Two Player [Arcade]
     - Two Player [Realistic]
     - Two Player [Competitive]
     - LAN [Traditional]
     - LAN [Competitive]
     - Quit

    Parameter(s):
     - mdw: Represents the maximum display width of a screen.
    """
    # Display options available
    window = 31  # longest option character count

    print(f'{GREEN}{"Please Select An Option Below:".center(MDW)}{DEFAULT}')
    print(f'{"(1) Single Player [Arcade]":<{window}}'.center(MDW))
    print(f'{"(2) Single Player [Realistic]":<{window}}'.center(MDW))
    print(f'{"(3) Single Player [Competitive]":<{window}}'.center(MDW))
    print(f'{"(4) Two Player [Traditional]":<{window}}'.center(MDW))
    print(f'{"(5) Two Player [Arcade]":<{window}}'.center(MDW))
    print(f'{"(6) Two Player [Realistic]":<{window}}'.center(MDW))
    print(f'{"(7) Two Player [Competitive]":<{window}}'.center(MDW))
    print(f'{"(8) LAN [Traditional]":<{window}}'.center(MDW))
    print(f'{"(9) LAN [Competitive]":<{window}}'.center(MDW))
    print(f'{"(0) QUIT":<{window}}'.center(MDW), f'\n')

    options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    # Ask user for valid option if applicable
    response = input(f'{PURPLE} >>> {DEFAULT}')
    while (response not in options) or (response == ''):
        response = input(f'{PURPLE} >>> {RED}Invalid Option{DEFAULT} - '
                         f'Please try again: ')

    if response == '1':  # Starts the Single Player Arcade game mode
        return False
    elif response == '2':  # Starts the Single Player Realistic game mode
        return False
    elif response == '3':  # Starts the Single Player Competitive game mode
        return False
    elif response == '4':  # Starts the Two Player Traditional game mode
        tpt_main()
        return False
    elif response == '5':  # Starts the Two Player Arcade game mode
        return False
    elif response == '6':  # Starts the Two Player Realistic game mode
        return False
    elif response == '7':  # Starts the Two Player Competitive game mode
        return False
    elif response == '8':  # Starts the LAN Traditional game mode
        return False
    elif response == '9':  # Starts the LAN Competitive game mode
        return False
    else:  # Terminates the program
        return True


if __name__ == '__main__':
    exit_permission = False  # Program will not exit unless True
    header(MDW)

    # Run program, exit when True
    while not exit_permission:
        exit_permission = menu()
