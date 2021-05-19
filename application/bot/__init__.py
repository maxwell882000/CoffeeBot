from application import telegram_bot
from config import Config
from application.core import userservice, orderservice
from application.resources import strings, keyboards
from flask import Blueprint, request, abort
import telebot
import os

bp = Blueprint('bot', __name__)

from application.bot import registration, catalog, notifications

if 'PRODUCTION' in os.environ:
    @bp.route(Config.WEBHOOK_URL_PATH, methods=['POST'])
    def receive_message():
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            telegram_bot.process_new_updates([update])
            return ''
        else:
            abort(400)


    telegram_bot.remove_webhook()
    telegram_bot.set_webhook(Config.WEBHOOK_URL_BASE + Config.WEBHOOK_URL_PATH)


@telegram_bot.message_handler(commands=['sorrytest'])
def send_test_sorry_message(message: telebot.types.Message):
    message_text = 'Коллектив “Домашней кухни” приносит свои извинения за предоставленные неудобства в виде ' \
                   'задержек доставки. Это первые дни работы с нашей собственной доставкой через БОТ, ' \
                   'честно говоря, мы не ожидали такого потока клиентов и наш сервис не был к этому подготовлен. ' \
                   'Просим Вас, понять нашу ситуацию. С нашей стороны мы каждому обещаем при следующей доставке комплимент ' \
                   'от заведения совершенно бесплатно(Важно! Не забудьте напомнить при заказе об этом!). ' \
                   'Пишите обязательно нам свои отзывы и замечания, нам важно каждое мнение!'
    test_ids = [76777495, 294957271]
    for id in test_ids:
        try:
            telegram_bot.send_message(id, message_text)
        except telebot.apihelper.ApiException as err:
            telegram_bot.send_message(message.chat.id, str(err))
    telegram_bot.send_message(message.chat.id, 'Извинения отправлены {} людям!'.format(len(test_ids)))


@telegram_bot.message_handler(commands=['sorry'])
def send_sorry_message(message: telebot.types.Message):
    import time
    chat_id = message.chat.id
    message_text = 'Коллектив “Домашней кухни” приносит свои извинения за предоставленные неудобства в виде ' \
                   'задержек доставки. Это первые дни работы с нашей собственной доставкой через БОТ, ' \
                   'честно говоря, мы не ожидали такого потока клиентов и наш сервис не был к этому подготовлен. ' \
                   'Просим Вас, понять нашу ситуацию. С нашей стороны мы каждому обещаем при следующей доставке комплимент ' \
                   'от заведения совершенно бесплатно(Важно! Не забудьте напомнить при заказе об этом!). ' \
                   'Пишите обязательно нам свои отзывы и замечания, нам важно каждое мнение!'
    fargona_id = 423084515
    yesterday_orders = orderservice.get_yesterday_orders()
    customers = [o.customer for o in yesterday_orders]
    sent_customers = []
    for customer in customers:
        if customer.id == fargona_id or customer.id in sent_customers:
            continue
        try:
            telegram_bot.send_message(customer.id, message_text)
            sent_customers.append(customer.id)
        except telebot.apihelper.ApiException as err:
            telegram_bot.send_message(chat_id, str(err))
        time.sleep(1)
    telegram_bot.send_message(message.chat.id, 'Извинения отправлены {} людям!'.format(len(customers)))


@telegram_bot.message_handler(content_types=['text'], func=lambda m: m.chat.type == 'private')
def empty_message(message: telebot.types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not userservice.is_user_registered(user_id):
        registration.welcome(message)
        return
    language = userservice.get_user_language(user_id)
    main_menu_message = strings.get_string('main_menu.choose_option', language)
    main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
    telegram_bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)
    return
