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
reddit_db = client.LastTryRedditBOJO2#RedditPostsBorisJohnsonRestart3#RedditPostsBorisJohnsonRestart2#RedditPostsBorisJohnsonRestart#RedditPostsBorisJohnson3
reddit_collection = reddit_db['SocialMediaPosts']

search_term = 'Boris Johnson'
reddit_posts = [] #{}


def getCommentsFromPosts(post_id, post_title, num_requests):
        comment_results = requests.get("https://oauth.reddit.com/r/all/comments/" + str(post_id),
                                headers=headers, params={'limit': '100'})

        if comment_results:

                num_requests += 1
        
                comments = comment_results.json()[1]['data']['children'][:-1]   #slices last value as it is just list of id's
        
            
                #reddit_posts.append(post_title)
                title = {'post': post_title}
                try:
                        reddit_collection.insert_one(title)
                except Exception as e:
                        print(e)
       
                for comment in comments:
                        comment_text = comment['data']['body']
                        text = {'post': comment_text}
                        print(text)
                        try:
                                reddit_collection.insert_one(text)
                        except Exception as e:
                                print(e)
                                break
                        #reddit_posts.append(comment_text)
                return num_requests

        else:
                return num_requests



def getPostsOnTopic(num_requests):
        results = requests.get("https://oauth.reddit.com/r/all/search", 
                headers=headers, params={'limit': '100', 'q':{search_term}})

        num_requests += 1

        try:
                posts = results.json()['data']['children']
        except Exception as e:
                print(e)
                return num_requests

        time.sleep(2)

        for post in posts:
                post_title = post['data']['title']
                post_id = post['data']['id']
                print(post_title)
                num_requests = getCommentsFromPosts(post_id, post_title, num_requests)
        return num_requests

num_requests = 0
start_time = time.time()

while True:
        #if num_requests < 60 and (start_time - time.time() < 60):
        num_requests = getPostsOnTopic(num_requests)
        #elif num_requests < 60 and (start_time - time.time() >= 60):
                #start_time = time.time()
               # num_requests = 0
                #getPostsOnTopic(num_requests)
       # else:
            #    print("Maxed out requests for now")
             #   num_requests = 0
           #     start_time = time.time()
            #    time.sleep(30)
        