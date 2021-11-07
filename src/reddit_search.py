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
reddit_db = client.RedditPostsNicolaSturgeon
reddit_collection = reddit_db['SocialMediaPosts']

search_term = 'Nicola Sturgeon'
reddit_posts = [] #{}


def getCommentsFromPosts(post_id, post_title, num_requests):
        comment_results = requests.get("https://oauth.reddit.com/r/all/comments/" + str(post_id),
                                headers=headers, params={'limit': '100'})

        num_requests += 1
        comments = comment_results.json()[1]['data']['children'][:-1]   #slices last value as it is just list of id's

        reddit_posts.append(post_title)
        post_title = {'post': post_title}
        reddit_collection.insert_one(post_title)

        for comment in comments:
                comment_text = comment['data']['body']
                text = {'post': comment_text}
                print(text)
                reddit_collection.insert_one(text)
                reddit_posts.append(comment_text)

        return num_requests

def getPostsOnTopic(num_requests):
        results = requests.get("https://oauth.reddit.com/r/all/search", 
                headers=headers, params={'limit': '100', 'q':{search_term}, 'sort':'new'})

        num_requests += 1
        posts = results.json()['data']['children']

        for post in posts:
                post_title = post['data']['title']
                post_id = post['data']['id']
                print(post_title)
                num_requests = getCommentsFromPosts(post_id, post_title, num_requests)
        
        return num_requests

num_requests = 0
start_time = time.time()

running = True

while running:
        if num_requests < 60 and (start_time - time.time() < 60):
                num_requests = getPostsOnTopic(num_requests)
        else:
                num_requests = 0
                time.sleep(60)
        