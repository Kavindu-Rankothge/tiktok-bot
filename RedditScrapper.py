import pandas as pd
import requests

import Constant

auth = requests.auth.HTTPBasicAuth(Constant.CLIENT, Constant.SECRET)

data = {
    'grant_type': 'password',
    'username': Constant.USER,
    'password': Constant.PASSWORD}

headers = {'User-Agent': 'scrapperAPI/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
        auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

post_res = requests.get('https://oauth.reddit.com/r/'+Constant.SUBREDDIT+'/hot',
        headers=headers)

df = pd.DataFrame()

for post in post_res.json()['data']['children']:
    df_row = pd.DataFrame({
        'title': [post['data']['title']],
        'selftext': [post['data']['selftext']],
        'id': [post['data']['id']],
        'url': [post['data']['url']]
    })
    df = pd.concat([df, df_row])

df.reset_index(drop=True, inplace=True)

def get_post_comments(id):
    comments = []
    comment_res = requests.get('https://oauth.reddit.com/r/'+Constant.SUBREDDIT+'/comments/'+id,
        headers=headers)
    for comment in comment_res.json()[1]['data']['children']:
        data = {
            'name': comment['data']['name'],
            'body': comment['data']['body'],
            'score': int(comment['data']['score'])
        }
        comments.append(data)
    comments = sorted(comments, key=lambda i: i['score'], reverse=True) 
    comments = comments[:int(Constant.COMMENT_NUM)]
    return comments

for index, row in df.iterrows():
    id = row['id']
    comments = get_post_comments(id)
    df.loc[[index], 'comments'] = pd.Series([comments], index=df.index[[index]])

df.to_json('reddit-data.json')
print(df)