"""
Точка входа, код запуска бота и инициализации всех остальных модулей.
"""

# внешние пакеты
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

# внутренний функционал
from config_reader import config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()


# внешние пакеты
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram import types
from aiogram import F

# внутренний функционал
from bot import dp
import text


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(text.start_phrase)


@dp.message(Command("hello"))
async def cmd_hello(message: types.Message):
    await message.answer(
        f"Здравствуйте, <b>{message.from_user.full_name}</b>!",
        parse_mode=ParseMode.HTML
    )


@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    await message.answer(
        f"Ваш id: {message.from_user.id}"
    )


@dp.message(Command("create_db"))
async def cmd_create_db(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Подтвердите ваше действие"
    )
    await message.answer(
        "Вы уверены, что хотите создать базу данных?",
        reply_markup=keyboard
    )


@dp.message(F.text.lower() == "да")
async def create_db_yes(message: types.Message):
    await message.reply(
        "База данных создана!",
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message(F.text.lower() == "нет")
async def create_db_no(message: types.Message):
    await message.reply(
        "Действие отменено.",
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message(Command("tables_list"))
async def cmd_tables_list(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 7):
        builder.add(types.KeyboardButton(text=f"Таблица {str(i)}"))
    builder.adjust(3)
    await message.answer(
        "Выберите таблицу из списка",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.message(Command("bot_info"))
async def cmd_bot_info(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub бота", url="https://github.com/TwinkleBlisss"
    ))
    builder.row(types.InlineKeyboardButton(
        text="Телеграм бота",
        url="https://t.me/chemical_industry_bot"
    ))

    # Чтобы иметь возможность показать ID-кнопку,
    # У юзера должен быть False флаг has_private_forwards
    admin_id1 = 498450978
    chat_info = await bot.get_chat(admin_id1)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text="Админ 1",
            url=f"tg://user?id={admin_id1}"
        ))

    admin_id2 = 498450978
    chat_info = await bot.get_chat(admin_id2)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text="Админ 2",
            url=f"https://t.me/krosha31"
        ))

    await message.answer(
        'Выберите ссылку',
        reply_markup=builder.as_markup(),
    )


# Запуск процесса пуллинга новых апдейтов
async def main():
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
