import os
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,ContentType

from module.vosk import Vosk
from module import service

load_dotenv()

BOT = Bot(token=os.getenv("TG_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()
vosk = Vosk("vosk-model-small-ru-0.22")

@dp.message(CommandStart())
async def welcome(message: Message):
    name = message.from_user.first_name
    text = (f"Приветствую, {name}! 🌟😊\n\nЯ - ваш личный бот для конвертации видео и аудио в текст.\
    Вы можете отправить мне видеокружки или аудизапись,и я помогу вам извлечь текст из них.💬✨\
    \nЯ могу распознать текст, но пока не научился расставлять запятые и точки по интонации 😞\
    \
    \n\nРазработчик @Georgikn ッ\
    \nБот на стадии 'написал на коленке' 💩\
    ")

    await BOT.send_message(chat_id=message.from_user.id,text =text)


@dp.message()
async def get_text_from_doc(message:Message):
    if message.content_type != ContentType.VOICE and message.content_type != ContentType.VIDEO_NOTE:
        await BOT.send_message(chat_id=message.from_user.id, text=f"Можно отправлять либо кружки, либо аудио")
        return

    response_message = await BOT.send_message(chat_id=message.from_user.id, text="сейчас...")
    m_id = response_message.message_id

    result = await service.get_text(bot = BOT, vosk = vosk, message = message)

    await BOT.delete_message(chat_id=message.from_user.id, message_id=m_id)
    if result:
        await BOT.send_message(chat_id=message.from_user.id, text=f"[ распознано ]\n{result}")
    else:
        await BOT.send_message(chat_id=message.from_user.id, text=f"Не удалось распознать речь.")


async def main():
    print('Running...')
    await dp.start_polling(BOT)

if __name__ == "__main__":
    asyncio.run(main())