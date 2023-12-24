from aiogram import types, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.db_keyboards import (
    get_create_db_kb,
    get_show_db_kb,
    get_table_menu_kb
)
from states import DBStates
import text

"""
Здесь будут команды create_db / show_db и тд
"""

router = Router()


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
async def create_db_exist(message: types.Message):
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
    # статус пользователя -> бд существует
    await state.set_state(DBStates.db_exist)

@router.message(DBStates.creating_db, F.text.lower() == "нет")
async def create_db_no(message: types.Message, state: FSMContext):
    await message.reply(
        "Действие отменено.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    # статус пользователя -> пустое
    await state.clear()

@router.message(DBStates.creating_db, ~F.text.lower().in_(("да", "нет")))
async def create_db_unknown(message: types.Message):
    await message.reply(
        "Я вас не понимаю. Попробуйте ещё раз",
        reply_markup=get_create_db_kb()
    )



# /show_db
@router.message(StateFilter(None), Command("show_db"))
@router.message(DBStates.creating_db, Command("show_db"))
async def cant_show_when_creating_db(message: types.Message):
    await message.reply(
        "Вы не можете посмотреть на базу данных, пока не создали ей. Нажмите /create_db",
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message(DBStates.db_exist, Command("show_db"))
async def cmd_show_db(message: types.Message, state: FSMContext):
    await message.answer(
        "Выберите таблицу из списка для дальнейших действий.",
        reply_markup=get_show_db_kb()
    )
    # статус пользователя -> просмотр бд
    await state.set_state(DBStates.show_db)


@router.message(DBStates.show_db, F.text.lower() == "назад")
async def stop_showing_db(message: types.Message, state: FSMContext):
    await message.reply(
        "Вы вышли из режима просмотра базы данных.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    # статус пользователя -> бд существует
    await state.set_state(DBStates.db_exist)

@router.message(DBStates.show_db, ~F.text.lower().in_([x.lower() for x in text.tables_name.values()]))
async def wrong_table_name(message: types.Message):
    await message.reply(
        "Такой таблицы не существует или вы ввели название некорректно. Попробуйте ещё раз",
        reply_markup=get_show_db_kb()
    )

@router.message(DBStates.show_db, F.text.lower().in_([x.lower() for x in text.tables_name.values()]))
async def table_menu(message: types.Message):
    table_name = message.text
    await message.answer(
        "Выберите действие",
        reply_markup=get_table_menu_kb(table_name)
    )


@router.message(DBStates.db_exist, ~F.text.in_(text.all_commands))
async def not_a_command(message: types.Message):
    await message.reply("Я вас не понимаю! Воспользуйтесь вкладкой 'Меню'")
