
from src.shared_modules import database_as_tweet
from pytest_mock_resources import create_mongo_fixture

mongo = create_mongo_fixture()

#collection = mongo["SocialMediaPosts"]

def test_reddit_database(mongo):
    collection = mongo["SocialMediaPosts"]
    reddit_data = [
        {"post": "i am never going to get the vaccine", "subreddit": "antivaxx"},
        {"post": "i am getting my vaccine tomorrow :)", "subreddit": "coronavirus"}
    ]
    collection.insert_many(reddit_data)
    df_returned = database_as_tweet(collection, "reddit")
    print(df_returned)