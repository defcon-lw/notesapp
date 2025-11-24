import json
import datetime
import os
import time
import sys

class Store_Manager:

    """Saves and Loads all necessary info"""

    import json
    users = {}
    filename='users.json'
    def load():
        try:
            with open(Store_Manager.filename, 'r') as file:
                Store_Manager.users = json.load(file)
            return Store_Manager.users
        except FileNotFoundError:
            return Store_Manager.users == {}
    def save():
        try:
            with open(Store_Manager.filename, 'w') as file:
                json.dump(Store_Manager.users, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

class Notes:

    """Note class capable of storing notes and timestamps"""

    def __init__(self, username, note_text, timestamp,):
        self.note_text = note_text
        self.timestamp = timestamp
        Store_Manager.users[username].setdefault('note_text', [])
        Store_Manager.users[username].setdefault('timestamps', [])
        if note_text =='' or timestamp == '':
            return
        else:
            Store_Manager.users[username]['note_text'].append(note_text)
            Store_Manager.users[username]['timestamps'].append(timestamp)
            Store_Manager.save()

class User:

    """User class capable of storing user info"""

    def __init__(self, username, name, password):
        self.username = username
        self.name = name
        self.password = password
        Store_Manager.users[username] = {
            "name": name,
            "password": password,
        }
        Store_Manager.save()

class Noteapp:

    """Main Noteapp class containing all functionalities"""
    
    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def sign_anim(text='', sec=0.5):
        for cycle in range(2):
            for dots in range(1, 4):
                sys.stdout.write(f'{text}{"." * dots}')
                sys.stdout.flush()
                time.sleep(sec)

    def register():

        """Registers the user and when all conditions are met, creates a user object and signs them in."""

        print('Register a new account')
        while True:
            username = input("Enter a username: ").strip().lower()
            password = input("Enter a password (must be 4 char long): ").strip()
            name = input("Enter your name: ").strip().title()
            if not username:
                print('Username field cannot be empty!')
                continue
            elif username in Store_Manager.users:
                print('Username already exists!')
                continue
            elif not password or len(password) < 4:
                print('Password is not secure!')
                continue
            elif not name:
                print('Name field cannot be empty!')
                continue
            else:
                User(username, name, password)
                Noteapp.clear_screen()
                Noteapp.sign_anim(text='\rAccount created successfully! Signing in')
                main_block(username)
                break

    def login():
        """docstrings"""
        print("Login to your account")
        while True:
            username = input("Enter your username: ").strip().lower()
            password = input("Enter your password: ").strip()
            if username in Store_Manager.users and Store_Manager.users[username]['password'] == password:
                Noteapp.clear_screen()
                Noteapp.sign_anim(text='\rLogin successful! Redirecting to your notes')
                main_block(username)
                break
            else:
                print("Invalid username or password. Please try again.")
                continue

    def add_note(username):
        while True:
            note_text = input("Enter your note: ").strip()
            if note_text:
                timestamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
                Notes(username, note_text, timestamp)
                print("Note added successfully.")
                break
            else:
                print("Note cannot be empty.")
                continue

    def view_notes(username):
        Notes(username, '', '')  # Initialize notes for the user if not present
        if not Store_Manager.users[username]['note_text']:
            print("No notes found.")
        else:
            for i, (note_text, timestamp) in enumerate(zip(Store_Manager.users[username]['note_text'], Store_Manager.users[username]['timestamps']), start=1):
                print(f"{i}. {note_text} (Added on: {timestamp})")

    def delete_note(username):
        Notes(username, '', '')  # Initialize notes for the user if not present
        if not Store_Manager.users[username]['note_text']:
            print("No notes to delete.")
        else:
            Noteapp.view_notes(username)
            while True:
                try:
                    note_index = int(input("Enter the note number to delete: ")) - 1
                    if 0 <= note_index < len(Store_Manager.users[username]['note_text']):
                        print(f"Deleted note: {Store_Manager.users[username]['note_text'][note_index]}")
                        del Store_Manager.users[username]['note_text'][note_index]
                        del Store_Manager.users[username]['timestamps'][note_index]
                        Store_Manager.save()
                        print("Note deleted successfully.")
                        break
                    else:
                        print("Invalid note number. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
        
def main_block(username):
    
    """App Menu"""

    print( f"""\nWelcome {Store_Manager.users[username]['name']}! """)
    print("1. Add a note")
    print("2. View notes")
    print("3. Delete a note")
    print("4. Logout")
    while True:
        ans = input("Please choose an option to continue: ")
        if ans == "1":
            Noteapp.add_note(username)
        elif ans == "2":
            Noteapp.view_notes(username)
        elif ans == "3":
            Noteapp.delete_note(username)
        elif ans == "4":
            Noteapp.clear_screen()
            print("Logged out successfully.")
            main()
            break
        else:
            print("Invalid option. Please try again.")
            continue

def main():

    """Sign In/Up Menu"""

    Store_Manager.load()
    print(f"""
{36 * "="}
        WELCOME TO THE NOTESAPP
{36 * "="}
""")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    while True:
        ans = input("Please choose an option to continue: ")
        if ans == "1":
            Noteapp.register()
            break
        elif ans == "2":
            Noteapp.login()
            break
        elif ans == "3":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
            continue
if __name__ == "__main__":
    main()