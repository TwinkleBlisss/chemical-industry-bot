import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
from handlers import general_commands, db_commands, scanning_barcodes


# Запуск процесса пуллинга новых апдейтов
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    # Объект бота
    bot = Bot(token=config.bot_token.get_secret_value())
    # Диспетчер
    dp = Dispatcher(storage=MemoryStorage())
    # Роутеры (должны быть указаны в нужной последовательности!)
    dp.include_routers(
        general_commands.router,
        db_commands.router,
        scanning_barcodes.router
    )

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)

    # await dp.run_polling(bot, )

if __name__ == "__main__":
    asyncio.run(main())
