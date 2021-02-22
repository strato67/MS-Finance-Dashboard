from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

#Creating search bar variables
class Search(FlaskForm):
    tickerSearch = StringField('Ticker')
    submit = SubmitField('Search')
