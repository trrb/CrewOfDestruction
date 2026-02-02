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
