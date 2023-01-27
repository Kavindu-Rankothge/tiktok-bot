import gtts

# creates and saves text audio in path
def generate_TTS(path, text):
    tts = gtts.gTTS(text)
    tts.save(path)

def save_comment_audios(title, id, comments):
    # make list of comments from dictionary
    comments = [d['body'] for d in comments]
    # for title
    generate_TTS('assets/'+id+'/tts0.mp3', title)
    # for each comment
    i = 1
    for comment in comments:
        path = 'assets/'+id+'/tts'+str(i)+'.mp3'
        generate_TTS(path, comment)
        i += 1