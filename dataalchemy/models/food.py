import sqlalchemy
from sqlalchemy.orm import relationship
from .base import Base


class Food(Base):

    __tablename__ = 'foods'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    count_now = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    dishes = relationship(
        'Dish',
        secondary='dish_ingredients',
        back_populates='foods'
    )
