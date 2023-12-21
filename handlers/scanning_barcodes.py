from aiogram import Router, types, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aspose.barcode import barcoderecognition
from keyboards.work_keyboards import (
    get_scan_barcode_kb,
    get_upload_barcode_kb
)
import os


"""
Здесь будут команды режима scan_barcode
"""

router = Router()


class ScanBarcode(StatesGroup):
    choosing_barcode_existance = State()
    waiting_for_new_photo = State()
    waiting_for_existing_photo = State()
    eurocube_found = State()


# /scan_barcode
@router.message(StateFilter(None), Command("scan_barcode"))
async def cmd_scan_barcode(message: types.Message, state: FSMContext):
    await message.answer(
        "Вы перешли в режим сканирования штрихкодов. "
        "Выберите дальнейшее действие:",
        reply_markup=get_scan_barcode_kb()
    )
    # статус пользователя -> выбор существует ли штрихкод
    await state.set_state(ScanBarcode.choosing_barcode_existance)


# @router.callback_query(F.data == "back_from_scan_barcode")
@router.message(ScanBarcode.choosing_barcode_existance, F.text.lower() == "назад")
async def scan_barcode_back(message: types.Message, state: FSMContext):
    await message.answer(
        "Вы вышли из режима сканирования штрихкодов.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    # статус пользователя -> None
    await state.clear()


# @router.callback_query(F.data == "barcode_exist")
@router.message(ScanBarcode.choosing_barcode_existance, F.text.endswith("есть"))
async def scan_barcode_exist(message: types.Message, state: FSMContext):
    await message.answer(
        "Отлично! Теперь сфотографируйте его и пришлите следующим сообщением.",
        reply_markup=get_upload_barcode_kb()
    )
    # статус пользователя -> ожидание фото штрихкода существующего куба
    await state.set_state(ScanBarcode.waiting_for_existing_photo)


# @router.callback_query(F.data == "barcode_not_exist")
@router.message(ScanBarcode.choosing_barcode_existance, F.text.endswith("нет"))
async def scan_barcode_not_exist(message: types.Message, state: FSMContext):
    await message.answer(
        "Ничего страшного! Давайте добавим этот еврокуб в базу.\n"
        "Прикрепите новый штрихкод на еврокуб, сфотографируйте его и"
        "пришлите следующим сообщением.",
        reply_markup=get_upload_barcode_kb()
    )
    # статус пользователя -> ожидание фото штрихкода нового куба
    await state.set_state(ScanBarcode.waiting_for_new_photo)


@router.message(ScanBarcode.waiting_for_existing_photo, F.photo)
async def existing_barcode(message: types.Message, state: FSMContext, bot: Bot):
    path = f"tmp/{message.photo[-1].file_id}.jpg"
    await bot.download(
        message.photo[-1],
        destination=path
    )
    # сканируем штрихкод
    barcode_id = barcode_recognizing(path)
    # регистрируем нужный еврокуб
    eurocube_id = 719243

    """
    1) Распознаём номер штрихкода.
    2) Ищем нужный штрихкод в таблице barcodes.
    3) Переходим к объекту еврокуба.
    """

    await message.reply(
        f"Еврокуб с id={eurocube_id} успешно идентифицирован по штрихкоду с id={barcode_id}!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.update_data(eurocube_found=eurocube_id)
    # статус пользователя -> куб найден
    await state.set_state(ScanBarcode.eurocube_found)


def barcode_recognizing(path):
    """
    Возвращает номер штрихкода с изображения, лежащего в path,
    и переименовывает файл в соответствии с этим номером.
    """

    # Инициализировать считыватель штрих-кода
    reader = barcoderecognition.BarCodeReader(path)
    # Чтение штрих-кодов (по умолчанию он на фотографии один)
    recognized_results = reader.read_bar_codes()
    # получение результата
    barcode_id = recognized_results[0].code_text
    # переименовывание файла
    try:
        os.rename(path, f"tmp/{barcode_id}.jpg")
    except FileNotFoundError:
        print("Файл не найден")
    except PermissionError:
        print("Нет доступа для переименования файла")

    return barcode_id


@router.message(ScanBarcode.waiting_for_new_photo, F.photo)
async def new_barcode(message: types.Message, state: FSMContext, bot: Bot):
    path = f"tmp/{message.photo[-1].file_id}.jpg"
    await bot.download(
        message.photo[-1],
        destination=path
    )
    # сканируем штрихкод
    barcode_id = barcode_recognizing(path)
    # регистрируем нужный еврокуб
    eurocube_id = 719243

    """
    Здесь мы обращаемся к бд, чтобы:
    1) Сохранить туда фото штрихкода.
    2) Создать объект штрихкода, еврокуба и их связи.
    *) Установить статус еврокуба.
    """
    await message.reply(
        f"Еврокуб с id={eurocube_id} успешно зарегистрирован по штрихкоду с id={barcode_id}!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.update_data(eurocube_found=eurocube_id)
    # статус пользователя -> куб найден
    await state.set_state(ScanBarcode.eurocube_found)


# @router.message(ScanBarcode.waiting_for_existing_photo | ScanBarcode.waiting_for_new_photo)
# async def not_a_photo(message: types.Message, state: FSMContext):


# @router.message(ScanBarcode.eurocube_found)
# async def