from redditcredentials import CLIENT_ID, CLIENT_SECRET, USERNAME_REDDIT, PASSWORD_REDDIT
import requests

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

search_term = 'Nicola Sturgeon'
reddit_posts = [] #{}


def getCommentsFromPosts(post_id, post_title):
        comment_results = requests.get("https://oauth.reddit.com/r/all/comments/" + str(post_id),
                                headers=headers, params={'limit': '100'})

        comments = comment_results.json()[1]['data']['children'][:-1]   #slices last value as it is just list of id's

        reddit_posts.append(post_title)

        for comment in comments:
                comment_text = comment['data']['body']
                reddit_posts.append(comment_text)


def getPostsOnTopic():
    results = requests.get("https://oauth.reddit.com/r/all/search", 
                headers=headers, params={'limit': '100', 'q':{search_term}, 'sort':'new'})

    posts = results.json()['data']['children']

    for post in posts:
        post_title = post['data']['title']
        post_id = post['data']['id']
        getCommentsFromPosts(post_id, post_title)

results = getPostsOnTopic()