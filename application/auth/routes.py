from application.core import userservice
from application.auth import bp
from application.auth.forms import LoginEmailForm
from flask_login import login_required, current_user, login_user, logout_user
from flask import redirect, url_for, render_template, flash


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginEmailForm()
    if form.validate_on_submit():
        user = userservice.get_admin_user_by_email(form.email.data)
        login_user(user, remember=False)
        return redirect(url_for('admin.index'))
    return render_template('auth/login.html', title='Вход в систему', form=form)
