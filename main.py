from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required
from dataalchemy.db_session import create_session, global_init
from dataalchemy.models import User, Role, Dish, Food, DishFood, LunchDish, BreakfastDish
from dataalchemy.models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.first_page import First_page

app = Flask(__name__)
app.config['SECRET_KEY'] = 'crewdestruct'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

global_init()


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    user = session.get(User, int(user_id))
    session.close()
    return user


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(
            User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            session.close()
            return redirect(url_for('first_page'))

        session.close()
        return "Неверный логин или пароль"

    return render_template('log_in.html', form=form)


@app.route('/first_page', methods=['GET', 'POST'])  # Изменил 02.02.2026
@login_required
def first_page():
    form = First_page()
    return render_template('first_page.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        session = create_session()

        if session.query(User).filter(User.email == form.email.data).first():
            session.close()
            return "Пользователь уже существует"

        role = session.query(Role).filter(Role.name == 'Student').first()

        user = User(
            name=form.name.data,
            email=form.email.data,
            role=role
        )
        user.set_password(form.password.data)

        session.add(user)
        session.commit()
        session.close()

        return redirect(url_for('login'))

    return render_template('registration.html', form=form)


@app.route("/test_db")
def test_db():
    # создаём сессию для этого запроса
    db = create_session()
    try:
        # 1️⃣ Проверяем роль
        role = db.query(Role).filter(Role.name == "Student").first()
        if not role:
            role = Role(name="Student")
            db.add(role)
            db.commit()  # commit чтобы role.id появился

        # 2️⃣ Проверяем пользователя
        user = db.query(User).filter(User.email == "ivan@example.com").first()
        if not user:
            user = User(email="ivan@example.com", password="12345",
                        balance=100.0, role=role)
            db.add(user)
            db.commit()  # commit сохраняет пользователя

        # 3️⃣ Выводим всех пользователей
        users = db.query(User).all()
        result = "<br>".join(
            [f"{u.email} — {u.role.name} — {u.balance}" for u in users])
        return f"<h3>Пользователи в базе:</h3>{result}"

    except Exception as e:
        db.rollback()  # если ошибка, откат
        return f"Ошибка: {e}"
    finally:
        db.close()  # закрываем сессию


if __name__ == "__main__":
    session = create_session()
    try:
        if session.query(Dish).count() == 0:
            default_menu = [
                BreakfastDish(name='Бутерброд с ветчиной', price=200.0),
                BreakfastDish(name='Какао', price=150.0),
                BreakfastDish(name='Омлет', price=250.0),
                BreakfastDish(name='Рисовая каша', price=210.0),
                Dish(name='Чай', price=70.0)
            ]
            session.add_all(default_menu)
            session.commit()
    except Exception as e:
        print(f'Аларм!!! сайта не будет потому что{e}')
        session.rollback()
    finally:
        session.close()
    app.run(debug=True)
