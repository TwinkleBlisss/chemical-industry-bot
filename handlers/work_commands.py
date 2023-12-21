from aiogram import types, F, Router
from aiogram.filters import Command
from keyboards.work_keyboards import (
    get_create_db_kb,
    get_show_db_kb
)

"""
Здесь будут команды create_db / delete_db
"""

router = Router()


# /create_db
@router.message(Command("create_db"))
async def cmd_create_db(message: types.Message):
    await message.answer(
        "Вы уверены, что хотите создать базу данных?",
        reply_markup=get_create_db_kb()
    )


@router.message(F.text.lower() == "да")
async def create_db_yes(message: types.Message):

    # логика создания БД...

    await message.reply(
        "База данных создана!",
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(F.text.lower() == "нет")
async def create_db_no(message: types.Message):
    await message.reply(
        "Действие отменено.",
        reply_markup=types.ReplyKeyboardRemove()
    )





# /show_db
@router.message(Command("show_db"))
async def cmd_show_db(message: types.Message):
    await message.answer(
        "Выберите таблицу из списка ниже:",
        reply_markup=get_show_db_kb()
    )
