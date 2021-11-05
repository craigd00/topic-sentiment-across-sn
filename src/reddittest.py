from redditcredentials import CLIENT_ID, CLIENT_SECRET, USERNAME_REDDIT, PASSWORD_REDDIT
import requests

# Authorisation code from https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c, as tried what API github suggested and did not work
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

data = {'grant_type': 'password',
        'username': USERNAME_REDDIT,
        'password': PASSWORD_REDDIT}

headers = {'User-Agent': 'TopicSentimentAcrossSN/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


def getPostsOnTopic():
        results = requests.get("https://oauth.reddit.com/r/all/search",
                   headers=headers, params={'limit': '25', 'q':{'Scotrail'}})

        print("PRINTING SEARCH RESULTS FOR THE TOPIC: \n")

        posts = results.json()['data']['children']

        for post in posts:
                post_title = post['data']['title']
                print(post_title)
                post_id = post['data']['id']
                getCommentsFromPosts(post_id)

def getCommentsFromPosts(post_id):
        comment_results = requests.get("https://oauth.reddit.com/r/all/comments/" + str(post_id),
                                headers=headers, params={'limit': '25'})

        print("PRINTING COMMENT RESULTS FOR THE TOPIC: \n")

        comments = comment_results.json()[1]['data']['children'][:-1]   #slices last value as it is just list of id's

        for comment in comments:
                comment_text = comment['data']['body']
                print(comment_text)

results = getPostsOnTopic()
        