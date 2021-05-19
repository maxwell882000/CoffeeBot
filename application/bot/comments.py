from application import telegram_bot as bot
from application.core import commentservice, userservice
from application.resources import strings, keyboards
from application.utils import bot as botutils
from application.bot import notifications
from telebot.types import Message
from . import registration


def check_comments(message: Message):
    if not message.text:
        return False
    user_id = message.from_user.id
    user = userservice.get_user_by_telegram_id(user_id)
    if not user:
        return False
    language = user.language
    return strings.get_string('main_menu.send_comment', language) in message.text and 'private' in message.chat.type


@bot.message_handler(commands=['/comment'])
@bot.message_handler(content_types='text', func=lambda m: botutils.check_auth(m) and check_comments(m))
def comments(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    comments_message = strings.get_string('comments.send_comment', language)
    comments_keyboard = keyboards.get_keyboard('comments.send_comment', language)
    bot.send_message(chat_id, comments_message, reply_markup=comments_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, comments_processor)


def comments_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        if message.text == '/start':
            registration.welcome(message)
            return
        error_msg = strings.get_string('comments.error', language)
        bot.send_message(chat_id, error_msg)
        bot.register_next_step_handler_by_chat_id(chat_id, comments_processor)

    if not message.text:
        error()
        return
    if strings.get_string('go_to_menu', language) in message.text:
        botutils.to_main_menu(chat_id, language)
    else:
        username = message.from_user.first_name
        if message.from_user.last_name:
            username += " {}".format(message.from_user.last_name)
        new_comment = commentservice.add_comment(user_id, message.text, username)
        notifications.notify_new_comment(new_comment)
        thanks_message = strings.get_string('comments.thanks', language)
        botutils.to_main_menu(chat_id, language, thanks_message)
