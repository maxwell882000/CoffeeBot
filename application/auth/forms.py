from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from application.core import userservice


class LoginEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Email обязателен'), Email('Неверный формат e-mail')])
    password = PasswordField('Введите свой пароль', validators=[DataRequired('Необходимо ввести пароль')])
    submit = SubmitField('Войти')

    def validate_email(self, email: StringField):
        if not userservice.is_admin_user_exists(email.data):
            raise ValidationError('Такой email не зарегистрирован')

    def validate_password(self, password: PasswordField):
        user = userservice.get_admin_user_by_email(self.email.data)
        if not user:
            return True
        if not user.check_password(password.data):
            raise ValidationError('Введён неверный пароль для {}'.format(self.email.data))
        return True
