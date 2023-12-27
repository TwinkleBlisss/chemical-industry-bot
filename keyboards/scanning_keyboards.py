from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import text


def get_scan_barcode_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад", callback_data="back_from_scan_barcode")
    kb.adjust(1)
    kb.button(text="Штрихкод есть") #, callback_data="barcode_exist")
    kb.button(text="Штрихкода нет") #, callback_data="barcode_not_exist")
    kb.adjust(1, 2)
    return kb.as_markup(
        resize_keyboard=True
    )


def get_upload_barcode_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад") #, callback_data="back_from_scan_barcode_not_exist")
    kb.adjust(1)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Ожидание фото.."
    )


def get_eurocube_found_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Выйти из режима (вернуться в начало сканирования)")
    kb.button(text="Добавить новый штрихкод")
    kb.button(text="Изменить статус еврокуба")
    kb.adjust(1)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие.."
    )


def get_change_status_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад")
    kb.button(text="Прибыл на базу (новый или от клиента)")
    kb.button(text="Уезжает в рейс")
    kb.adjust(1)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите статус.."
    )


def get_waiting_order_id_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад")
    kb.adjust(1)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Ожидание номера заказа.."
    )


def get_products_names_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад")
    kb.adjust(1)
    for chem in text.chemicals:
        kb.button(text=chem)
    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите название химиката"
    )