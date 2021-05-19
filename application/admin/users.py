from application.admin import bp
from application.core import userservice
from flask_login import login_required
from flask import render_template, redirect, url_for, flash
from .forms import UserForm
from application import telegram_bot


@bp.route('/users')
@login_required
def users():
    all_users = userservice.get_all_bot_users()
    return render_template('admin/users.html', title='Пользователи Telegram-bot', users=all_users, area='users')


@bp.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user_name = form.name.data
        phone_number = form.phone_number.data
        created_user = userservice.create_user(user_name, phone_number)
        return redirect(url_for('admin.user_created', user_id=created_user.id))
    return render_template('admin/new_user.html', title='Добавить пользователя', form=form, area='users')


@bp.route('/users/<int:user_id>/edit')
@login_required
def edit_user(user_id: int, methods=['GET', 'POST']):
    form = UserForm()
    if form.validate_on_submit():
        user_name = form.name.data
        phone_number = form.phone_number.data
        userservice.update_user(user_id, user_name, phone_number)
        flash('Пользователь {} отредактирован'.format(user_name), category='success')
        return redirect(url_for('admin.users'))
    user = userservice.get_user_by_id(user_id)
    form.fill_from_object(user)
    return render_template('admin/edit_user.html', title=user.full_user_name, form=form, user=user, area='users')


@bp.route('/users/<int:user_id>/created')
@login_required
def user_created(user_id: int):
    user = userservice.get_user_by_id(user_id)
    return render_template('admin/user_created.html', title=user.full_user_name, user=user, area='users',
                           bot_username=telegram_bot.get_me().username)


@bp.route('/users/<int:user_id>/remove')
@login_required
def remove_user(user_id):
    userservice.remove_user(user_id)
    flash('Пользователь удалён!', category='success')
    return redirect(url_for('admin.users'))
