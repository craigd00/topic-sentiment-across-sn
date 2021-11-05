import tweepy
import json
from pymongo import MongoClient
from datetime import datetime
import time
import sys

import emoji
import re

from twittercredentials import consumer_key, consumer_secret, access_token, access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret )
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

query = "Nicola Sturgeon"  #test query at the moment to test

count = 100 # number of tweets to grab in one go

last_id = -1    # used to update last id to gather tweets from different users
new_tweets = True   # used to go round in loop
counter = -1    # counter to update times we have gathered data

storing_tweets = []

while new_tweets:
        counter+=1 

        try:
            if(counter < 180):  
                new_tweets = api.search(q=query, count=count, lang="en", tweet_mode='extended', max_id=str(last_id - 1))
         
                if not new_tweets:
                    break
          
                for t in new_tweets:
                   
                    t = json.dumps(t._json) 
                    tweet = json.loads(t)

                    retweet = False

                    if tweet['retweeted'] or tweet['full_text'].startswith('RT') == True:
                        retweet = True

                    if tweet['truncated']:
                        text = tweet['extended_tweet']['full_text']
                    else:
                        text = tweet['full_text']

                    if (retweet == False) and (text not in storing_tweets): #no point adding same text to list, will encourage bot tweets etc
                        storing_tweets.append(text)
                     
                last_id = new_tweets[-1].id
            else:
                print("15 minute delay")
                counter = 0
                time.sleep(15*60) 
                
        except tweepy.TweepError as e:
            break