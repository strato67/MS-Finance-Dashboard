from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class Search(FlaskForm):
    tickerSearch = StringField('Ticker')
    submit = SubmitField('Search')
