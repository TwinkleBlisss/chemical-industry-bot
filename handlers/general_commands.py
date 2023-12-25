from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from random import randint
from keyboards.general_keyboards import (
    get_bot_info_kb,
    get_random_kb
)
from states import DBStates
import text

"""
Здесь будут команды start / help / bot_info и тд
"""

router = Router()


# /start
@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(text.start_phrase, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(DBStates.db_exist)


# /bot_info
@router.message(StateFilter(None), Command("bot_info"))
@router.message(DBStates.db_exist, Command("bot_info"))
async def cmd_bot_info(message: types.Message):
    await message.answer(
        'Выберите ссылку',
        reply_markup=get_bot_info_kb()
    )


# /id
@router.message(StateFilter(None), Command("id"))
@router.message(DBStates.db_exist, Command("id"))
async def cmd_id(message: types.Message):
    await message.answer(
        f"Ваш id: {message.from_user.id}"
    )


# /name
@router.message(StateFilter(None), Command("name"))
@router.message(DBStates.db_exist, Command("name"))
async def cmd_name(message: types.Message):
    await message.answer(
        f"Вас зовут <b>{message.from_user.full_name}</b>!",
        parse_mode=ParseMode.HTML
    )


# /random
@router.message(StateFilter(None), Command("random"))
async def cmd_random(message: types.Message):
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10.",
        reply_markup=get_random_kb()
    )


@router.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer()


@router.message(StateFilter(None), Command("cancel"))
async def cmd_cancel(message: types.Message):
    await message.answer(
        "Отменять нечего, но клавиатура скрыта.",
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    # статус пользователя -> None
    await state.clear()
    await message.answer(
        "Вы прервали текущую операцию.",
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(StateFilter(None), ~F.text.in_(text.all_commands))
async def not_a_command(message: types.Message):
    await message.reply("Я вас не понимаю! Воспользуйтесь вкладкой 'Меню'")
