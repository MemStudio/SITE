# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class Register(FlaskForm):
    user = StringField('Пользователь', [DataRequired()])
    fio = StringField('ФИО', [DataRequired()])
    password = PasswordField('Пароль', [DataRequired()])
    submit = SubmitField('Зарегестрироваться')

