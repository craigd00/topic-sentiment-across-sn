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


#res = requests.get("https://oauth.reddit.com/r/all/search",
                  # headers=headers, params={'limit': '25', 'q':{'trump', 'Donald Trump'}})

#for post in res.json()['data']['children']:
       # print(post['data']['title'])
        #print(post)

#print(res.json()['data']['comments'])

comments = requests.get("https://oauth.reddit.com/r/all/comments/House votes to hold Trump ally Steve Bannon in criminal contempt for defying subpoena", #article is the ['name']?
                   headers=headers, params={'limit': '25'})

print(comments.json())