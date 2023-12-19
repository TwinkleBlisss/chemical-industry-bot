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


def get_scan_barcode_kb() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data="back_from_scan_barcode")
    kb.adjust(1)
    kb.button(text="Штрихкод есть", callback_data="barcode_exist")
    kb.button(text="Штрихкода нет", callback_data="barcode_not_exist")
    kb.adjust(1, 2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Нажмите одну из кнопок"
    )


def get_scan_barcode_not_exist_kb() -> types.ReplyKeyboardMarkup:

    kb = ReplyKeyboardBuilder()
    """
    Идея: можно потом кнопки-картинки сделать, чтобы работник видел что такое тара,
    а что такое обрешетка.
    """
    kb.button(text="Назад", callback_data="back_from_scan_barcode_not_exist")
    kb.adjust(1)
    kb.button(text="Тара", callback_data="tare")
    kb.button(text="Обрешетка", callback_data="grate")
    kb.adjust(1, 2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Части еврокуба"
    )


def get_show_db_kb() -> types.InlineKeyboardMarkup:
    """Клавиатура для команды вывода списка таблиц."""
    kb = InlineKeyboardBuilder()

    # логика получения списка таблиц БД
    # вместе с их названиями...

    for i in range(1, 9):
        kb.button(text=f"Таблица {str(i)}", callback_data=f"table_{str(i)}")

    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите таблицу из списка"
    )
