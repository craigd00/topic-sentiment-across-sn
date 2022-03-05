import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob
from flair.data import Sentence
from scipy.special import softmax
import urllib.request
import csv
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import emoji
import re


def get_top_subreddits(db):
    top_subreddits = db.SocialMediaPosts.aggregate([
        { "$group": { "_id": "$subreddit", "count": { "$sum": 1 }}}, 
        { "$sort": { "_id.subreddit":1, "count": -1 }  },
    ])
    top_subreddits = save_results(top_subreddits)
    return top_subreddits[:10]


def save_results(data):
    results = []
    for result in data:
        dictionary = {}
        dictionary['subreddit'] = result['_id']
        dictionary['count'] = result['count']
        results += [dictionary]

    return results


def database_as_dictionary(db, analyzer):
    list_of_dicts = []

    for entry in db.SocialMediaPosts.find():
        empty = {}
        empty['post'] = entry['post']
        empty['subreddit'] = entry['subreddit']

        vs = analyzer.polarity_scores(entry['post'])
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
    results = {}
    total_sentiment = {}
    total_sentiment['positive'] = 0
    total_sentiment['negative'] = 0
    total_sentiment['neutral'] = 0

    num_of_posts = 0

    for post in dictionary:
        num_of_posts += 1
        if post['subreddit'] not in results:
            sentiment = {}
            sentiment['positive'] = 0
            sentiment['negative'] = 0
            sentiment['neutral'] = 0
            results[post['subreddit']] = sentiment
     
        if post['sentiment'] == 'positive':
            results[post['subreddit']]['positive'] += 1
            total_sentiment['positive'] += 1

        elif post['sentiment'] == 'negative':
            results[post['subreddit']]['negative'] += 1
            total_sentiment['negative'] += 1

        else:
            results[post['subreddit']]['neutral'] += 1
            total_sentiment['neutral'] += 1

    total_sentiment['pos_perc'] = (total_sentiment['positive']/num_of_posts) * 100
    total_sentiment['neg_perc'] = (total_sentiment['negative']/num_of_posts) * 100
    total_sentiment['neu_perc'] = (total_sentiment['neutral']/num_of_posts) * 100

    for subreddit in results:
        pos_len = results[subreddit]['positive']
        neg_len = results[subreddit]['negative']
        neu_len = results[subreddit]['neutral']

        subr_posts = pos_len + neg_len + neu_len
        
        results[subreddit]['num_of_posts'] = subr_posts
        results[subreddit]['pos_perc'] = (pos_len/subr_posts) * 100
        results[subreddit]['neg_perc'] = (neg_len/subr_posts) * 100
        results[subreddit]['neu_perc'] = (neu_len/subr_posts) * 100

    
    
    return total_sentiment, results


def top_subr_counts(counts, sentiments):
    subreddits = []
    data_points = []
    pos_vals = []
    neg_vals = []
    neu_vals = []
    for popular in counts:
    #for subr in sentiments:
        #for popular in counts:
        for subr in sentiments:
            if subr == popular['subreddit']:
                subreddits += [subr]
                pos_vals += [sentiments[subr]['pos_perc']]
                neg_vals += [sentiments[subr]['neg_perc']]
                neu_vals += [sentiments[subr]['neu_perc']]

    data_points += [pos_vals]
    data_points += [neg_vals]
    data_points += [neu_vals]

    return subreddits, data_points


def plot_sentiment_top10(title, subreddits, data_points, filename):
    fig = plt.figure()
    x_point = np.arange(10)
    fig = plt.figure(figsize=(18, 8))

    ax = fig.add_axes([0,0,1,1])
    ax.bar(x_point + 0.00, data_points[0], color = 'g', width = 0.25)
    ax.bar(x_point + 0.25, data_points[1], color = 'r', width = 0.25)
    ax.bar(x_point + 0.50, data_points[2], color = 'b', width = 0.25)
    ax.set_ylabel('Percentage of posts (%)', fontweight='bold', fontsize=16)
    ax.set_xlabel('Subreddit name', fontweight='bold', fontsize=16)
    ax.set_title("Sentiment amongst top 10 " + title + " subreddits", fontweight='bold', fontsize=20)
    
    plt.xticks(x_point + 0.25, subreddits)
    ax.legend(labels=['Positive', 'Negative', 'Neutral'])
    plt.savefig(filename)


def plot_topics(list_of_topics, data_points):
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
    ax.set_title("Sentiment amongst reddit queries", fontweight='bold', fontsize=20)
    plt.xticks(x_point + 0.25, list_of_topics)

    ax.legend(labels=['Positive', 'Negative', 'Neutral'])


def database_as_textblob(db):
    list_of_dicts = []

    for entry in db.SocialMediaPosts.find():
        empty = {}
        empty['post'] = entry['post']
        empty['subreddit'] = entry['subreddit']

        text = TextBlob(entry['post'])
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
        empty['post'] = entry['post']
        empty['subreddit'] = entry['subreddit']

        text = Sentence(entry['post'])
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
        empty['post'] = entry['post']
        empty['subreddit'] = entry['subreddit']

        polarity = analyzer.score(entry['post'])
  
        if (polarity > 0):
            empty['sentiment'] = 'positive'

        elif (polarity < 0):
            empty['sentiment'] = 'negative'

        else:
            empty['sentiment'] = 'neutral'

        list_of_dicts += [empty]
    return list_of_dicts


labels=[]
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/sentiment/mapping.txt"

with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')

labels = [row[1] for row in csvreader if len(row) > 1]


model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment", model_max_length=512, padding_side="right")
    
model.save_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
tokenizer.save_pretrained("cardiffnlp/twitter-roberta-base-sentiment", model_max_length=512, padding_side="right")


def process_emoji(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text


def bert_preprocess(tweet):
    new_tweet = []
    for t in tweet.split(" "):
        t = 'http' if t.startswith('http') else t
        new_tweet.append(t)
   
    return " ".join(new_tweet)