import requests
from mongodbcredentials import CONNECTION_STRING, CONNECTION_STRING_JAN_A, CONNECTION_STRING_JAN_1, CONNECTION_STRING_JAN_2, CONNECTION_STRING_TRAINING_DATA
from pymongo import MongoClient
import certifi
import time
import datetime

from reddit_modules import lengthOfComments, splitListIntoStrings

client = MongoClient(CONNECTION_STRING_TRAINING_DATA, tlsCAFile=certifi.where())
reddit_db = client.TrainValTestReddit
reddit_collection = reddit_db['TrainingValidationTest']

query = "coronavirus"

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
date_from = datetime.datetime(2022, 2, 6, 00, 00) #Y/M/D/HOUR/MINS
timestamp = int(time.mktime(date_from.timetuple()))#"1633124765"

post_ids = []

def searching_reddit(search_type, filter_by):
    try:
        posts = pushshiftSearch(search_type, timestamp)
    except:
        return

    while len(posts) > 0:
        for post in posts:
            if search_type == "submission":
                reddit_titles.append(post[filter_by])
                post_ids.append(post['id'])
                #getCommentsFromTitles(post['id'])
                
            else:
                reddit_comments_query.append(post[filter_by])
            #print(post["subreddit"])
            reddit_post = {'post': post[filter_by], 'subreddit': post["subreddit"]}
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
            reddit_comment = {'post': comment_text, 'subreddit': comment["subreddit"]}
            reddit_collection.insert_one(reddit_comment)
            
        comment_list, comment_ids = lengthOfComments(comment_ids)
        runBefore = True
        print("LENGTH OF COMMENTS LIST IS NOW: ", len(reddit_comments))
        time.sleep(1)


searching_reddit(search_type = "submission", filter_by = "title")
searching_reddit(search_type = "comment", filter_by = "body")

for id in post_ids:
    try:
        getCommentsFromTitles(id)
    except:
        continue
   

print(len(reddit_titles))
print(len(reddit_comments_query))
print(len(reddit_comments))