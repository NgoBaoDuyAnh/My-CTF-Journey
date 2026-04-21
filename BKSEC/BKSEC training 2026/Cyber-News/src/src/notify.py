from typing import List, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib

from repositories.user import UserRepository
from utils import render_template

EMAIL_SENDER = "noreply@pixelblog.local"
from models.user import User
from models.post import Post


async def send_new_post_email(author: User, post: Post) -> None:
    subscribers = [
        user
        for subscriber in author.subscribers
        if (user := UserRepository.get_user({"user_id": subscriber})) is not None
    ]
    subscriber_emails = [
        subscriber.email
        for subscriber in subscribers
        if subscriber and subscriber.email is not None
    ]

    template_data = {
        "author_user_id": str(author.user_id),
        "author_username": author.username,
        "post_id": str(post.post_id),
        "post_title": post.title,
        "post_content": post.content,
    }
    messages = [("html", render_template("new_post.html", **template_data))]

    await send_email(subscriber_emails, "New Post Published!", messages)


async def send_new_subscriber_email(receiver: User, subscriber: User) -> None:
    assert receiver.email is not None

    template_data = {
        "username": receiver.username,
        "subscriber_username": subscriber.username,
        "subscriber_user_id": str(subscriber.user_id),
    }
    messages = [("html", render_template("new_subscriber.html", **template_data))]

    await send_email([receiver.email], "You Have a New Subscriber!", messages)


async def send_email(
    receiver_emails: List[str], subject: str, messages: List[Tuple[str, str]]
) -> None:
    if not receiver_emails:
        return

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(receiver_emails)
    msg["Subject"] = subject

    for type, content in messages:
        msg.attach(MIMEText(content, type))

    email_hash = hashlib.md5(receiver_emails[0].encode()).hexdigest()
    filepath = f"/tmp/{email_hash}.html"

    with open(filepath, "w") as f:
        f.write(msg.as_string())
