import asyncio
from aiogram import Dispatcher, types, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand
from handlers.contribution import register_handlers_contribution
from config import *


async def set_commands(dp) -> None:
    await dp.bot.set_my_commands([
        BotCommand(command="start", description="Начать расчет процентов по вкладу."),
        BotCommand(command="cancel", description="Отмена диалога.")
    ])


async def main():
    bot_percent = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot_percent, storage=MemoryStorage())
    register_handlers_contribution(dp)
    await set_commands(dp)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
