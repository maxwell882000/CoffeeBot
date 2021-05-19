from application import telegram_bot
from application.resources import strings, keyboards
from application.core import userservice
from telebot.types import Message


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


def to_main_menu(chat_id, language, message_text=None):
    if message_text:
        main_menu_message = message_text
    else:
        main_menu_message = strings.get_string('main_menu.choose_option', language)
    main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
    telegram_bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)
