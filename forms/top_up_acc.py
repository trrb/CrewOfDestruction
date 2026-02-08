from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import Optional


class Top_up_acc(FlaskForm):
    menu = SubmitField('Меню')
    basket = SubmitField('Корзина')
    profile = SubmitField('Профиль')
    top_up_acc = SubmitField('Пополнить')
    top_up_acc_balance = SubmitField('Пополнить')
    reviews = SubmitField('Отзывы')
    top_up = IntegerField('Cумма пополнения', validators=[Optional()])
    button_add_reviews = SubmitField('Добавить отзыв')
    submit_subscription = SubmitField('Оплатить абонемент')
