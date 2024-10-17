#------------------------------------------------------------------------------
# data.py
#------------------------------------------------------------------------------
# this file handles all data loading and saving operations.
# it reads and writes user data, posts, messages, and notifications.
#------------------------------------------------------------------------------

import os
import json
import base64
import bcrypt

# ensure necessary directories and files exist
if not os.path.exists('users'):
    os.makedirs('users')

if not os.path.exists('posts.json'):
    with open('posts.json', 'w') as f:
        json.dump([], f)

if not os.path.exists('messages.json'):
    with open('messages.json', 'w') as f:
        json.dump({}, f)  # dictionary with usernames as keys

def load_posts():
    """
    loads all posts from the posts.json file.
    """
    with open('posts.json', 'r') as f:
        return json.load(f)

def save_posts(posts):
    """
    saves the list of posts to the posts.json file.
    """
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

def load_user_data(username):
    """
    loads a user's data from their json file.
    """
    user_file = os.path.join('users', f'{username}.json')
    with open(user_file, 'r') as f:
        return json.load(f)

def save_user_data(username, data):
    """
    saves a user's data to their json file.
    """
    user_file = os.path.join('users', f'{username}.json')
    with open(user_file, 'w') as f:
        json.dump(data, f, indent=4)

def load_messages():
    """
    loads all messages from the messages.json file.
    """
    with open('messages.json', 'r') as f:
        return json.load(f)

def save_messages(messages):
    """
    saves all messages to the messages.json file.
    """
    with open('messages.json', 'w') as f:
        json.dump(messages, f, indent=4)

def save_notifications(username, notification):
    """
    adds a notification to a user's data.
    """
    user_data = load_user_data(username)
    notifications = user_data.get('notifications', [])
    notifications.append(notification)
    user_data['notifications'] = notifications
    save_user_data(username, user_data)
