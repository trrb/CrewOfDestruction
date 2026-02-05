from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class New_reviews(FlaskForm):
    menu = SubmitField('Меню')
    basket = SubmitField('Корзина')
    profile = SubmitField('Профиль')
    top_up_acc = SubmitField('Пополнить')
    reviews = SubmitField('Отзывы')
    info = StringField('Впишите отзыв')
    button_add_reviews = SubmitField('Оставить отзыв')
