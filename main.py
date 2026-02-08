from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, \
    current_user
from dataalchemy import create_session, global_init
from dataalchemy import User, Dish, Food, DishFood, LunchDish, \
    BreakfastDish, RoleAdmin, RoleCook, Review, Bascket, Allergen
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
from flask import flash
from dataalchemy.models.history import History
import datetime
from datetime import timedelta
from forms.cook_dashboard import Cook

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
            role = user.role_id 
            session.close()
            if role == 3: # Админ
                return redirect(url_for('admin_dashboard'))
            elif role == 2: # Повар
                return redirect(url_for('cook_dashboard'))
            else: # Ученик
                return redirect(url_for('first_page'))
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
    user = session.query(User).get(current_user.id)
    breakfast = session.query(Dish).filter(Dish.type == 'breakfast').all()
    lunch = session.query(Dish).filter(Dish.type == 'lunch').all()
    dishes = session.query(Dish).filter(Dish.type == 'dish').all()
    forbidden_allergens = [a.name for a in user.allergens]

    def is_safe(dish):
        if not dish.allergen_name:
            return True
        if dish.allergen_name in forbidden_allergens:
            return False
        return True
    
    breakfast_access = [d for d in breakfast if is_safe(d)]
    lunch_access = [d for d in lunch if is_safe(d)]
    dishes_access = [d for d in dishes if is_safe(d)]
    if request.method == 'POST':
        dish_id = request.form.get('dish_id')
        if dish_id:
            new_bascket = Bascket(dish_id=int(dish_id), # 123
                                  user_id=current_user.id)
            session.add(new_bascket)
            session.commit()
            added_dish = session.query(Dish).get(int(dish_id))
            
            anchor = 'top'
            if added_dish:
                if added_dish.type == 'breakfast':
                    anchor = 'section-breakfast'
                elif added_dish.type == 'lunch':
                    anchor = 'section-lunch'
        
            return redirect(url_for('first_page', _anchor=anchor))
    session.close() # Проверка
    if form.validate_on_submit():
        anchor = 'top'
        if form.profile.data:
            return redirect(url_for('profile', _anchor=anchor))
        elif form.reviews.data:
            return redirect(url_for('reviews', _anchor=anchor))
        elif form.basket.data:
            return redirect(url_for('bascket', _anchor=anchor))
        elif form.top_up_acc.data:
            return redirect(url_for('top_up_acc', _anchor=anchor))
    return render_template('first_page.html', form=form, dishes=dishes_access,
                               breakfast=breakfast_access, lunch=lunch_access)


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
    user_history = session.query(History).filter(History.id_user == current_user.id).order_by(History.created_date.desc()).all()
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
    session.close()
    return render_template('profile.html', form=form, user=user, history=user_history)


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
    is_free = False
    if current_user.has_active_subscription():
        is_free = True
        final_price_to_pay = 0 # Платить ничего не надо
    else:
        final_price_to_pay = bascket_sum
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
        if form.accept_bascket.data:  # Если нажали "Оформить заказ"
            user = session.query(User).filter(User.id == current_user.id).first()
            if user.balance >= final_price_to_pay:
                user.balance -= final_price_to_pay
                dish_names = [item.dish.name for item in object]
                dishes_string = ", ".join(dish_names)
                new_order = History(
                    id_user=current_user.id,
                    name=dishes_string,      # Список блюд
                    summa=bascket_sum,       # Общая сумма
                    info="Оплачено"          # Статус (т.к. поле обязательное)
                )
                session.add(new_order)
                for item in object:
                    session.delete(item)#ПОтом добавить чтоб поварихам все улетало------------
                
                session.commit()
                flash('Заказ успешно оплачен!')
                return redirect(url_for('profile')) # Перекидываем в профиль
            else:
                #сидим на попе ровно и не чирикаем
                print("Недостаточно средств!") 
                flash('Недостаточно средств!', 'error')
                # Остаемся на странице корзины
        delete_dish_id = request.form.get('delete_dish_id')
        if delete_dish_id:
            item_to_delete = session.query(Bascket).filter(
                Bascket.user_id == current_user.id,
                Bascket.dish_id == int(delete_dish_id)
            ).first()
            if item_to_delete:
                session.delete(item_to_delete)
                session.commit()
            else:
                print("Такого товара нет в корзине")
        return redirect(url_for('bascket'))
    return render_template('bascket.html', form=form, object=object, dishes=dishes, breakfast=breakfast, lunch=lunch, bascket_sum=bascket_sum)


@app.route('/top_up_acc', methods=['GET', 'POST'])
def top_up_acc():
    form = Top_up_acc()
    if request.method == 'POST':
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        if form.top_up_acc_balance.data:
            print('Кнопка нажата!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            if user:
                money_to_add = int(form.top_up.data)
                current_balance = user.balance if user.balance else 0
                user.balance = current_balance + money_to_add
                session.commit()
                print(f'Баланс пополнен на {money_to_add}! Теперь: {user.balance}')
                print('ВСЕ РАБОТАЕТ!!!!!!!!!!!!!!!!!!!!')
                session.close()
            return redirect(url_for('top_up_acc'))
        if form.submit_subscription.data:
            SUBSCRIPTION_PRICE = 3000
            
            if user.balance >= SUBSCRIPTION_PRICE:
                user.balance -= SUBSCRIPTION_PRICE
                
                # Если уже был абонемент, продлеваем, если нет ставим с сегодня
                now = datetime.datetime.now()
                if user.subscription_until and user.subscription_until > now:
                    user.subscription_until += timedelta(days=30)
                else:
                    user.subscription_until = now + timedelta(days=30)
                
                session.commit()
                flash('Абонемент успешно куплен!', 'success')
            else:
                flash('Недостаточно средств для покупки абонемента!', 'error')
    else:
        print("НЕ работает!!!!!!!!!!!!!!!")
    return render_template('top_up_acc.html', form=form)


@app.route('/alergen_add', methods=['GET', 'POST'])
@login_required
def alergen_add():
    form = Alergen_add()
    session = create_session()
    all_allergens = session.query(Allergen).all()
    user = session.query(User).get(current_user.id)
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
    if request.method == 'POST' and 'save_allergens' in request.form:
        user.allergens = []
        selected_ids = request.form.getlist('allergen_ids')
        for a_id in selected_ids:
            allergen = session.query(Allergen).get(int(a_id))
            if allergen:
                user.allergens.append(allergen)
        session.commit()
        flash('Список аллергенов обновлен!', 'success')
        return redirect(url_for('alergen_add'))
    return render_template('alergen_add.html', form=form, 
                           all_allergens=all_allergens, user=user)

@app.route('/cook_dashboard', methods=['GET', 'POST'])
@login_required
def cook_dashboard():
    form = Cook()
    session = create_session()
    history_dish = session.query(History).all()
    user = session.query(User).get(current_user.id)
    if form.validate_on_submit():
        if form.profile.data:
            return redirect(url_for('profile'))
        elif form.menu.data:
            return redirect(url_for('first_page'))
        elif form.reviews.data:
            return redirect(url_for('reviews'))
        elif form.basket.data:
            return redirect(url_for('bascket'))
    if request.method == 'POST' and 'save_allergens' in request.form:
        user.allergens = []
        selected_ids = request.form.getlist('allergen_ids')
        for a_id in selected_ids:
            allergen = session.query(Allergen).get(int(a_id))
            if allergen:
                user.allergens.append(allergen)
        session.commit()
        flash('Список аллергенов обновлен!', 'success')
        return redirect(url_for('alergen_add'))
    return render_template('alergen_add.html', form=form, 
                           all_allergens=all_allergens, user=user)
if __name__ == "__main__":
    session = create_session()
    try:
        allergen_names = ['lactose', 'eggs'] 
        for name in allergen_names:
            if not session.query(Allergen).filter(Allergen.name == name).first():
                session.add(Allergen(name=name)) 
        session.commit()
        a = session.query(Dish).all()
        names = [x.name for x in a]
        for dish in default_menu:
            if dish.name not in names:
                session.add(dish)    
        admin_email = "sosok@school.ru"
        if not session.query(User).filter(User.email == admin_email).first():
            admin = RoleAdmin(
                name="Админушка батюшка",
                email=admin_email,
                role_id=3
            )
            admin.set_password("admin_god")
            session.add(admin)
            session.commit()
            print("Админ создан")
        
        # Проверка
        cook_email = "cook@school.ru"
        if not session.query(User).filter(User.email == cook_email).first():
            cook = RoleCook(
                name="Меган фокс",
                email=cook_email,
                role_id=2
            )
            cook.set_password("cook123")
            session.add(cook)
            print("Повар создан")  
        session.commit()
    except Exception as e:
        print(f'Аларм!!! сайта не будет потому что {e}')
        session.rollback()
    finally:
        session.close()
    app.run(debug=True)
