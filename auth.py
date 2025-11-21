from pathlib import Path
import json
import sys
import os
import time
import hashlib

path = Path('auth.json')


if not path.exists():
    login = {'username': None, 'password': None}
else:
    with path.open('r', encoding='utf-8') as fc:
        saved_log = json.loads(fc.read())


def hash_pwd(password: str) -> str:
    """docstrings"""
    return hashlib.sha256(password.encode()).hexdigest()

def new_name():
    """docstrings"""
    entering = True
    while entering:
        username = input("\nEnter a username: ").strip().lower()
        if not username:
            print('Username field cannot be empty!')
        else:
            entering = False
    return username


def new_pwd():
    """docstrings"""
    entering = True
    while entering:
        password = input("\nEnter a password (mininmum 4 char): ").strip().lower()
        if not password or len(password) < 4:
            print('Password is not secure!')
        else:
            entering = False
    return hash_pwd(password)


def ex_name():
    """docstrings"""
    entering = True
    while entering:
        username = input('\nEnter your username: ').strip().lower()
        if not username or username != saved_log.get('username', None):
            print('Username not recognized.')
        else:
            entering = False
    return True


def ex_pwd():
    """docstrings"""
    entering = True
    while entering:
        password = input('\nEnter your password: ').strip().lower()
        if not password or hash_pwd(password) != saved_log.get('password', None):
            print('Password incorrect!')
        else:
            entering = False
    return True


def clear_screen():
    """Clears the console screen depending on OS."""
    os.system("cls" if os.name == "nt" else "clear")

def clear_line():
    """docstrings"""
    sys.stdout.write('\r\033[K')

def save_info(file):
    """docstrings"""
    with path.open('w', encoding='utf-8') as fc:
        fc.write(json.dumps(file))

def sign_anim(r=2, text='\rSigning in', sec=0.5):
    """docstrings"""
    for cycle in range(2):
        for dots in range(1, 4):
            sys.stdout.write(f'{text}{"." * dots}')
            sys.stdout.flush()
            time.sleep(sec)


def main():
    """docstrings"""
    clear_screen()

    if not path.exists():
        print("=" * 24, "Sign Up", 24 * "=")
        username = new_name()
        password = new_pwd()

        login['username'] = username
        login['password'] = password

        save_info(login)
        print('\nAccount created successfully.')

    else:
        print("=" * 24, "Sign in", 24 * "=")
        username_ok = ex_name()
        password_ok = ex_pwd()
        if username_ok and password_ok:
            clear_screen()
            sign_anim()
            clear_line()
            print(
                f'\nWelcome back, {saved_log.get("username", None).title()}.'
                )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Program finished.]")
        sys.exit()
