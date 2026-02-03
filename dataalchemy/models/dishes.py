import sqlalchemy
from sqlalchemy.orm import relationship
from .base import Base


class Dish(Base):

    __tablename__ = 'dishes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    foods = relationship(
        'Food',
        secondary='dish_foods',
        back_populates='dishes'
    )

    type = sqlalchemy.Column(sqlalchemy.String(50))

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
