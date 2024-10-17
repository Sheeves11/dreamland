#------------------------------------------------------------------------------
# friends.py
#------------------------------------------------------------------------------
# this file handles everything related to discovering new users and managing friends.
# users can view a list of all users, follow them, and manage their friends list.
#------------------------------------------------------------------------------

from helpers import (
    clear_screen,
    show_header,
    show_footer,
    format_text,
    wrap_text,
    format_menu_options,
    color_text,
    current_screen,
    current_user,
)
from data import load_user_data
from user import user_profile_screen
import os

def discover_users_screen():
    """
    allows the user to discover new users.
    displays a list of all users with options to view profiles.
    """
    while True:
        clear_screen()
        show_header(current_user[0])
        print(format_text("discover users\n"))
        user_files = os.listdir('users')
        all_users = [user_file[:-5] for user_file in user_files if user_file.endswith('.json')]

        if not all_users:
            print(format_text("no users found."))
            input(format_text("press enter to continue..."))
            current_screen[0] = "main_menu"
            return
        else:
            user_data = load_user_data(current_user[0])
            following = user_data.get('following', [])

            index = 1
            for user in all_users:
                if user == current_user[0]:
                    continue  # skip the current user
                user_info = load_user_data(user)
                display_name = user_info.get('display_name', user)
                bio = user_info.get('bio', 'no bio available.')
                if user in following:
                    username_display = color_text(user, '32')  # green if following
                else:
                    username_display = color_text(user, '34')  # blue otherwise
                user_text = f"{index}. {display_name} (@{username_display})\nbio: {bio}\n"
                print(format_text("-" * 50))
                print(format_text(user_text))
                print(format_text("-" * 50 + "\n"))
                index += 1

            print(format_text("enter the number of a user to view their profile."))
            print(format_text("type 'back' to return to the main menu.\n"))
            choice = input(format_text("enter your choice: ")).strip()

            if choice.lower() == 'back':
                current_screen[0] = "main_menu"
                return

            try:
                choice = int(choice)
                selected_users = [u for u in all_users if u != current_user[0]]
                if 1 <= choice <= len(selected_users):
                    selected_user = selected_users[choice - 1]
                    user_profile_screen(selected_user)
                else:
                    print(format_text("invalid choice. please try again."))
                    input(format_text("press enter to continue..."))
            except ValueError:
                print(format_text("invalid input. please try again."))
                input(format_text("press enter to continue..."))

def friends_list_screen():
    """
    displays the list of users that the current user is following.
    allows the user to view their profiles.
    """
    while True:
        clear_screen()
        show_header(current_user[0])
        print(format_text("your friends\n"))
        user_data = load_user_data(current_user[0])
        following = user_data.get('following', [])

        if not following:
            print(format_text("you are not following anyone yet."))
            input(format_text("press enter to continue..."))
            current_screen[0] = "main_menu"
            return

        for idx, friend in enumerate(following, start=1):
            friend_data = load_user_data(friend)
            display_name = friend_data.get('display_name', friend)
            bio = friend_data.get('bio', 'no bio available.')
            friend_info = f"{idx}. {display_name} (@{friend})\nbio: {bio}\n"
            print(format_text("-" * 50))
            print(format_text(friend_info))
            print(format_text("-" * 50 + "\n"))

        print(format_text("enter the number of a friend to view their profile."))
        print(format_text("type 'back' to return to the main menu.\n"))
        choice = input(format_text("enter your choice: ")).strip()

        if choice.lower() == 'back':
            current_screen[0] = "main_menu"
            return

        try:
            choice = int(choice)
            if 1 <= choice <= len(following):
                selected_friend = following[choice - 1]
                user_profile_screen(selected_friend)
            else:
                print(format_text("invalid choice. please try again."))
                input(format_text("press enter to continue..."))
        except ValueError:
            print(format_text("invalid input. please try again."))
            input(format_text("press enter to continue..."))
