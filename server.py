from flask import Flask, render_template, request
from search import Search
import yfinance as yf 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pass'

#NOTE, NOW THAT YOU HAVE TICKER ACCESS, SEE IF YOU CAN SUB INTO REMAINING TRADINGVIEW FUCNTIONS

@app.route('/', methods=['GET','POST'])
def mainPage():
    form = Search()
    if form.is_submitted():
        result = request.form.getlist('tickerSearch')
        result=result[0]

        stock = yf.Ticker(result)
        info = sorted([[k, v]for k, v in stock.info.items()])

        return render_template('stockboard.html',result=info)
    return render_template('mainPage.html', form = form)

if __name__ =='__main__':
    app.run()
