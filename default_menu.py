from dataalchemy import Dish, DishFood, LunchDish, BreakfastDish

default_menu = [
    BreakfastDish(name='Бутерброд с ветчиной', price=50.0),
    BreakfastDish(name='Какао', price=70.0, allergen_name='lactose'), # Молоко
    BreakfastDish(name='Омлет', price=130.0, allergen_name='eggs'), # Яйца
    BreakfastDish(name='Рисовая каша', price=200.0, allergen_name='lactose'),
    BreakfastDish(name='Бутерброд с сыром и маслом', price=30.0, allergen_name='lactose'),
    BreakfastDish(name='Каша овсянка', price=99.0),
    BreakfastDish(name='Оладья', price=110.0),
    BreakfastDish(name='Сырники', price=70.0, allergen_name='lactose'),
    BreakfastDish(name='Булгур отварной', price=99.0), 
    LunchDish(name='Борщ', price=210.0),
    LunchDish(name='Кола', price=150.0),
    LunchDish(name='Компот', price=60.0),
    LunchDish(name='Котлеты с гречкой', price=120.0),
    LunchDish(name='Куриный суп', price=170.0),
    LunchDish(name='Макароны с курицей', price=130.0), 
    LunchDish(name='Рассольник', price=130.0),
    LunchDish(name='Салат из морковки', price=56.0),
    LunchDish(name='Салат из свеклы', price=50.0),
    LunchDish(name='Суп гороховый', price=110.0),
    LunchDish(name='Яблочный сок', price=20.0),
    BreakfastDish(name='Чай', price=70.0)
]
