import asyncio

from aiogram import Dispatcher, types, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand
from handlers.contribution import register_handlers_contribution
from handlers.common import register_handlers_common


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="/start", description="Начать расчет процентов по вкладу"),
    ]
    await bot.set_my_commands(commands)


async def main():
    bot_percent = Bot(token="1865326027:AAEnGQB8zzyGZYQQm5qyHYABcxmMtMCX5x8")
    dp = Dispatcher(bot_percent, storage=MemoryStorage())

    register_handlers_contribution(dp)
    register_handlers_common(dp)

    await set_commands(bot_percent)

    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
