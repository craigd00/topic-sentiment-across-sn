import requests
from mongodbcredentials import CONNECTION_STRING
from pymongo import MongoClient
import certifi
import time
import datetime


client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
reddit_db = client.RedditPushshiftBorisJohnsonRerun
reddit_collection = reddit_db['SocialMediaPosts']


query="Boris Johnson"

def pushshiftSearch(search_type, date_from):
    url = f"https://api.pushshift.io/reddit/search/{search_type}/?q={query}&after={date_from}&size=100"

    results = requests.get(url)
    data = results.json()
    posts = data['data']
    return posts

reddit_titles = []
reddit_comments_query = []
reddit_comments = []

#https://www.geeksforgeeks.org/how-to-convert-datetime-to-unix-timestamp-in-python/
date_from = datetime.datetime(2021, 10, 1, 00, 00) #Y/M/D/HOUR/MINS
timestamp = int(time.mktime(date_from.timetuple()))#"1633124765"


def searching_reddit(search_type, filter_by):
    try:
        posts = pushshiftSearch(search_type, timestamp)
    except:
        return

    while len(posts) > 0:
        for post in posts:
            if search_type == "submission":
                reddit_titles.append(post[filter_by])
                getCommentsFromTitles(post['id'])
                
            else:
                reddit_comments_query.append(post[filter_by])

            reddit_post = {'post': post[filter_by]}
            reddit_collection.insert_one(reddit_post)

            print(post[filter_by])

        time.sleep(1)   
        try:
            posts = pushshiftSearch(search_type, date_from=posts[-1]['created_utc'])
        except:
            continue

def getCommentsFromTitles(post_id):
    url = f"https://api.pushshift.io/reddit/submission/comment_ids/{post_id}"
    results = requests.get(url)
    data = results.json()
    comment_ids = data['data']
    
    comment_list, comment_ids = lengthOfComments(comment_ids)
    print("TOTAL COMMENTS TO ADD: ", len(comment_ids))
    runBefore = False

    while len(comment_list) > 0:
        if len(comment_list) <= 100 and runBefore:
            break

        comment_id_split = splitListIntoStrings(comment_ids)
       
        url = f"https://api.pushshift.io/reddit/comment/search?ids={comment_id_split}"
        results = requests.get(url)
       
        try:
            comment_results = results.json()
        except Exception as e:
            print(e)
            break
        comment_results = comment_results['data']
        for comment in comment_results:
            comment_text = comment['body']
            print(comment_text)
            reddit_comments.append(comment_text)
            reddit_comment = {'post': comment_text}
            reddit_collection.insert_one(reddit_comment)
            
        comment_list, comment_ids = lengthOfComments(comment_ids)
        runBefore = True
        print("LENGTH OF COMMENTS LIST IS NOW: ", len(reddit_comments))
        time.sleep(1)
	

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


searching_reddit(search_type = "submission", filter_by = "title")
searching_reddit(search_type = "comment", filter_by = "body")

print(len(reddit_titles))
print(len(reddit_comments_query))
print(len(reddit_comments))