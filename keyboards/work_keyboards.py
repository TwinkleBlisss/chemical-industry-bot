from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_create_db_kb() -> types.ReplyKeyboardMarkup:
    """Клавиатура для команды создания базы данных."""
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Подтвердите ваше действие"
    )


def get_scan_barcode_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад", callback_data="back_from_scan_barcode")
    kb.adjust(1)
    kb.button(text="Штрихкод есть") #, callback_data="barcode_exist")
    kb.button(text="Штрихкода нет") #, callback_data="barcode_not_exist")
    kb.adjust(1, 2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Нажмите одну из кнопок"
    )


def get_upload_barcode_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад") #, callback_data="back_from_scan_barcode_not_exist")
    kb.adjust(1)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Пришлите фотографию штрихкода или нажмите 'назад'"
    )


def get_show_db_kb() -> types.InlineKeyboardMarkup:
    """Клавиатура для команды вывода списка таблиц."""
    kb = InlineKeyboardBuilder()

    # логика получения списка таблиц БД
    # вместе с их названиями...
    # этот словарик должен быть в базе по идее
    tables_name = {
        "barcodes": "Штрихкоды",
        "eurocube_barcodes": "Штрихкод-еврокуб",
        "eurocubes": "Еврокубы",
        "actions": "События",
        "products": "Товары",
        "order_list": "Товары в заказе",
        "orders": "Заказы",
        "partners": "Клиенты"
    }
    kb.button(text="Назад", callback_data="back_from_show_bd")
    kb.adjust(1)
    for eng_name, rus_name in tables_name.items():
        kb.button(text=rus_name, callback_data=eng_name)
    kb.adjust(1, 2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите таблицу из списка"
    )
