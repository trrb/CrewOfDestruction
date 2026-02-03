from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired
# для простого создания карточек
from flask import Flask, render_template
from dataalchemy.models import Dish
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class First_page(FlaskForm):
    # menu = SubmitField('Меню')
    basket = SubmitField('Корзина')
    profile = SubmitField('Профиль')
    top_up_acc = SubmitField('Пополнить')
    reviews = SubmitField('Отзывы')
    add = SubmitField('+')

app = Flask(__name__)

# Подключаемся к бд
engine = create_engine('sqlite:///school.db')
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    session = Session()
    dishes = session.query(Dish).all()  # Получаем все блюда
    session.close()
    form = First_page()
    return render_template('first_page.html', dishes=dishes, form=form)