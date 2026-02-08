import sqlalchemy
from sqlalchemy.orm import relationship
from .base import Base 


user_allergens_table = sqlalchemy.Table(
    'user_allergens',
    Base.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('allergen_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('allergens.id'))
)

class Allergen(Base):
    __tablename__ = 'allergens'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)


    sufferers = relationship(
        'User',
        secondary=user_allergens_table,
        back_populates='allergens'
    )
