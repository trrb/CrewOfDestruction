"""import sqlalchemy
import datetime
from sqlalchemy.orm import relationship
from .base import Base


class Bascket(Base):
    __tablename__ = 'bascket'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_dish = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('dish.id'))
    info = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = relationship('Dish', back_populates='reviews', lazy='joined')"""
