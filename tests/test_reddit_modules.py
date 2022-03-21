from src.shared_modules import database_as_tweet, positive_neg_count_df, bert_preprocess, process_emoji

from pymongo import MongoClient
import certifi
import pandas as pd

CONNECTION_STRING = "mongodb+srv://craig:Dissertation2021-22@socialmediadatasets.aye5g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
reddit_data = [
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx"},
        {"post": "cant wait for my vaccine tomorrow :)", "subreddit": "covid19"},
        {"post": "tomorrow is my vaccine", "subreddit": "covid19"}
    ]

def test_reddit_database():


    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    database = client.RedditVaccination2
    
    db_return = database_as_tweet(database, "reddit")

    assert db_return['subreddit'].iloc[4] == "Anxiety"


def test_bert_preprocess():
    post = "@PiersMorgan https://twitter.com please delete your account"

    processed = bert_preprocess(post)
   
    assert processed == " http please delete your account"


def test_emoji_regex():
    post = "Today is a great day😀"

    remove_emoji = process_emoji(post)

    assert remove_emoji == "Today is a great day"