from redditcredentials import CLIENT_ID, CLIENT_SECRET, USERNAME_REDDIT, PASSWORD_REDDIT
import requests
from mongodbcredentials import CONNECTION_STRING
from pymongo import MongoClient
import certifi
import time


# Authorisation code adapted from https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c, as tried what API github suggested and did not work
req_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

user_info = {'grant_type': 'password',
        'username': USERNAME_REDDIT,
        'password': PASSWORD_REDDIT}

headers = {'User-Agent': 'TopicSentimentAcrossSN/0.0.1'}

response = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=req_auth, data=user_info, headers=headers)

TOKEN = response.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
reddit_db = client.RedditTitlesOnly2#RedditPostsBorisJohnsonRestart3#RedditPostsBorisJohnsonRestart2#RedditPostsBorisJohnsonRestart#RedditPostsBorisJohnson3
reddit_collection = reddit_db['SocialMediaPosts']

search_term = 'Boris Johnson'

def getCommentsFromPosts(post_id, post_title, subreddit):
        print("BEFORE COMMENT RESULTS")
        comment_results = requests.get("https://oauth.reddit.com/r/" + subreddit + "/comments/" + str(post_id),
                                headers=headers, params={'limit': '100'})
        print("AFTER COMMENT RESULTS")
        if comment_results:
                print("SET COMMENTS")
                comments = comment_results.json()[1]['data']['children'][:-1]   #slices last value as it is just list of id's
                print("AFTER SET COMMENTS")
                title = {'post': post_title}
                print(title)

                try:
                        print("INSERTING TITLE TO COLLECTION")
                        reddit_collection.insert_one(title)
                except Exception as e:
                        print(e)
       
                for comment in comments:
                        print("SETTING COMMENT TEXT")
                        comment_text = comment['data']['body']
                        text = {'post': comment_text}
                        print(text)
                        try:
                                print("INSERTING COMMENT TO COLLECTION")
                                reddit_collection.insert_one(text)
                        except Exception as e:
                                print(e)
                                break
        time.sleep(2)
                
          



def getPostsOnTopic():
        print("BEFORE RESULTS")
        results = requests.get("https://oauth.reddit.com/r/" + "all" + "/search", 
                headers=headers, params={'limit': '100', 'q':{search_term}, 'sort':'new'})
        print("AFTER RESULTS")

        posts = results.json()['data']['children']
        print("SET POSTS")

        for post in posts:
                post_title = post['data']['title']
                title = {'post': post_title}
                print(title)
                reddit_collection.insert_one(title)
            
          

subreddits = ['ukpolitics', 'worldnews', 'unitedkingdom', 'europe', 'politics']

while True:
        getPostsOnTopic()