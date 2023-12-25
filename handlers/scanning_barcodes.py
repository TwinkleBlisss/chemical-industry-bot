from bot import conn

from aiogram import Router, types, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aspose.barcode import barcoderecognition
from keyboards.scanning_keyboards import (
    get_scan_barcode_kb,
    get_upload_barcode_kb,
    get_eurocube_found_kb,
    get_change_status_kb,
    get_waiting_order_id_kb,
    get_products_names_kb
)
from states import DBStates, ScanBarcode
import text
import os




"""
Здесь будут команды режима scan_barcode
"""

router = Router()


# /scan_barcode
@router.message(DBStates.db_exist, Command("scan_barcode"))
@router.message(ScanBarcode.waiting_for_existing_photo, F.text.lower() == "назад")
@router.message(ScanBarcode.waiting_for_new_photo, F.text.lower() == "назад")
@router.message(ScanBarcode.eurocube_found, F.text.startswith("Выйти"))
async def cmd_scan_barcode(message: types.Message, state: FSMContext):
    await message.answer(
        "Вы перешли в режим сканирования штрихкодов. "
        "Выберите дальнейшее действие:",
        reply_markup=get_scan_barcode_kb()
    )
    # статус пользователя -> выбор существует ли штрихкод
    await state.set_state(ScanBarcode.choosing_barcode_existance)

@router.message(StateFilter(None), Command("scan_barcode"))
@router.message(DBStates.creating_db, Command("scan_barcode"))
async def cant_scan_barcode(message: types.Message):
    await message.reply(
        "Вы не можете включить режим сканирования, пока не создана база данных. "
        "Для создания базы данных используйте команду /create_db"
    )

@router.message(ScanBarcode.choosing_barcode_existance, F.text.lower() == "назад")
async def scan_barcode_back(message: types.Message, state: FSMContext):
    await message.answer(
        "Вы вышли из режима сканирования штрихкодов.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    # статус пользователя -> бд существует
    await state.set_state(DBStates.db_exist)


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
        "Ничего страшного! Давайте добавим этот еврокуб в базу.\n\n"
        "Прикрепите новый штрихкод на еврокуб, сфотографируйте его и "
        "пришлите следующим сообщением.",
        reply_markup=get_upload_barcode_kb()
    )
    # статус пользователя -> ожидание фото штрихкода нового куба
    await state.set_state(ScanBarcode.waiting_for_new_photo)


@router.message(
    ScanBarcode.choosing_barcode_existance,
    ~F.text.endswith(("есть", "нет"))
)
async def unknown_command(message: types.Message):
    await message.answer("Такой команды нет, либо она недоступна в данный момент. Попробуйте ещё раз")


def barcode_recognizing(path):
    """
    Возвращает номер штрихкода с изображения, лежащего в path.
    """
    try:
        # Инициализировать считыватель штрих-кода
        reader = barcoderecognition.BarCodeReader(path)
        # Чтение штрих-кодов (по умолчанию он на фотографии один)
        recognized_results = reader.read_bar_codes()
        # получение результата
        barcode_id = recognized_results[0].code_text
        return barcode_id

    except:
        print("Pizda")
    """
    # переименовывание файла
    try:
        os.rename(path, f"tmp/{barcode_id}.jpg")
    except FileNotFoundError:
        print("Файл не найден")
    except PermissionError:
        print("Нет доступа для переименования файла")
    """



@router.message(ScanBarcode.waiting_for_existing_photo, F.photo)
async def existing_barcode(message: types.Message, state: FSMContext, bot: Bot):
    path = f"tmp/{message.photo[-1].file_id}.jpg"
    await bot.download(
        message.photo[-1],
        destination=path
    )
    # сканируем штрихкод
    barcode_id = barcode_recognizing(path)

    # тут нужно будет удалить новое фото, так как фото этого штрихкода уже есть в базе
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

    # ищем нужный еврокуб
    eurocube = conn.scan_barcode(barcode_id)
    if not eurocube:
        await message.reply(
            "Еврокуба с таким штрихкодом нет в базе. Вернитесь назад и добавьте штрихкод.",
            reply_markup=get_scan_barcode_kb()
        )
        return
    eurocube_id = eurocube[0][0]



    """
    1) Распознаём номер штрихкода.
    2) Ищем нужный штрихкод в таблице barcodes.
    3) Переходим к объекту еврокуба.
    """

    await message.reply(
        f"Еврокуб с id={eurocube_id} успешно идентифицирован по штрихкоду с id={barcode_id}!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await message.answer(
        "Что вы хотите сделать с еврокубом?",
        reply_markup=get_eurocube_found_kb()
    )
    # await state.update_data(eurocube_found=eurocube_id)
    await state.update_data(eurocube_found=eurocube_id)
    # статус пользователя -> куб найден
    await state.set_state(ScanBarcode.eurocube_found)


@router.message(ScanBarcode.waiting_for_new_photo, F.photo)
async def new_barcode(message: types.Message, state: FSMContext, bot: Bot):
    path = f"tmp/{message.photo[-1].file_id}.jpg"
    await bot.download(
        message.photo[-1],
        destination=path
    )
    # сканируем штрихкод
    barcode_id = barcode_recognizing(path)

    # удаляем фото
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

    # регистрируем нужный еврокуб

    """
    Здесь мы обращаемся к бд, чтобы:
    1) Создать объект штрихкода, еврокуба и их связи.
    *) Установить статус еврокуба.
    """
    conn.insert_into_table("eurocube", barcode_id, "1994-03-17", 0)
    eurocube_id = conn.scan_barcode(barcode_id)[0][0]
    await message.reply(
        f"Еврокуб с id={eurocube_id} успешно зарегистрирован по штрихкоду с id={barcode_id}!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await message.answer(
        "Что вы хотите сделать с еврокубом?",
        reply_markup=get_eurocube_found_kb()
    )
    # await state.update_data(eurocube_found=eurocube_id)
    await state.update_data(eurocube_found=eurocube_id)
    # статус пользователя -> куб найден
    await state.set_state(ScanBarcode.eurocube_found)


@router.message(ScanBarcode.waiting_for_existing_photo, ~F.photo)
@router.message(ScanBarcode.waiting_for_new_photo, ~F.photo)
@router.message(ScanBarcode.waiting_for_add_photo, ~F.photo, F.text.lower() != "назад")
async def not_a_photo(message: types.Message):
    await message.answer("Это не фото! Попробуйте ещё раз")


@router.message(ScanBarcode.waiting_for_add_photo, F.text.lower() == "назад")
@router.message(ScanBarcode.waiting_for_status, F.text.lower() == "назад")
async def menu_eurocube(message: types.Message, state: FSMContext):
    await state.set_state(ScanBarcode.eurocube_found)
    await message.answer(
        "Что вы хотите сделать с еврокубом?",
        reply_markup=get_eurocube_found_kb()
    )
@router.message(ScanBarcode.eurocube_found, F.text.startswith("Добавить"))
async def add_barcode(message: types.Message, state: FSMContext):
    await message.answer(
        "Пришлите мне штрихкод, который вы хотите добавить к этому еврокубу",
        reply_markup=get_upload_barcode_kb()
    )
    # статус пользователя -> ожидание фото дополнительного штрихкода куба
    await state.set_state(ScanBarcode.waiting_for_add_photo)
@router.message(ScanBarcode.waiting_for_add_photo, F.photo)
async def upload_additional_barcode(message: types.Message, state: FSMContext, bot: Bot):
    path = f"tmp/{message.photo[-1].file_id}.jpg"
    await bot.download(
        message.photo[-1],
        destination=path
    )

    data = await state.get_data()
    eurocube_id = data['eurocube_found'] # ЭТО ТЕСТ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    # ФУНКЦИЯ В РАЗРАБОТКЕ!!!!!!!!!!

    # сканируем штрихкод
    barcode_id = barcode_recognizing(path)

    # удаляем фото
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

    """
    В БД добавляем новый штрихкод в barcodes, указывая текущий eurocube_id.
    """
    conn.insert_into_table("barcodes", barcode_id, eurocube_id)

    await message.reply(
        f"Штрихкод с id={barcode_id} успешно добавлен к еврокубу с id={eurocube_id}", # ЭТО ТЕСТ!!!!!
        reply_markup=types.ReplyKeyboardRemove()
    )
    await message.answer(
        "Что вы хотите сделать с еврокубом?",
        reply_markup=get_eurocube_found_kb()
    )
    # статус пользователя -> куб найден
    await state.set_state(ScanBarcode.eurocube_found)
@router.message(ScanBarcode.eurocube_found, F.text.startswith("Изменить"))
@router.message(ScanBarcode.waiting_for_order_id, F.text.lower() == "назад")
@router.message(ScanBarcode.waiting_for_product, F.text.lower() == "назад")
async def change_status(message: types.Message, state: FSMContext):
    # статус пользователя -> ожидание выбора статуса
    await state.set_state(ScanBarcode.waiting_for_status)
    await message.answer(
        "Выберите текущий статус еврокуба",
        reply_markup=get_change_status_kb()
    )
@router.message(ScanBarcode.waiting_for_status, F.text.startswith("Прибыл"))
async def status_arrived(message: types.Message, state: FSMContext):
    pass
    """
    В БД  в таблицу actions добавляется запись о статусе куба (arrived).
    """
    data = await state.get_data()
    eurocube_id = data['eurocube_found']
    conn.insert_into_table("actions", eurocube_id, "arrived")
    await message.reply("Статус записан!")
    await message.answer(
        "Что вы хотите сделать с еврокубом?",
        reply_markup=get_eurocube_found_kb()
    )
    # статус пользователя -> действия с еврокубом
    await state.set_state(ScanBarcode.eurocube_found)
@router.message(ScanBarcode.waiting_for_status, F.text.startswith("Уезжает"))
async def status_leaves(message: types.Message, state: FSMContext):
    pass
    """
    В БД  в таблицу actions добавляется запись о статусе куба (leaves).
    """
    data = await state.get_data()
    eurocube_id = data['eurocube_found']
    conn.insert_into_table("actions", eurocube_id, "leaves")
    await message.reply(
        "Статус записан! Теперь введите номер заказа",
        reply_markup=get_waiting_order_id_kb()
    )
    # статус пользователя -> ожидание номера заказа
    await state.set_state(ScanBarcode.waiting_for_order_id)
@router.message(ScanBarcode.waiting_for_order_id, F.text.isdecimal())
async def waiting_for_order_id(message: types.Message, state: FSMContext):
    pass
    """
    Ищем в БД заказ по id.
    """
    order_id = conn.get_order(int(message.text))

    if order_id is None:
        await message.reply(
            "Такого заказа нет в базе. Введите заново или нажмите 'назад'.",
            reply_markup=get_waiting_order_id_kb()
        )
    else:
        # статус пользователя -> ожидание названия химиката
        await state.set_state(ScanBarcode.waiting_for_product)
        await state.update_data(order_id=order_id)
        await message.answer(
            "Заказ найден! Теперь выберите химикат, который зальют в еврокуб.",
            reply_markup=get_products_names_kb()
        )
@router.message(ScanBarcode.waiting_for_order_id, ~F.text.isdecimal())
async def incorrect_order_id(message: types.Message):
    await message.reply(
        "С номером заказа что-то не так. Попробуйте ещё раз",
        reply_markup=get_waiting_order_id_kb()
    )
@router.message(ScanBarcode.waiting_for_product, F.text.in_(text.chemicals))
async def product_selected(message: types.Message, state: FSMContext):
    pass
    """
    В БД обновляется таблица order_list. 
    """
    data = await state.get_data()
    order_id = data.get("order_id")
    eurocube_id = data.get("eurocube_found")
    product_id = conn.get_product_id(message.text)
    conn.update_table("order_list", order_id, eurocube_id, product_id)
    await message.reply("Химикат выбран!")
    await message.answer(
        "Что вы хотите сделать с еврокубом?",
        reply_markup=get_eurocube_found_kb()
    )
    # статус пользователя -> действия с еврокубом
    await state.set_state(ScanBarcode.eurocube_found)
@router.message(ScanBarcode.waiting_for_product, ~F.text.in_(text.chemicals))
async def product_selected(message: types.Message):
    await message.reply(
        "Такого химиката в базе нет. Попробуйте ещё раз",
        reply_markup=get_products_names_kb()
    )



@router.message(
    ScanBarcode.eurocube_found,
    ~F.text.startswith(("Выйти", "Добавить", "Изменить"))
)
@router.message(
    ScanBarcode.waiting_for_status,
    ~F.text.startswith(("Назад", "Прибыл", "Уезжает"))
)
async def unknown_barcode_command(message: types.Message):
    await message.answer(
        "Такого действия нет! Попробуйте ещё раз"
    )
