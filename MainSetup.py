import asyncio
from GenerateTTS import save_comment_audios 
from GetScreenshots import get_screenshots
from RedditScrapper import update_data
from ClipEditor import generate_video

# returns top non-used post details from dataframe
def get_top_post(df):
    df = df.sort_values('score',ascending = False)
    temp_df = df[df['posted'] == False] 
    return temp_df.iloc[0]

# main method updates dataframe and gets screenshots
if __name__ == '__main__':
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