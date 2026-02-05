from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, \
    current_user
from dataalchemy import create_session, global_init
from dataalchemy import User, Dish, Food, DishFood, LunchDish, \
    BreakfastDish, RoleAdmin, RoleCook, Review, Bascket
from default_menu import default_menu
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.first_page import First_page
from forms.profile import Profile
from forms.reviews import Reviews
from forms.bascketform import BascketForm
from forms.alergen_add import Alergen_add
from forms.new_reviews import New_reviews

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


@app.route('/first_page', methods=['GET', 'POST'])
@login_required
def first_page():
    form = First_page()
    session = create_session()
    breakfast = session.query(Dish).filter(Dish.type == 'breakfast').all()
    lunch = session.query(Dish).filter(Dish.type == 'lunch').all()
    dishes = session.query(Dish).filter(Dish.type == 'dish').all()

    if request.method == 'POST':
        dish_id = request.form.get('dish_id')
        if dish_id:
            new_bascket = Bascket(dish_id=int(dish_id),
                                  user_id=current_user.id)
            session.add(new_bascket)
            session.commit()
    rendered = render_template('first_page.html', form=form, dishes=dishes,
                               breakfast=breakfast, lunch=lunch)
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
    session.close()
    return rendered


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

        user = User(
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
    session = create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    print(user)
    session.close()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
        elif form.alergen.data:
            return redirect(url_for('alergen_add'))
    return render_template('profile.html', form=form, user=user)


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    form = Reviews()
    session = create_session()
    reviews = session.query(Review).all()
    session.close()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.button_add_reviews.data:
            return redirect(url_for('reviews'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
        elif form.button_add_reviews.data:
            return redirect(url_for('new_reviews'))
    return render_template('reviews.html', form=form, reviews=reviews)


@app.route('/new_reviews', methods=['GET', 'POST'])
def new_reviews():
    form = New_reviews()
    #session = create_session()
    #reviews = session.query(Review).all()
    #session.close()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.button_add_reviews.data:
            return redirect(url_for('reviews'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
    return render_template('new_reviews.html', form=form, reviews=reviews)


@app.route('/bascket', methods=['GET', 'POST'])
def bascket():
    form = BascketForm()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
    return render_template('bascket.html', form=form)


@app.route('/alergen_add', methods=['GET', 'POST'])
def alergen_add():
    form = Alergen_add()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
    return render_template('alergen_add.html', form=form)


if __name__ == "__main__":
    session = create_session()
    try:
        a = session.query(Dish).all()
        names = [x.name for x in a]
        for dish in default_menu:
            if dish.name not in names:
                session.add(dish)
        session.commit()
    except Exception as e:
        print(f'Аларм!!! сайта не будет потому что {e}')
        session.rollback()
    finally:
        session.close()
    app.run(debug=True)
