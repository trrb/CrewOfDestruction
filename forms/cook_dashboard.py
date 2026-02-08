from flask_wtf import FlaskForm
from wtforms import SubmitField



class Cook(FlaskForm):
    send_request = SubmitField('Подать заявку')
    give_dish = SubmitField('выдать')
