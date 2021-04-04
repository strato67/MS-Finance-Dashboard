from newsapi.newsapi_client import NewsApiClient



# Init
newsapi = NewsApiClient(api_key='2472f965378e4f079bc9f24dac794181')

# /v2/top-headlines
top_headlines = newsapi.get_everything(q='tsla',language='en',page_size=3)

articles = top_headlines['articles']  

print(articles[0].values())
                                    
