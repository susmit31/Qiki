from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    query = StringField('Topic or link', validators=[DataRequired()])
    is_url = BooleanField('Is URL')
    search_button = SubmitField('Search')
