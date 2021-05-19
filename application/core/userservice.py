from application import db
from application.core.models import User, UserAdmin, UserDish, Dish, RegistrationRequest, CartItem
from application.utils import date
from . import dishservice
from datetime import datetime, timedelta
import secrets
from typing import List


def is_user_exists(user_id: int):
    return get_user_by_telegram_id(user_id) is not None


def get_user_by_id(user_id):
    return User.query.get_or_404(user_id)


def get_user_by_telegram_id(telegram_id: int):
    return User.query.get(telegram_id)


def get_user_by_token(token: str):
    return User.query.filter(User.token == token).first()


def confirm_user(user: User, telegram_id, username: str):
    if user.confirmed:
        return False
    user.telegram_id = telegram_id
    user.confirmed = True
    user.username = username
    db.session.commit()
    return True


def register_user(user_id: int, username: str, full_user_name: str, phone_number: str, language: str):
    user = User(id=user_id, username=username, language=language, registration_date=datetime.utcnow(),
                full_user_name=full_user_name, phone_number=phone_number)
    db.session.add(user)
    db.session.commit()


def create_user(full_user_name: str, phone_number: str):
    token = secrets.token_urlsafe(20)
    user = User(token=token, registration_date=datetime.utcnow(),
                full_user_name=full_user_name, phone_number=phone_number)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user_id, name, phone_number):
    user = get_user_by_id(user_id)
    user.full_user_name = name
    user.phone_number = phone_number
    db.session.commit()


def remove_user(user_id):
    db.session.delete(get_user_by_id(user_id))
    db.session.commit()


def set_user_phone_number(user_id: int, phone_number: str):
    user = get_user_by_telegram_id(user_id)
    user.phone_number = phone_number
    db.session.commit()


def set_user_language(user_id: int, language: str):
    user = get_user_by_telegram_id(user_id)
    user.language = language
    db.session.commit()


def get_admin_user_by_email(email: str) -> UserAdmin:
    return UserAdmin.query.filter(UserAdmin.email == email).first()


def get_admin_user_by_id(user_id: int) -> UserAdmin:
    return UserAdmin.query.get(user_id)


def is_user_registered(user_id):
    user = get_user_by_telegram_id(user_id)
    if user is None:
        return False
    return user.language is not None


def get_user_language(user_id: int):
    user = get_user_by_id(user_id)
    return user.language


def set_user_admin_password(user: UserAdmin, password: str):
    user.set_password(password)
    db.session.commit()


def set_user_admin_email(user: UserAdmin, email: str):
    user.email = email
    db.session.commit()


def is_admin_user_exists(email):
    return get_admin_user_by_email(email) is not None


def get_all_bot_users():
    return User.query.order_by(User.registration_date.desc()).all()


def get_bot_users_yesterday_today_statistic():
    all_users = get_all_bot_users()
    yesterday = date.convert_utc_to_asia_tz(datetime.utcnow() - timedelta(days=1))
    yesterday_start = datetime(yesterday.year, yesterday.month, yesterday.day, tzinfo=yesterday.tzinfo)
    yesterday_end = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59, tzinfo=yesterday.tzinfo)
    yesterday_bot_users_count = len([u for u in all_users if yesterday_start <= date.convert_utc_to_asia_tz(u.registration_date) <= yesterday_end])
    today = date.convert_utc_to_asia_tz(datetime.utcnow())
    today_start = datetime(today.year, today.month, today.day, tzinfo=today.tzinfo)
    today_bot_users_count = len([u for u in all_users if today_start <= date.convert_utc_to_asia_tz(u.registration_date) <= today])
    return yesterday_bot_users_count, today_bot_users_count


def set_current_user_dish(user_id: int, dish_id: int):
    user_dish = UserDish.query.get(user_id)
    if not user_dish:
        db.session.add(UserDish(user_id=user_id, dish_id=dish_id))
        db.session.commit()
    else:
        user_dish.dish_id = dish_id
        db.session.commit()


def get_current_user_dish(user_id: int):
    user_dish = UserDish.query.get(user_id)
    return dishservice.get_dish_by_id(user_dish.dish_id)


def get_user_cart(user_id: int) -> list:
    user = get_user_by_telegram_id(user_id)
    return user.cart.all()


def clear_user_cart(user_id: int):
    user = get_user_by_telegram_id(user_id)
    dishes = [cart_item for cart_item in user.cart.all()]
    for dish in dishes:
        user.remove_dish_from_cart(dish)
    db.session.commit()


def add_dish_to_cart(user_id: int, dish: Dish, count: int):
    user = get_user_by_telegram_id(user_id)
    user.add_dish_to_cart(dish, count)
    db.session.commit()


def remove_dish_from_user_cart(user_id: int, dish_name: str, language: str) -> bool:
    user = get_user_by_telegram_id(user_id)
    if language == 'uz':
        dish = user.cart.filter(Dish.description_uz == dish_name).first()
    else:
        dish = user.cart.filter(Dish.description == dish_name).first()
    if not dish:
        return False
    user.remove_dish_from_cart(dish)
    db.session.commit()
    return True


def create_registration_request(user_id: int, phone_number: str, tg_username: str, username: str):
    request = RegistrationRequest(user_id=user_id, phone_number=phone_number,
                                  tg_username=tg_username, username=username)
    db.session.add(request)
    db.session.commit()


def get_all_registration_requests() -> List[RegistrationRequest]:
    return RegistrationRequest.query.order_by(RegistrationRequest.created_at.desc()).all()


def delete_registration_request(request_id: int):
    request = RegistrationRequest.query.get_or_404(request_id)
    db.session.delete(request)
    db.session.commit()


def confirm_registration_request(request_id: int):
    request = RegistrationRequest.query.get_or_404(request_id)
    return create_user(request.username, request.phone_number)
