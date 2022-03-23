from src.shared_modules import database_as_tweet, positive_neg_count_df, bert_preprocess, process_emoji
from src.reddit_modules import get_subreddit_results, get_most_popular_results


from pymongo import MongoClient
import certifi
import pandas as pd

CONNECTION_STRING = "mongodb+srv://craig:Dissertation2021-22@socialmediadatasets.aye5g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

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


def test_subreddit_results():

    reddit_data = [
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx", "sentiment": "negative"},
        {"post": "you should all get the vaccine", "subreddit": "antivaxx", "sentiment": "positive"},
        {"post": "cant wait for my vaccine tomorrow :)", "subreddit": "covid19", "sentiment": "positive"},
        {"post": "really looking forward to my vaccine tomorrow!", "subreddit": "covid19",  "sentiment": "positive"},
        {"post": "excited for my vaccine this afternoon :D", "subreddit": "covid19",  "sentiment": "positive"},
        {"post": "scared about my vaccine today :(", "subreddit": "covid19",  "sentiment": "negative"},
        {"post": "how do you change vaccine appointment", "subreddit": "covid19",  "sentiment": "neutral"},
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx", "sentiment": "neutral"},
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx", "sentiment": "negative"},
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx", "sentiment": "negative"}
    ]

    vaccine_df = pd.DataFrame(reddit_data)

    results = get_subreddit_results(vaccine_df)

    assert results["positive"]["covid19"] == 3
    assert results["negative"]["antivaxx"] == 3
    assert results["pos_perc"]["antivaxx"] == 20.0
    assert results["neg_perc"]["antivaxx"] == 60.0
    assert results["neg_perc"]["covid19"] == 20.0
    assert results["total_num"]["covid19"] == 5

def test_most_popular_results():

    reddit_data = [
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx", "sentiment": "negative"},
        {"post": "you should all get the vaccine", "subreddit": "antivaxx", "sentiment": "positive"},
        {"post": "cant wait for my vaccine tomorrow :)", "subreddit": "covid19", "sentiment": "positive"},
        {"post": "scared about my vaccine today :(", "subreddit": "covid19",  "sentiment": "negative"},
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx", "sentiment": "neutral"},
        {"post": "i am not getting the vaccine", "subreddit": "antivaxx", "sentiment": "negative"},
    ]

    vaccine_df = pd.DataFrame(reddit_data)

    results = get_most_popular_results(vaccine_df)

    assert results.index[0] == "antivaxx"