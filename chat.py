#------------------------------------------------------------------------------
# chat.py
#------------------------------------------------------------------------------
# this file handles everything related to direct messaging.
# users can view their conversations and send messages to other users.
#------------------------------------------------------------------------------

from helpers import (
    clear_screen,
    show_header,
    show_footer,
    format_text,
    wrap_text,
    format_menu_options,
    color_text,
    format_timestamp,
    current_screen,
    current_user,
)
from data import load_messages, save_messages, load_user_data, save_notifications
from datetime import datetime

def direct_messages_screen():
    """
    displays the user's direct messages.
    allows them to select a conversation to view or start a new one.
    """
    clear_screen()
    show_header(current_user[0])
    print(format_text("direct messages\n"))
    messages = load_messages()
    user_messages = messages.get(current_user[0], {})

    conversations = []
    for user, msgs in user_messages.items():
        unread_count = sum(1 for msg in msgs if not msg.get('read') and msg['sender'] != current_user[0])
        last_message_time = msgs[-1]['timestamp'] if msgs else ''
        conversations.append({
            'user': user,
            'unread': unread_count,
            'last_message_time': last_message_time
        })

    # sort conversations by last message time
    conversations.sort(key=lambda x: datetime.strptime(x['last_message_time'], '%Y-%m-%d %H:%M:%S') if x['last_message_time'] else datetime.min, reverse=True)

    for idx, convo in enumerate(conversations, start=1):
        user = convo['user']
        unread = convo['unread']
        user_data = load_user_data(user)
        display_name = user_data.get('display_name', user)
        display_text = f"{idx}. {display_name} (@{user})"
        if unread > 0:
            display_text += color_text(f" ({unread} new messages)", '33')  # yellow for unread messages
        print(format_text(display_text))

    print(format_text("\nenter the number of a user to chat with."))
    print(format_text("press enter to return to the main menu.\n"))
    choice = input(format_text("enter your choice: ")).strip()

    if choice == '':
        current_screen[0] = "main_menu"
        return

    try:
        choice = int(choice)
        if 1 <= choice <= len(conversations):
            selected_user = conversations[choice - 1]['user']
            view_conversation(selected_user)
        else:
            print(format_text("invalid choice. please try again."))
            input(format_text("press enter to continue..."))
    except ValueError:
        print(format_text("invalid input. please try again."))
        input(format_text("press enter to continue..."))

def view_conversation(other_user):
    """
    displays the conversation with another user.
    allows the user to send messages.
    """
    messages = load_messages()
    conversation = messages.get(current_user[0], {}).get(other_user, [])
    while True:
        clear_screen()
        show_header(current_user[0])
        print(format_text(f"conversation with {other_user}\n"))
        if not conversation:
            print(format_text("no messages yet."))
        else:
            # mark messages as read
            for msg in conversation:
                if msg['sender'] != current_user[0]:
                    msg['read'] = True
            save_messages(messages)

            # display messages
            conversation.sort(key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'))
            for msg in conversation:
                sender = msg['sender']
                timestamp = format_timestamp(msg['timestamp'])
                message_text = wrap_text(msg['message'], indent=4)
                msg_display = f"{sender} - {timestamp}\n{message_text}\n"
                print(format_text(msg_display))

        print(format_text("\ntype your message and press enter to send."))
        print(format_text("type 'back' to go back.\n"))
        user_input = input(format_text("enter your message: ")).strip()

        if user_input.lower() == 'back':
            return
        elif user_input == '':
            continue
        else:
            send_message_to_user(other_user, user_input)
            messages = load_messages()
            conversation = messages.get(current_user[0], {}).get(other_user, [])

def send_message_to_user(recipient, message):
    """
    sends a direct message to another user.
    updates the messages data and notifies the recipient.
    """
    messages = load_messages()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_data = {
        'sender': current_user[0],
        'recipient': recipient,
        'message': message,
        'timestamp': timestamp,
        'read': False
    }

    # update the messages for both users
    messages.setdefault(current_user[0], {}).setdefault(recipient, []).append(message_data)
    messages.setdefault(recipient, {}).setdefault(current_user[0], []).append(message_data)

    save_messages(messages)
    notification = f"you have a new message from {current_user[0]}."
    save_notifications(recipient, notification)
