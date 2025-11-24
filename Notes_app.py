import datetime
import json
import os
import sys
import time

users = {}
users_file = "users.json"

def load():
    global users
    try:
        with open(users_file, "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

def save():
    try:
        with open(users_file, "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

def register():
    """docstrings"""

    print('Register a new account')
    while True:
        username = input("Enter a username: ").strip().lower()
        if not username:
            print('Username field cannot be empty!')
            continue
        elif username not in users:
            users[username] = {"name": "", 
                               "password": "", 
                               "note_text": [], 
                               "timestamps": []}
        else:
            print('Username already exists!')
            continue
        break
    while True:
        password = input("Enter a password (must be 4 char long): ").strip()
        if not password or len(password) < 4:
            print('Password is not secure!')
        else:
            users[username]['password'] = password
            break
    while True:
        name = input("Enter your name: ").strip().title()
        if not name:
            print('Name field cannot be empty!')
            continue
        else:
            users[username]['name'] = name
            save()
            clear_screen()
            sign_anim(text='\rAccount created successfully! Signing in')
            main_block(username)
            break
            
    
def login():
    """docstrings"""

    print('Login to your account')
    while True:
        username = input('Enter your username: ').strip().lower()
        if not username or username not in users:
            print('Username not recognized.')
            continue
        else:
            break
        
    while True:
        password = input('Enter your password: ').strip()
        if not password or password != users[username]['password']:
            print('Inaccurate password!')
            continue
        else:
            clear_screen()
            sign_anim(text='\rLogin successful! Redirecting to your notes')
            main_block(username)
            break


def add(username):
    while True:
        note_text = input("Enter your note: ").strip()
        if not note_text:
            print("Note cannot be empty.")
            continue
        else:
            timestamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
            users[username]['note_text'].append(note_text)
            users[username]['timestamps'].append(timestamp)
            print("Note added successfully.")
            save()
            break
    

def view(username):
    if not users[username]['note_text']:
        print("No notes found.")
    else:
        for i, (note_text, timestamp) in enumerate(zip(users[username]['note_text'], users[username]['timestamps']), start=1):
            print(f"{i}. {note_text} (Added on: {timestamp})")
    

def delete(username):
    if not users[username]['note_text']:
        print("No notes found.")
    else:
        view(username)
        while True:
            input_ = input("Enter the note number to delete: ")
            try:
                note_index = int(input_) - 1
                if 0 <= note_index < len(users[username]['note_text']):
                    deleted_note = users[username]['note_text'].pop(note_index)
                    users[username]['timestamps'].pop(note_index)
                    save()
                    print(f"Deleted note: {deleted_note}")
                    break
                else:
                    print("Invalid note number.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue


def sign_anim(r=2, text='\rSigning in', sec=0.5):
    """docstrings"""
    for cycle in range(2):
        for dots in range(1, 4):
            sys.stdout.write(f'{text}{"." * dots}')
            sys.stdout.flush()
            time.sleep(sec)
    
def clear_screen():
    """Clears the console screen depending on OS."""
    os.system("cls" if os.name == "nt" else "clear")

def main_block(username):
    print(f"""Welcome {users[username]['name']}! """)
    print("1. Add a note")
    print("2. View notes")
    print("3. Delete a note")
    print("4. Logout")
    while True:
        ans = input("Please choose an option to continue: ")
        if ans == "1":
            add(username)
        elif ans == "2":
            view(username)
        elif ans == "3":
            delete(username)
        elif ans == "4":
            clear_screen()
            print("Logged out successfully.")
            main()
            break
        else:
            print("Invalid option. Please try again.")
            continue

def main():
    print("""Welcome to the Notes App!
          Please register or login to continue.""")
    
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    while True:
        ans = input("Please choose an option to continue: ")
        if ans == "1":
            register()
            break
        elif ans == "2":
            login()
            break
        elif ans == "3":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
            continue

    
load()
if __name__ == "__main__":
    main()
