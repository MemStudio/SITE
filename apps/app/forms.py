# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, DateField
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

class Allergy(FlaskForm):
    aller = StringField("Аллергия на", [DataRequired()])
    submit = SubmitField('Добавить')

class Pay(FlaskForm):
    count = IntegerField("Пополнить на: ", [DataRequired()])
    submit = SubmitField('Пополнить')

class CHGPASS(FlaskForm):
    passw = PasswordField("Новый пароль", [DataRequired()])
    submit =SubmitField("Сменить")
class ING(FlaskForm):
    ingr = StringField("Ингредиент", [DataRequired()])
    count = IntegerField("Стоимость", [DataRequired()])
    submit = SubmitField('Добавить')

class FOOD(FlaskForm):
    type = RadioField(label="Тип", choices=[('Завтрак', 'Завтрак'), ('Обед','Обед')], validators=[DataRequired()])
    date = DateField(label="Дата", format="%Y-%m-%d", validators=[DataRequired()])
    food = StringField("Блюдо", [DataRequired()])
    cost = IntegerField("Стоимость", [DataRequired()])
    submit = SubmitField('Добавить')
