import sqlalchemy
from .base import Base


class DishFood(Base):
    __tablename__ = 'dish_foods'

    dish_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('dishes.id'),
        primary_key=True
    )

    food_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('foods.id'),
        primary_key=True
    )
