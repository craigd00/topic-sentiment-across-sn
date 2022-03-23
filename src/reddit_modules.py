import matplotlib.pyplot as plt
import pandas as pd
from bson.objectid import ObjectId


#---------- FOR REDDIT PUSHSHIFT FILTERING ----------#
def lengthOfComments(comment_ids):

    if len(comment_ids) > 100:
        comment_list = comment_ids[:100]
        comment_ids = comment_ids[100:]
        return comment_list, comment_ids
    else:
        comment_list = comment_ids
        return comment_list, comment_ids


def splitListIntoStrings(comment_ids):
    print(len(comment_ids))
    comments_strings = ""
    for id in comment_ids:
        comments_strings += id
        if id != comment_ids[-1]:
            comments_strings += ","
    
    return comments_strings
#---------- ACQUIRING DATABASE AS DICTIONARY ----------#

def posts_as_dict(db):
    reddit_posts = []

    for entry in db.SocialMediaPosts.find():
        empty = {}
        empty['post'] = entry['post']
        empty['subreddit'] = entry['subreddit']
        empty['_id'] = entry['_id']
        reddit_posts += [empty]
        
    return reddit_posts


#---------- FOR REMOVING POSTS FROM DATABASE ----------#

def remove_terms(dictionary, db, terms):

    for entry in dictionary:

        post = entry['post']
        post = post.lower()
        id = entry['_id']
        term_in_post = [ele for ele in terms if(ele in post)]
    
        if not term_in_post:
            db.SocialMediaPosts.delete_one({"_id": ObjectId(id)})



#---------- WORD CLOUDS ----------#

def reddit_wordcloud_terms(df, sentiment):
    wordcloud_terms = " ".join(post for post in df[df["sentiment"]==sentiment].post.astype(str))
    return wordcloud_terms


#---------- GET TOP SUBREDDIT SENTIMENT RESULTS ----------#

def get_subreddit_results(df):
    negative = df[df["sentiment"] == "negative"]
    positive = df[df["sentiment"] == "positive"]

    num_of_posts = df.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"]
    negative_num = negative.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"]
    positive_num = positive.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"]

    final_df = pd.merge(pd.merge(positive_num, negative_num,on='subreddit'), num_of_posts,on='subreddit').rename(columns={"post_x" : "positive", "post_y": "negative", "post": "total_num"}) 

    final_df["pos_perc"] = final_df["positive"] / final_df["total_num"] * 100
    final_df["neg_perc"] = final_df["negative"] / final_df["total_num"] * 100
    return final_df


#---------- GRAPH SUBREDDIT SENTIMENTS ----------#

def graph_subreddit(df, sentiment, library, topic, run, filetype):

    colours = {"pos_perc": "green", "neg_perc": "red"}
    plt.style.use('default') 

    df.reset_index().plot(
        x="subreddit", y=["pos_perc", "neg_perc"], kind="barh",
        color=colours
    )
    
    plt.legend(["Positive", "Negative"], loc="upper right")
    plt.title(library.capitalize() + " Reddit Top " + topic.capitalize() + " " + sentiment + " Subreddits " + run.capitalize(), fontweight='bold')
    plt.xlabel("Percentage of posts (%)", fontweight='bold')
    plt.ylabel("Subreddit Name", fontweight='bold')
    plt.savefig("sentiment_graphs/" + library + "/subreddits/" + filetype + "/" + run + "/" + sentiment + "_" + topic + ".png", bbox_inches='tight')
    plt.close()
    plt.rcParams.update({'figure.max_open_warning': 0})


#---------- GET MOST POPULAR SUBREDDITS RESULTS ----------#

def get_most_popular_results(df):

    num_of_posts = df.groupby("subreddit").count().sort_values(["post"], ascending=False)["post"].head(10)
 
    return num_of_posts


#---------- GRAPH MOST POPULAR SUBREDDITS RESULTS ----------#

def graph_most_popular(df, topic, run):

    df = df.sort_values(ascending=True)

    plt.style.use('default') 
    df.reset_index().plot(
        x="subreddit", y="post", kind="barh",
        color="red", alpha=0.4, edgecolor='red'
    )

    plt.title("Reddit Top " + topic.capitalize() + " Subreddits " + run.capitalize(), fontweight='bold')
    plt.xticks(rotation=0)
    plt.legend(loc="lower right")
    plt.xlabel("Number of Posts", fontweight='bold')
    plt.ylabel("Subreddit Name", fontweight='bold')
    plt.savefig("reddit_graphs/most_popular/" + run + "/" + topic + "_mostpopular.png", bbox_inches='tight')
    plt.close()
    plt.rcParams.update({'figure.max_open_warning': 0})