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
    df = df.sort_values('score',ascending = False)
    temp_df = df[df['posted'] == False] 
    return temp_df.iloc[0]

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
    print('Done!')