from aiogram import types, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.db_keyboards import (
    get_create_db_kb,
    get_show_db_kb
)
import text

"""
Здесь будут команды create_db / delete_db
"""

router = Router()


class DBStates(StatesGroup):
    creating_db = State()
    db_exist = State()


# /create_db
@router.message(StateFilter(None), Command("create_db"))
async def cmd_create_db_new(message: types.Message, state: FSMContext):
    # статус пользователя -> создание бд
    await state.set_state(DBStates.creating_db)
    await message.answer(
        "Вы уверены, что хотите создать базу данных?",
        reply_markup=get_create_db_kb()
    )

@router.message(DBStates.db_exist, Command("create_db"))
async def create_db_exist(message: types.Message, state: FSMContext):
    await message.reply(
        "Вы не можете создать базу данных, так как она уже существует.\n"
        "Используйте команду /show_db, чтобы взглянуть на неё."
    )

@router.message(DBStates.creating_db, F.text.lower() == "да")
async def create_db_yes(message: types.Message, state: FSMContext):

    # логика создания БД...

    await message.reply(
        "База данных создана!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    # статус пользователя -> нет статуса
    await state.set_state(DBStates.db_exist)

@router.message(DBStates.creating_db, F.text.lower() == "нет")
async def create_db_no(message: types.Message, state: FSMContext):
    await message.reply(
        "Действие отменено.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()

@router.message(DBStates.creating_db, ~F.text.lower().in_(("да", "нет")))
async def create_db_unknown(message: types.Message):
    await message.reply(
        "Я вас не понимаю. Попробуйте ещё раз",
        reply_markup=get_create_db_kb()
    )



# /show_db
@router.message(DBStates.db_exist, Command("show_db"))
async def cmd_show_db(message: types.Message):
    await message.answer(
        "Выберите таблицу из списка ниже:",
        reply_markup=get_show_db_kb()
    )

@router.message(StateFilter(None), Command("show_db"))
@router.message(DBStates.creating_db, Command("show_db"))
async def cant_show_when_creating_db(message: types.Message, state: FSMContext):
    await message.reply(
        "Вы не можете посмотреть на базу данных, пока не создали ей. Нажмите /create_db",
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message(DBStates.db_exist, ~F.text.in_(text.all_commands))
async def not_a_command(message: types.Message):
    await message.reply("Я вас не понимаю! Воспользуйтесь вкладкой 'Меню'")