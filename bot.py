import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import general_commands, work_commands


# Запуск процесса пуллинга новых апдейтов
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=config.bot_token.get_secret_value())
    # Диспетчер
    dp = Dispatcher()
    # Роутеры (должны быть указаны в нужной последовательности!)
    dp.include_routers(
        general_commands.router,
        work_commands.router
    )

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
