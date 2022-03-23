import requests

# all the connection strings to connect to mongo db, used for the different runs
from mongodbcredentials import CONNECTION_STRING, CONNECTION_STRING_JAN_A, CONNECTION_STRING_JAN_1, CONNECTION_STRING_JAN_2, CONNECTION_STRING_TRAINING_DATA
from pymongo import MongoClient
import certifi
import time
import datetime

from reddit_modules import lengthOfComments, splitListIntoStrings


client = MongoClient(CONNECTION_STRING_TRAINING_DATA, tlsCAFile=certifi.where())        # connects to the Mongo DB
reddit_db = client.TrainValTestReddit       # specifies the database to save it into
reddit_collection = reddit_db['TrainingValidationTest']     # collection name

query = "coronavirus"       # query/term to search for

#https://www.geeksforgeeks.org/how-to-convert-datetime-to-unix-timestamp-in-python/

date_from = datetime.datetime(2022, 2, 6, 00, 00) #Y/M/D/HOUR/MINS
timestamp = int(time.mktime(date_from.timetuple()))#"1633124765"

post_ids = []       # holds the post ids that contain term so can collect the comments from post after


def pushshiftSearch(search_type, date_from):        # searches reddit for the type of submission, query term, after the date from
    url = f"https://api.pushshift.io/reddit/search/{search_type}/?q={query}&after={date_from}&size=100"     # retrieves 100 at a time

    results = requests.get(url)     # gets the results
    data = results.json()       # turns results into json
    posts = data['data']        # gets the post data
    return posts


def searching_reddit(search_type, filter_by):
    try:
        posts = pushshiftSearch(search_type, timestamp)     # gets posts from pushshiftSearch
    except:     # if theres an exception, stops
        return

    while len(posts) > 0:       # while theres posts
        for post in posts:
            if search_type == "submission":     # if it is a submission (post and not a comment)
                post_ids.append(post['id'])     # adds the post id to post ids to search through later

            reddit_post = {'post': post[filter_by], 'subreddit': post["subreddit"]}     
            reddit_collection.insert_one(reddit_post)       # inserts the post and subreddit into the mongo db
           
            print(post[filter_by])

        time.sleep(1)       # sleeps the code for 1 second to avoid request limit
        try:
            posts = pushshiftSearch(search_type, date_from=posts[-1]['created_utc'])        # as it only gets 100 at time, this gets new batch newer than the previous 100
        except:
            continue        # if there is none left


def getCommentsFromTitles(post_id):
    url = f"https://api.pushshift.io/reddit/submission/comment_ids/{post_id}"       # gets the comments from each post using the id
    results = requests.get(url)
    data = results.json()
    comment_ids = data['data']      # retrieves the comment ids on the post
    
    comment_list, comment_ids = lengthOfComments(comment_ids)       # as it can only do 100 requests at a time, if theres more than 100 comments, has to traverse through 100 at a time 
    print("TOTAL COMMENTS TO ADD: ", len(comment_ids))
    runBefore = False       # used to say that this is first time checking comments

    while len(comment_list) > 0:        # while there is still comment ids left
        if len(comment_list) <= 100 and runBefore:      # if the comment list is less than 100 and it has been runBefore
            break       # breaks as means it has already retrieved all the comments

        comment_id_split = splitListIntoStrings(comment_ids)        # gets comment ids as string to search
       
        url = f"https://api.pushshift.io/reddit/comment/search?ids={comment_id_split}"      # retrieves all the comments
        results = requests.get(url)
       
        try:
            comment_results = results.json()        # tries to get the comment results as json
        except Exception as e:
            print(e)
            break
        
        comment_results = comment_results['data']
        for comment in comment_results:
            comment_text = comment['body']      # gets the comment text to do with query
            print(comment_text)

            reddit_comment = {'post': comment_text, 'subreddit': comment["subreddit"]}
            reddit_collection.insert_one(reddit_comment)        # adds comment to the database
            
        comment_list, comment_ids = lengthOfComments(comment_ids)       # gets the new comment list to search through, as it can only do 100 at a time
        runBefore = True        # sets variable runBefore to true, meaning it has retrieved a batch of comments once

        time.sleep(1)       # sleeps to avoid maxing out requests


searching_reddit(search_type = "submission", filter_by = "title")       # searches reddit for the query for main posts containing the query term
searching_reddit(search_type = "comment", filter_by = "body")       # searches reddit comments that contain the query term

for id in post_ids:
    try:
        getCommentsFromTitles(id)       # gets all the comments from the posts that contain a query term
    except:
        continue