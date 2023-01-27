from pytube import YouTube

# download youtube video with link
def download_video(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(filename='background-video.mp4', output_path='assets')
    except:
        raise Exception('Background video not downloaded')