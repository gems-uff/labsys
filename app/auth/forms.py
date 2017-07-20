from flask_wtf import Form
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    ValidationError,
)
from wtforms.validators import (
    InputRequired, Length, Email, Regexp, EqualTo,
)

from app.models import User


class LoginForm(Form):
    email = StringField('Email', validators=[
        InputRequired(), Length(1, 64), Email()])
    password = PasswordField('Senha', validators=[InputRequired()])
    remember_me = BooleanField('Lembrar')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email', validators=[
        InputRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        InputRequired(), Length(1, 64)])
    password = PasswordField('Senha', validators=[
        InputRequired(), EqualTo('password2',
                                 message='Senhas devem ser iguais')])
    password2 = PasswordField('Confirmar senha', validators=[InputRequired()])
    submit = SubmitField('Registrar')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Esse email já está em uso!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Esse usuário já está em uso!')
