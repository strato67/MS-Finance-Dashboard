from newsapi.newsapi_client import NewsApiClient



# Init
newsapi = NewsApiClient(api_key='2472f965378e4f079bc9f24dac794181')

# /v2/top-headlines
top_headlines = newsapi.get_everything(q='bitcoin')
                                          
print (top_headlines)

    
                                    
