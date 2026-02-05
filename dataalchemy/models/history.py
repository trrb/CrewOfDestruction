import sqlalchemy
import datetime
from sqlalchemy.orm import relationship
from .base import Base


class History(Base):
    __tablename__ = 'history'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    summa = sqlalchemy.Column(sqlalchemy.Integer)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = relationship('User', back_populates='history', lazy='joined')