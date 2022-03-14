import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob
from scipy.special import softmax
import urllib.request
import csv
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import emoji
import re
import pandas as pd

def get_mostcommon_posts(db):
    top_tweets = db.SocialMediaPosts.aggregate([
        { "$group": { "_id": "$tweet", "count": { "$sum": 1 }}}, 
        { "$sort": { "_id.tweet":1, "count": -1 }  },
    ])
    top_tweets = save_results(top_tweets)
    return top_tweets[:10]


def save_results(data):
    results = []
    for result in data:
        dictionary = {}
        dictionary['tweet'] = result['_id']
        dictionary['count'] = result['count']
        results += [dictionary]

    return results


def database_as_dictionary(db, analyzer):
    list_of_dicts = []

    for entry in db.SocialMediaPosts.find():
        empty = {}
        empty['tweet'] = entry['tweet']

        vs = analyzer.polarity_scores(entry['tweet'])
        compound = vs['compound']
  
        if (compound >= 0.05):
            empty['sentiment'] = 'positive'

        elif (compound <= -0.05):
            empty['sentiment'] = 'negative'

        else:
            empty['sentiment'] = 'neutral'

        list_of_dicts += [empty]
    return list_of_dicts


def pos_neg_count(dictionary):
    total_sentiment = {}
    total_sentiment['positive'] = 0
    total_sentiment['negative'] = 0
    total_sentiment['neutral'] = 0
    num_of_posts = 0
    
    for post in dictionary:
        num_of_posts += 1
        if post['sentiment'] == 'positive':
            total_sentiment['positive'] += 1

        elif post['sentiment'] == 'negative':
            total_sentiment['negative'] += 1

        else:
            total_sentiment['neutral'] += 1

    total_sentiment['pos_perc'] = (total_sentiment['positive']/num_of_posts) * 100
    total_sentiment['neg_perc'] = (total_sentiment['negative']/num_of_posts) * 100
    total_sentiment['neu_perc'] = (total_sentiment['neutral']/num_of_posts) * 100
    
    return total_sentiment


def plot_topics(data_points, filename):
    list_of_topics = ['Facemasks', 'Lockdown', 'PCR', 'Pfizer', 'Quarantine', 'Restrictions', 'Vaccine']
    fig = plt.figure()
    x_point = np.arange(7)
    fig = plt.figure(figsize=(18, 10))

    ax = fig.add_axes([0,0,1,1])
    ax.bar(x_point + 0.00, data_points[0], color = 'g', width = 0.25)
    ax.bar(x_point + 0.25, data_points[1], color = 'r', width = 0.25)
    ax.bar(x_point + 0.50, data_points[2], color = 'b', width = 0.25)
    ax.set_ylabel('Number of posts', fontweight='bold', fontsize=16)
    ax.set_xlabel('Search query', fontweight='bold', fontsize=16)
    ax.set_title("Sentiment amongst Twitter queries", fontweight='bold', fontsize=20)

    plt.xticks(x_point + 0.25, list_of_topics)
    ax.legend(labels=['Positive', 'Negative', 'Neutral'])
    plt.savefig(filename)

def database_as_textblob(db):
    list_of_dicts = []

    for entry in db.SocialMediaPosts.find():
        empty = {}
        empty['tweet'] = entry['tweet']

        text = TextBlob(entry['tweet'])
        polarity = text.sentiment.polarity
  
        if (polarity >= 0.05):
            empty['sentiment'] = 'positive'

        elif (polarity <= -0.05):
            empty['sentiment'] = 'negative'

        else:
            empty['sentiment'] = 'neutral'

        list_of_dicts += [empty]
    return list_of_dicts


def database_as_flair(db, classifier):
    list_of_dicts = []

    for entry in db.SocialMediaPosts.find():
        empty = {}
        empty['tweet'] = entry['tweet']

        text = Sentence(entry['tweet'])
        classifier.predict(text)
        polarity = text.labels[0].value

        if (polarity == "POSITIVE"):
            empty['sentiment'] = 'positive'

        else:
            empty['sentiment'] = 'negative'

        list_of_dicts += [empty]
    return list_of_dicts


def database_as_afinn(db, analyzer):
    list_of_dicts = []

    for entry in db.SocialMediaPosts.find():
        empty = {}
        empty['tweet'] = entry['tweet']

        polarity = analyzer.score(entry['tweet'])
  
        if (polarity > 0):
            empty['sentiment'] = 'positive'

        elif (polarity < 0):
            empty['sentiment'] = 'negative'

        else:
            empty['sentiment'] = 'neutral'

        list_of_dicts += [empty]
    return list_of_dicts


#---------- WORD CLOUDS ----------#
def twitter_wordcloud_terms(df, sentiment):
    wordcloud_terms = " ".join(tweet for tweet in df[df["sentiment"]==sentiment].tweet.astype(str))
    return wordcloud_terms
