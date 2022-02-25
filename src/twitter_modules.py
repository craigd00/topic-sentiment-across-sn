import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob
from flair.data import Sentence
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


def plot_topics(data_points):
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


def database_as_tweet(db):
    list_of_dicts = []

    for entry in db.SocialMediaPosts.find():
        empty = {}
        empty['tweet'] = entry['tweet']

        list_of_dicts += [empty]

    dataframe = pd.DataFrame(list_of_dicts, columns=['tweet'])
    return dataframe


def bert_preprocess(tweet):
    new_tweet = []
 
    for t in tweet.split(" "):
        t = '' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_tweet.append(t)
    return " ".join(new_tweet)


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


def database_as_bert(df):
    
    for t in df:
        try:
            t = bert_preprocess(t)
            encoded_input = tokenizer(t, return_tensors='pt')
            output = model(**encoded_input)
        except:
            t = process_emoji(t)
            encoded_input = tokenizer(t, max_length=512, truncation=True, return_tensors='pt')
            output = model(**encoded_input)
        finally:
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            ranking = np.argsort(scores)
            ranking = ranking[::-1]
            df["sentiment"] = labels[ranking[0]]

    return df


def positive_neg_count_df(df):
    positive = df[df["sentiment"]=="positive"].count()["sentiment"]
    negative = df[df["sentiment"]=="negative"].count()["sentiment"]
    neutral = df[df["sentiment"]=="neutral"].count()["sentiment"]

    pos_perc = (positive/len(df)) * 100
    neg_perc = (negative/len(df)) * 100
    neu_perc = (neutral/len(df)) * 100

    sentiment_percent = {"pos_perc": pos_perc, "neg_perc": neg_perc, "neu_perc": neu_perc}
    return sentiment_percent


def sentiment_dpts(f_sent, l_sent, pcr_sent, pf_sent, q_sent, r_sent, v_sent):
    
    query_dpts = []
    positive = []
    negative = []
    neutral = []

    for sentiment in f_sent, l_sent, pcr_sent, pf_sent, q_sent, r_sent, v_sent:
        positive += [sentiment['pos_perc']]
        negative += [sentiment['neg_perc']]
        neutral += [sentiment['neu_perc']]

    query_dpts += [positive, negative, neutral]