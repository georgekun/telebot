from moviepy.editor import VideoFileClip

def get_audio_from_video(path):
    video_path = path
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile("tmp/tmp.wav")
    video.close()
