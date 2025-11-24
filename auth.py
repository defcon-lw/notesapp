"""
Authentication module for the notes/text app.

Handles:
- creating new accounts
- verifying existing login credentials
- password hashing
- interacting with CLI utility functions located in cli_utils.py
"""

import json
import sys
import hashlib
import cli_utils as ut


def hash_pwd(password: str) -> str:
    """
    Hash a plaintext password using SHA-256.

    This helps avoid storing raw passwords in the auth file.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def new_name() -> str:
    """
    Prompt the user for a new username.

    Ensures:
    - username is not empty
    - username is normalized to lowercase
    """
    entering = True
    while entering:
        username = input("\nEnter a username: ").strip().lower()
        if not username:
            print('Username field cannot be empty!')
        else:
            entering = False
    return username


def new_pwd() -> str:
    """
    Prompt the user for a new password.

    Basic rule:
    - minimum length of 4 characters

    Returns the *hashed* password.
    """
    entering = True
    while entering:
        password = (
            input("\nEnter a password (minimum 4 char): ")
            .strip()
            .lower()
        )

        if not password or len(password) < 4:
            print('Password is not secure!')
        else:
            entering = False

    return hash_pwd(password)


def ex_name(data: dict) -> bool:
    """
    Validate an existing username.

    Compares user input with the username stored in `data`.

    Returns:
        True  -> username matches
        False -> too many failed attempts
    """
    attempts = 4
    entering = True

    while entering:
        username = input('\nEnter your username: ').strip().lower()

        if not username or username != data.get('username'):
            print('Username not recognized.')
            attempts -= 1

            if attempts == 0:
                entering = False
                return False

            print(f"\n{attempts} attempt(s) left!")
        else:
            entering = False
            return True


def ex_pwd(data: dict) -> bool:
    """
    Validate an existing password.

    Compares hashed user input with stored hashed password.

    Returns:
        True  -> password matches
        False -> too many failed attempts
    """
    attempts = 4
    entering = True

    while entering:
        password = input('\nEnter your password: ').strip().lower()

        if not password or hash_pwd(password) != data.get('password'):
            print('Password incorrect!')
            attempts -= 1

            if attempts == 0:
                entering = False
                return False

            print(f"\n{attempts} attempt(s) left!")
        else:
            entering = False
            return True


def main():
    """
    Entry point for login/signup workflow.

    Behaviour:
    - If no auth file exists → create new account
    - If auth file exists → sign in
    - Uses cli_utils.py for animations, file operations, clearing screen, etc.
    """
    ut.clear_screen()
    fp = ut.filepath()

    # -----------------------------
    # FIRST-TIME SIGN UP
    # -----------------------------
    if not fp.exists():
        login = {'username': None, 'password': None}

        print("=" * 24, "Sign Up", "=" * 24)
        username = new_name()
        password = new_pwd()

        login['username'] = username
        login['password'] = password

        ut.save_info(login)
        ut.sign_anim(text='\rSigning up')
        ut.clear_line()
        print('\nAccount created successfully.\n')
        sys.exit()

    # -----------------------------
    # EXISTING ACCOUNT → SIGN IN
    # -----------------------------
    else:
        with fp.open('r', encoding='utf-8') as fc:
            saved_log = json.loads(fc.read())

        print("=" * 24, "Sign in", "=" * 24)

        username_ok = ex_name(saved_log)
        if not username_ok:
            ut.create_acct()

        password_ok = ex_pwd(saved_log)
        if not password_ok:
            ut.create_acct()

        ut.clear_screen()
        ut.sign_anim()
        ut.clear_line()

        print(
            f'\nWelcome back, '
            f'{saved_log.get("username", None).title()}.\n'
        )


# Safe entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Program finished.]")
        sys.exit()
