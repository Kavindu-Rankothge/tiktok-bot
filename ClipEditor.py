from moviepy.editor import *
import random

import Constant

# reads all audio clips and returns as list and total duration
def get_audio_info(id):
    audioclips = []
    audio_duration = 0
    for i in range(Constant.COMMENT_NUM+1):
        audioclip = AudioFileClip('assets/'+id+'/tts'+str(i)+'.mp3')
        audio_duration += audioclip.duration
        audioclips.append(audioclip)
    return audioclips, audio_duration

# slices and crops part of main video for audio duration
def edit_background_clip(audio_duration):
    background_video = VideoFileClip('assets/background-video.mp4')
    # gets random start point from video
    start = random.randint(0, int(background_video.duration-audio_duration))
    end = start + audio_duration
    video_clip = background_video.subclip(start, end)
    # cropping video according to tiktok resolution
    width = video_clip.size[0]
    height = video_clip.size[1]
    video_clip = video_clip.crop(x1=width/2-height*Constant.TIKTOK_RATIO/2,
            y1=0,
            x2=width/2+height*Constant.TIKTOK_RATIO/2,
            y2=height)
    return video_clip

# puts screenshots on video relative to audio
def edit_pics(id, video_clip, audioclips):
    i = 0
    start = 0
    clips = []
    clips.append(video_clip)
    height = video_clip.size[1]
    for audio in audioclips:
        end = audio.duration
        pic = ImageClip('assets/'+id+'/pic'+str(i)+'.png').set_start(start).set_duration(end).set_pos(("center","center")).resize(
                width=height*Constant.TIKTOK_RATIO*0.9) 
        clips.append(pic)
        start += end
        i += 1
    return clips

def generate_video(id):
    # get audio details
    audioclips, audio_duration = get_audio_info(id)
    # combine list of audios
    tts_audio = concatenate_audioclips(audioclips)
    # get background clip
    video_clip = edit_background_clip(audio_duration)
    # combine audios of video and TTS
    video_audio = CompositeAudioClip([video_clip.audio.volumex(0.2), tts_audio])
    video_clip.audio = video_audio
    # edit screenshots to video
    clips = edit_pics(id, video_clip, audioclips)
    final = CompositeVideoClip(clips)
    # save video
    final.write_videofile('assets/'+id+'/'+id+'.mp4')