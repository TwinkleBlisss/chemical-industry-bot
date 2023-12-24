from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import text


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


def get_show_db_kb() -> types.ReplyKeyboardMarkup:
    """Клавиатура для команды вывода списка таблиц."""
    kb = ReplyKeyboardBuilder()

    # логика получения списка таблиц БД
    # вместе с их названиями...
    # этот словарик должен быть в базе по идее

    kb.button(text="Назад")
    for rus_name in text.tables_name.values():
        kb.button(text=rus_name)
    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите таблицу из списка"
    )

def get_table_menu_kb(table_name: str) -> types.ReplyKeyboardMarkup:
    """Клавиатура для команды вывода списка таблиц."""
    kb = ReplyKeyboardBuilder()

    kb.button(text="Назад")
    kb.button(text="Показать содержимое")
    kb.button(text="Внести запись")
    kb.button(text="Заменить запись")
    kb.button(text="Удалить запись")
    kb.button(text="Очистить таблицу")
    kb.adjust(2)
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder=f"Таблица {table_name}"
    )
