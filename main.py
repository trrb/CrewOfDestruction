from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from dataalchemy import create_session, global_init
from dataalchemy import User, Dish, Food, DishFood, LunchDish, \
    BreakfastDish, RoleStudent, RoleAdmin, RoleCook
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.first_page import First_page
from forms.profile import Profile
from forms.reviews import Reviews
from forms.Bascket import Bascket

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
    session = create_session()
    dishes = session.query(Dish).all()
    session.close()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
    return render_template('first_page.html', form=form, dishes=dishes)


@app.route('/logout')
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

        user = RoleStudent(
            name=form.name.data,
            email=form.email.data
        )

        user.set_password(form.password.data)

        session.add(user)
        session.commit()
        session.close()

        return redirect(url_for('login'))

    return render_template('registration.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])

def profile():
    form = Profile()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
    return render_template('profile.html', form=form)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    form = Reviews()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
    return render_template('reviews.html', form=form)

@app.route('/bascket', methods=['GET', 'POST'])
def bascket():
    form = Bascket()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
    return render_template('Bascket.html', form=form)


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
        print(f'Аларм!!! сайта не будет потому что {e}')
        session.rollback()
    finally:
        session.close()
    app.run(debug=True)
