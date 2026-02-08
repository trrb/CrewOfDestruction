import datetime
import sqlalchemy
from sqlalchemy.orm import relationship
from .base import Base

class PurchaseRequest(Base):
    __tablename__ = 'purchase_requests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    product_name = sqlalchemy.Column(sqlalchemy.String, nullable=False) 
    count = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String, default='pending')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    
    cook_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    cook = relationship('User', backref='purchase_requests')
