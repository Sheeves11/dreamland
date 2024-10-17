#------------------------------------------------------------------------------
# feed.py
#------------------------------------------------------------------------------
# this file handles everything related to the feed and posts.
# users can view the feed, create posts, like posts, comment, etc.
#------------------------------------------------------------------------------

from helpers import (
    clear_screen,
    show_header,
    show_footer,
    format_text,
    color_text,
    display_hearts,
    format_timestamp,
    wrap_text,
    format_menu_options,
    current_screen,
    current_user,
)
from data import load_posts, save_posts, load_user_data, save_notifications
from datetime import datetime

def feed_screen():
    """
    displays the user's feed with posts from people they follow.
    they can interact with posts by liking, commenting, etc.
    """
    clear_screen()
    show_header(current_user[0])
    print(format_text("your feed\n"))
    user_data = load_user_data(current_user[0])
    following = user_data.get('following', [])
    posts = load_posts()
    feed_posts = [post for post in posts if post['user'] in following or post['user'] == current_user[0]]

    if not feed_posts:
        print(format_text("no posts to show. follow users to see their posts."))
        input(format_text("press enter to continue..."))
        current_screen[0] = "main_menu"
        return

    feed_posts.reverse()  # most recent first
    page = 0
    total_posts = len(feed_posts)

    while True:
        clear_screen()
        show_header(current_user[0])
        print(format_text(f"your feed (post {page + 1} of {total_posts})\n"))

        post = feed_posts[page]
        hearts_display = display_hearts(post.get('likes', []))
        timestamp = format_timestamp(post['timestamp'])
        post_user_data = load_user_data(post['user'])
        display_name = post_user_data.get('display_name', post['user'])
        post_header = f"{display_name} (@{post['user']}) - {timestamp}\n"
        post_content = wrap_text(post['content'], indent=4)
        post_details = f"{post_header}{post_content}\nlikes: {hearts_display}\n"
        print(format_text("-" * 50))
        print(format_text(post_details))
        print(format_text("-" * 50 + "\n"))

        options = [
            "1. like/unlike",      "2. view likes",
            "3. comment",          "4. view comments",
            "5. repost",           "6. quote post",
            "n. next post",        "p. previous post",
            "enter: main menu",
        ]
        print(format_menu_options(options))
        show_footer()
        choice = input(format_text("enter your choice: ")).strip().lower()

        if choice == '':
            current_screen[0] = "main_menu"
            return
        elif choice == 'n':
            if page < total_posts - 1:
                page += 1
            else:
                print(format_text("you are on the last post."))
                input(format_text("press enter to continue..."))
        elif choice == 'p':
            if page > 0:
                page -= 1
            else:
                print(format_text("you are on the first post."))
                input(format_text("press enter to continue..."))
        elif choice == '1':
            like_unlike_post(post)
        elif choice == '2':
            view_likes(post)
        elif choice == '3':
            add_comment(post)
        elif choice == '4':
            view_comments(post)
        elif choice == '5':
            repost(post)
        elif choice == '6':
            quote_post(post)
        else:
            print(format_text("invalid choice. please try again."))
            input(format_text("press enter to continue..."))

def create_post_screen():
    """
    allows the user to create a new post by entering content.
    saves the new post to the posts file.
    """
    clear_screen()
    show_header(current_user[0])
    print(format_text("create a new post\n"))
    content = input(format_text("enter your post content (or type 'back' to cancel): ")).strip()

    if content.lower() == 'back':
        current_screen[0] = "main_menu"
        return

    if content == '':
        print(format_text("you cannot post empty content."))
    else:
        posts = load_posts()
        post = {
            'id': len(posts) + 1,
            'user': current_user[0],
            'content': content,
            'likes': [],
            'comments': [],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        posts.append(post)
        save_posts(posts)
        print(format_text("post created successfully!"))

    input(format_text("press enter to continue..."))
    current_screen[0] = "main_menu"

def my_posts_screen():
    """
    displays the user's own posts.
    allows them to edit or delete their posts.
    """
    clear_screen()
    show_header(current_user[0])
    user_data = load_user_data(current_user[0])
    display_name = user_data.get('display_name', current_user[0])
    bio = user_data.get('bio', 'no bio available.')
    pronouns = user_data.get('pronouns', '')
    age = user_data.get('age', '')

    profile_info = f"{display_name} (@{current_user[0]})\npronouns: {pronouns} | age: {age}\nbio: {bio}\n"
    print(format_text(profile_info))

    posts = load_posts()
    user_posts = [post for post in posts if post['user'] == current_user[0]]
    user_posts.reverse()  # most recent first

    if not user_posts:
        print(format_text("you haven't posted anything yet."))
        input(format_text("press enter to continue..."))
        current_screen[0] = "main_menu"
        return

    page = 0
    total_posts = len(user_posts)

    while True:
        clear_screen()
        show_header(current_user[0])
        print(format_text(profile_info))
        print(format_text(f"my posts (post {page + 1} of {total_posts})\n"))

        post = user_posts[page]
        hearts_display = display_hearts(post.get('likes', []))
        timestamp = format_timestamp(post['timestamp'])
        post_content = wrap_text(post['content'], indent=4)
        post_details = f"{timestamp}\n{post_content}\nlikes: {hearts_display}\n"
        print(format_text("-" * 50))
        print(format_text(post_details))
        print(format_text("-" * 50 + "\n"))

        options = [
            "1. edit post",         "2. delete post",
            "3. view likes",        "4. view comments",
            "n. next post",         "p. previous post",
            "enter: main menu",
        ]
        print(format_menu_options(options))
        show_footer()
        choice = input(format_text("enter your choice: ")).strip().lower()

        if choice == '':
            current_screen[0] = "main_menu"
            return
        elif choice == 'n':
            if page < total_posts - 1:
                page += 1
            else:
                print(format_text("you are on the last post."))
                input(format_text("press enter to continue..."))
        elif choice == 'p':
            if page > 0:
                page -= 1
            else:
                print(format_text("you are on the first post."))
                input(format_text("press enter to continue..."))
        elif choice == '1':
            edit_post(post)
        elif choice == '2':
            delete_post(post, user_posts, page)
            total_posts -= 1
            if total_posts == 0:
                print(format_text("you have no more posts."))
                input(format_text("press enter to continue..."))
                current_screen[0] = "main_menu"
                return
            if page >= total_posts:
                page = total_posts - 1
        elif choice == '3':
            view_likes(post)
        elif choice == '4':
            view_comments(post)
        else:
            print(format_text("invalid choice. please try again."))
            input(format_text("press enter to continue..."))

def view_user_posts(username):
    """
    displays the posts of a specific user.
    used when viewing another user's profile.
    """
    clear_screen()
    show_header(current_user[0])
    user_data = load_user_data(username)
    display_name = user_data.get('display_name', username)
    bio = user_data.get('bio', 'no bio available.')
    pronouns = user_data.get('pronouns', '')
    age = user_data.get('age', '')

    profile_info = f"{display_name} (@{username})\npronouns: {pronouns} | age: {age}\nbio: {bio}\n"
    print(format_text(profile_info))

    posts = load_posts()
    user_posts = [post for post in posts if post['user'] == username]
    user_posts.reverse()  # most recent first

    if not user_posts:
        print(format_text(f"{username} hasn't posted anything yet."))
        input(format_text("press enter to continue..."))
        return

    page = 0
    total_posts = len(user_posts)

    while True:
        clear_screen()
        show_header(current_user[0])
        print(format_text(profile_info))
        print(format_text(f"{username}'s posts (post {page + 1} of {total_posts})\n"))

        post = user_posts[page]
        hearts_display = display_hearts(post.get('likes', []))
        timestamp = format_timestamp(post['timestamp'])
        post_content = wrap_text(post['content'], indent=4)
        post_details = f"{timestamp}\n{post_content}\nlikes: {hearts_display}\n"
        print(format_text("-" * 50))
        print(format_text(post_details))
        print(format_text("-" * 50 + "\n"))

        options = [
            "1. like/unlike",      "2. view likes",
            "3. comment",          "4. view comments",
            "n. next post",        "p. previous post",
            "enter: go back",
        ]
        print(format_menu_options(options))
        show_footer()
        choice = input(format_text("enter your choice: ")).strip().lower()

        if choice == '':
            return  # go back to the previous screen
        elif choice == 'n':
            if page < total_posts - 1:
                page += 1
            else:
                print(format_text("you are on the last post."))
                input(format_text("press enter to continue..."))
        elif choice == 'p':
            if page > 0:
                page -= 1
            else:
                print(format_text("you are on the first post."))
                input(format_text("press enter to continue..."))
        elif choice == '1':
            like_unlike_post(post)
        elif choice == '2':
            view_likes(post)
        elif choice == '3':
            add_comment(post)
        elif choice == '4':
            view_comments(post)
        else:
            print(format_text("invalid choice. please try again."))
            input(format_text("press enter to continue..."))

def edit_post(post):
    """
    allows the user to edit the content of their post.
    """
    new_content = input(format_text("enter new content: ")).strip()
    if new_content == '':
        print(format_text("content cannot be empty."))
        input(format_text("press enter to continue..."))
    else:
        posts = load_posts()
        for p in posts:
            if p['id'] == post['id']:
                p['content'] = new_content
                break
        save_posts(posts)
        print(format_text("post updated successfully!"))
        post['content'] = new_content
        input(format_text("press enter to continue..."))

def delete_post(post, user_posts, page):
    """
    allows the user to delete their post.
    removes it from the posts list and updates the file.
    """
    posts = load_posts()
    posts = [p for p in posts if p['id'] != post['id']]
    save_posts(posts)
    print(format_text("post deleted successfully!"))
    input(format_text("press enter to continue..."))
    user_posts.pop(page)

def like_unlike_post(post):
    """
    toggles a like on a post.
    if the user has already liked the post, it unlikes it.
    otherwise, it likes the post and notifies the post owner.
    """
    if 'likes' not in post:
        post['likes'] = []

    if current_user[0] in post['likes']:
        post['likes'].remove(current_user[0])
        print(format_text("you unliked the post."))
    else:
        post['likes'].append(current_user[0])
        print(format_text("you liked the post."))
        if current_user[0] != post['user']:
            notification = f"{current_user[0]} liked your post."
            save_notifications(post['user'], notification)

    posts = load_posts()
    for p in posts:
        if p['id'] == post['id']:
            p['likes'] = post['likes']
            break
    save_posts(posts)
    input(format_text("press enter to continue..."))

def view_likes(post):
    """
    shows a list of users who have liked the post.
    """
    clear_screen()
    show_header(current_user[0])
    print(format_text("users who liked this post:\n"))
    if not post.get('likes'):
        print(format_text("no likes yet."))
    else:
        for user in post['likes']:
            user_data = load_user_data(user)
            display_name = user_data.get('display_name', user)
            print(format_text(f"- {display_name} (@{user})"))
    show_footer()
    input(format_text("press enter to go back."))

def add_comment(post):
    """
    allows the user to add a comment to a post.
    notifies the post owner about the comment.
    """
    comment = input(format_text("enter your comment: ")).strip()
    if comment == '':
        print(format_text("comment cannot be empty."))
        input(format_text("press enter to continue..."))
    else:
        if 'comments' not in post:
            post['comments'] = []
        post['comments'].append({
            'user': current_user[0],
            'comment': comment,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        posts = load_posts()
        for p in posts:
            if p['id'] == post['id']:
                p['comments'] = post['comments']
                break
        save_posts(posts)
        print(format_text("comment added successfully!"))
        if current_user[0] != post['user']:
            notification = f"{current_user[0]} commented on your post."
            save_notifications(post['user'], notification)
        input(format_text("press enter to continue..."))

def view_comments(post):
    """
    displays all comments on a post.
    """
    clear_screen()
    show_header(current_user[0])
    print(format_text("comments:\n"))
    if 'comments' not in post or not post['comments']:
        print(format_text("no comments yet."))
    else:
        for idx, comment in enumerate(post['comments'], start=1):
            timestamp = format_timestamp(comment['timestamp'])
            user_data = load_user_data(comment['user'])
            display_name = user_data.get('display_name', comment['user'])
            comment_text = wrap_text(comment['comment'], indent=4)
            comment_info = f"{display_name} (@{comment['user']}) - {timestamp}\n{comment_text}\n"
            print(format_text(comment_info))
    show_footer()
    input(format_text("press enter to go back."))

def repost(post):
    """
    allows the user to repost someone else's post.
    creates a new post with the original content and credits the original user.
    """
    posts = load_posts()
    new_post = {
        'id': len(posts) + 1,
        'user': current_user[0],
        'content': f"reposted from {post['user']}: {post['content']}",
        'likes': [],
        'comments': [],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    posts.append(new_post)
    save_posts(posts)
    print(format_text("post reposted successfully!"))
    if current_user[0] != post['user']:
        notification = f"{current_user[0]} reposted your post."
        save_notifications(post['user'], notification)
    input(format_text("press enter to continue..."))

def quote_post(post):
    """
    allows the user to quote a post and add their own comment.
    creates a new post with the quote and the original content.
    """
    quote = input(format_text("enter your comment on the post: ")).strip()
    if quote == '':
        print(format_text("you cannot post an empty quote."))
        input(format_text("press enter to continue..."))
    else:
        posts = load_posts()
        new_post = {
            'id': len(posts) + 1,
            'user': current_user[0],
            'content': f"{quote}\nquoted from {post['user']}: {post['content']}",
            'likes': [],
            'comments': [],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        posts.append(new_post)
        save_posts(posts)
        print(format_text("quote posted successfully!"))
        if current_user[0] != post['user']:
            notification = f"{current_user[0]} quoted your post."
            save_notifications(post['user'], notification)
        input(format_text("press enter to continue..."))
