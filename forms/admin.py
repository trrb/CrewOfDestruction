from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class ChangeRoleForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Роль', choices=[('2', 'Повар'), ('1', 'Ученик')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить')
