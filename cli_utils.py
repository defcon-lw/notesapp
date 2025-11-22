"""
Utility functions for interactions in the auth.py script

This module handles:
- screen clearing
- line clearing
- simple yes/no prompts
- account recreation workflow
- file handling for authentication data
- small animations
"""

import os
import sys
import time
import json
from pathlib import Path
import auth


YES = ['y', 'yes']
NO = ['n', 'no']


def filepath(fp: str = 'authen.json') -> Path:
    """
    Return a Path object pointing to the authentication file.

    Parameters:
        fp (str): filename to use for storing auth data.

    Returns:
        pathlib.Path
    """
    return Path(fp)


def req() -> bool:
    """
    Prompt the user to confirm whether they want to create a new account.

    Returns:
        True  -> user chose yes
        False -> user chose no
    """
    requesting = True

    while requesting:
        new = (
            input("\nWould you like to create a new account? (y/n): ")
            .lower()
            .strip()
        )

        if new in YES:
            requesting = False
            return True
        elif new in NO:
            requesting = False
            return False
        else:
            print('Invalid input!')


def create_acct():
    """
    Delete the existing auth file and redirect the user
    back to the sign-up flow within auth.main().

    Called when:
    - user fails login attempts
    - user chooses to recreate account
    """
    create_new = req()

    if create_new:
        fp = filepath()

        try:
            os.remove(fp)
        except FileNotFoundError:
            print("\nAuth file missing or corrupted")

        sign_anim(text='\rRedirecting to sign up page')
        auth.main()
    else:
        sys.exit()


def clear_screen():
    """
    Clear the console screen depending on the OS.

    Uses:
        cls  -> Windows
        clear -> Linux / Mac
    """
    os.system("cls" if os.name == "nt" else "clear")


def clear_line(n: int = 1):
    """
    Clear the previous N lines in the terminal.

    Parameters:
        n (int): number of lines to erase upward.

    Uses ANSI escape codes:
    - \033[1A -> move cursor up by 1 line
    - \033[2K -> clear entire line
    """
    for _ in range(n):
        sys.stdout.write('\033[1A')       # move cursor up
        sys.stdout.write('\r\033[2K')    # clear entire line
    sys.stdout.flush()


def save_info(data: dict):
    """
    Save user authentication data to the JSON file.

    Parameters:
        data (dict): {'username': str, 'password': str (hashed)}
    """
    fp = filepath()
    with fp.open('w', encoding='utf-8') as fc:
        fc.write(json.dumps(data))


def sign_anim(r: int = 2, text: str = '\rSigning in', sec: float = 0.5):
    """
    Display a simple loading animation for CLI transitions.

    Parameters:
        r (int): number of animation cycles (unused internally but kept for compat)
        text (str): text prefix for animation
        sec (float): delay between frames

    Clears screen before animating.
    """
    clear_screen()

    for cycle in range(2):
        for dots in range(1, 4):
            sys.stdout.write(f'{text}{"." * dots}')
            sys.stdout.flush()
            time.sleep(sec)
