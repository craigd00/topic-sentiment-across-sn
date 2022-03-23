from src.shared_modules import database_as_vader, database_as_afinn, database_as_textblob, database_as_bert, \
    positive_neg_count_df, database_as_tweet, bert_preprocess, process_emoji

from pymongo import MongoClient
import certifi
import pandas as pd

CONNECTION_STRING = "mongodb+srv://craig:Dissertation2021-22@socialmediadatasets.aye5g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


def test_twitter_database():
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    database = client.TwitterVaccination2    
    db_return = database_as_tweet(database, "twitter")

    assert db_return['tweet'].iloc[0] == "The coronavirus vaccine programme has continued at pace in Suffolk, with more than 1.6million doses being administered so far. https://t.co/hpKIlidebg"


def test_positive_neg_count():
    reddit_data = [
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx", "sentiment": "negative"},
        {"post": "you should all get the vaccine", "subreddit": "antivaxx", "sentiment": "positive"},
        {"post": "cant wait for my vaccine tomorrow :)", "subreddit": "covid19", "sentiment": "positive"},
        {"post": "really looking forward to my vaccine tomorrow!", "subreddit": "covid19",  "sentiment": "positive"},
        {"post": "excited for my vaccine this afternoon :D", "subreddit": "covid19",  "sentiment": "positive"},
        {"post": "scared about my vaccine today :(", "subreddit": "covid19",  "sentiment": "negative"},
        {"post": "how do you change vaccine appointment", "subreddit": "covid19",  "sentiment": "neutral"},
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx", "sentiment": "negative"},
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx", "sentiment": "negative"},
        {"post": "whats a vaccine", "subreddit": "lockdowm", "sentiment": "neutral"},
    ]

    vaccine_df = pd.DataFrame(reddit_data)
    results = positive_neg_count_df(vaccine_df)

    assert results["neg_perc"] == 40
    assert results["neu_perc"] == 20
    assert results["pos_perc"] == 40
    assert results["negative"] == 4
    assert results["neutral"] == 2
    assert results["positive"] == 4


def test_vader_sentiment():
    post = "excited for my vaccine this afternoon :D"
    result = database_as_vader(post)
    assert result == "positive"


def test_textblob_sentiment():
    post = "I hate vaccines"
    result = database_as_textblob(post)
    assert result == "negative"


def test_afinn_sentiment():
    post = "i am getting the vaccine tomorrow"
    result = database_as_afinn(post)
    assert result == "neutral"


def test_bert_sentiment():
    post = "finally getting my vaccine tomorrow :)"
    result = database_as_bert(post)
    assert result == "positive"


def test_bert_preprocess():
    post = "@PiersMorgan https://twitter.com please delete your account"
    processed = bert_preprocess(post)
    assert processed == " http please delete your account"


def test_emoji_regex():
    post = "Today is a great day😀"
    remove_emoji = process_emoji(post)
    assert remove_emoji == "Today is a great day"