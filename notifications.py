#------------------------------------------------------------------------------
# notifications.py
#------------------------------------------------------------------------------
# this file handles displaying notifications to the user.
# users can view their notifications and then they are cleared.
#------------------------------------------------------------------------------

from helpers import (
    clear_screen,
    show_header,
    show_footer,
    format_text,
    current_screen,
    current_user,
)
from data import load_user_data, save_user_data

def notifications_screen():
    """
    displays the user's notifications.
    after viewing, notifications are cleared.
    """
    clear_screen()
    show_header(current_user[0])
    print(format_text("notifications\n"))
    user_data = load_user_data(current_user[0])
    notifications = user_data.get('notifications', [])
    if not notifications:
        print(format_text("no new notifications."))
    else:
        for idx, note in enumerate(notifications, start=1):
            print(format_text(f"{idx}. {note}"))
        # clear notifications after viewing
        user_data['notifications'] = []
        save_user_data(current_user[0], user_data)
    show_footer()
    input(format_text("press enter to continue..."))
    current_screen[0] = "main_menu"
