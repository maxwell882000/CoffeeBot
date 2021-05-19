from application import telegram_bot
from application.core import userservice
from application.resources import strings, keyboards
from application.utils import bot as botutlis
from telebot.types import Message
from . import registration


def check_language(message: Message):
    if not message.text:
        return False
    user_id = message.from_user.id
    user = userservice.get_user_by_telegram_id(user_id)
    if not user:
        return False
    language = user.language
    return strings.get_string('main_menu.language', language) in message.text and message.chat.type == 'private'


def checker(message: Message):
    if not message.text:
        return False
    return botutlis.check_auth(message) and check_language(message)


@telegram_bot.message_handler(commands=['language'])
@telegram_bot.message_handler(content_types=['text'], func=checker)
def language_handler(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    change_language_message = strings.get_string('language.change', language)
    change_language_keyboard = keyboards.from_change_language(language)
    telegram_bot.send_message(chat_id, change_language_message, reply_markup=change_language_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, change_language_processor)


def change_language_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        if message.text == '/start':
            registration.welcome(message)
            return
        error_msg = strings.get_string('language.change', language)
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, change_language_processor)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        botutlis.to_main_menu(chat_id, language)
        return
    elif strings.get_string('language.russian') in message.text:
        new_language = 'ru'
        userservice.set_user_language(user_id, new_language)
    elif strings.get_string('language.uzbek') in message.text:
        new_language = 'uz'
    else:
        error()
        return
    userservice.set_user_language(user_id, new_language)
    success_message = strings.get_string('language.success', new_language)
    botutlis.to_main_menu(chat_id, new_language, success_message)
