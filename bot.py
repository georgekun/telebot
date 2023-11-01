import asyncio

from config import bot, dp

async def main():
    print('Running...')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())