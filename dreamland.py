#!/usr/bin/env python

import os
import bcrypt
import base64
import json
from getpass import getpass
import sys
from datetime import datetime, timedelta

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#                       welcome to dreamland, darling
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#   [dreamland.py]:
#           welcome_screen
#           login_screen
#           register_screen
#           main_menu_screen
#           bio_screen
#           view_bios_screen
#           friends_list_screen
#           friend_options_screen
#           user_profile_screen
#           post_status_screen
#           view_own_posts_screen
#           feed_screen
#           dm_screen
#           notifications_screen
#           logout_screen
#           helper functions (e.g., clear_screen, header, display_hearts)
#------------------------------------------------------------------------------
# Global variables
loop = True
screen = "welcome"
current_user = None
logged_in_users = set()

# Ensure necessary directories and files exist
if not os.path.exists('users'):
    os.makedirs('users')

if not os.path.exists('posts.json'):
    with open('posts.json', 'w') as f:
        json.dump([], f)

if not os.path.exists('dms.json'):
    with open('dms.json', 'w') as f:
        json.dump({}, f)  # Dictionary with usernames as keys

#------------------------------------------------------------------------------
# Helper Functions
#------------------------------------------------------------------------------

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def header():
    print("\n\n\n\n" + " " * 10 + "-" * 60)
    print(" " * 10 + "welcome to dreamland, darling")
    print(" " * 10 + "-" * 60 + "\n")

def indent_text(text, indent=10):
    indented_lines = [" " * indent + line for line in text.split('\n')]
    return '\n'.join(indented_lines)

def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def load_posts():
    with open('posts.json', 'r') as f:
        return json.load(f)

def save_posts(posts):
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

def load_user_data(username):
    user_file = os.path.join('users', f'{username}.txt')
    with open(user_file, 'r') as f:
        return json.load(f)

def save_user_data(username, data):
    user_file = os.path.join('users', f'{username}.txt')
    with open(user_file, 'w') as f:
        json.dump(data, f, indent=4)

def display_hearts(hearts_list):
    total_hearts = len(hearts_list)
    if total_hearts == 0:
        return color_text("<3", '90')  # Grey heart for no hearts
    hearts_to_display = min(total_hearts, 10)
    heart_string = color_text("<3 ", '31') * hearts_to_display  # Red hearts
    heart_string = heart_string.strip()
    if total_hearts > 10:
        heart_string += f" +{total_hearts - 10}"
    return heart_string

def load_dms():
    with open('dms.json', 'r') as f:
        return json.load(f)

def save_dms(dms):
    with open('dms.json', 'w') as f:
        json.dump(dms, f, indent=4)

def save_notifications(username, notification):
    user_data = load_user_data(username)
    notifications = user_data.get('notifications', [])
    notifications.append(notification)
    user_data['notifications'] = notifications
    save_user_data(username, user_data)

def format_timestamp(timestamp_str):
    if not timestamp_str:
        return "unknown time"
    try:
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return "invalid time format"
    now = datetime.now()
    today = now.date()
    time_format = "%I:%M%p"
    if timestamp.date() == today:
        return f"today at {timestamp.strftime(time_format).lstrip('0').lower()}"
    elif timestamp.date() == today - timedelta(days=1):
        return f"yesterday at {timestamp.strftime(time_format).lstrip('0').lower()}"
    else:
        return f"{timestamp.strftime('%-m/%-d')} at {timestamp.strftime(time_format).lstrip('0').lower()}"

#------------------------------------------------------------------------------
# Screen Functions
#------------------------------------------------------------------------------

def welcome_screen():
    global screen
    clear_screen()
    header()
    text = "welcome to dreamland\n\n1. log in\n2. register\n3. exit\n"
    print(indent_text(text))
    choice = input(indent_text("enter your choice: ")).strip()
    if choice == '1':
        screen = "login"
    elif choice == '2':
        screen = "register"
    elif choice == '3':
        print(indent_text("\ngoodbye!"))
        sys.exit()
    else:
        print(indent_text("\ninvalid choice."))
        input(indent_text("press enter to continue..."))
        screen = "welcome"

def login_screen():
    global screen, current_user
    clear_screen()
    header()
    print(indent_text("login to your account\n"))
    username = input(indent_text("enter your username: ")).strip()
    password = getpass(indent_text("enter your password: ")).strip()

    user_file = os.path.join('users', f'{username}.txt')

    if not os.path.exists(user_file):
        print(indent_text("\ninvalid username or password."))
        input(indent_text("press enter to continue..."))
        screen = "welcome"
        return

    # Load user data from file
    user_data = load_user_data(username)

    stored_hash = base64.b64decode(
        user_data['password_hash'].encode('utf-8'))

    if bcrypt.checkpw(password.encode(), stored_hash):
        print(indent_text("\nlogin successful!"))
        current_user = username
        logged_in_users.add(username)
        input(indent_text("press enter to continue..."))
        screen = "main_menu"
    else:
        print(indent_text("\ninvalid username or password."))
        input(indent_text("press enter to continue..."))
        screen = "welcome"

def register_screen():
    global screen
    clear_screen()
    header()
    print(indent_text("register a new account\n"))
    username = input(indent_text("choose a username: ")).strip()
    display_name = input(indent_text("enter your display name: ")).strip()
    password = getpass(indent_text("choose a password: ")).strip()
    confirm_password = getpass(indent_text("confirm your password: ")).strip()

    if password != confirm_password:
        print(indent_text("passwords do not match."))
        input(indent_text("press enter to continue..."))
        screen = "welcome"
        return

    user_file = os.path.join('users', f'{username}.txt')

    if os.path.exists(user_file):
        print(indent_text("username already exists!"))
        input(indent_text("press enter to continue..."))
        screen = "welcome"
        return

    # Hash the password with bcrypt
    password_hash = bcrypt.hashpw(password.encode(),
                                  bcrypt.gensalt())
    password_hash_encoded = base64.b64encode(
        password_hash).decode('utf-8')

    # Create the data before making the .json file
    user_data = {
        'password_hash': password_hash_encoded,
        'display_name': display_name,
        'bio': '',
        'pronouns': '',
        'age': '',
        'follows': [],
        'notifications': []
    }

    # Save user data to file with nice formatting
    save_user_data(username, user_data)

    print(indent_text("\nregistration successful! welcome to dreamland :3"))
    input(indent_text("press enter to continue..."))
    screen = "welcome"

def main_menu_screen():
    global screen
    clear_screen()
    header()
    # Check for notifications
    user_data = load_user_data(current_user)
    notifications = user_data.get('notifications', [])
    notification_text = ""
    if notifications:
        notification_text = color_text(f"you have {len(notifications)} new notifications!", '33')  # Yellow text
    menu_text = f"{notification_text}\nlogged in as: {current_user}\n\n1. view feed\n2. post a status\n3. view your posts\n4. direct messages\n5. notifications\n6. edit profile\n7. discover friends\n8. friends list\n9. logout\n"
    print(indent_text(menu_text))
    choice = input(indent_text("enter your choice: ")).strip()

    if choice == '1':
        screen = "feed"
    elif choice == '2':
        screen = "post_status"
    elif choice == '3':
        screen = "view_own_posts"
    elif choice == '4':
        screen = "dm"
    elif choice == '5':
        screen = "notifications"
    elif choice == '6':
        screen = "bio"
    elif choice == '7':
        screen = "view_bios"
    elif choice == '8':
        screen = "friends_list"
    elif choice == '9':
        screen = "logout"
    else:
        print(indent_text("\ninvalid choice."))
        input(indent_text("press enter to continue..."))
        screen = "main_menu"

def bio_screen():
    global screen
    clear_screen()
    header()
    print(indent_text("edit your profile\n"))
    user_data = load_user_data(current_user)

    display_name = input(indent_text(f"enter your display name [{user_data.get('display_name', '')}]: ")).strip()
    bio = input(indent_text(f"enter your bio [{user_data.get('bio', '')}]: ")).strip()
    pronouns = input(indent_text(f"enter your pronouns [{user_data.get('pronouns', '')}]: ")).strip()
    age = input(indent_text(f"enter your age [{user_data.get('age', '')}]: ")).strip()

    if display_name:
        user_data['display_name'] = display_name
    if bio:
        user_data['bio'] = bio
    if pronouns:
        user_data['pronouns'] = pronouns
    if age:
        user_data['age'] = age

    save_user_data(current_user, user_data)
    print(indent_text("\nprofile updated!"))
    input(indent_text("press enter to continue..."))
    screen = "main_menu"

def view_bios_screen():
    global screen
    clear_screen()
    header()
    print(indent_text("discover\n"))

    user_files = os.listdir('users')
    all_users = [user_file[:-4] for user_file in user_files
                 if user_file.endswith('.txt')]

    if not all_users:
        print(indent_text("no users found."))
        input(indent_text("press enter to continue..."))
        screen = "main_menu"
        return
    else:
        # Load current user's follow list
        user_data = load_user_data(current_user)
        follows = user_data.get('follows', [])

        for idx, user in enumerate(all_users, start=1):
            if user == current_user:
                username_display = color_text(user, '34')  # Blue
            elif user in follows:
                username_display = color_text(user, '32')  # Green
            else:
                username_display = user

            print(indent_text(f"{idx}. username: {username_display}"))

        # View User Profile Options
        print(indent_text("\nenter the number of a user to view their profile."))
        print(indent_text("press enter to return to the main menu.\n"))
        choice = input(indent_text("enter your choice: ")).strip()

        if choice == '':
            screen = "main_menu"
            return

        try:
            choice = int(choice)
            if 1 <= choice <= len(all_users):
                selected_user = all_users[choice - 1]
                screen = ("user_profile", selected_user)
            else:
                print(indent_text("\ninvalid choice."))
                input(indent_text("press enter to continue..."))
        except ValueError:
            print(indent_text("\ninvalid input."))
            input(indent_text("press enter to continue..."))

def friends_list_screen():
    global screen
    clear_screen()
    header()
    print(indent_text("your friends\n"))
    user_data = load_user_data(current_user)
    follows = user_data.get('follows', [])

    if not follows:
        print(indent_text("you are not following anyone yet."))
        input(indent_text("press enter to continue..."))
        screen = "main_menu"
        return

    for idx, friend in enumerate(follows, start=1):
        friend_data = load_user_data(friend)
        display_name = friend_data.get('display_name', friend)
        print(indent_text(f"{idx}. {display_name} (@{friend})"))

    print(indent_text("\nenter the number of a friend to view options."))
    print(indent_text("press enter to return to the main menu.\n"))
    choice = input(indent_text("enter your choice: ")).strip()

    if choice == '':
        screen = "main_menu"
        return

    try:
        choice = int(choice)
        if 1 <= choice <= len(follows):
            selected_friend = follows[choice - 1]
            friend_options_screen(selected_friend)
        else:
            print(indent_text("\ninvalid choice."))
            input(indent_text("press enter to continue..."))
    except ValueError:
        print(indent_text("\ninvalid input."))
        input(indent_text("press enter to continue..."))

def friend_options_screen(friend_username):
    while True:
        clear_screen()
        header()
        friend_data = load_user_data(friend_username)
        display_name = friend_data.get('display_name', friend_username)
        print(indent_text(f"{display_name}'s profile\n"))
        print(indent_text("options:"))
        print(indent_text("1. view profile"))
        print(indent_text("2. send message"))
        print(indent_text("press enter to go back.\n"))
        choice = input(indent_text("enter your choice: ")).strip()

        if choice == '':
            return
        elif choice == '1':
            user_profile_screen(friend_username)
            return
        elif choice == '2':
            send_direct_message(friend_username)
        else:
            print(indent_text("\ninvalid choice."))
            input(indent_text("press enter to continue..."))

def user_profile_screen(selected_user):
    global screen
    while True:
        clear_screen()
        header()
        user_data = load_user_data(selected_user)
        display_name = user_data.get('display_name', selected_user)
        bio = user_data.get('bio', 'no bio available.')
        pronouns = user_data.get('pronouns', '')
        age = user_data.get('age', '')

        # Load current user's follow list
        current_user_data = load_user_data(current_user)
        follows = current_user_data.get('follows', [])

        profile_info = f"display name: {display_name}\npronouns: {pronouns}\nage: {age}\nbio: {bio}\n"
        print(indent_text(profile_info))

        # Follow/Unfollow option
        if selected_user != current_user:
            if selected_user in follows:
                follow_status = "unfollow"
            else:
                follow_status = "follow"
            print(indent_text(f"1. {follow_status} {selected_user}"))
        else:
            print(indent_text("you are viewing your own profile."))

        print(indent_text("2. view posts"))
        if selected_user != current_user:
            print(indent_text("3. send direct message"))
        print(indent_text("press enter to return to the previous menu.\n"))

        choice = input(indent_text("enter your choice: ")).strip()

        if choice == '':
            return

        if selected_user != current_user:
            if choice == '1':
                # Follow/Unfollow user
                if selected_user in follows:
                    follows.remove(selected_user)
                    print(indent_text(f"\nyou have unfollowed {selected_user}."))
                else:
                    follows.append(selected_user)
                    print(indent_text(f"\nyou are now following {selected_user}."))
                    # Send notification to the followed user
                    notification = f"{current_user} started following you."
                    save_notifications(selected_user, notification)
                # Update current user's follow list
                current_user_data['follows'] = follows
                save_user_data(current_user, current_user_data)
                input(indent_text("press enter to continue..."))
            elif choice == '2':
                view_user_posts(selected_user)
            elif choice == '3':
                send_direct_message(selected_user)
            else:
                print(indent_text("\ninvalid choice."))
                input(indent_text("press enter to continue..."))
        else:
            if choice == '2':
                view_own_posts_screen()
            else:
                print(indent_text("\ninvalid choice."))
                input(indent_text("press enter to continue..."))

def view_user_posts(username):
    clear_screen()
    header()
    user_data = load_user_data(username)
    display_name = user_data.get('display_name', username)
    bio = user_data.get('bio', 'no bio available.')
    pronouns = user_data.get('pronouns', '')
    age = user_data.get('age', '')

    profile_header = f"{display_name} (@{username})\nPronouns: {pronouns} | Age: {age}\nBio: {bio}\n"
    print(indent_text(profile_header))

    posts = load_posts()
    user_posts = [post for post in posts if post['user'] == username]
    user_posts.reverse()  # Most recent first

    if not user_posts:
        print(indent_text(f"{username} hasn't posted anything yet."))
        input(indent_text("press enter to continue..."))
        return

    page = 0
    page_size = 5
    total_pages = (len(user_posts) - 1) // page_size + 1

    while True:
        clear_screen()
        header()
        print(indent_text(profile_header))
        print(indent_text(f"{display_name}'s posts (page {page + 1} of {total_pages})\n"))

        start = page * page_size
        end = start + page_size
        for idx, post in enumerate(user_posts[start:end], start=1):
            heart_string = display_hearts(post.get('hearts', []))
            timestamp_formatted = format_timestamp(post['timestamp'])
            post_content = f"{idx}. {timestamp_formatted}\n   {post['content']}\n   hearts: {heart_string}\n"
            print(indent_text("-" * 60))
            print(indent_text(post_content))
            print(indent_text("-" * 60 + "\n"))

        print(indent_text("options:"))
        print(indent_text("n - next page"))
        print(indent_text("p - previous page"))
        print(indent_text("enter the number of a post to interact with it."))
        print(indent_text("type 'back' to return to the profile.\n"))
        choice = input(indent_text("enter your choice: ")).strip()

        if choice.lower() == 'back':
            return
        elif choice.lower() == 'n':
            if page < total_pages - 1:
                page += 1
            else:
                print(indent_text("\nyou are on the last page."))
                input(indent_text("press enter to continue..."))
        elif choice.lower() == 'p':
            if page > 0:
                page -= 1
            else:
                print(indent_text("\nyou are on the first page."))
                input(indent_text("press enter to continue..."))
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(user_posts[start:end]):
                    selected_post = user_posts[start + idx]
                    interact_with_post(selected_post)
                else:
                    print(indent_text("\ninvalid choice."))
                    input(indent_text("press enter to continue..."))
            except ValueError:
                print(indent_text("\ninvalid input."))
                input(indent_text("press enter to continue..."))

def view_own_posts_screen():
    global screen
    clear_screen()
    header()
    user_data = load_user_data(current_user)
    display_name = user_data.get('display_name', current_user)
    bio = user_data.get('bio', 'no bio available.')
    pronouns = user_data.get('pronouns', '')
    age = user_data.get('age', '')

    profile_header = f"{display_name} (@{current_user})\nPronouns: {pronouns} | Age: {age}\nBio: {bio}\n"
    print(indent_text(profile_header))

    posts = load_posts()
    user_posts = [post for post in posts if post['user'] == current_user]
    user_posts.reverse()  # Most recent first

    if not user_posts:
        print(indent_text("you haven't posted anything yet."))
        input(indent_text("press enter to continue..."))
        screen = "main_menu"
        return

    page = 0
    page_size = 5
    total_pages = (len(user_posts) - 1) // page_size + 1

    while True:
        clear_screen()
        header()
        print(indent_text(profile_header))
        print(indent_text(f"your posts (page {page + 1} of {total_pages})\n"))

        start = page * page_size
        end = start + page_size
        for idx, post in enumerate(user_posts[start:end], start=1):
            heart_string = display_hearts(post.get('hearts', []))
            timestamp_formatted = format_timestamp(post['timestamp'])
            post_content = f"{idx}. {timestamp_formatted}\n   {post['content']}\n   hearts: {heart_string}\n"
            print(indent_text("-" * 60))
            print(indent_text(post_content))
            print(indent_text("-" * 60 + "\n"))

        print(indent_text("options:"))
        print(indent_text("n - next page"))
        print(indent_text("p - previous page"))
        print(indent_text("enter the number of a post to interact with it."))
        print(indent_text("press enter to return to the main menu.\n"))
        choice = input(indent_text("enter your choice: ")).strip()

        if choice == '':
            screen = "main_menu"
            return
        elif choice.lower() == 'n':
            if page < total_pages - 1:
                page += 1
            else:
                print(indent_text("\nyou are on the last page."))
                input(indent_text("press enter to continue..."))
        elif choice.lower() == 'p':
            if page > 0:
                page -= 1
            else:
                print(indent_text("\nyou are on the first page."))
                input(indent_text("press enter to continue..."))
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(user_posts[start:end]):
                    selected_post = user_posts[start + idx]
                    view_post_options(selected_post)
                else:
                    print(indent_text("\ninvalid choice."))
                    input(indent_text("press enter to continue..."))
            except ValueError:
                print(indent_text("\ninvalid input."))
                input(indent_text("press enter to continue..."))

def view_post_options(post):
    while True:
        clear_screen()
        header()
        post_content = f"post content: {post['content']}\nposted on: {format_timestamp(post['timestamp'])}\n"
        heart_string = display_hearts(post.get('hearts', []))
        options_text = f"\nhearts: {heart_string}\n\n1. edit post\n2. delete post\n3. view hearts\n4. view comments\npress enter to go back\n"
        print(indent_text(post_content))
        print(indent_text(options_text))
        choice = input(indent_text("enter your choice: ")).strip()

        if choice == '':
            return
        elif choice == '1':
            new_content = input(indent_text("enter new content: ")).strip()
            if new_content == '':
                print(indent_text("\ncontent cannot be empty."))
                input(indent_text("press enter to continue..."))
            else:
                posts = load_posts()
                for p in posts:
                    if p['id'] == post['id']:
                        p['content'] = new_content
                        break
                save_posts(posts)
                print(indent_text("\npost updated."))
                post['content'] = new_content  # Update the local variable
                input(indent_text("press enter to continue..."))
        elif choice == '2':
            posts = load_posts()
            posts = [p for p in posts if p['id'] != post['id']]
            save_posts(posts)
            print(indent_text("\npost deleted."))
            input(indent_text("press enter to continue..."))
            return  # Exit the function after deleting
        elif choice == '3':
            view_hearts(post)
        elif choice == '4':
            view_comments(post)
        else:
            print(indent_text("\ninvalid choice."))
            input(indent_text("press enter to continue..."))

def feed_screen():
    global screen
    clear_screen()
    header()
    print(indent_text("your feed\n"))

    # Load current user's follow list
    user_data = load_user_data(current_user)
    follows = user_data.get('follows', [])

    posts = load_posts()
    # Include own posts
    feed_posts = [post for post in posts if post['user'] in follows or post['user'] == current_user]

    if not feed_posts:
        print(indent_text("no posts to show. follow users to see their posts."))
        input(indent_text("press enter to continue..."))
        screen = "main_menu"
        return

    feed_posts.reverse()  # Most recent first
    page = 0
    page_size = 5
    total_pages = (len(feed_posts) - 1) // page_size + 1

    while True:
        clear_screen()
        header()
        print(indent_text(f"your feed (page {page + 1} of {total_pages})\n"))

        start = page * page_size
        end = start + page_size
        for idx, post in enumerate(feed_posts[start:end], start=1):
            heart_string = display_hearts(post.get('hearts', []))
            timestamp_formatted = format_timestamp(post['timestamp'])
            post_user_data = load_user_data(post['user'])
            display_name = post_user_data.get('display_name', post['user'])
            post_content = f"{idx}. {display_name} (@{post['user']}) -> {timestamp_formatted}\n   {post['content']}\n   hearts: {heart_string}\n"
            print(indent_text("-" * 60))
            print(indent_text(post_content))
            print(indent_text("-" * 60 + "\n"))

        print(indent_text("options:"))
        print(indent_text("n - next page"))
        print(indent_text("p - previous page"))
        print(indent_text("enter the number of a post to interact with it."))
        print(indent_text("press enter to return to the main menu.\n"))
        choice = input(indent_text("enter your choice: ")).strip()

        if choice == '':
            screen = "main_menu"
            return
        elif choice.lower() == 'n':
            if page < total_pages - 1:
                page += 1
            else:
                print(indent_text("\nyou are on the last page."))
                input(indent_text("press enter to continue..."))
        elif choice.lower() == 'p':
            if page > 0:
                page -= 1
            else:
                print(indent_text("\nyou are on the first page."))
                input(indent_text("press enter to continue..."))
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(feed_posts[start:end]):
                    selected_post = feed_posts[start + idx]
                    interact_with_post(selected_post)
                else:
                    print(indent_text("\ninvalid choice."))
                    input(indent_text("press enter to continue..."))
            except ValueError:
                print(indent_text("\ninvalid input."))
                input(indent_text("press enter to continue..."))

def interact_with_post(post):
    while True:
        clear_screen()
        header()
        post_user_data = load_user_data(post['user'])
        display_name = post_user_data.get('display_name', post['user'])
        post_content = f"post by {display_name} (@{post['user']}) on {format_timestamp(post['timestamp'])}\n\n   {post['content']}\n"
        heart_string = display_hearts(post.get('hearts', []))
        options_text = f"hearts: {heart_string}\n\noptions:\n1. heart/unheart\n2. view hearts\n3. comment\n4. view comments\n5. repost\n6. quote post\npress enter to go back\n"
        print(indent_text(post_content))
        print(indent_text(options_text))
        choice = input(indent_text("enter your choice: ")).strip()

        if choice == '':
            return
        elif choice == '1':
            heart_unheart_post(post)
        elif choice == '2':
            view_hearts(post)
        elif choice == '3':
            add_comment(post)
        elif choice == '4':
            view_comments(post)
        elif choice == '5':
            repost(post)
        elif choice == '6':
            quote_post(post)
        else:
            print(indent_text("\ninvalid choice."))
            input(indent_text("press enter to continue..."))

def heart_unheart_post(post):
    if 'hearts' not in post:
        post['hearts'] = []

    if current_user in post['hearts']:
        post['hearts'].remove(current_user)
        print(indent_text("\nyou unhearted the post."))
    else:
        post['hearts'].append(current_user)
        print(indent_text("\nyou hearted the post."))
        # Send notification to the post owner
        if current_user != post['user']:
            notification = f"{current_user} hearted your post."
            save_notifications(post['user'], notification)

    # Update the post in the database
    posts = load_posts()
    for p in posts:
        if p['id'] == post['id']:
            p['hearts'] = post['hearts']
            break
    save_posts(posts)
    input(indent_text("press enter to continue..."))

def view_hearts(post):
    clear_screen()
    header()
    print(indent_text("users who hearted this post:\n"))
    if not post.get('hearts'):
        print(indent_text("no one has hearted this post yet."))
    else:
        for user in post['hearts']:
            user_data = load_user_data(user)
            display_name = user_data.get('display_name', user)
            print(indent_text(f"- {display_name} (@{user})"))
    input(indent_text("\npress enter to go back."))

def add_comment(post):
    comment = input(indent_text("enter your comment: ")).strip()
    if comment == '':
        print(indent_text("\ncomment cannot be empty."))
        input(indent_text("press enter to continue..."))
    else:
        if 'comments' not in post:
            post['comments'] = []
        post['comments'].append({
            'user': current_user,
            'comment': comment,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        # Update the post in the database
        posts = load_posts()
        for p in posts:
            if p['id'] == post['id']:
                p['comments'] = post['comments']
                break
        save_posts(posts)
        print(indent_text("\ncomment added!"))
        # Send notification to the post owner
        if current_user != post['user']:
            notification = f"{current_user} commented on your post."
            save_notifications(post['user'], notification)
        input(indent_text("press enter to continue..."))

def view_comments(post):
    clear_screen()
    header()
    print(indent_text("comments:\n"))
    if 'comments' not in post or not post['comments']:
        print(indent_text("no comments yet."))
    else:
        for idx, comment in enumerate(post['comments'], start=1):
            timestamp_formatted = format_timestamp(comment['timestamp'])
            user_data = load_user_data(comment['user'])
            display_name = user_data.get('display_name', comment['user'])
            comment_text = f"{display_name} (@{comment['user']}) -> {timestamp_formatted}\n   {comment['comment']}\n"
            print(indent_text(comment_text))
    input(indent_text("press enter to go back."))

def repost(post):
    posts = load_posts()
    new_post = {
        'id': len(posts) + 1,
        'user': current_user,
        'content': f"Reposted from {post['user']}: {post['content']}",
        'hearts': [],
        'comments': [],
        'reposts': [],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    posts.append(new_post)
    save_posts(posts)
    print(indent_text("\npost reposted!"))
    # Send notification to the original post owner
    if current_user != post['user']:
        notification = f"{current_user} reposted your post."
        save_notifications(post['user'], notification)
    input(indent_text("press enter to continue..."))

def quote_post(post):
    quote = input(indent_text("enter your comment on the post: ")).strip()
    if quote == '':
        print(indent_text("\nyou cannot post an empty quote."))
        input(indent_text("press enter to continue..."))
    else:
        posts = load_posts()
        new_post = {
            'id': len(posts) + 1,
            'user': current_user,
            'content': f"{quote}\nQuoted from {post['user']}: {post['content']}",
            'hearts': [],
            'comments': [],
            'reposts': [],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        posts.append(new_post)
        save_posts(posts)
        print(indent_text("\nquote posted!"))
        # Send notification to the original post owner
        if current_user != post['user']:
            notification = f"{current_user} quoted your post."
            save_notifications(post['user'], notification)
        input(indent_text("press enter to continue..."))

def post_status_screen():
    global screen
    clear_screen()
    header()
    print(indent_text("post a new status\n"))
    content = input(indent_text("enter your status (or type 'back' to cancel): ")).strip()

    if content.lower() == 'back':
        screen = "main_menu"
        return

    if content == '':
        print(indent_text("\nyou cannot post an empty status."))
    else:
        posts = load_posts()
        post = {
            'id': len(posts) + 1,
            'user': current_user,
            'content': content,
            'hearts': [],
            'comments': [],
            'reposts': [],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        posts.append(post)
        save_posts(posts)
        print(indent_text("\nstatus posted!"))

    input(indent_text("press enter to continue..."))
    screen = "main_menu"

def dm_screen():
    global screen
    clear_screen()
    header()
    print(indent_text("direct messages\n"))
    dms = load_dms()
    user_data = load_user_data(current_user)
    follows = user_data.get('follows', [])
    user_dms = dms.get(current_user, {})

    # Collect conversations with unread messages
    conversations = []
    for user, messages in user_dms.items():
        unread_count = sum(1 for msg in messages if not msg.get('read') and msg['sender'] != current_user)
        last_message_time = messages[-1]['timestamp'] if messages else ''
        conversations.append({
            'user': user,
            'unread': unread_count,
            'last_message_time': last_message_time
        })

    # Add followed users without conversations
    for user in follows:
        if user not in [conv['user'] for conv in conversations]:
            conversations.append({
                'user': user,
                'unread': 0,
                'last_message_time': ''
            })

    # Sort conversations by last message time (most recent first)
    conversations.sort(key=lambda x: datetime.strptime(x['last_message_time'], '%Y-%m-%d %H:%M:%S') if x['last_message_time'] else datetime.min, reverse=True)

    for idx, convo in enumerate(conversations, start=1):
        user = convo['user']
        unread = convo['unread']
        user_data = load_user_data(user)
        display_name = user_data.get('display_name', user)
        display_text = f"{idx}. {display_name} (@{user})"
        if unread > 0:
            display_text += color_text(f" ({unread} new messages)", '33')  # Yellow text
        print(indent_text(display_text))

    print(indent_text("\nenter the number of a user to chat with."))
    print(indent_text("press enter to return to the main menu.\n"))
    choice = input(indent_text("enter your choice: ")).strip()

    if choice == '':
        screen = "main_menu"
        return

    try:
        choice = int(choice)
        if 1 <= choice <= len(conversations):
            selected_user = conversations[choice - 1]['user']
            view_conversation(selected_user)
        else:
            print(indent_text("\ninvalid choice."))
            input(indent_text("press enter to continue..."))
    except ValueError:
        print(indent_text("\ninvalid input."))
        input(indent_text("press enter to continue..."))

def send_direct_message(recipient):
    message = input(indent_text("enter your message: ")).strip()
    if message == '':
        print(indent_text("\nmessage cannot be empty."))
        input(indent_text("press enter to continue..."))
        return
    send_direct_message_to_user(recipient, message)
    print(indent_text("\nmessage sent!"))
    input(indent_text("press enter to continue..."))

def send_direct_message_to_user(recipient, message):
    dms = load_dms()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_data = {
        'sender': current_user,
        'recipient': recipient,
        'message': message,
        'timestamp': timestamp,
        'read': False
    }

    # Add message to sender's DM
    dms.setdefault(current_user, {}).setdefault(recipient, []).append(message_data)
    # Add message to recipient's DM
    dms.setdefault(recipient, {}).setdefault(current_user, []).append(message_data)

    save_dms(dms)
    # Send notification to the recipient
    notification = f"you have a new message from {current_user}."
    save_notifications(recipient, notification)

def view_conversation(other_user):
    dms = load_dms()
    conversation = dms.get(current_user, {}).get(other_user, [])
    while True:
        clear_screen()
        header()
        print(indent_text(f"conversation with {other_user}\n"))
        if not conversation:
            print(indent_text("no messages yet."))
        else:
            # Mark messages as read
            for msg in conversation:
                if msg['sender'] != current_user:
                    msg['read'] = True
            save_dms(dms)

            # Display messages
            conversation.sort(key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'))
            for msg in conversation:
                sender = msg['sender']
                timestamp_formatted = format_timestamp(msg['timestamp'])
                message = msg['message']
                message_text = f"{sender} -> {timestamp_formatted}\n   {message}\n"
                print(indent_text(message_text))

        print(indent_text("\npress 'r' to refresh, 'q' to go back, or type your message and press Enter to send.\n"))
        user_input = input(indent_text("enter your choice or message: ")).strip()

        if user_input.lower() == 'q':
            return
        elif user_input.lower() == 'r':
            continue  # Will refresh the conversation
        elif user_input == '':
            continue
        else:
            # Send the message
            send_direct_message_to_user(other_user, user_input)
            # Reload the conversation
            dms = load_dms()
            conversation = dms.get(current_user, {}).get(other_user, [])

def notifications_screen():
    global screen
    clear_screen()
    header()
    print(indent_text("notifications\n"))
    user_data = load_user_data(current_user)
    notifications = user_data.get('notifications', [])
    if not notifications:
        print(indent_text("no new notifications."))
    else:
        for idx, note in enumerate(notifications, start=1):
            print(indent_text(f"{idx}. {note}"))
        # Clear notifications after viewing
        user_data['notifications'] = []
        save_user_data(current_user, user_data)
    input(indent_text("\npress enter to continue..."))
    screen = "main_menu"

def logout_screen():
    global screen, current_user
    logged_in_users.remove(current_user)
    current_user = None
    print(indent_text("\nyou have been logged out."))
    input(indent_text("press enter to continue..."))
    screen = "welcome"

#------------------------------------------------------------------------------
# Main Loop
#------------------------------------------------------------------------------

while loop:
    if screen == "welcome":
        welcome_screen()
    elif screen == "login":
        login_screen()
    elif screen == "register":
        register_screen()
    elif screen == "main_menu":
        main_menu_screen()
    elif screen == "bio":
        bio_screen()
    elif screen == "view_bios":
        view_bios_screen()
    elif screen == "friends_list":
        friends_list_screen()
    elif isinstance(screen, tuple) and screen[0] == "user_profile":
        user_profile_screen(screen[1])
    elif screen == "post_status":
        post_status_screen()
    elif screen == "view_own_posts":
        view_own_posts_screen()
    elif screen == "feed":
        feed_screen()
    elif screen == "dm":
        dm_screen()
    elif screen == "notifications":
        notifications_screen()
    elif screen == "logout":
        logout_screen()
    else:
        # If the screen is not recognized, go back to welcome
        screen = "welcome"

# eof
