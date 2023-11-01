
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message,ContentType

import config #берем из настроек
from module import service

router = Router()

@router.message(CommandStart())
async def welcome(message: Message):
    chat_id = message.chat.id
    chat_type = message.chat.type
    
    if chat_type != "private":
            return
    name = message.from_user.first_name
    text = (f"Приветствую, {name}! 🌟😊\n\nЯ - ваш личный бот для конвертации видео и аудио в текст.\
    Вы можете отправить мне видеокружки или аудизапись,и я помогу вам извлечь текст из них.💬✨\
    \nЯ могу распознать текст, но пока не научился расставлять запятые и точки по интонации 😞\
    \
    \n\nРазработчик @Georgikn ッ\
    \nБот на стадии 'написал на коленке' 💩\
    ")

    await config.bot.send_message(chat_id=chat_id,text = text)


@router.message() 
async def get_text_from_message(message:Message):
    
    chat_id = message.chat.id
    chat_type = message.chat.type
   
    # надо будет сохранить эти данные в базу
    if message.content_type != ContentType.VOICE and message.content_type != ContentType.VIDEO_NOTE:
        return
    
    result = await service.get_text(message = message)

    if result:
        await message.reply(text = result)
    else:
        await message.reply(text = "Не удалось распознать речь.")
