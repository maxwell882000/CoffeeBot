from . import bp
from flask_login import login_required
from flask import render_template, redirect, url_for, flash
from application.core import userservice


@bp.route('/requests', methods=['GET'])
@login_required
def list_requests():
    requests = userservice.get_all_registration_requests()
    return render_template('admin/requests.html', title="Запросы на регистрацию", area='requests', requests=requests)


@bp.route('/requests/<int:request_id>/delete', methods=['GET'])
@login_required
def delete_request(request_id: int):
    userservice.delete_registration_request(request_id)
    return redirect(url_for('admin.list_requests'))


@bp.route('/requests/<int:request_id>/confirm', methods=['GET'])
@login_required
def confirm_request(request_id: int):
    created_user = userservice.confirm_registration_request(request_id)
    return redirect(url_for('admin.user_created', user_id=created_user.id))
