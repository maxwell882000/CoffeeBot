from application import db
from application.core.models import NotificationChat
from typing import List


def add_notification_chat(chat_id: int, chat_title: str) -> bool:
    if NotificationChat.query.get(chat_id):
        return False
    notification_chat = NotificationChat(chat_id=chat_id, chat_title=chat_title)
    db.session.add(notification_chat)
    db.session.commit()
    return True


def get_all_notification_chats() -> List[NotificationChat]:
    return NotificationChat.query.all()
