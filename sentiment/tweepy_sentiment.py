from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import tweepy
import numpy as np
import pandas as pd



class Import_tweet_sentiment:
    
    # consumer_key = "96Cf6dirsIICAsIgEFdD9Ovr1"
    # consumer_secret = "AhRpwzogff1Er00R8ZO1Rrt7WdRApRcwlf4uvaj1SM6ZfxILpc"
    # access_token = "1273571257821196293-TJ7fYe5le58Ht5Ob849sAEu3YoRtLL"
    # access_token_secret = "oXHKRe23ZQ4bga0uhybhSGeF3ERy3cXABYx9SCN74P6GM"

    # consumer_key="pda0lb8na7kjeFpPbW9nwgz2P"
    # consumer_secret="lRfQ2Z5FzHpVf5wL5BKdpXoKfV13x5MkGWFRD42aNRCWnSQOuZ"
    # access_token="1394133781825560582-eNYfHOqtM96wDWoq2xbLlQ1u9l3NwN"
    # access_token_secret="m910Sg4Imp0gYnqzNi6CjIoPl8zvGSiSrfX14w35sFzmd"

    consumer_key = "96Cf6dirsIICAsIgEFdD9Ovr1"
    consumer_secret = "AhRpwzogff1Er00R8ZO1Rrt7WdRApRcwlf4uvaj1SM6ZfxILpc"
    access_token = "1273571257821196293-TJ7fYe5le58Ht5Ob849sAEu3YoRtLL"
    access_token_secret = "oXHKRe23ZQ4bga0uhybhSGeF3ERy3cXABYx9SCN74P6GM"


    def tweet_to_data_frame(self, tweets):
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=['Tweets'])
        return df

    def get_tweets(self, handle):
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        auth_api = API(auth)

        account = handle
        item = auth_api.user_timeline(id=account, count=50)
        df = self.tweet_to_data_frame(item)

        all_tweets = []
        for j in range(50):
            all_tweets.append(df.loc[j]['Tweets'])
        return all_tweets

    def get_hashtag(self, hashtag):
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        auth_api = API(auth)

        account = hashtag
        all_tweets = []

        for tweet in tweepy.Cursor(auth_api.search, q=account, tweet_mode="extended", lang='id').items(50):
            all_tweets.append(tweet.full_text)

        return all_tweets

    
