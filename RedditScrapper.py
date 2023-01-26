import requests
import pandas as pd

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

res = requests.get('https://oauth.reddit.com/r/'+Constant.SUBREDDIT+'/hot',
        headers=headers)

df = pd.DataFrame()

for post in res.json()['data']['children']:
    df_row = pd.DataFrame({
        'title': [post['data']['title']],
        'selftext': [post['data']['selftext']]
    })
    df = pd.concat([df, df_row])

df.reset_index(drop=True, inplace=True)
print(df)