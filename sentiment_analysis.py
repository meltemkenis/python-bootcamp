# Meltem Keniş
# August 2019 - "Python and Machine Learning" project
# Sentiment Analysis of Global Warming Using Twitter

## Data retrieval from Twitter:

from warnings import filterwarnings
filterwarnings('ignore')

# Key and tokens which are necessary to enter Twitter API:

import tweepy, codecs

consumer_key = 'XXX'
consumer_secret = 'XXX'
access_token = 'XXX'
access_token_secret = 'XXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# We specify the features of the data that we will extract from Twitter:

tweetler = api.search(q = "#globalwarming", lang = "en", result_type = "mix", count = 1000)


#  We specify the features of the tweets with globalwarming hashtag:

import pandas as pd

def hashtag_df(tweetler):
    id_list = [tweet.id for tweet in tweetler]
    df = pd.DataFrame(id_list, columns = ["id"])
    
    df["text"] = [tweet.text for tweet in tweetler]
    df["created_at"] = [tweet.created_at for tweet in tweetler]
    df["retweeted"] = [tweet.retweeted for tweet in tweetler]
    df["retweet_count"] = [tweet.retweet_count for tweet in tweetler]
    df["user_screen_name"] = [tweet.author.screen_name for tweet in tweetler]
    df["user_followers_count"] = [tweet.author.followers_count for tweet in tweetler]
    df["user_location"] = [tweet.author.location for tweet in tweetler]
    df["Hashtags"] = [tweet.entities.get('hashtags') for tweet in tweetler]
    
    return df


# Converting tweets with globalwarming hashtag to a dataframe:
df = hashtag_df(tweetler)


# Saving dataframe as csv file.
df.to_csv("data_twitter.csv")


## Text Mining:


# Case conversion:
df['text'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))

# Removing numbers, punctuations and 'rt' expressions:
df['text'] = df['text'].str.replace('[^\w\s]','')
df['text'] = df['text'].str.replace('rt','')
df['text'] = df['text'].str.replace('\d','')

# Removing stopwords (I, me, myself, he, she, they, our, mine, you, yours):
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
sw = stopwords.words('english')
df['text'] = df['text'].apply(lambda x: " ".join(x for x in x.split() if x not in sw))

get_ipython().system('pip install textblob')

# Lemmi
from textblob import Word
nltk.download('wordnet')
df['text'] = df['text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()])) 


## Creating Word Cloud:

get_ipython().system('pip install WordCloud')


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


text = " ".join(i for i in df.text)

wordcloud = WordCloud(background_color = "white").generate(text)
plt.imshow(wordcloud, interpolation = "bilinear")
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()


## Sentiment Analysis:

from textblob import TextBlob
def sentiment_skorla(df):

    text = df["text"]

    for i in range(0,len(text)):
        textB = TextBlob(text[i])
        sentiment_skoru = textB.sentiment.polarity
        df.set_value(i, 'sentiment_skoru', sentiment_skoru)
        
        if sentiment_skoru <0.00:
            duygu_sinifi = 'Negatif'
            df.set_value(i, 'duygu_sinifi', duygu_sinifi )

        elif sentiment_skoru >0.00:
            duygu_sinifi = 'Pozitif'
            df.set_value(i, 'duygu_sinifi', duygu_sinifi )

        else:
            duygu_sinifi = 'Notr'
            df.set_value(i, 'duygu_sinifi', duygu_sinifi )
            
    return df

df = hashtag_df(tweetler)
sgw = sentiment_skorla(df)

sgw.to_csv("sentiment_global_warming.csv")
df.groupby("duygu_sinifi").count()["id"]
duygu_freq = df.groupby("duygu_sinifi").count()["id"]
duygu_freq.plot.bar(x = "duygu_sinifi",y = "id");
