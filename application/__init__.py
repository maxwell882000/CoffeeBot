# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from telebot import TeleBot, logger
import os
import logging

telegram_bot = TeleBot(Config.API_TOKEN, threaded=False)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = 'Для входа в систему необходима авторизация.'
login.login_message_category = 'warning'

import application.core.models as models


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': models.User,
            'UserAdmin': models.UserAdmin,
            'Dish': models.Dish,
            'CartItem': models.CartItem,
            'DishCategory': models.DishCategory,
            'Order': models.Order}


from application.bot import bp as bot_bp
app.register_blueprint(bot_bp)
from application.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')
from application.admin import bp as admin_bp
app.register_blueprint(admin_bp)
from application.utils import filters

if 'ADMIN_DEV' not in os.environ and 'PRODUCTION' not in os.environ:
    logger.setLevel(logging.DEBUG)
    telegram_bot.remove_webhook()
    telegram_bot.polling(none_stop=True)
