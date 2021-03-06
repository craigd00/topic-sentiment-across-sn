import matplotlib.pyplot as plt
import pandas as pd
from bson.objectid import ObjectId


#---------- FOR REDDIT PUSHSHIFT FILTERING ----------#

def lengthOfComments(comment_ids):

    if len(comment_ids) > 100:      # if the comment ids is greater than 100
        comment_list = comment_ids[:100]        # gets the first 100 comment ids
        comment_ids = comment_ids[100:]     # saves the 100 onwards ids to a new variable and returns both
        return comment_list, comment_ids
    else:
        comment_list = comment_ids      # less than 100, so no action has to be taken
        return comment_list, comment_ids


def splitListIntoStrings(comment_ids):      # inputs an array of comment ids
    print(len(comment_ids))
    comments_strings = ""       # empty string 
    for id in comment_ids:      
        comments_strings += id      # adds the comment id to string var
        if id != comment_ids[-1]:       # if its not the last element in list, appends a comma
            comments_strings += ","
    
    return comments_strings     # returns the string of comment ids as this has to be input 


#---------- ACQUIRING DATABASE AS DICTIONARY ----------#

def posts_as_dict(db):
    reddit_posts = []       # empty list to hold list of dictionaries

    for entry in db.SocialMediaPosts.find():        # for each entry in the database
        empty = {}      # sets up empty dictionary and sets post subreddit and _id to be that of the database
        empty['post'] = entry['post']
        empty['subreddit'] = entry['subreddit']
        empty['_id'] = entry['_id']
        reddit_posts += [empty]     # adds the entry to the list
        
    return reddit_posts


#---------- FOR REMOVING POSTS FROM DATABASE ----------#

def remove_terms(dictionary, db, terms):

    for entry in dictionary:        # for each item in the dictionary

        post = entry['post']
        post = post.lower()     # lowercases the post
        id = entry['_id']
        term_in_post = [ele for ele in terms if(ele in post)]       # checks to see if the search term is contained in the post
    
        if not term_in_post:        # if it is not
            db.SocialMediaPosts.delete_one({"_id": ObjectId(id)})       # removes it from the database


#---------- WORD CLOUDS ----------#

def reddit_wordcloud_terms(df, sentiment):
    wordcloud_terms = " ".join(post for post in df[df["sentiment"]==sentiment].post.astype(str))        # joins the words terms together as strings
    return wordcloud_terms


#---------- GET TOP SUBREDDIT SENTIMENT RESULTS ----------#

def get_subreddit_results(df):
    negative = df[df["sentiment"] == "negative"]        # dataframe of the negative posts
    positive = df[df["sentiment"] == "positive"]        # dataframe of the positive posts

    num_of_posts = df.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"]       # gets number of posts from each subreddit
    negative_num = negative.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"]     # number of negative posts from each subreddit
    positive_num = positive.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"]     # number of positive posts from each subreddit

    final_df = pd.merge(pd.merge(positive_num, negative_num,on='subreddit'), num_of_posts,on='subreddit').rename(columns={"post_x" : "positive", "post_y": "negative", "post": "total_num"}) 

    final_df["pos_perc"] = final_df["positive"] / final_df["total_num"] * 100       # calculates percentages of positive neutral and negative posts by total number of posts in subreddit
    final_df["neg_perc"] = final_df["negative"] / final_df["total_num"] * 100

    return final_df


#---------- GRAPH SUBREDDIT SENTIMENTS ----------#

def graph_subreddit(df, sentiment, library, topic, run, filetype):

    colours = {"pos_perc": "green", "neg_perc": "red"}      # colours to be used for positive and negative
    plt.style.use('default') 

    df.reset_index().plot(      # plots the top neg/pos subreddits along with their percent
        x="subreddit", y=["pos_perc", "neg_perc"], kind="barh",
        color=colours
    )
    
    plt.legend(["Positive", "Negative"], loc="upper right")     # plots legend
    plt.title(library.capitalize() + " Reddit Top " + topic.capitalize() + " " + sentiment + " Subreddits " + run.capitalize(), fontweight='bold')
    plt.xlabel("Percentage of posts (%)", fontweight='bold')        # x and y axis labels
    plt.ylabel("Subreddit Name", fontweight='bold')
    plt.savefig("sentiment_graphs/" + library + "/subreddits/" + filetype + "/" + run + "/" + sentiment + "_" + topic + ".png", bbox_inches='tight')
    plt.close()     # saves the image then closes
    plt.rcParams.update({'figure.max_open_warning': 0})     # to stop warning as there is so many graphs being produced


#---------- GET MOST POPULAR SUBREDDITS RESULTS ----------#

def get_most_popular_results(df):

    num_of_posts = df.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"].head(10)      # gets top 10 most posted subreddits
 
    return num_of_posts


#---------- SIMILAR TO GET MOST POPULAR SUBREDDITS BUT THIS WAY IS NEEDED TO RETURN NEUTRAL COUNT ----------#

def get_subreddit_breakdown(df):
    negative = df[df["sentiment"] == "negative"]        # dataframe of the negative posts
    positive = df[df["sentiment"] == "positive"]        # dataframe of the positive posts
    neutral = df[df["sentiment"] == "neutral"]      # dataframe of the neutral posts

    num_of_posts = df.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"]       # gets number of posts from each subreddit
    negative_num = negative.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"]     # number of negative posts from each subreddit
    positive_num = positive.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"]     # number of positive posts from each subreddit
    neutral_num = neutral.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"]       # number of neutral posts

    final_df = pd.merge(pd.merge(positive_num, negative_num,on='subreddit'), neutral_num,on='subreddit').rename(columns={"post_x" : "positive", "post_y": "negative", "post": "neutral"}) 
    final_df = pd.merge(final_df, num_of_posts,on='subreddit').rename(columns={"post" : "total_num"})       # merges the pos neg neu counts with the num of posts

    final_df["pos_perc"] = final_df["positive"] / final_df["total_num"] * 100       # calculates percentages of positive neutral and negative posts by total number of posts in subreddit
    final_df["neg_perc"] = final_df["negative"] / final_df["total_num"] * 100
    final_df["neu_perc"] = final_df["neutral"] / final_df["total_num"] * 100

    return final_df


#---------- GRAPH MOST POPULAR SUBREDDITS RESULTS ----------#

def graph_most_popular(df, topic, run):

    df = df.sort_values(ascending=True)     # sorts the values to plot

    plt.style.use('default') 
    df.reset_index().plot(      # plots the most popular subreddits horizontally
        x="subreddit", y="post", kind="barh",
        color="red", alpha=0.4, edgecolor='red'
    )

    plt.title("Reddit Top " + topic.capitalize() + " Subreddits " + run.capitalize(), fontweight='bold')
    plt.xticks(rotation=0)      # to make x-axis labels flat
    plt.legend(loc="lower right")
    plt.xlabel("Number of Posts", fontweight='bold')
    plt.ylabel("Subreddit Name", fontweight='bold')
    plt.savefig("reddit_graphs/most_popular/" + run + "/" + topic + "_mostpopular.png", bbox_inches='tight')        # saves image to folder
    plt.close()
    plt.rcParams.update({'figure.max_open_warning': 0})


#---------- GRAPH MOST POPULAR SUBREDDITS WITH BREAKDOWN OF SENTIMENT ----------#

def graph_popular_breakdown(df, topic, run, library):

    df = df.sort_values(by="total_num", ascending=False).head(10)    # sorts the values to plot
    df = df.sort_values(by="total_num", ascending=True)
    plt.style.use('default') 
 
    df[['positive','negative', 'neutral']].plot(kind='barh', stacked=True,color=["green", "red", "blue"])       # plots stacked bar graph

    plt.title("Reddit Top " + topic.capitalize() + " Subreddits " + run.capitalize(), fontweight='bold')
    plt.xticks(rotation=0)      # to make x-axis labels flat
    plt.legend(loc="lower right")
    plt.xlabel("Number of Posts", fontweight='bold')
    plt.ylabel("Subreddit Name", fontweight='bold')
    plt.savefig("reddit_graphs/most_popular/" + run + "/" + library + "/" + topic + "_mostpopular.png", bbox_inches='tight')        # saves image to folder
    plt.close()
    plt.rcParams.update({'figure.max_open_warning': 0})


#---------- COUNTS CROSSOVER BETWEEN SUBREDDITS ----------#

def shared_subreddits(reddit_vars):
    subreddits_negative = {}        # holds vars for positive and negative subreddit count
    subreddits_positive = {}

    subreddits_pos_p_posts = {}     # pos subredit pos posts
    subreddits_pos_n_posts = {}     # pos subredit neg posts
    
    subreddits_neg_p_posts = {}     # neg subredit pos posts
    subreddits_neg_n_posts = {}     # neg subredit neg posts

    for library in reddit_vars:
        for run in reddit_vars[library]:
            for topic in reddit_vars[library][run]:
                if topic != "time" and library == "bert":
                    df = get_subreddit_results(reddit_vars[library][run][topic])
                    ratio = df["total_num"].mean()
                    
                    neg_df = df[df["total_num"] > ratio].sort_values(["neg_perc"], ascending=False).head(10)
                    pos_df = df[df["total_num"] > ratio].sort_values(["pos_perc"], ascending=False).head(10)
                    
                    for index, row in neg_df.iterrows():        # loop adds subreddit to dictionary count each time it apears in top 10
                        if index in subreddits_negative:
                            subreddits_negative[index] += 1
                            subreddits_neg_p_posts[index] += row["positive"]        # adds positive and negative count if in dictionary
                            subreddits_neg_n_posts[index] += row["negative"]

                        else:
                            subreddits_negative[index] = 1
                            subreddits_neg_p_posts[index] = row["positive"]     # sets positive and negative count if not in dictionary
                            subreddits_neg_n_posts[index] = row["negative"]
                    
                    for index, row in pos_df.iterrows():
                        if index in subreddits_positive:
                            subreddits_positive[index] += 1
                            subreddits_pos_p_posts[index] += row["positive"]
                            subreddits_pos_n_posts[index] += row["negative"]
                        else:
                            subreddits_positive[index] = 1
                            subreddits_pos_p_posts[index] = row["positive"]
                            subreddits_pos_n_posts[index] = row["negative"]

    neg_df = pd.DataFrame(list(subreddits_negative.items()), columns=['subreddit', 'count'])        # turns into dataframe for analysis
    neg_n_df = pd.DataFrame(list(subreddits_neg_n_posts.items()), columns=['subreddit', 'negative'])
    neg_p_df = pd.DataFrame(list(subreddits_neg_p_posts.items()), columns=['subreddit', 'positive'])

    pos_df = pd.DataFrame(list(subreddits_positive.items()), columns=['subreddit', 'count'])
    pos_p_df = pd.DataFrame(list(subreddits_pos_p_posts.items()), columns=['subreddit', 'positive'])
    pos_n_df = pd.DataFrame(list(subreddits_pos_n_posts.items()), columns=['subreddit', 'negative'])

    neg_final = pd.merge(pd.merge(neg_df, neg_p_df,on='subreddit'), neg_n_df,on='subreddit')        # merges positive and negative dfs
    pos_final = pd.merge(pd.merge(pos_df, pos_p_df,on='subreddit'), pos_n_df,on='subreddit')
    return neg_final, pos_final


#---------- GRAPHS CROSSOVER BETWEEN SUBREDDITS ----------#

def graph_common_subreddits(df, sentiment):

    df = df.sort_values(by="count", ascending=True)     # sorts the values to plot
    df = df.set_index('subreddit')
    plt.style.use('default') 

    df[['positive','negative']].plot(kind='barh', stacked=True, alpha=0.4, color=["green", "red"])
    plt.title("Reddit Top Overall " + sentiment.capitalize() + " Subreddits", fontweight='bold')
    plt.xticks(rotation=0)      # to make x-axis labels flat
    plt.legend(loc="lower right")
    plt.xlabel("Number of positive and negative posts", fontweight='bold')
    plt.ylabel("Subreddit Name", fontweight='bold')
    plt.savefig("reddit_graphs/crossover/" + sentiment + "_mostcommon.png", bbox_inches='tight')        # saves image to folder
