from newsapi.newsapi_client import NewsApiClient



# Init
newsapi = NewsApiClient(api_key='2472f965378e4f079bc9f24dac794181')

# /v2/top-headlines
top_headlines = newsapi.get_everything(q='tsla',language='en',page_size=3)

articles = top_headlines['articles']  

for x,y in enumerate(articles):
    print(f'{x}{y["title"]}')

for key, value in articles[0].items():
    print(value)
    
                                    
