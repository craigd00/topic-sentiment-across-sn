import tweepy
import json
from pymongo import MongoClient
import certifi
import time
from twittercredentials import consumer_key, consumer_secret, access_token, access_token_secret
from mongodbcredentials import CONNECTION_STRING, CONNECTION_STRING_JAN_A, CONNECTION_STRING_JAN_1, CONNECTION_STRING_JAN_2, CONNECTION_STRING_TRAINING_DATA
import datetime

auth = tweepy.OAuthHandler(consumer_key, consumer_secret )      # twitter auth credentials
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


client = MongoClient(CONNECTION_STRING_TRAINING_DATA, tlsCAFile=certifi.where())        # connects to MongoDB
twitter_db = client.CoronavirusTwitter     # connects to database
tweet_collection = twitter_db['TrainingValidationTest']     # database in collection

query = "vaccine"       #test query at the moment to test

num_of_tweets = 100     # number of tweets to retrieve at a time
last_id = -1        # allows collection of tweets not looked at yet
tweets = True       # for determining if there is still new tweets coming in
requests = -1        # tracks how many requests made

storing_tweets = []

while tweets:       # while there is still new tweets
        requests+=1      # increments requests

        try:
            if(requests < 150):      # to respect limit of api

                tweets = api.search_tweets(q=query, count=num_of_tweets, lang="en", tweet_mode='extended', max_id=str(last_id - 1))     # searches for the tweets with query
         
                if not tweets:      # if no more tweets has been retrieved, stops
                    break
          
                for t in tweets:        # for each new tweet
                   
                    t = json.dumps(t._json)     # gets tweet as json
                    tweet = json.loads(t)
                    
                    retweet = False

                    if tweet['retweeted'] or tweet['full_text'].startswith('RT') == True:       # checks if it is a retweet
                        retweet = True

                    if tweet['truncated']:      # if truncated, it gets the full text
                        text = tweet['extended_tweet']['full_text']
                    else:
                        text = tweet['full_text']

                    if (retweet == False) and (text not in storing_tweets):     # no point adding exact same text to tweet database
                        storing_tweets.append(text)     # adds to total list
                        text = {'tweet': text}
                        print(text)
                        tweet_collection.insert_one(text)       # adds tweet to collection
                     
                last_id = tweets[-1].id
            else:
                print("Sleeping for 15 minutes")
                requests = 0     # resets requests
                time.sleep(15*60)       # sleeps for 15 minutes
                print(str(datetime.datetime.now()))     # prints date
                
        except tweepy.TweepyException as e:
            pass