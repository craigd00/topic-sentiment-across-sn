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


res = requests.get("https://oauth.reddit.com/r/all/search",
                   headers=headers, params={'limit': '25', 'q':{'COP26'}})

print("PRINTING SEARCH RESULTS FOR THE TOPIC: \n")
for post in res.json()['data']['children']:
        print(post['data']['title'])
        post_title = post['data']['title']
        post_id = post['data']['id']
        print(post['data']['id'])

        comments = comments = requests.get("https://oauth.reddit.com/r/all/comments/" + str(post_id),
                                headers=headers, params={'limit': '25'})
                                
        print("PRINTING COMMENT RESULTS FOR THE TOPIC: \n")

        length_of_comments = len(comments.json()[1]['data']['children'])

        for comment in (comments.json()[1]['data']['children'])[:-1]:
                print(comment['data']['body'])


#~~ HOW TO GET COMMENTS FROM AN ARTICLE TYPE ~~#
#comments = requests.get("https://oauth.reddit.com/r/all/comments/qcs08h", #article is the ['name']?
                   #headers=headers, params={'limit': '25'})


#print("PRINTING COMMENT RESULTS FOR THE TOPIC: \n")

#length_of_comments = len(comments.json()[1]['data']['children'])

#for comment in (comments.json()[1]['data']['children'])[:-1]:
        #print(comment['data']['body'])

        