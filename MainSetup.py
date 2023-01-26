import asyncio
import pandas as pd
from GetScreenshots import get_screenshots
from RedditScrapper import update_data

# returns top non-used post details from dataframe
def get_top_post_id_url(df):
    df = df.sort_values('score',ascending = False)
    temp_df = df[df['posted'] == False] 
    return temp_df.iloc[0]['id'], temp_df.iloc[0]['url']

# main method updates dataframe and gets screenshots
if __name__ == '__main__':
    print('Updating dataframe...')
    df = update_data()
    print(df.head())
    print('\nGenerating screenshots...')
    id, url = get_top_post_id_url(df)
    asyncio.run(get_screenshots(id, url))
    print('Done!')