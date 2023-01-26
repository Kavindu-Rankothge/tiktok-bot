import pandas as pd
import requests

import Constant

# setting up request headers using tokens
def setup_headers():
    auth = requests.auth.HTTPBasicAuth(Constant.CLIENT, Constant.SECRET)
    data = {
        'grant_type': 'password',
        'username': Constant.USER,
        'password': Constant.PASSWORD}
    headers = {'User-Agent': 'scrapperAPI/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth,
            data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    return headers

# adding top comments to a post using id
def get_post_comments(id, headers):
    comments = []
    # get request
    comment_res = requests.get('https://oauth.reddit.com/r/'+Constant.SUBREDDIT+'/comments/'+id,
            headers=headers)
    # creating list of all comments
    for comment in comment_res.json()[1]['data']['children']:
        data = {
            'name': comment['data']['name'],
            'body': comment['data']['body'],
            'score': int(comment['data']['score'])}
        comments.append(data)
    # sorting and slicing top comments
    comments = sorted(comments, key=lambda i: i['score'], reverse=True) 
    comments = comments[:int(Constant.COMMENT_NUM)]
    return comments

# adding new posts into dataframe
def add_posts(df, headers):
    rows = []
    # get request
    post_res = requests.get('https://oauth.reddit.com/r/'+Constant.SUBREDDIT+'/hot',
            headers=headers)
    # creating list of all posts
    for post in post_res.json()['data']['children']:
        row = {
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'id': post['data']['id'],
            'url': post['data']['url']}
        rows.append(row)
    # removing old posts using id
    if not df.empty:
        temp_rows = []
        for row in rows:
            if row['id'] not in df['id'].values:
                temp_rows.append(row)
        rows = temp_rows
    # adding top comments to new post dataframe
    df_new = pd.DataFrame.from_records(rows)
    for index, row in df_new.iterrows():
        comments = get_post_comments(row['id'], headers)
        df_new.loc[[index], 'comments'] = pd.Series([comments], index=df_new.index[[index]])
    # appending new posts to main dataframe
    df = pd.concat([df, df_new], ignore_index=True)
    df.reset_index(drop=True, inplace=True)
    return df

if __name__ == '__main__':
    headers = setup_headers()
    # check if json exist, else create new dataframe
    try:
        df = pd.read_json('reddit-data.json')
    except:
        df = pd.DataFrame()
    df = add_posts(df, headers)
    # save dataframe to json
    df.to_json('reddit-data.json')
    print(df)