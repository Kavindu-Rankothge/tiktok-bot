# TikTok Reddit Bot

## Intro
This project aims to automate the creation of TikTok videos that reads Reddit posts.

## Steps
1. Read Reddit API and store text posts.
2. Get screenshots of those posts and top comments.
3. Create Audio files for reading title and comments.
4. Edit the video with the post and sound.
5. Upload video to TikTok

## Installation
1. Clone repository.
2. Create a personal Reddit application script. Store personal use script and secret token.
3. Edit the constants.txt file with those tokens and the Reddit account username and password.
4. Run MainSetup.py.

## Dependencies
* Python libraries: pip install -r requirements.txt
* Tested on python v3.11 64-bit

### Note
Currently saved videos have to be uploaded manually. Although you can do it using the TikTok API it is difficult to gain access for personal use. Other ways would include using web automation like selenium or AutoIt. However, these options seem rather dirty and even triggers bot warning in TikTok website filters.