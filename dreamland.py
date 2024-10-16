#!/usr/bin/env python

import os
import bcrypt
import base64
import json
from getpass import getpass

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#                       welcome to dreamland, darling
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#   [dreamland.py]:
#           login_screen
#           register_screen
#           main_menu_screen
#           bio_screen
#           view_bios_screen
#           logout_screen
#           helper functions (e.g., clear_screen, header)
#------------------------------------------------------------------------------

# global variables
loop = True
screen = "login"
current_user = None
logged_in_users = set()

# ensure the users directory exists and make it if it doesn't
if not os.path.exists('users'):
    os.makedirs('users')

#------------------------------------------------------------------------------
# Helper Functions
#------------------------------------------------------------------------------

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def header():
    print("\n" + "-" * 80)
    print("welcome to dreamland, darling")
    print("-" * 80 + "\n")

#------------------------------------------------------------------------------
# Screen Functions
#------------------------------------------------------------------------------

def login_screen():
    global screen, current_user
    clear_screen()
    header()
    print("login to your account\n")
    username = input("enter your username: ").strip()
    password = getpass("enter your password: ").strip()

    user_file = os.path.join('users', f'{username}.txt')

    if not os.path.exists(user_file):
        print("\ninvalid username or password.")
        input("press enter to continue...")
        screen = "login"
        return

    # Load user data from file
    with open(user_file, 'r') as f:
        user_data = json.load(f)

    stored_hash = base64.b64decode(user_data['password_hash'].encode('utf-8'))

    if bcrypt.checkpw(password.encode(), stored_hash):
        print("\nLogin successful!")
        current_user = username
        logged_in_users.add(username)
        input("Press Enter to continue...")
        screen = "main_menu"
    else:
        print("\nInvalid username or password.")
        input("Press Enter to continue...")
        screen = "login"

def register_screen():
    global screen
    clear_screen()
    header()
    print("register a new account\n")
    username = input("choose a username: ").strip()
    password = getpass("choose a password: ").strip()
    confirm_password = getpass("confirm your password: ").strip()

    if password != confirm_password:
        print("\passwords do not match.")
        input("press enter to continue...")
        screen = "register"
        return

    user_file = os.path.join('users', f'{username}.txt')

    if os.path.exists(user_file):
        print("\username already exists!")
        input("press enter to continue...")
        screen = "register"
        return

    # hash the password with bcrypt
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    password_hash_encoded = base64.b64encode(password_hash).decode('utf-8')

    # create the data before making the .json file
    user_data = {
        'password_hash': password_hash_encoded,
        'bio': ''
    }

    # save user data to file
    with open(user_file, 'w') as f:
        json.dump(user_data, f)

    print("\nregistration successful! welcome to dreamland :3")
    input("press enter to continue...")
    screen = "login"

def main_menu_screen():
    global screen
    clear_screen()
    header()
    print(f"Logged in as: {current_user}\n")
    print("1. edit bio")
    print("2. discover friends")
    print("3. logout\n")
    choice = input("enter your choice: ").strip()

    if choice == '1':
        screen = "bio"
    elif choice == '2':
        screen = "view_bios"
    elif choice == '3':
        screen = "logout"
    else:
        print("\ninvalid choice.")
        input("press enter to continue...")
        screen = "main_menu"

def bio_screen():
    global screen
    clear_screen()
    header()
    print("edit Your bio\n")
    bio = input("enter your new bio: ").strip()

    user_file = os.path.join('users', f'{current_user}.txt')

    # Load user data
    with open(user_file, 'r') as f:
        user_data = json.load(f)

    # Update bio
    user_data['bio'] = bio

    # Save user data
    with open(user_file, 'w') as f:
        json.dump(user_data, f)

    print("\nBio updated!")
    input("Press Enter to continue...")
    screen = "main_menu"

def view_bios_screen():
    global screen
    clear_screen()
    header()
    print("Bios of Other Logged-in Users\n")

    other_users = logged_in_users - {current_user}

    if not other_users:
        print("No other users are currently logged in.")
    else:
        for user in other_users:
            user_file = os.path.join('users', f'{user}.txt')

            if os.path.exists(user_file):
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                bio = user_data.get('bio', 'No bio available.')
                print(f"Username: {user}")
                print(f"Bio: {bio}\n")
            else:
                print(f"Username: {user}")
                print("Bio: No bio available.\n")

    input("Press Enter to continue...")
    screen = "main_menu"

def logout_screen():
    global screen, current_user
    logged_in_users.remove(current_user)
    current_user = None
    print("\nYou have been logged out.")
    input("Press Enter to continue...")
    screen = "login"

#------------------------------------------------------------------------------
# Main Loop
#------------------------------------------------------------------------------

while loop:
    if screen == "login":
        login_screen()

    elif screen == "register":
        register_screen()

    elif screen == "main_menu":
        main_menu_screen()

    elif screen == "bio":
        bio_screen()

    elif screen == "view_bios":
        view_bios_screen()

    elif screen == "logout":
        logout_screen()

    else:
        # If the screen is not recognized, go back to login
        screen = "login"

# eof
