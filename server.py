from flask import Flask, render_template, request
from search import Search
import yfinance as yf 
from newsapi import NewsApiClient

# Initialize news api and test documentation
newsapi = NewsApiClient(api_key='2472f965378e4f079bc9f24dac794181')
#top_headlines = newsapi.get_top_headlines(q='bitcoin')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pass'


#Dashboard main page
@app.route('/', methods=['GET','POST'])

def mainPage():
    form = Search()
    
    if form.is_submitted():

        #Try catch to prevent invalid ticker searches
        try:
            result = request.form.getlist('tickerSearch')
            result=result[0]
            stock = yf.Ticker(result)
            info = list(stock.info.items())
            financials = stock.financials.items()

            
            return render_template('stockboard.html',info=info,result=result, length = len(info))
        except:
            return render_template('stockboard.html')
    return render_template('mainPage.html', form = form)

if __name__ =='__main__':
    app.run()
    msft = yf.Ticker("MSFT")
    print(msft.financials.keys)
                                    
