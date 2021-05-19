from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from application.resources.strings import get_string, from_order_shipping_method, from_order_payment_method
from application.core.models import Order

_keyboards_ru = {
    'remove': ReplyKeyboardRemove()
}
_keyboards_uz = {
    'remove': ReplyKeyboardRemove()
}

_default_value = ReplyKeyboardMarkup(resize_keyboard=True)
_default_value.add('no_keyboard')

# Initialization russian keyboards
_welcome_language = ReplyKeyboardMarkup(resize_keyboard=True)
_welcome_language.add(get_string('language.russian'), get_string('language.uzbek'))
_keyboards_ru['welcome.language'] = _welcome_language

_main_menu_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_main_menu_ru.add(get_string('main_menu.make_order'))
# _main_menu_ru.add(get_string('main_menu.profile'))
_keyboards_ru['main_menu'] = _main_menu_ru

_go_back_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_go_back_ru.add(get_string('go_back'))
_keyboards_ru['go_back'] = _go_back_ru

_dish_keyboard_ru = ReplyKeyboardMarkup(row_width=3)
_dish_keyboard_ru.add(*[str(x) for x in list(range(1, 10))])
_dish_keyboard_ru.add(get_string('go_back'))
_keyboards_ru['catalog.dish_keyboard'] = _dish_keyboard_ru

_shipping_methods_keyboard_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_shipping_methods_keyboard_ru.add(from_order_shipping_method(Order.ShippingMethods.DELIVERY, 'ru'),
                                  from_order_shipping_method(Order.ShippingMethods.PICK_UP, 'ru'),
                                  get_string('go_to_menu'))
_keyboards_ru['order.shipping_methods'] = _shipping_methods_keyboard_ru

_order_location_keyboard_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
location_button = KeyboardButton(get_string('my_location'), request_location=True)
_order_location_keyboard_ru.add(location_button)
_order_location_keyboard_ru.add(get_string('go_back'))
_keyboards_ru['order.address'] = _order_location_keyboard_ru

_order_payment_keyboard_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_order_payment_keyboard_ru.add(from_order_payment_method(Order.PaymentMethods.CASH, 'ru'))
_order_payment_keyboard_ru.add(get_string('go_back'), get_string('go_to_menu'))
_keyboards_ru['order.payment'] = _order_payment_keyboard_ru

_order_confirmation_keyboard_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_order_confirmation_keyboard_ru.add(get_string('order.confirm'), get_string('order.cancel'))
_keyboards_ru['order.confirmation'] = _order_confirmation_keyboard_ru
_order_confirmation_payment_keyboard_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_order_confirmation_payment_keyboard_ru.add(get_string('order.cancel', 'ru'))
_keyboards_ru['order.payment_confirmation'] = _order_confirmation_payment_keyboard_ru

_comments_keyboard_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_comments_keyboard_ru.add(*[get_string('comments.point_' + str(x)) for x in list(reversed(range(1, 6)))])
_comments_keyboard_ru.add(get_string('go_to_menu'))
_keyboards_ru['comments.send_comment'] = _comments_keyboard_ru

# Initialization uzbek keyboards
_main_menu_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_main_menu_uz.add(get_string('main_menu.make_order', 'uz'))
_main_menu_uz.add(get_string('main_menu.send_comment', 'uz'))
_main_menu_uz.add(get_string('main_menu.language', 'uz'))
_keyboards_uz['main_menu'] = _main_menu_uz
_go_back_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_go_back_uz.add(get_string('go_back', 'uz'))
_keyboards_uz['go_back'] = _go_back_uz
_dish_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
_dish_keyboard_uz.add(*[str(x) for x in list(range(1, 10))])
_dish_keyboard_uz.add(get_string('catalog.cart', 'uz'), get_string('go_back', 'uz'))
_keyboards_uz['catalog.dish_keyboard'] = _dish_keyboard_uz
_shipping_methods_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_shipping_methods_keyboard_uz.add(from_order_shipping_method(Order.ShippingMethods.DELIVERY, 'uz'),
                                  from_order_shipping_method(Order.ShippingMethods.PICK_UP, 'uz'),
                                  get_string('go_to_menu', 'uz'))
_keyboards_uz['order.shipping_methods'] = _shipping_methods_keyboard_uz
_order_location_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
location_button_uz = KeyboardButton(get_string('my_location', 'uz'), request_location=True)
_order_location_keyboard_uz.add(location_button_uz)
_order_location_keyboard_uz.add(get_string('go_back', 'uz'))
_keyboards_uz['order.address'] = _order_location_keyboard_uz
_order_payment_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_order_payment_keyboard_uz.add(from_order_payment_method(Order.PaymentMethods.CASH, 'uz'),
                               from_order_payment_method(Order.PaymentMethods.PAYME, 'uz'),
                               get_string('go_back', 'uz'), get_string('go_to_menu', 'uz'))
_keyboards_uz['order.payment'] = _order_payment_keyboard_uz
_order_confirmation_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_order_confirmation_keyboard_uz.add(get_string('order.confirm', 'uz'), get_string('order.cancel', 'uz'))
_keyboards_uz['order.confirmation'] = _order_confirmation_keyboard_uz
_order_confirmation_payment_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_order_confirmation_payment_keyboard_uz.add(get_string('order.cancel', 'uz'))
_keyboards_uz['order.payment_confirmation'] = _order_confirmation_payment_keyboard_uz
_comments_keyboard_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
_comments_keyboard_uz.add(*[get_string('comments.point_' + str(x), 'uz') for x in list(reversed(range(1, 6)))])
_comments_keyboard_uz.add(get_string('go_to_menu', 'uz'))
_keyboards_uz['comments.send_comment'] = _comments_keyboard_uz


def get_keyboard(key, language='ru'):
    if language == 'ru':
        return _keyboards_ru.get(key, _default_value)
    elif language == 'uz':
        return _keyboards_uz.get(key, _default_value)
    else:
        raise Exception('Invalid language')


def from_dish_categories(language: str) -> ReplyKeyboardMarkup:
    categories_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    categories_keyboard.add(get_string('catalog.make_order', language))
    categories_keyboard.add(get_string('go_back', language))
    return categories_keyboard


def from_dishes(dishes, language: str) -> ReplyKeyboardMarkup:
    dishes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    dishes_keyboard.add(get_string('go_back', language), get_string('catalog.cart', language))
    if language == 'uz':
        names = [dish.name_uz for dish in dishes]
    else:
        names = [dish.name for dish in dishes]
    dishes_keyboard.add(*names)
    return dishes_keyboard


def from_cart_items(cart_items, language) -> ReplyKeyboardMarkup:
    cart_items_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if language == 'uz':
        names = [cart_item.dish.description_uz for cart_item in cart_items]
    else:
        names = [cart_item.dish.description for cart_item in cart_items]
    names = ['❌ ' + name for name in names]
    cart_items_keyboard.add(*names)
    cart_items_keyboard.add(get_string('go_back', language), get_string('cart.clear', language))
    cart_items_keyboard.add(get_string('catalog.make_order', language))
    return cart_items_keyboard


def from_change_language(current_language: str) -> ReplyKeyboardMarkup:
    change_language_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    if current_language == 'uz':
        change_language_keyboard.add(get_string('language.russian'))
    else:
        change_language_keyboard.add(get_string('language.uzbek'))
    change_language_keyboard.add(get_string('go_back', current_language))
    return change_language_keyboard


def from_user_phone_number(language, phone_number: str = None, go_back: bool = True) -> ReplyKeyboardMarkup:
    phone_number_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    if phone_number and phone_number != '':
        phone_number_keyboard.add(phone_number)
    phone_button = KeyboardButton(get_string('my_number', language), request_contact=True)
    phone_number_keyboard.add(phone_button)
    if go_back:
        phone_number_keyboard.add(get_string('go_back', language))
    return phone_number_keyboard
