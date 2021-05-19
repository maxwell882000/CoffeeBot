from application.admin import bp
from flask_login import login_required, current_user
from application.admin.forms import AdministratorEmailForm, AdministratorPasswordForm
from application.core import userservice
from flask import render_template, redirect, url_for, flash


@login_required
@bp.route('/administrator', methods=['GET'])
def administrator():
    email_form = AdministratorEmailForm()
    password_form = AdministratorPasswordForm()
    email_form.fill_from_current_user()
    return render_template('admin/administrator.html',
                           title='Администратор',
                           area='admin',
                           email_form=email_form,
                           password_form=password_form)


@login_required
@bp.route('/administrator/change-email', methods=['POST'])
def change_email():
    form = AdministratorEmailForm()
    if form.validate_on_submit():
        email = form.email.data
        userservice.set_user_admin_email(current_user, email)
        flash('Email администратора изменён', category='success')
    return redirect(url_for('admin.administrator'))


@login_required
@bp.route('/administrator/change-password', methods=['POST'])
def change_password():
    form = AdministratorPasswordForm()
    if form.validate_on_submit():
        new_password = form.new_password.data
        userservice.set_user_admin_password(current_user, new_password)
        flash('Пароль для пользователя {} изменён'.format(current_user.email), category='success')
    return redirect(url_for('admin.administrator'))
