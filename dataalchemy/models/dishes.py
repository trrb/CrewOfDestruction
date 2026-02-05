import sqlalchemy
from sqlalchemy.orm import relationship
from .base import Base


class Dish(Base):

    __tablename__ = 'dishes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    price = sqlalchemy.Column(sqlalchemy.Float, default=0.0)
    type = sqlalchemy.Column(sqlalchemy.String)

    foods = relationship(
        'Food',
        secondary='dish_foods',
        back_populates='dishes'
    )

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "dish"
    }

class BreakfastDish(Dish):
    __mapper_args__ = {
        "polymorphic_identity": "breakfast"
    }


class LunchDish(Dish):
    __mapper_args__ = {
        "polymorphic_identity": "lunch"
    }
