import asyncio
import os.path
import Constant
from ClipEditor import generate_video
from DownloadAssets import download_video
from GenerateTTS import save_comment_audios 
from GetScreenshots import get_screenshots
from RedditScrapper import update_data

# returns top non-used post details from dataframe
def get_top_post(df):
    df = df.sort_values('score', ascending = False)
    temp_df = df[df['posted'] == False]
    return temp_df.iloc[0]

# changes post status after posted
def update_posted_status(df, id):
    idx = df.index[df['id'] == id].tolist()
    df.at[idx[0],'posted'] = True
    return df

# function posts video on tiktok
def post_video(title):
    prompt = input('Do you want to post video on tiktok? ')
    if (prompt == 'y' or prompt == 'yes'):
        # TODO post_tiktok()
        print('Post it yourself smh')
        pass

# main method handles all scripts
if __name__ == '__main__':
    # checks if background video downloaded, else downloads it
    if not os.path.isfile('assets/background-video.mp4'):
        print('Downloading assets...')
        download_video(Constant.BACKGROUND)
    print('Updating dataframe...')
    df = update_data()
    print(df.head())
    print('\nGenerating screenshots...')
    post = get_top_post(df)
    asyncio.run(get_screenshots(post['id'], post['url'], post['comments']))
    print('\nGenerating TTS...')
    save_comment_audios(post['title']+' '+post['selftext'], post['id'], post['comments'])
    print('\nEditing Video...')
    generate_video(post['id'])
    # save title of file
    with open('assets/'+post['id']+'/details.txt', 'w') as f:
        f.write(post['title'])
    print('\nFile can be found in: assets/'+post['id']+' folder.')
    post_video(post['title'])
    df = update_posted_status(df, post['id'])
    df.to_json('assets/reddit-data.json')
    print('Done!')