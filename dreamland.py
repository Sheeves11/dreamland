#!/usr/bin/env python

#------------------------------------------------------------------------------
# dreamland.py
#------------------------------------------------------------------------------
# this is the main file that runs the application.
# it handles the main menu and navigation between different screens.
# it uses functions from other modules to keep things organized.
#------------------------------------------------------------------------------

from getpass import getpass
import sys
import os
import base64
import bcrypt

from helpers import (
    clear_screen,
    show_splash_screen,
    show_header,
    show_footer,
    format_text,
    color_text,
    format_menu_options,
    current_screen,
    current_user,
)
from data import load_user_data, save_user_data
from chat import direct_messages_screen
from friends import discover_users_screen, friends_list_screen
from feed import feed_screen, create_post_screen, my_posts_screen
from user import edit_profile_screen, user_profile_screen
from notifications import notifications_screen

def welcome_screen():
    """
    displays the welcome screen where users can log in, register, or exit.
    """
    clear_screen()
    print("""

   °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.
  °                               °
  ° weclome to dreamland, darling °
  °                               °
   °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.

  this is perhaps what social media
      always should have been

⋆˖⁺‧₊☽◯☾₊‧⁺˖⋆⋆˖⁺‧₊☽◯☾₊‧⁺˖⋆⋆˖⁺‧₊☽◯☾₊‧⁺˖⋆

  options:

  1. login
  2. register

        """)
    choice = input("  select: ").strip().lower()
    if choice == '1':
        current_screen[0] = "login"
    elif choice == '2':
        current_screen[0] = "register"
    else:
        print(("\ninvalid choice."))
        input(("press enter to continue..."))
        current_screen[0] = "welcome"

def login_screen():
    """
    allows the user to log in by entering their username and password.
    checks the credentials and logs them in if correct.
    """
    clear_screen()
    show_header()
    username = input(("enter your username: ")).strip()
    password = getpass(("enter your password: ")).strip()

    user_file = os.path.join('users', f'{username}.json')

    if not os.path.exists(user_file):
        print(("\ninvalid username or password."))
        input(("press enter to continue..."))
        current_screen[0] = "welcome"
        return

    # load user data from file
    user_data = load_user_data(username)

    stored_hash = base64.b64decode(
        user_data['password_hash'].encode('utf-8'))

    if bcrypt.checkpw(password.encode(), stored_hash):
        print(("\nlogin successful!"))
        current_user[0] = username
        input(("press enter to continue..."))
        current_screen[0] = "main_menu"
    else:
        print(("\ninvalid username or password."))
        input(("press enter to continue..."))
        current_screen[0] = "welcome"

def register_screen():
    """
    allows a new user to create an account by entering a username and password.
    saves the new user data to a file.
    """
    clear_screen()
    print("""

   °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.
  °                               °
  °    let's get you registered!  °
  °                               °
   °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.

   note: don't reuse old passwords!!

⋆˖⁺‧₊☽◯☾₊‧⁺˖⋆⋆˖⁺‧₊☽◯☾₊‧⁺˖⋆⋆˖⁺‧₊☽◯☾₊‧⁺˖⋆

        """)
    username = input(("choose a username: ")).strip()
    password = getpass(("choose a password: ")).strip()
    confirm_password = getpass(("confirm your password:  ")).strip()

    if password != confirm_password:
        print(("passwords do not match."))
        input(f("press enter to continue..."))
        current_screen[0] = "welcome"
        return

    user_file = os.path.join('users', f'{username}.json')

    if os.path.exists(user_file):
        print(("username already exists!"))
        input(("press enter to continue..."))
        current_screen[0] = "welcome"
        return

    # hash the password with bcrypt
    password_hash = bcrypt.hashpw(password.encode(),
                                  bcrypt.gensalt())
    password_hash_encoded = base64.b64encode(
        password_hash).decode('utf-8')

    # create the user data
    user_data = {
        'password_hash': password_hash_encoded,
        'display_name': display_name,
        'bio': '',
        'pronouns': '',
        'age': '',
        'following': [],
        'notifications': []
    }

    # save user data to file
    save_user_data(username, user_data)

    print(("\nregistration successful! welcome to dreamland :3"))
    input(("press enter to continue..."))
    current_screen[0] = "welcome"

def main_menu_screen():
    """
    displays the main menu after the user logs in.
    from here, they can navigate to different parts of the app.
    """
    clear_screen()
    show_header(current_user[0])  # pass username to header
    # check for notifications
    user_data = load_user_data(current_user[0])
    notifications = user_data.get('notifications', [])
    notification_text = ""
    if notifications:
        notification_text = color_text(f"you have {len(notifications)} new notifications!", '33')  # yellow text
    menu_text = f"{notification_text}\n"
    print((menu_text))
    options = [
        "1. view feed",         "2. create a post",
        "3. my profile",        "4. messages",
        "5. notifications",     "6. edit profile",
        "7. discover",          "8. see friends",
        "9. logout",
    ]
    print(format_menu_options(options))
    show_footer()
    choice = input(("enter your choice: ")).strip()
    if choice == '1':
        current_screen[0] = "feed"
    elif choice == '2':
        current_screen[0] = "create_post"
    elif choice == '3':
        current_screen[0] = "my_posts"
    elif choice == '4':
        current_screen[0] = "direct_messages"
    elif choice == '5':
        current_screen[0] = "notifications"
    elif choice == '6':
        current_screen[0] = "edit_profile"
    elif choice == '7':
        current_screen[0] = "discover_users"
    elif choice == '8':
        current_screen[0] = "friends_list"
    elif choice == '9':
        current_screen[0] = "logout"
    else:
        print(("\ninvalid choice."))
        input(("press enter to continue..."))
        current_screen[0] = "main_menu"

def logout_screen():
    """
    logs the user out and returns to the welcome screen.
    """
    current_user[0] = None
    print(("\nyou have been logged out."))
    input(("press enter to continue..."))
    current_screen[0] = "welcome"

#------------------------------------------------------------------------------
# Main Loop
#------------------------------------------------------------------------------
if __name__ == '__main__':
    while True:
        if current_screen[0] == "splash":
            show_splash_screen()
        elif current_screen[0] == "welcome":
            welcome_screen()
        elif current_screen[0] == "login":
            login_screen()
        elif current_screen[0] == "register":
            register_screen()
        elif current_screen[0] == "main_menu":
            main_menu_screen()
        elif current_screen[0] == "edit_profile":
            edit_profile_screen()
        elif current_screen[0] == "discover_users":
            discover_users_screen()
        elif current_screen[0] == "friends_list":
            friends_list_screen()
        elif current_screen[0] == "create_post":
            create_post_screen()
        elif current_screen[0] == "my_posts":
            my_posts_screen()
        elif current_screen[0] == "feed":
            feed_screen()
        elif current_screen[0] == "direct_messages":
            direct_messages_screen()
        elif current_screen[0] == "notifications":
            notifications_screen()
        elif current_screen[0] == "logout":
            logout_screen()
        else:
            # if the screen is not recognized, go back to welcome
            current_screen[0] = "welcome"
