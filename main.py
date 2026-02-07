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
from forms.top_up_acc import Top_up_acc
from sqlalchemy import desc 

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
            new_bascket = Bascket(dish_id=int(dish_id), # 123
                                  user_id=current_user.id)
            session.add(new_bascket)
            session.commit()
    rendered = render_template('first_page.html', form=form, dishes=dishes,
                               breakfast=breakfast, lunch=lunch)
    session.close() # Проверка
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
        elif form.top_up_acc.data:
            return redirect(url_for('top_up_acc'))
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
        elif form.top_up_acc.data:
            return redirect(url_for('top_up_acc'))
    return render_template('profile.html', form=form, user=user)


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    form = Reviews()
    session = create_session()
    reviews = session.query(Review).order_by(Review.created_date.desc()).all()
    session.close()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
        elif form.button_add_reviews.data:
            return redirect(url_for('new_reviews'))
        elif form.top_up_acc.data:
            return redirect(url_for('top_up_acc'))
    return render_template('reviews.html', form=form, reviews=reviews)


@app.route('/new_reviews', methods=['GET', 'POST'])
def new_reviews():
    form = New_reviews()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
        elif form.top_up_acc.data:
            return redirect(url_for('top_up_acc'))
        elif form.button_add_reviews.data:
            session = create_session()
            
            new_review = Review(
                info=form.info.data,  # То, что ввели в поле
                id_user=current_user.id  # Кто написал
            )
            
            session.add(new_review)
            session.commit()
            session.close()
            print('ВСЕ РАБОТАЕТ!!!!!!!!!!!!!!!!!!!!')
            return redirect(url_for('reviews'))
    else:
        print("НЕ работает!!!!!!!!!!!!!!!")
    return render_template('new_reviews.html', form=form)


@app.route('/bascket', methods=['GET', 'POST'])
def bascket():
    form = BascketForm()
    session = create_session()
    object = session.query(Bascket).filter(Bascket.user_id == current_user.id).all()
    breakfast = session.query(Dish).filter(Dish.type == 'breakfast' and Bascket.user_id == current_user.id).all()
    lunch = session.query(Dish).filter(Dish.type == 'lunch' and Bascket.user_id == current_user.id).all()
    dishes = session.query(Dish).filter(Dish.type == 'dish' and Bascket.user_id == current_user.id).all()
    bascket_sum = sum(elem.dish.price for elem in object)
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
        elif form.top_up_acc.data:
            return redirect(url_for('top_up_acc'))
    if request.method == 'POST':
        dish_id = request.form.get('dish_id')
        if dish_id:
            # 1. ИЩЕМ существующую запись в базе
            # Находим ПЕРВУЮ попавшуюся запись с таким блюдом у этого юзера
            item_to_delete = session.query(Bascket).filter(
                Bascket.user_id == current_user.id,
                Bascket.dish_id == int(dish_id)
            ).first()

            # 2. Если нашли — удаляем
            if item_to_delete:
                session.delete(item_to_delete)
                session.commit()
            else:
                print("Такого товара нет в корзине") # Для отладки
        return redirect(url_for('bascket'))
    return render_template('bascket.html', form=form, object=object, dishes=dishes, breakfast=breakfast, lunch=lunch, bascket_sum=bascket_sum)


@app.route('/top_up_acc', methods=['GET', 'POST'])
def top_up_acc():
    form = Top_up_acc()
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
    return render_template('top_up_acc.html', form=form)


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
