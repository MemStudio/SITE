# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class Register(FlaskForm):
    user = StringField('Пользователь', [DataRequired()])
    fio = StringField('ФИО', [DataRequired()])
    password = PasswordField('Пароль', [DataRequired()])
    submit = SubmitField('Зарегестрироваться')

class SIGN(FlaskForm):
    user = StringField('Пользователь', [DataRequired()])
    password = PasswordField('Пароль', [DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Зарегестрироваться')
