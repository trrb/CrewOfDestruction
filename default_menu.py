from dataalchemy import Dish, LunchDish, BreakfastDish

default_menu = [
    BreakfastDish(name='Бутерброд с ветчиной', price=50.0, allergen_name='gluten'), 
    BreakfastDish(name='Какао', price=70.0, allergen_name='lactose'),
    BreakfastDish(name='Омлет', price=130.0, allergen_name='eggs'),
    BreakfastDish(name='Рисовая каша', price=200.0, allergen_name='lactose'), 
    BreakfastDish(name='Бутерброд с сыром и маслом', price=30.0, allergen_name='lactose'), 
    BreakfastDish(name='Каша овсянка', price=99.0, allergen_name='gluten'), 
    BreakfastDish(name='Оладья', price=110.0, allergen_name='gluten'), 
    BreakfastDish(name='Сырники', price=70.0, allergen_name='lactose'),
    BreakfastDish(name='Булгур отварной', price=99.0, allergen_name='gluten'), 
    BreakfastDish(name='Рыбные котлеты', price=400, allergen_name='fish'),
    LunchDish(name='Борщ', price=210.0),
    LunchDish(name='Кола', price=150.0),
    LunchDish(name='Компот', price=60.0),
    LunchDish(name='Котлеты с гречкой', price=120.0),
    LunchDish(name='Куриный суп', price=170.0), 
    LunchDish(name='Макароны с курицей', price=130.0, allergen_name='gluten'), 
    LunchDish(name='Рассольник', price=130.0),
    LunchDish(name='Салат из морковки', price=56.0),
    LunchDish(name='Салат из свеклы', price=50.0),
    LunchDish(name='Суп гороховый', price=110.0),
    LunchDish(name='Яблочный сок', price=20.0),
    LunchDish(name='Красная рыба', price=500, allergen_name='fish'),
    LunchDish(name='Морепродукты', price=700, allergen_name='fish'),
    BreakfastDish(name='Чай', price=70.0)
]
