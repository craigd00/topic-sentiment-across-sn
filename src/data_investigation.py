from mongodbcredentials import CONNECTION_STRING
from pymongo import MongoClient
import certifi
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
database = client.RedditTitlesOnly2

boris_data = database.SocialMediaPosts.find()

reddit_posts = []
lowercase_reddit_posts = []

unique_posts = set()

for bd in boris_data:
    lowercase_reddit_posts += [bd['post'].lower()]
    reddit_posts += [bd['post']]
    unique_posts.add(bd['post'])

print(len(reddit_posts))
print(len(unique_posts))



def emotionClassification(posts, pos, neg, neu):

    analyzer = SentimentIntensityAnalyzer()

    for post in posts:
        vs = analyzer.polarity_scores(post)
        compound = vs['compound']
  
        if (compound >= 0.05):
            pos += 1

        elif (compound <= -0.05):
            neg += 1

        else:
            neu += 1
    
    return pos, neg, neu


positive = 0
neutral = 0
negative = 0

positive_lowercase = 0
neutral_lowercase = 0
negative_lowercase = 0

pos, neg, neu = emotionClassification(reddit_posts, positive, negative, neutral)
pos_lower, neg_lower, neu_lower = emotionClassification(lowercase_reddit_posts, positive_lowercase, negative_lowercase, neutral_lowercase)

print("The amount of positive, negative and neutral posts in NORMAL was\n", pos, neg, neu)
print("The amount of positive, negative and neutral posts in LOWER CASE was\n", pos, neg, neu)