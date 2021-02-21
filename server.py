from flask import Flask, render_template, request
from search import Search
import yfinance as yf 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pass'

#NOTE, NOW THAT YOU HAVE TICKER ACCESS, SEE IF YOU CAN SUB INTO REMAINING TRADINGVIEW FUCNTIONS, ALSO CHANGE OUTPUT FORMAT FOR info, LOOK IN NOTEPAD BACKUP

@app.route('/', methods=['GET','POST'])
def mainPage():
    form = Search()
    if form.is_submitted():
        try:
            result = request.form.getlist('tickerSearch')
            result=result[0]
            stock = yf.Ticker(result)
            info = stock.info.items()
            return render_template('stockboard.html',info=info,result=result)
        except:
            return render_template('stockboard.html')
    return render_template('mainPage.html', form = form)

if __name__ =='__main__':
    app.run()
