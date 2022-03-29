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


#---------- LABEL MAPPING FOR BERT ----------#

# code from https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment
labels=[]
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/sentiment/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')

labels = [row[1] for row in csvreader if len(row) > 1]

#---------- GET MODEL AND TOKENIZER FOR BERT ----------#

model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment", model_max_length=512, padding_side="right")
    
model.save_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
tokenizer.save_pretrained("cardiffnlp/twitter-roberta-base-sentiment", model_max_length=512, padding_side="right")


#---------- TURNING POSTS INTO A DATAFRAME ----------#

def database_as_tweet(db, type):
    list_of_dicts = []

    if (type == "twitter"):     # if it is twitter database
        for entry in db.SocialMediaPosts.find():
            empty = {}
            empty['tweet'] = entry['tweet']     # adds tweet to dictionary, then adds it to list of dictionaries
            list_of_dicts += [empty]

        dataframe = pd.DataFrame(list_of_dicts, columns=['tweet'])      # turns the dictionary into a dataframe

    else:       # if it is reddit database
        for entry in db.SocialMediaPosts.find():
            empty = {}
            empty['post'] = entry['post']       # adds post and subreddit to dictionary
            empty['subreddit'] = entry['subreddit']
            list_of_dicts += [empty]

        dataframe = pd.DataFrame(list_of_dicts, columns=['post', 'subreddit'])      # turns reddit dictionary into dataframe for analysis

    return dataframe


#---------- COUNTING POSITIVE AND NEGATIVE ----------#

def positive_neg_count_df(df):
    positive = df[df["sentiment"]=="positive"].count()["sentiment"]     # gets positive/negative/neutral count for dataframe
    negative = df[df["sentiment"]=="negative"].count()["sentiment"]
    neutral = df[df["sentiment"]=="neutral"].count()["sentiment"]

    pos_perc = (positive/len(df)) * 100     # gets positive/negative/neutral percentage for dataframe
    neg_perc = (negative/len(df)) * 100
    neu_perc = (neutral/len(df)) * 100

    sentiment_percent = {"positive": positive, "negative": negative, "neutral": neutral,\
                        "pos_perc": pos_perc, "neg_perc": neg_perc, "neu_perc": neu_perc}
    
    return sentiment_percent


#---------- VADER SENTIMENT ----------#

def database_as_vader(post):
    vader_analyzer = SentimentIntensityAnalyzer()       # creates vader instance
    scores = vader_analyzer.polarity_scores(post)       # gets polarity scores of post
    compound = scores['compound']       # gets the compound value
  
    if (compound >= 0.05):      # if its >= 0.05, positive
        sentiment = 'positive'

    elif (compound <= -0.05):       # if its <= 0.05, negative
        sentiment= 'negative'

    else:
        sentiment = 'neutral'       # otherwise its neutral

    return sentiment


#---------- TEXTBLOB SENTIMENT ----------#

def database_as_textblob(post):
    text = TextBlob(post)       # creates textblob instance of post
    polarity = text.sentiment.polarity      # gets the polarity score from text
  
    if (polarity >= 0.05):      # if its >= 0.05, positive
        sentiment = 'positive'

    elif (polarity <= -0.05):       # if its <= 0.05, negative
        sentiment = 'negative'

    else:
        sentiment = 'neutral'       # otherwise its neutral
    
    return sentiment


#---------- AFINN SENTIMENT ----------#

def database_as_afinn(post):
    afinn_analyser = Afinn()        # creates afinn instance
    polarity = afinn_analyser.score(post)       # gets polarity score of post
  
    if (polarity > 0):      # if its greater than zero, positive
        sentiment = 'positive'

    elif (polarity < 0):        # if its less than zero, negative
        sentiment = 'negative'

    else:
        sentiment = 'neutral'       # otherwise its neutral

    return sentiment


#---------- BERT FUNCTIONS ----------#

# Preprocesses the text to remove the @ for users and the http links

def bert_preprocess(post):
    new_post = []
 
    for t in post.split(" "):
        t = '' if t.startswith('@') and len(t) > 1 else t       # removes @, e.g. if someone mentions someone on twitter
        t = 'http' if t.startswith('http') else t       # removes big hyperlinks to http
        new_post.append(t)

    return " ".join(new_post)


# Removes the emojis from text

def process_emoji(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)      # removes emoji
    return new_text


#---------- BERT SENTIMENT ----------#

# code from https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment

def database_as_bert(post):

    try:
        t = bert_preprocess(post)       # preprocesses post
        encoded_input = tokenizer(t, return_tensors='pt')       # puts post into tokenizer
        output = model(**encoded_input)     # puts input into the model

    except:     # exceptions were happening on unrecognised emojis, so it then removes this
        t = process_emoji(t)        # only removes emoji on exception, they can provide sentimental value to post
        encoded_input = tokenizer(t, max_length=512, truncation=True, return_tensors='pt')
        output = model(**encoded_input)

    finally:
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)        # turns into probability
        ranking = np.argsort(scores)        # sorts scores in order
        ranking = ranking[::-1]     # reverses to get top ranking at first item in list
        sentiment = labels[ranking[0]]      # gets the sentiment of the top ranking from model

    return sentiment


#---------- PLOTTING GRAPHICS FOR ALL TERMS ----------#

def plot_run_sentiment(data_points, filename, title):
    list_of_topics = ['Facemasks', 'Lockdown', 'PCR', 'Pfizer', 'Quarantine', 'Restrictions', 'Vaccine']        # list of topics to plot
    fig = plt.figure()
    x_point = np.arange(7)      # used to plot the 7 terms
    fig = plt.figure(figsize=(8, 4))

    ax = fig.add_axes([0,0,1,1])
    ax.bar(x_point + 0.00, data_points[0], color = 'g', width = 0.25)       # positive points
    ax.bar(x_point + 0.25, data_points[1], color = 'r', width = 0.25)       # negative points
    ax.bar(x_point + 0.50, data_points[2], color = 'b', width = 0.25)       # neutral points
    ax.set_ylabel('Number of posts', fontweight='bold', fontsize=16)
    ax.set_xlabel('Search query', fontweight='bold', fontsize=16)
    ax.set_title(title, fontweight='bold', fontsize=20)
    
    plt.xticks(x_point + 0.25, list_of_topics)      # plots list of topics
    ax.legend(labels=['Positive', 'Negative', 'Neutral'])
    plt.savefig(filename, bbox_inches='tight')


#---------- GETTING DATAPOINTS ----------#

def sentiment_dpts(f_sent, l_sent, pcr_sent, pf_sent, q_sent, r_sent, v_sent):
    
    query_dpts = []     # used to get the datapoints for plotting
    positive = []
    negative = []
    neutral = []

    for sentiment in f_sent, l_sent, pcr_sent, pf_sent, q_sent, r_sent, v_sent:
        positive += [sentiment['pos_perc']]     # adds percentage to positive list
        negative += [sentiment['neg_perc']]     # adds percentage to negative list
        neutral += [sentiment['neu_perc']]      # adds percentage to neutral list

    query_dpts += [positive, negative, neutral]     # adds each list to the datapoints for plotting
    return query_dpts


#---------- RETURN WORD CLOUDS ----------#

def wordcloud_image(library, sn, topic, sent, terms):
    stopwords = set(STOPWORDS)
    stopwords.update(["https", "t", "co", "amp"])       # adds words to the stopwords

    wordcloud = WordCloud(stopwords=stopwords, max_words=100, background_color="white").generate(terms)     # generates a wordcloud from terms
    wordcloud.to_file("wordclouds/" + library + "/" + sn + "/" + topic + "/" + sent + "_wordcloud.png")     # saves to file


#---------- LOADS THE VARS FROM DILL ----------#

def load_dill_vars(sn):
    sn_dict = {}
    libraries = ["afinn", "bert", "textblob", "vader"]
    runs = ["run1", "run2", "run3"]

    for lib in libraries:       # for each library
        run_dict = {}
        for run in runs:        # for each run
            
            filename = sn + "_vars/" + sn + "_" + lib + "_" + run       # sets filename of vars
            with open(filename, 'rb') as f:     # opens file with saved variables from earlier
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
                                "vaccine": vac, "time": time}       # creates dictionary of this

        sn_dict[lib] = run_dict

    return sn_dict


#---------- RETURN TIMES ----------#

def get_times(vars):
    times_dict = {}
    for lib in vars:
        times = []

        for run in vars[lib]:
            time = vars[lib][run]["time"]       # gets the time from dill var
            times += [-time.total_seconds()]        # gets time taken in seconds

        times_dict[lib] = times

    return pd.DataFrame(times_dict)     # returns as a dataframe of times


#---------- GRAPH TIME TAKEN ----------#

def graph_time(twitter_times, reddit_times, filename):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
    fig.suptitle('Time taken to run')

    ax1.set_title("Twitter Times")
    ax1.plot([1,2,3], twitter_times, '-x')        # plots twitter times for each run
    ax1.set_xticks([1,2,3])
    ax1.semilogy()
    ax1.legend(twitter_times, loc='best', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
    ax1.set_xlabel('Run Number')
    ax1.set_ylabel('Time to run (s)')
    
    ax2.set_title("Reddit Times")
    ax2.plot([1,2,3], reddit_times, '-x')     # plots reddit times for each run
    ax2.set_xticks([1,2,3])
    ax2.semilogy()
    ax2.legend(reddit_times, loc='best', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
    ax2.set_xlabel('Run Number')
    ax2.set_ylabel('Time to run (s)')
    plt.subplots_adjust(wspace=0.4)
    plt.savefig(filename, bbox_inches='tight')


#---------- FOR EACH LIBRARY ----------#

def get_library_results(twitter_vars, reddit_vars, library):
    term_and_lib(twitter_vars, reddit_vars, library, "facemasks")       # used to compare twitter and reddit for each term
    term_and_lib(twitter_vars, reddit_vars, library, "lockdown")
    term_and_lib(twitter_vars, reddit_vars, library, "pcr")
    term_and_lib(twitter_vars, reddit_vars, library, "pfizer")
    term_and_lib(twitter_vars, reddit_vars, library, "quarantine")
    term_and_lib(twitter_vars, reddit_vars, library, "restrictions")
    term_and_lib(twitter_vars, reddit_vars, library, "vaccine")


#---------- GET INDIVIDUAL TERM DATAPOINTS ----------#

# Used to plot the Twitter and Reddit runs for a term against eachother

def term_and_lib(twitter_vars, reddit_vars, lib, topic):

    query_dpts = []
    positive = []
    negative = []
    neutral = []

    for library in twitter_vars:
        if library != lib:      # if library is not equal to one looking for, continues
            continue
        for run in twitter_vars[library]:
            for term in twitter_vars[library][run]:
                if term != "time" and term == topic:        # if it is not time and is equal to the topic, e.g. facemasks
                    twitter = positive_neg_count_df(twitter_vars[library][run][term])       # gets data from function
                    reddit = positive_neg_count_df(reddit_vars[library][run][term])
                    
                    positive += [twitter['pos_perc'], reddit['pos_perc']]       # adds this data to the lists
                    negative += [twitter['neg_perc'], reddit['neg_perc']]
                    neutral += [twitter['neu_perc'], reddit['neu_perc']]

    query_dpts += [positive, negative, neutral]     # gets datapoints for the library and term 
    
    graph_comparing_terms(query_dpts, lib, topic)

    
#---------- COMPARES RUNS FOR TERM SIDE BY SIDE ----------#

def graph_comparing_terms(dpts, library, term):
    list_of_runs = ['Twitter Run1', 'Reddit Run1', 'Twitter Run2', 'Reddit Run2', 'Twitter Run3', 'Reddit Run3']
    fig = plt.figure()
    x_point = np.arange(6)
    fig = plt.figure(figsize=(14, 8))

    ax = fig.add_axes([0,0,1,1])
    ax.bar(x_point + 0.00, dpts[0], color = 'g', width = 0.25)      # plots positive, negative, neutral
    ax.bar(x_point + 0.25, dpts[1], color = 'r', width = 0.25)
    ax.bar(x_point + 0.50, dpts[2], color = 'b', width = 0.25)
    ax.set_ylabel('Percentage of Posts', fontweight='bold', fontsize=16)
    ax.set_xlabel('Social Network and Run Number', fontweight='bold', fontsize=16)      # Reddit VS Twitter
    ax.set_title(library.capitalize() + " " + term.capitalize() + " Results", fontweight='bold', fontsize=20)       # title of graph
        
    plt.xticks(x_point + 0.25, list_of_runs)        # x-axis is the run names
    ax.legend(labels=['Positive', 'Negative', 'Neutral'])
    plt.savefig("sentiment_graphs/" + library + "/" + term + ".png", bbox_inches='tight')



#---------- GETS EACH TERM RUN FOR EACH LIBRARY ----------#

def get_specific_run(dill_vars, topic, r, sn):
    query_dpts = []     # works similar to previous datapoints
    positive = []
    negative = []
    neutral = []
    
    for library in dill_vars:       # loops through the libraries
 
        results = positive_neg_count_df(dill_vars[library][r][topic])       # gets data from function
                        
                        
        positive += [results['pos_perc']]    # adds this data to the lists
        negative += [results['neg_perc']]
        neutral += [results['neu_perc']]

    query_dpts += [positive, negative, neutral]     # gets datapoints for the library and term
    graph_comparing_library(query_dpts, topic, sn, r)


#---------- LOOPS THROUGH EACH TERM AND RUN ----------#

def run_and_term(dill_vars, sn):
    for term in dill_vars["afinn"]["run1"]:     # just used as a loop for term names
        if term != "time":      # makes sure term isnt time
            for run in dill_vars["afinn"]:      # gets data for each run
                get_specific_run(dill_vars, term, run, sn)


#---------- COMPARES LIBRARY RESULTS FOR TERM SIDE BY SIDE ----------#

def graph_comparing_library(dpts, term, sn, run):
    list_of_libs = ['Afinn', 'BERT', 'TextBlob', 'VADER']
    fig = plt.figure()
    x_point = np.arange(4)
    fig = plt.figure(figsize=(14, 8))

    ax = fig.add_axes([0,0,1,1])
    ax.bar(x_point + 0.00, dpts[0], color = 'g', width = 0.25)      # plots positive, negative, neutral
    ax.bar(x_point + 0.25, dpts[1], color = 'r', width = 0.25)
    ax.bar(x_point + 0.50, dpts[2], color = 'b', width = 0.25)
    ax.set_ylabel('Percentage of Posts', fontweight='bold', fontsize=16)
    ax.set_xlabel('Library', fontweight='bold', fontsize=16)      # Reddit VS Twitter
    ax.set_title(sn.capitalize() + " " + term.capitalize() + " " + run.capitalize() + " Results", fontweight='bold', fontsize=20)       # title of graph
        
    plt.xticks(x_point + 0.25, list_of_libs)        # x-axis is the library names
    ax.legend(labels=['Positive', 'Negative', 'Neutral'])
    plt.savefig("sentiment_graphs/lib_comparisons/" + sn + "/" + term + run + ".png", bbox_inches='tight')
    plt.close()     # saves the image then closes
    plt.rcParams.update({'figure.max_open_warning': 0})     # to stop warning as there is so many graphs being produced


#---------- GETS ENTIRE LIB RESULTS AS DF ----------#

def library_total(vars, lib):
    initial_df = pd.DataFrame()

    for library in vars:
        if library == lib:      # gets result for specific library
            for run in vars[library]:
                for topic in vars[library][run]:
                    if topic != "time":
                        df = vars[library][run][topic]
                        positive = df[df["sentiment"]=="positive"].count()["sentiment"]
                        negative = df[df["sentiment"]=="negative"].count()["sentiment"]
                        neutral = df[df["sentiment"]=="neutral"].count()["sentiment"]
                        # topics holds the numerical data for one run to sum all afinn, bert etc results
                        topics = {"term": [topic], "run": [run], "positive": [positive], "negative": [negative], "neutral": [neutral], "total_num": [df.count()["sentiment"]]}

                        topic_df = pd.DataFrame(topics)     # gets dataframe of topics
                        topic_df = pd.concat([topic_df, initial_df], ignore_index=True)     # adds this to the current results
                        initial_df = topic_df

    return topic_df


#---------- GETS DATAPOINTS FOR LIBRARY DF ----------#

def library_datapoints(libraries):
    lib_dpts = []       # datapoints to graph results
    positive = []
    negative = []
    neutral = []

    for df in libraries:
        positive += [(df["positive"].sum()/df["total_num"].sum())*100]      # sums the total count
        negative += [(df["negative"].sum()/df["total_num"].sum())*100]
        neutral += [(df["neutral"].sum()/df["total_num"].sum())*100]

    lib_dpts += [positive, negative, neutral]
    return lib_dpts


#---------- GRAPHS A SUBPLOT OF THE RESULTS ----------#

def graph_totalled_results(afinn_dpts, bert_dpts, tblob_dpts, vader_dpts):
              
      x_point = np.arange(2)
      fig, ax = plt.subplots(2, 2, figsize=(14, 10))        # creates subplots to show comparison of sentiment
      fig.suptitle("Comparison of the total sentiment", fontweight='bold')
      
      ax[0,0].bar(x_point + 0.00, afinn_dpts[0], color = 'g', width = 0.2)      # plots positive, negative, neutral
      ax[0,0].bar(x_point + 0.2, afinn_dpts[1], color = 'r', width = 0.2)
      ax[0,0].bar(x_point + 0.4, afinn_dpts[2], color = 'b', width = 0.2)
      ax[0,0].set_ylabel('Percentage of Posts', fontweight='bold')
      ax[0,0].set_xlabel('Library', fontweight='bold')      # library names
      plt.sca(ax[0,0])   
      plt.xticks((x_point + 0.2), ['Afinn Twitter', 'Afinn Reddit'])        # x-axis is the library names
      ax[0,0].legend(labels=['Positive', 'Negative', 'Neutral'])

      ax[0,1].bar(x_point + 0.00, bert_dpts[0], color = 'g', width = 0.2)      # plots positive, negative, neutral
      ax[0,1].bar(x_point + 0.2, bert_dpts[1], color = 'r', width = 0.2)
      ax[0,1].bar(x_point + 0.4, bert_dpts[2], color = 'b', width = 0.2)
      ax[0,1].set_ylabel('Percentage of Posts', fontweight='bold')
      ax[0,1].set_xlabel('Library', fontweight='bold')      # library names
      plt.sca(ax[0,1]) 
      plt.xticks(x_point + 0.2, ['BERT Twitter', 'BERT Reddit'])        # x-axis is the library names
      ax[0,1].legend(labels=['Positive', 'Negative', 'Neutral'])

      ax[1,0].bar(x_point + 0.00, tblob_dpts[0], color = 'g', width = 0.2)      # plots positive, negative, neutral
      ax[1,0].bar(x_point + 0.2, tblob_dpts[1], color = 'r', width = 0.2)
      ax[1,0].bar(x_point + 0.4, tblob_dpts[2], color = 'b', width = 0.2)
      ax[1,0].set_ylabel('Percentage of Posts', fontweight='bold')
      ax[1,0].set_xlabel('Library', fontweight='bold')      # library names
      plt.sca(ax[1,0]) 
      plt.xticks(x_point + 0.2, ['TextBlob Twitter', 'TextBlob Reddit'])        # x-axis is the library names
      ax[1,0].legend(labels=['Positive', 'Negative', 'Neutral'])

      ax[1,1].bar(x_point + 0.00, vader_dpts[0], color = 'g', width = 0.2)      # plots positive, negative, neutral
      ax[1,1].bar(x_point + 0.2, vader_dpts[1], color = 'r', width = 0.2)
      ax[1,1].bar(x_point + 0.4, vader_dpts[2], color = 'b', width = 0.2)
      ax[1,1].set_ylabel('Percentage of Posts', fontweight='bold')
      ax[1,1].set_xlabel('Library', fontweight='bold')      # library names
      plt.sca(ax[1,1]) 
      plt.xticks(x_point + 0.2, ['VADER Twitter', 'VADER Reddit'])        # x-axis is the library names
      ax[1,1].legend(labels=['Positive', 'Negative', 'Neutral'])
      
      plt.savefig("sentiment_graphs/lib_comparisons/overall.png", bbox_inches='tight')