import sqlalchemy
from sqlalchemy.orm import relationship
from .base import Base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    balance = sqlalchemy.Column(sqlalchemy.Float, default=0.0)

    role_id = sqlalchemy.Column(sqlalchemy.Integer)

    reviews = relationship('Review', back_populates='user')

    history = relationship('History', back_populates='user')

    bascket = relationship('Bascket', back_populates='user')

    __mapper_args__ = {
        'polymorphic_on': role_id,
        'polymorphic_identity': 'student',
    }

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class RoleAdmin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }


class RoleCook(User):
    __mapper_args__ = {
        'polymorphic_identity': 'cook',
    }