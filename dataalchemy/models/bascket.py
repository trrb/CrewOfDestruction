import sqlalchemy
import datetime
from sqlalchemy.orm import relationship
from .base import Base


class Bascket(Base):
    __tablename__ = 'bascket'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('users.id'),
        nullable=False
    )

    dish_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('dishes.id'),
        nullable=False
    )


    user = relationship('User', back_populates='bascket')
    dish = relationship('Dish', back_populates='bascket')