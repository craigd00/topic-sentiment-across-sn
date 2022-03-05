from transformers import AutoTokenizer, AutoModelForSequenceClassification
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from afinn import Afinn

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import emoji
import re
from scipy.special import softmax
import urllib.request
import csv

# Variables for BERT model to load
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


#Start of functions 

#Function for turning posts into a dataframe
def database_as_tweet(db, type):
    list_of_dicts = []

    if (type == "twitter"):
        for entry in db.SocialMediaPosts.find():
            empty = {}
            empty['tweet'] = entry['tweet']
            list_of_dicts += [empty]

        dataframe = pd.DataFrame(list_of_dicts, columns=['tweet'])

    else:
        for entry in db.SocialMediaPosts.find():
            empty = {}
            empty['post'] = entry['post']
            empty['subreddit'] = entry['subreddit']
            list_of_dicts += [empty]

        dataframe = pd.DataFrame(list_of_dicts, columns=['post', 'subreddit'])

    return dataframe


# Function for counting the postive and negative counts

def positive_neg_count_df(df):
    positive = df[df["sentiment"]=="positive"].count()["sentiment"]
    negative = df[df["sentiment"]=="negative"].count()["sentiment"]
    neutral = df[df["sentiment"]=="neutral"].count()["sentiment"]

    pos_perc = (positive/len(df)) * 100
    neg_perc = (negative/len(df)) * 100
    neu_perc = (neutral/len(df)) * 100

    sentiment_percent = {"positive": positive, "negative": negative, "neutral": neutral,\
                        "pos_perc": pos_perc, "neg_perc": neg_perc, "neu_perc": neu_perc}
    
    return sentiment_percent


# Function for calculating VADER sentiment with dataframe column input

def database_as_vader(post):
    vader_analyzer = SentimentIntensityAnalyzer()
    scores = vader_analyzer.polarity_scores(post)
    compound = scores['compound']
  
    if (compound >= 0.05):
        sentiment = 'positive'

    elif (compound <= -0.05):
        sentiment= 'negative'

    else:
        sentiment = 'neutral'

    return sentiment


# Function for calculating TextBlob sentiment with dataframe column input

def database_as_textblob(post):
    text = TextBlob(post)
    polarity = text.sentiment.polarity
  
    if (polarity >= 0.05):
        sentiment = 'positive'

    elif (polarity <= -0.05):
        sentiment = 'negative'

    else:
        sentiment = 'neutral'
    
    return sentiment


# Function for calculating Afinn sentiment with dataframe column input

def database_as_afinn(post):
    afinn_analyser = Afinn()
    polarity = afinn_analyser.score(post)
  
    if (polarity > 0):
        sentiment = 'positive'

    elif (polarity < 0):
        sentiment = 'negative'

    else:
        sentiment = 'neutral'

    return sentiment


#BERT Functions

# Preprocesses the text to remove the @ for users and the http links

def bert_preprocess(post):
    new_post = []
 
    for t in post.split(" "):
        t = '' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_post.append(t)

    return " ".join(new_post)


# Removes the emojis from text

def process_emoji(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text


# Calculates the sentiment from the model from the hugging face transformer library

def database_as_bert(post):

    try:
        t = bert_preprocess(post)
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
        sentiment = labels[ranking[0]]

    return sentiment


# Functions for plotting graphics

def plot_run_sentiment(data_points, filename, title):
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
    ax.set_title(title, fontweight='bold', fontsize=20)
    
    plt.xticks(x_point + 0.25, list_of_topics)
    ax.legend(labels=['Positive', 'Negative', 'Neutral'])
    plt.savefig(filename, bbox_inches='tight')


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
    return query_dpts