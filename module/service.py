import os

from aiogram.types import Message, ContentType

from . import tools
async def get_text(bot,vosk,message:Message):
    audio_file = "tmp/tmp.wav"
    convert_file = "tmp/convert.wav"

    if message.content_type == ContentType.VOICE:
        file = message.voice
        await bot.download(file, destination=audio_file)

    elif message.content_type == ContentType.VIDEO_NOTE:
        file = message.video_note
        await bot.download(file, destination="tmp/tmp.mp4")
        tools.get_audio_from_video("tmp/tmp.mp4")
        os.remove("tmp/tmp.mp4")

    try:
        vosk.convert_audio(audio_file, convert_file)
        result = vosk.transcriber(path_audio=convert_file)
        os.remove(convert_file)
    except:
        result = None
        await bot.send_message(chat_id=message.from_user.id, text="Произошла ошибка :/ \nПовторите еще раз.")

    finally:
        os.remove(audio_file)


    return result

