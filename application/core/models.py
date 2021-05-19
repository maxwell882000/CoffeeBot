from application import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_mptt.mixins import BaseNestedSets
from datetime import datetime


class CartItem(db.Model):
    """
    Model for cart item
    """
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id', ondelete='SET NULL'), nullable=True)
    count = db.Column(db.Integer)
    dish = db.relationship('Dish')


class OrderItem(db.Model):
    """
    Model for order item
    """
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id', ondelete='SET NULL'), nullable=True)
    count = db.Column(db.Integer)
    dish = db.relationship('Dish')


class User(db.Model):
    """
    Model for users in Telegram Bot
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_user_name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    language = db.Column(db.String(5))
    token = db.Column(db.String(50))
    confirmed = db.Column(db.Boolean)
    telegram_id = db.Column(db.Integer)
    registration_date = db.Column(db.DateTime)
    count_orders = db.Column(db.Integer, default=0)
    cart = db.relationship('CartItem', lazy='dynamic', backref='user', cascade='all, delete-orphan')
    orders = db.relationship('Order', lazy='dynamic', backref='customer', cascade='all, delete-orphan')
    comments = db.relationship('Comment', lazy='dynamic', backref='author')

    def _get_cart_item_for_dish(self, dish) -> CartItem:
        """
        Check if dish is exists in cart
        :param dish: Dish
        :return: Check's result
        """
        return self.cart.filter(CartItem.dish_id == dish.id).first()

    def add_dish_to_cart(self, dish, count):
        """
        Add a dish to cart if there isn't it in cart.
        And add cart item to database session
        :param dish: Dish
        :param count: Numbers of the dish
        :return: void
        """
        cart_item = self._get_cart_item_for_dish(dish)
        if cart_item:
            cart_item.count = count
            return
        cart_item = CartItem(count=count, dish=dish)
        self.cart.append(cart_item)
        db.session.add(cart_item)

    def remove_dish_from_cart(self, dish):
        """
        Remove dish from cart if it exists
        :param dish: Dish
        :return: void
        """
        self.cart.remove(dish)


class UserAdmin(db.Model, UserMixin):
    """
    Model for users in admin panel
    """
    __tablename__ = 'user_admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True)
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class DishCategory(db.Model, BaseNestedSets):
    """
    Model for dish category
    """
    __tablename__ = 'dish_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    name_uz = db.Column(db.String(100))
    number = db.Column(db.Integer, default=1)
    image_id = db.Column(db.String(150))
    image_path = db.Column(db.String(150))
    dishes = db.relationship('Dish', lazy='dynamic', backref='category')

    def get_nested_names(self):
        name = self.name
        if self.parent:
            name = self.parent.name + ' |=>| ' + name
            if self.parent.parent:
                name = self.parent.parent.name + ' |=>| ' + name
                if self.parent.parent.parent:
                    name = self.parent.parent.parent.name + ' |=>| ' + name
        return name

    def get_nested_names_uz(self):
        name = self.name_uz
        if self.parent:
            name = self.parent.name_uz + ' |=>| ' + name
            if self.parent.parent:
                name = self.parent.parent.name_uz + ' |=>| ' + name
                if self.parent.parent.parent:
                    name = self.parent.parent.parent.name_uz + ' |=>| ' + name
        return name


class Dish(db.Model):
    """
    Model for dishes
    """
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    name_uz = db.Column(db.String(100))
    image_id = db.Column(db.String(150))
    image_path = db.Column(db.String(150))
    description = db.Column(db.String(500))
    description_uz = db.Column(db.String(500))
    show_usd = db.Column(db.Boolean, default=False)
    is_hidden = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float)
    number = db.Column(db.Integer, default=1)
    category_id = db.Column(db.Integer, db.ForeignKey('dish_categories.id'))
    quantity = db.Column(db.Integer, default=0)

    def get_full_name(self):
        return self.category.get_nested_names() + ' |=>| ' + self.name

    def get_full_name_uz(self):
        return self.category.get_nested_names_uz() + ' |=>| ' + self.name_uz


class Order(db.Model):
    """
    Model for orders
    Contains class OrderTypes to set type of order
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.Column(db.String(100))
    shipping_method = db.Column(db.String(50))
    payment_method = db.Column(db.String(50))
    address_txt = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    confirmed = db.Column(db.Boolean, default=False)
    confirmation_date = db.Column(db.DateTime)
    delivery_price = db.Column(db.Integer)
    total_amount = db.Column(db.Float)
    order_items = db.relationship('OrderItem', lazy='dynamic',
                                  backref='order', cascade='all, delete-orphan')
    location = db.relationship('Location', uselist=False, cascade='all,delete', backref='order')

    def fill_from_user_cart(self, cart):
        """
        Fill order items from user's cart.
        Add new objects to db.session
        :param cart: User's cart
        :return: void
        """
        # Clear current order items collection
        for order_item in self.order_items.all():
            self.order_items.remove(order_item)
        # And add fresh cart items to order
        for cart_item in cart:
            order_item = OrderItem()
            order_item.count = cart_item.count
            order_item.dish = cart_item.dish
            self.order_items.append(order_item)
            db.session.add(order_item)

    class ShippingMethods:
        PICK_UP = 'pickup'
        DELIVERY = 'delivery'

    class PaymentMethods:
        CASH = 'cash'
        PAYME = 'payme'


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(100))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))


class Comment(db.Model):
    """
    Model for users' comments
    """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    username = db.Column(db.String(100))


class UserDish(db.Model):
    """
    Model for saving current dish of user
    """
    user_id = db.Column(db.Integer, index=True, primary_key=True)
    dish_id = db.Column(db.Integer, index=True)


class NotificationChat(db.Model):
    __tablename__ = "notification_chats"
    chat_id = db.Column(db.Integer, primary_key=True)
    chat_title = db.Column(db.String(100))


class RegistrationRequest(db.Model):
    __tablename__ = "registration_requests"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    phone_number = db.Column(db.String(20))
    tg_username = db.Column(db.String(100))
    username = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login.user_loader
def load_user(user_id):
    return UserAdmin.query.get(int(user_id))
