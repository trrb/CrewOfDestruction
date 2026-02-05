from flask_wtf import FlaskForm
from wtforms import SubmitField



class First_page(FlaskForm):
    basket = SubmitField('Корзина')
    profile = SubmitField('Профиль')
    top_up_acc = SubmitField('Пополнить')
    reviews = SubmitField('Отзывы')
