from aiogram import types, F, Router
from aiogram.filters import Command
from keyboards.work_keyboards import (
    get_create_db_kb,
    get_scan_barcode_kb,
    get_scan_barcode_not_exist_kb,
    get_show_db_kb
)
# import text


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


# /scan_barcode
@router.message(Command("scan_barcode"))
async def cmd_scan_barcode(message: types.Message):
    await message.answer(
        "Вы перешли в режим сканирования штрихкодов. "
        "Выберите дальнейшее действие:",
        reply_markup=get_scan_barcode_kb()
    )


@router.callback_query(F.data == "back_from_scan_barcode")
async def scan_barcode_back(callback: types.CallbackQuery):
    await callback.message.answer(
        "Вы вышли из режима сканирования штрихкодов.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await callback.answer()


@router.callback_query(F.data == "barcode_exist")
async def scan_barcode_exist(callback: types.CallbackQuery):
    await callback.message.answer(
        "Отлично! Теперь сфотографируйте его и пришлите следующим сообщением.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await callback.answer()


@router.callback_query(F.data == "barcode_not_exist")
async def scan_barcode_not_exist(callback: types.CallbackQuery):
    await callback.message.answer(
        "Ничего страшного! Давайте добавим этот еврокуб в базу.\n"
        "Для начала выберите ту его часть, к которой вы прикрепите штрихкод.",
        reply_markup=get_scan_barcode_not_exist_kb()
    )
    await callback.answer()


# /show_db
@router.message(Command("show_db"))
async def cmd_show_db(message: types.Message):
    await message.answer(
        "Таблицы БД",
        reply_markup=get_show_db_kb()
    )
