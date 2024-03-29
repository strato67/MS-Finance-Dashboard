from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import yfinance as yf 
import os
import requests
from newsapi.newsapi_client import NewsApiClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Crave123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Dashboard/mydb.db'
newsapi = NewsApiClient(api_key='2472f965378e4f079bc9f24dac794181')

Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#database table
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=25)])
    remember = BooleanField('remember')
 
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=25)])

#Creating search bar variables
class Search(FlaskForm):
     tickerSearch = StringField('Ticker')
     submit = SubmitField('Search')


@app.route('/')
def index():
    form = LoginForm()    
    #test that form submits
    if form.validate_on_submit(): 
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember = form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username/password </h1>'
    #     return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'


    return render_template('index.html',form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()    
    #test that form submits
    if form.validate_on_submit(): 
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember = form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username/password </h1>'
    #     return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html',form=form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegisterForm()
    #test that form submits
    if form.validate_on_submit(): 
        new_user = User(username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('index'))
        
    #     return '<h1>' + form.username.data + ' ' + form.password.data + ' ' + form.email.data + '</h1>'

    return render_template('Register.html', form=form)

@app.route('/dashboard',  methods = ['GET', 'POST'])
@login_required
def dashboard():
    form = Search()
    
    if form.is_submitted():

        #Try catch to prevent invalid ticker searches
        try:
            
            result = request.form.getlist('tickerSearch')
            result=result[0]
            stock = yf.Ticker(result)
            info = list(stock.info.items())
            top_headlines = newsapi.get_everything(
                q=result + " " + "stock", language='en', page_size=5)
            articles = top_headlines['articles']
            return render_template('stockboard.html',info=info,result=result, length = len(info), headlines = articles)
        except:
            return render_template('stockboard.html')
    return render_template('mainPage.html', form = form)
    
    # return render_template('dashboard.html', name = current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
