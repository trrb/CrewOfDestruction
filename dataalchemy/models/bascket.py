import sqlalchemy
import datetime
from sqlalchemy.orm import relationship
from .base import Base


class Bascket(Base):
    __tablename__ = 'bascket'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    id_dish = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('dishes.id'))

    user = relationship('User', back_populates='bascket', lazy='joined')
    dishes = relationship('Dish', back_populates='bascket', lazy='joined')