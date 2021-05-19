from application import telegram_bot as bot
from application.core import userservice
from application.resources import strings, keyboards
from telebot.types import Message
from .catalog import back_to_the_catalog, catalog_processor
from .orders import order_processor
from . import registration


def _total_cart_sum(cart) -> int:
    summary_dishes_sum = [cart_item.dish.price * cart_item.count for cart_item in cart]
    total = sum(summary_dishes_sum)
    return total


def cart_action_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        if message.text == '/start':
            registration.welcome(message)
            return
        error_msg = strings.get_string('cart.error', language)
        bot.send_message(chat_id, error_msg)
        bot.register_next_step_handler_by_chat_id(chat_id, cart_action_processor)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        back_to_the_catalog(chat_id, language)
    elif strings.get_string('cart.clear', language) in message.text:
        userservice.clear_user_cart(user_id)
        back_to_the_catalog(chat_id, language)
    elif strings.get_string('catalog.make_order', language) in message.text:
        order_processor(message)
    else:
        dish_name = message.text[2:]
        removing_result = userservice.remove_dish_from_user_cart(user_id, dish_name, language)
        if removing_result:
            cart = userservice.get_user_cart(user_id)
            if len(cart) == 0:
                back_to_the_catalog(chat_id, language)
                return
            total = _total_cart_sum(cart)
            cart_contains_message = strings.from_cart_items(cart, language, total)
            cart_contains_keyboard = keyboards.from_cart_items(cart, language)
            bot.send_message(chat_id, cart_contains_message, parse_mode='HTML', reply_markup=cart_contains_keyboard)
            bot.register_next_step_handler_by_chat_id(chat_id, cart_action_processor)
            return
        else:
            error()
            return


def cart_processor(message: Message, callback=None):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    cart = userservice.get_user_cart(user_id)
    if len(cart) == 0:
        cart_empty_message = strings.get_string('cart.empty', language)
        bot.send_message(chat_id, cart_empty_message)
        if callback:
            bot.register_next_step_handler_by_chat_id(chat_id, callback)
        else:
            bot.register_next_step_handler_by_chat_id(chat_id, catalog_processor)
        return
    cart_help_message = strings.get_string('cart.help', language)
    total = _total_cart_sum(cart)
    cart_contains_message = strings.from_cart_items(cart, language, total)
    cart_items_keyboard = keyboards.from_cart_items(cart, language)
    bot.send_message(chat_id, cart_help_message, parse_mode='HTML')
    bot.send_message(chat_id, cart_contains_message, parse_mode='HTML', reply_markup=cart_items_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, cart_action_processor)
