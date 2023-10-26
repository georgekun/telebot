import os
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,ContentType

from module.vosk import Vosk

load_dotenv()

BOT = Bot(token=os.getenv("TG_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()
vosk = Vosk("vosk-model-small-ru-0.22")

@dp.message(CommandStart())
async def welcome(message: Message):
    name = message.from_user.first_name
    text = f"Привет, {name}\nОтправь/перешли мне аудиозапись, а я расшифрую его! (:"
    await BOT.send_message(chat_id=message.from_user.id,text =text)


@dp.message()
async def get_text_from_audio(message:Message): #message:Message

    if  message.content_type != ContentType.VOICE:
        await BOT.send_message(chat_id=message.from_user.id,text = "Это не голосовое сообщение.")
        return

    response_message = await BOT.send_message(chat_id=message.from_user.id, text="сейчас...")
    m_id = response_message.message_id

    voice = message.voice
    await BOT.download(voice, destination="voices/test.wav")

    try:
        vosk.convert_audio("voices/test.wav", "voices/convert.wav")
        result = vosk.transcriber(path_audio="voices/convert.wav")
    except:
        await BOT.send_message(chat_id=message.from_user.id, text="Произошла ошибка :/ \nПовторите еще раз.")

    if result:
        await BOT.delete_message(chat_id=message.from_user.id,message_id=m_id)
        await BOT.send_message(chat_id=message.from_user.id, text = f"Распознано:\n\n{result}")

    os.remove("voices/convert.wav")
    os.remove("voices/test.wav")


async def main():
    print('Работаем...')
    await dp.start_polling(BOT)

if __name__ == "__main__":
    asyncio.run(main())