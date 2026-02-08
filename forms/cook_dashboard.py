from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CookForm(FlaskForm):
    product_name = StringField('Название продукта', validators=[DataRequired()])
    quantity = StringField('Количество', validators=[DataRequired()])
    send_request = SubmitField('Отправить заявку')
