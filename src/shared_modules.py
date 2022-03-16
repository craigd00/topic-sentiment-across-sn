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
from wordcloud import WordCloud, STOPWORDS
import dill
from dill import dump, load

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
    fig = plt.figure(figsize=(8, 4))

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


#---------- RETURN WORD CLOUDS ----------#

def wordcloud_image(library, sn, topic, sent, terms):
    stopwords = set(STOPWORDS)
    stopwords.update(["https", "t", "co", "amp"])

    wordcloud = WordCloud(stopwords=stopwords, max_words=100, background_color="white").generate(terms)
    wordcloud.to_file("wordclouds/" + library + "/" + sn + "/" + topic + "/" + sent + "_wordcloud.png")


#---------- RETURN WORD CLOUDS ----------#

def load_dill_vars(sn):
    sn_dict = {}
    libraries = ["afinn", "bert", "textblob", "vader"]
    runs = ["run1", "run2", "run3"]

    for lib in libraries:
        run_dict = {}
        for run in runs:
            
            filename = sn + "_vars/" + sn + "_" + lib + "_" + run
            with open(filename, 'rb') as f:
                fmasks = dill.load(f)
                ldown = dill.load(f)
                pcr = dill.load(f)
                pfizer = dill.load(f)
                quar = dill.load(f)
                rest = dill.load(f)
                vac = dill.load(f)
                time = dill.load(f)
            run_dict[run] = {"facemasks": fmasks, "lockdown": ldown, "pcr": pcr, \
                                "pfizer": pfizer, "quarantine": quar, "restrictions": rest,\
                                "vaccine": vac, "time": time}

        sn_dict[lib] = run_dict

    return sn_dict


#---------- RETURN TIMES ----------#
def get_times(vars):
    times_dict = {}
    for lib in vars:
        times = []

        for run in vars[lib]:
            time = vars[lib][run]["time"]
            times += [-time.total_seconds()]

        times_dict[lib] = times

    return pd.DataFrame(times_dict)

#---------- GRAPH TIME TAKEN ----------#
def graph_time(twitter_times, reddit_times, filename):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
    fig.suptitle('Time taken to run')

    ax1.set_title("Twitter Times")
    ax1.plot([1,2,3], twitter_times)
    ax1.set_xticks([1,2,3])
    ax1.legend(twitter_times)
    ax1.set_xlabel('Run Number')
    ax1.set_ylabel('Time to run (s)')

    ax2.set_title("Reddit Times")
    ax2.plot([1,2,3], reddit_times)
    ax2.set_xticks([1,2,3])
    ax2.legend(reddit_times)
    ax2.set_xlabel('Run Number')
    ax2.set_ylabel('Time to run (s)')

    plt.subplots_adjust(wspace=0.4)
    plt.savefig(filename, bbox_inches='tight')

#---------- FOR EACH LIBRARY ----------#
def get_library_results(twitter_vars, reddit_vars, library):
    term_and_lib(twitter_vars, reddit_vars, library, "facemasks")
    term_and_lib(twitter_vars, reddit_vars, library, "lockdown")
    term_and_lib(twitter_vars, reddit_vars, library, "pcr")
    term_and_lib(twitter_vars, reddit_vars, library, "pfizer")
    term_and_lib(twitter_vars, reddit_vars, library, "quarantine")
    term_and_lib(twitter_vars, reddit_vars, library, "restrictions")
    term_and_lib(twitter_vars, reddit_vars, library, "vaccine")

#---------- GET INDIVIDUAL TERM DATAPOINTS ----------#
def term_and_lib(twitter_vars, reddit_vars, lib, topic):

    query_dpts = []
    positive = []
    negative = []
    neutral = []

    for library in twitter_vars:
        if library != lib:
            continue
        for run in twitter_vars[library]:
            for term in twitter_vars[library][run]:
                if term != "time" and term == topic:
                    twitter = positive_neg_count_df(twitter_vars[library][run][term])
                    reddit = positive_neg_count_df(reddit_vars[library][run][term])
                    
                    positive += [twitter['pos_perc'], reddit['pos_perc']]
                    negative += [twitter['neg_perc'], reddit['neg_perc']]
                    neutral += [twitter['neu_perc'], reddit['neu_perc']]

    query_dpts += [positive, negative, neutral]
    
    graph_comparing_terms(query_dpts, lib, topic)
    

def graph_comparing_terms(dpts, library, term):
    list_of_runs = ['Twitter Run1', 'Reddit Run1', 'Twitter Run2', 'Reddit Run2', 'Twitter Run3', 'Reddit Run3']
    fig = plt.figure()
    x_point = np.arange(6)
    fig = plt.figure(figsize=(14, 8))

    ax = fig.add_axes([0,0,1,1])
    ax.bar(x_point + 0.00, dpts[0], color = 'g', width = 0.25)
    ax.bar(x_point + 0.25, dpts[1], color = 'r', width = 0.25)
    ax.bar(x_point + 0.50, dpts[2], color = 'b', width = 0.25)
    ax.set_ylabel('Percentage of Posts', fontweight='bold', fontsize=16)
    ax.set_xlabel('Social Network and Run Number', fontweight='bold', fontsize=16)
    ax.set_title(library.capitalize() + " " + term.capitalize() + " Results", fontweight='bold', fontsize=20)
        
    plt.xticks(x_point + 0.25, list_of_runs)
    ax.legend(labels=['Positive', 'Negative', 'Neutral'])
    plt.savefig("sentiment_graphs/" + library + "/" + term + ".png", bbox_inches='tight')
