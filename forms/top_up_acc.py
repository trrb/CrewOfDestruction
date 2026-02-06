from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField


class Top_up_acc(FlaskForm):
    menu = SubmitField('Меню')
    basket = SubmitField('Корзина')
    profile = SubmitField('Профиль')
    top_up_acc = SubmitField('Пополнить')
    reviews = SubmitField('Отзывы')
    top_up = IntegerField('Cумма пополнения')
    button_add_reviews = SubmitField('Добавить отзыв')
