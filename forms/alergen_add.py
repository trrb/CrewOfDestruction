from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField
from wtforms.validators import DataRequired
# для простого создания карточек
from flask import Flask, render_template
from dataalchemy.models import Dish
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Alergen_add(FlaskForm):
    menu = SubmitField('Меню')
    basket = SubmitField('Корзина')
    profile = SubmitField('Профиль')
    top_up_acc = SubmitField('Пополнить')
    alergen_add  = SubmitField('Добавить аллергены')
    reviews = SubmitField('Отзывы')
    alergen_field = StringField('Напишите аллерген')
    add = SubmitField('+')