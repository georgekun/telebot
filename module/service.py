import os

from aiogram.types import Message, ContentType

from moviepy.editor import VideoFileClip
import config


#получения текста из документов
async def get_text(message:Message):
    audio_file = "tmp/tmp.wav"
    convert_file = "tmp/convert.wav"

    if message.content_type == ContentType.VOICE:
        file = message.voice
        await config.bot.download(file, destination=audio_file)

    elif message.content_type == ContentType.VIDEO_NOTE:
        file = await message.video_note
        await config.bot.download(file, destination="tmp/tmp.mp4")
        get_audio_from_video("tmp/tmp.mp4")
        os.remove("tmp/tmp.mp4")

    try:
        config.vosk.convert_audio(audio_file, convert_file)
        result = config.vosk.transcriber(path_audio=convert_file)
        os.remove(convert_file)

    except:
        result = None
        await config.bot.send_message(chat_id=message.from_user.id, text="Произошла ошибка :/ \nПовторите еще раз.")

    finally:
        os.remove(audio_file)

    return result


async def get_audio_from_video(path):
    video_path = path
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile("tmp/tmp.wav")
    video.close()

