from application.admin import bp
from application.core import orderservice
from flask import render_template
from flask_login import login_required
from application.utils import date


def _total_order_sum(order_items) -> int:
    summary_dishes_sum = [order_item.count * order_item.dish.price for order_item in order_items]
    total = sum(summary_dishes_sum)
    return total


@bp.route('/orders', methods=['GET'])
@login_required
def orders():
    all_orders = orderservice.get_all_confirmed_orders()
    return render_template('admin/orders.html', title='Заказы', area='orders', orders=all_orders)


@bp.route('/orders/<int:order_id>')
@login_required
def order(order_id: int):
    current_order = orderservice.get_order_by_id(order_id)
    order_date = date.convert_utc_to_asia_tz(current_order.confirmation_date).strftime('%d.%m.%Y %H:%M:%S')
    total_sum = _total_order_sum(current_order.order_items.all())
    return render_template('admin/order.html', title="Заказ от {}".format(order_date),
                           area='orders', order=current_order, total_sum=total_sum)
