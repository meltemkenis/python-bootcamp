# Meltem Keniş
# Ağustos 2019 - Kodluyoruz Akademi "Python ve Makine Öğrenmesi" bitirme projesi
# Sentiment Analysis of Global Warming Using Twitter

## Twitter'dan Veri Çekmek:

from warnings import filterwarnings
filterwarnings('ignore')

# Twitter API'sine girmek için gereken key ve token'lar:
import tweepy, codecs

consumer_key = 'XXX'
consumer_secret = 'XXX'
access_token = 'XXX'
access_token_secret = 'XXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Veri çekeceğimiz hashtag'in adını, dilini belirtiyoruz. Çekeceğimiz tweetler popular mi olsun, güncel mi olsun, 
# karma mı olsun seçeneklerinden karma'yı (mix) seçiyoruz. Count'u 1000 ayarladık ama api limiti olduğu için kaç gelir
# bilmiyoruz:
tweetler = api.search(q = "#globalwarming", lang = "en", result_type = "mix", count = 1000)


# globalwarming hashtagindeki tweet'lerin hangi özellikleri içereceğini belirtiyoruz:
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


# globalwarming hashtag'i ile atılan tweet'leri dataframe'e çevirmek:
df = hashtag_df(tweetler)


# dataframe'i csv olarak kaydetme
df.to_csv("data_twitter.csv")


## Text Mining:


# büyük-küçük harf dönüşümü
df['text'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))

# sayıları, noktalama işaretlerini, 'rt' ifadesini kaldırma:
df['text'] = df['text'].str.replace('[^\w\s]','')
df['text'] = df['text'].str.replace('rt','')
df['text'] = df['text'].str.replace('\d','')

# stopwords (I, me, myself, he, she, they, our, mine, you, yours) ifadelerini kaldırma:
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
sw = stopwords.words('english')
df['text'] = df['text'].apply(lambda x: " ".join(x for x in x.split() if x not in sw))


get_ipython().system('pip install textblob')
# lemmi
from textblob import Word
nltk.download('wordnet')
df['text'] = df['text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()])) 


## Word Cloud Oluşturma:

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


## Sentiment Analizi:

get_ipython().system('pip install vaderSentiment')


# Sentiment analizi için hazır kütüphaneler kullanıyoruz. Burada bazı kelimelerin skorları var. Mesela "bad" 
# kelimesinin skoru -5 iken, "good" kelimesinin skoru +4. 
# Biz bir cümle veya kelime sorduğumuzda da bu skorlara göre kelime skoru veya cümlenin toplam skoru veriliyor.

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

# Çıktıdaki compound cümlenin/kelimenin genel olarak pozitif mi negatif mi olduğunu söylüyor bize. 
# Bu arada aynı cümleyi ünlem işaretini artırarak yazdığımızda cümlenin negativitesinin arttığını görebiliriz.

analyser.polarity_scores("Let me form a bad sentence.")

analyser.polarity_scores("Let me form a bad sentence.")

analyser.polarity_scores("Let me form a bad sentence!")

analyser.polarity_scores("Let me form a bad sentence!!")

analyser.polarity_scores("Let me form a BAD sentence.")

analyser.polarity_scores("Let me form a bad sentence!!!")


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
