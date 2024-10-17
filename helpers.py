#------------------------------------------------------------------------------
# helpers.py
#------------------------------------------------------------------------------
# this file contains helper functions that are used throughout the application.
# these functions handle tasks like clearing the screen, displaying headers and footers,
# formatting text, and managing global variables like the current screen and user.
#------------------------------------------------------------------------------

import os
from datetime import datetime, timedelta
import textwrap

# global variables to keep track of the current screen and user
current_screen = ["splash"]  # we start with the splash screen
current_user = [None]        # this will hold the username of the logged-in user

def clear_screen():
    """
    clears the terminal screen.
    this makes the output cleaner by removing previous text.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def show_splash_screen():
    """
    displays the splash screen with some ascii art.
    waits for the user to press enter before moving to the welcome screen.
    """
    clear_screen()
    art = r"""
      
  ▓█████▄  ██▀███  ▓█████ ▄▄▄       ███▄ ▄███▓
  ▒██▀ ██▌▓██ ▒ ██▒▓█   ▀▒████▄    ▓██▒▀█▀ ██▒
  ░██   █▌▓██ ░▄█ ▒▒███  ▒██  ▀█▄  ▓██    ▓██░
  ░▓█▄   ▌▒██▀▀█▄  ▒▓█  ▄░██▄▄▄▄██ ▒██    ▒██ 
  ░▒████▓ ░██▓ ▒██▒░▒████▒▓█   ▓██▒▒██▒   ░██▒
   ▒▒▓  ▒ ░ ▒▓ ░▒▓░░░ ▒░ ░▒▒   ▓▒█░░ ▒░   ░  ░
   ░ ▒  ▒   ░▒ ░ ▒░ ░ ░  ░ ▒   ▒▒ ░░  ░      ░
   ░ ░  ░   ░░   ░    ░    ░   ▒   ░      ░   
     ░       ░        ░  ░     ░  ░       ░                                            
      ██▓    ▄▄▄       ███▄    █ ▓█████▄      
     ▓██▒   ▒████▄     ██ ▀█   █ ▒██▀ ██▌     
     ▒██░   ▒██  ▀█▄  ▓██  ▀█ ██▒░██   █▌     
     ▒██░   ░██▄▄▄▄██ ▓██▒  ▐▌██▒░▓█▄   ▌     
     ░██████▒▓█   ▓██▒▒██░   ▓██░░▒████▓      
     ░ ▒░▓  ░▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒▓  ▒      
     ░ ░ ▒  ░ ▒   ▒▒ ░░ ░░   ░ ▒░ ░ ▒  ▒      
       ░ ░    ░   ▒      ░   ░ ░  ░ ░  ░      
         ░  ░     ░  ░         ░    ░         
                                     ░           


    """
    print(art)
    print(format_text("press enter to continue", indent=12))
    input()
    current_screen[0] = "welcome"  # move to the welcome screen

def show_header(username=None):
    """
    displays the header with a welcome message.
    if a username is provided, it personalizes the message.
    the username is displayed in a different color.
    """
    art = r"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    if username:
        welcome_text = f"welcome to dreamland, {color_text(username, '35')}"
    else:
        welcome_text = "welcome to dreamland"
    centered_text = welcome_text.center(35)
    print(art)
    print(centered_text)
    print(art)
    print('\n')

def show_footer():
    """
    displays a footer line to separate content.
    """
    print("\n" + "~" * 35)

def format_text(text, indent=5):
    """
    formats text to ensure it wraps properly and is indented.
    this makes the output look neat within the terminal width.
    """
    wrapper = textwrap.TextWrapper(width=40 - indent, subsequent_indent=' ' * indent)
    indented_text = wrapper.fill(text)
    indented_lines = [" " * indent + line for line in indented_text.split('\n')]
    return '\n'.join(indented_lines)

def color_text(text, color_code):
    """
    adds color to the text using ansi escape codes.
    this enhances the visual appeal of the text.
    color codes are strings like '31' for red, '32' for green, etc.
    """
    return f"\033[{color_code}m{text}\033[0m"

def display_hearts(hearts_list):
    """
    creates a string of heart symbols to represent likes.
    if there are no likes, it shows a grey heart.
    """
    total_hearts = len(hearts_list)
    if total_hearts == 0:
        return color_text("<3", '90')  # grey heart
    hearts_to_display = min(total_hearts, 10)
    heart_string = color_text("<3 ", '31') * hearts_to_display  # red hearts
    heart_string = heart_string.strip()
    if total_hearts > 10:
        heart_string += f" +{total_hearts - 10}"
    return heart_string

def format_timestamp(timestamp_str):
    """
    formats a timestamp string into a more readable form.
    shows 'today', 'yesterday', or the date and time.
    """
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

def wrap_text(text, indent=5):
    """
    wraps text to fit within the terminal width, with indentation.
    useful for displaying long pieces of text like posts or comments.
    """
    wrapper = textwrap.TextWrapper(width=40 - indent, subsequent_indent=' ' * indent)
    wrapped_text = wrapper.fill(text)
    indented_lines = [" " * indent + line for line in wrapped_text.split('\n')]
    return '\n'.join(indented_lines)

def format_menu_options(options):
    """
    formats menu options to display them in two columns and centered.
    this makes the menu look organized and easy to read.
    """
    half = (len(options) + 1) // 2
    col1 = options[:half]
    col2 = options[half:]
    formatted_lines = []
    max_width = 40
    for i in range(len(col1)):
        left = col1[i]
        right = col2[i] if i < len(col2) else ''
        line = f"{left:<18}{right:<18}"
        centered_line = line.center(max_width)
        formatted_lines.append(centered_line)
    return '\n'.join(formatted_lines)
