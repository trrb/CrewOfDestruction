from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired
# для простого создания карточек
from flask import Flask, render_template
from dataalchemy.models import Dish
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class BascketForm(FlaskForm):
    menu = SubmitField('Меню')
    basket = SubmitField('Корзина')
    profile = SubmitField('Профиль')
    top_up_acc = SubmitField('Пополнить')
    reviews = SubmitField('Отзывы')
    add = SubmitField('+')
    remove = SubmitField('-')
    accept_bascket = SubmitField('Офрмить заказ')