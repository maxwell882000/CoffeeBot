from application.admin import bp
from application.core import orderservice
from flask_login import login_required
from flask import render_template


@bp.route('/orders-map', methods=['GET'])
@login_required
def orders_map():
    locations = orderservice.get_all_order_locations()
    return render_template('admin/orders_map.html', title='Карта заказов', area='map', locations=locations)
