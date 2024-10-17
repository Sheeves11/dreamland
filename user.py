#------------------------------------------------------------------------------
# user.py
#------------------------------------------------------------------------------
# this file handles everything related to the user's profile.
# users can edit their profile and view other users' profiles.
#------------------------------------------------------------------------------

from helpers import (
    clear_screen,
    show_header,
    show_footer,
    format_text,
    wrap_text,
    format_menu_options,
    current_screen,
    current_user,
)
from data import load_user_data, save_user_data, save_notifications
from feed import view_user_posts
from chat import send_message_to_user

def edit_profile_screen():
    """
    lets the user edit their profile information like display name, bio, etc.
    """
    clear_screen()
    show_header(current_user[0])
    print(format_text("edit your profile\n"))
    user_data = load_user_data(current_user[0])

    # get current values or empty strings if not set
    display_name = input(format_text(f"display name [{user_data.get('display_name', '')}]: ")).strip()
    bio = input(format_text(f"bio [{user_data.get('bio', '')}]: ")).strip()
    pronouns = input(format_text(f"pronouns [{user_data.get('pronouns', '')}]: ")).strip()
    age = input(format_text(f"age [{user_data.get('age', '')}]: ")).strip()

    # update the user data if new values are provided
    if display_name:
        user_data['display_name'] = display_name
    if bio:
        user_data['bio'] = bio
    if pronouns:
        user_data['pronouns'] = pronouns
    if age:
        user_data['age'] = age

    save_user_data(current_user[0], user_data)
    print(format_text("profile updated successfully!"))
    input(format_text("press enter to continue..."))
    current_screen[0] = "main_menu"

def user_profile_screen(selected_user):
    """
    displays another user's profile.
    allows the current user to follow/unfollow, view posts, or send a message.
    """
    while True:
        clear_screen()
        show_header(current_user[0])
        user_data = load_user_data(selected_user)
        display_name = user_data.get('display_name', selected_user)
        bio = user_data.get('bio', 'no bio available.')
        pronouns = user_data.get('pronouns', '')
        age = user_data.get('age', '')

        current_user_data = load_user_data(current_user[0])
        following = current_user_data.get('following', [])

        profile_info = f"display name: {display_name}\npronouns: {pronouns} | age: {age}\nbio: {bio}\n"
        print(format_text(profile_info))

        options = []
        if selected_user != current_user[0]:
            # if the user is not viewing their own profile
            if selected_user in following:
                follow_status = f"1. unfollow {selected_user}"
            else:
                follow_status = f"1. follow {selected_user}"
            options.append(follow_status)
            options.append("2. view posts")
            options.append("3. send message")
        else:
            # if the user is viewing their own profile
            print(format_text("you are viewing your own profile."))
            options.append("1. view my posts")

        options.append("enter: go back")
        print(format_menu_options(options))
        show_footer()
        choice = input(format_text("enter your choice: ")).strip()

        if choice == '':
            return  # go back to the previous screen

        if selected_user != current_user[0]:
            if choice == '1':
                # toggle follow/unfollow
                if selected_user in following:
                    following.remove(selected_user)
                    print(format_text(f"you have unfollowed {selected_user}."))
                else:
                    following.append(selected_user)
                    print(format_text(f"you are now following {selected_user}."))
                    notification = f"{current_user[0]} started following you."
                    save_notifications(selected_user, notification)
                current_user_data['following'] = following
                save_user_data(current_user[0], current_user_data)
                input(format_text("press enter to continue..."))
            elif choice == '2':
                # view the selected user's posts
                view_user_posts(selected_user)
            elif choice == '3':
                # send a direct message to the selected user
                send_message_to_user(selected_user)
                input(format_text("press enter to continue..."))
            else:
                print(format_text("invalid choice. please try again."))
                input(format_text("press enter to continue..."))
        else:
            if choice == '1':
                # view the current user's own posts
                current_screen[0] = "my_posts"
                return
            else:
                print(format_text("invalid choice. please try again."))
                input(format_text("press enter to continue..."))
