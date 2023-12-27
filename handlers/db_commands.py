from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.db_keyboards import (
    get_create_db_kb,
    get_show_db_kb,
    get_table_menu_kb,
    get_add_update_row_kb,
    get_delete_row_kb,
    get_clear_table_kb,
    get_yes_no_delete_row_kb
)
from connection import conn
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

    conn.create_db("chemical-industry-database")

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
@router.message(DBStates.in_table, F.text.lower() == "назад")
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
async def table_menu(message: types.Message, state: FSMContext):
    table_name = message.text
    await state.update_data(table_name=table_name)
    await message.answer(
        "Выберите действие",
        reply_markup=get_table_menu_kb(table_name)
    )
    # статус пользователя -> просмотр бд
    await state.set_state(DBStates.in_table)


@router.message(DBStates.in_table, ~F.text.startswith(tuple(text.operations_starts)))
async def wrong_table_action(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    await message.reply(
        "Такой команды нет! Попробуйте ещё раз"
    )
    await message.answer(
        "Выберите действие",
        reply_markup=get_table_menu_kb(table_name)
    )


@router.message(DBStates.in_table, F.text.startswith("Показать"))
async def show_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    eng_table_name = text.tables_name_reversed[table_name]

    # проверка доступна ли операция для таблицы
    if "show_table" in text.tables_operations[eng_table_name]:

        # вывод содержимого таблицы
        table = conn.get_table(eng_table_name)

        raw_output = [text.tables_columns[eng_table_name], *table]
        result_output = []
        for i in raw_output:
            result_output.append("    |    ".join(map(str, i)))
        result_output = "\n".join(result_output)
        await message.answer(
            f"Содержимое таблицы:\n"
            f"{result_output}",
            reply_markup=get_table_menu_kb(table_name)
        )

    else:
        await message.reply(
            "К сожалению в данный момент данная операция для этой таблицы недоступна. "
            "Попробуйте позже",
            reply_markup=get_table_menu_kb(table_name)
        )


@router.message(DBStates.in_table, F.text.startswith("Внести"))
async def add_row_to_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    eng_table_name = text.tables_name_reversed[table_name]

    # проверка доступна ли операция для таблицы
    if "add_row" in text.tables_operations[eng_table_name]:
        await message.answer(
            "Напиши через пробел данные для внесения в таблицу.\n"
            "Внимательно соблюдайте типы столбцов!",
            reply_markup=get_add_update_row_kb(table_name)
        )
        await state.set_state(DBStates.waiting_add_row)
    else:
        await message.reply(
            "К сожалению, в данный момент данная операция для этой таблицы недоступна. "
            "Попробуйте позже",
            reply_markup=get_table_menu_kb(table_name)
        )


@router.message(DBStates.waiting_add_row, F.text)
async def new_row_added(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    # eng_table_name = text.tables_name_reversed[table_name]

    # в бд в нужную таблицу добавляется строчка
    # conn.insert_into_table(eng_table_name, message.text.split())

    await message.reply(
        "Новая запись успешно добавлена в таблицу!",
        reply_markup=get_table_menu_kb(table_name)
    )
    await state.set_state(DBStates.in_table)


@router.message(DBStates.waiting_add_row, F.text.lower() == "назад")
@router.message(DBStates.waiting_update_row_number, F.text.lower() == "назад")
@router.message(DBStates.waiting_delete_row_number, F.text.lower() == "назад")
async def back_add_update_delete_row(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    await message.answer(
        "Выберите действие",
        reply_markup=get_table_menu_kb(table_name)
    )
    # статус пользователя -> просмотр бд
    await state.set_state(DBStates.in_table)


@router.message(DBStates.in_table, F.text.startswith("Заменить"))
@router.message(DBStates.waiting_update_row_data, F.text.lower() == "назад")
async def update_row(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    eng_table_name = text.tables_name_reversed[table_name]

    # проверка доступна ли операция для таблицы
    if "update_row" in text.tables_operations[eng_table_name]:
        await message.answer(
            "Выберите строку таблицы, которую хотите заменить. "
            "При выборе номера проверьте, что такая строчка существует!",
            reply_markup=get_add_update_row_kb(table_name)
        )
        await state.set_state(DBStates.waiting_update_row_number)
    else:
        await message.reply(
            "К сожалению, в данный момент данная операция для этой таблицы недоступна. "
            "Попробуйте позже",
            reply_markup=get_table_menu_kb(table_name)
        )


@router.message(DBStates.waiting_update_row_number, ~F.text.isdecimal())
async def wrong_row_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    await message.reply(
        "Это не номер строки! Попробуйте ещё раз",
        reply_markup=get_add_update_row_kb(table_name)
    )


@router.message(DBStates.waiting_update_row_number, F.text.isdecimal())
async def right_row_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']

    # запоминаем номер строчки
    await state.update_data(row_number=int(message.text))
    await message.reply(
        "Строчку выбрали. Теперь напишите значения для замены через пробел, "
        "соблюдая типы столбцов!",
        reply_markup=get_add_update_row_kb(table_name)
    )
    await state.set_state(DBStates.waiting_update_row_data)


@router.message(DBStates.waiting_update_row_data, F.text)
async def new_row_updated(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    # eng_table_name = text.tables_name_reversed[table_name]

    # в бд в нужную таблицу добавляется строчка
    # conn.update_table(eng_table_name, message.text.split())

    await message.reply(
        "Запись успешно заменена!",
        reply_markup=get_table_menu_kb(table_name)
    )
    await state.set_state(DBStates.in_table)


@router.message(DBStates.in_table, F.text.startswith("Удалить"))

async def delete_row(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    eng_table_name = text.tables_name_reversed[table_name]

    # проверка доступна ли операция для таблицы
    if "delete_row" in text.tables_operations[eng_table_name]:
        await message.answer(
            "Выберите строку таблицы, которую хотите удалить. "
            "При выборе номера проверьте, что такая строчка существует!",
            reply_markup=get_delete_row_kb(table_name)
        )
        await state.set_state(DBStates.waiting_delete_row_number)
    else:
        await message.reply(
            "К сожалению, в данный момент данная операция для этой таблицы недоступна. "
            "Попробуйте позже",
            reply_markup=get_table_menu_kb(table_name)
        )


@router.message(DBStates.waiting_delete_row_number, F.text.isdecimal())
async def right_row_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']

    # запоминаем номер строчки
    await state.update_data(row_number=int(message.text))
    await message.reply(
        "Строчка выбрана. Вы уверены, что хотите удалить её?",
        reply_markup=get_yes_no_delete_row_kb(table_name)
    )
    await state.set_state(DBStates.waiting_delete_row_agree)


@router.message(DBStates.waiting_delete_row_number, ~F.text.isdecimal())
async def wrong_row_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    await message.reply(
        "Это не номер строки! Попробуйте ещё раз",
        reply_markup=get_delete_row_kb(table_name)
    )


@router.message(DBStates.waiting_delete_row_agree, F.text.lower() == "да")
async def yes_delete_row(message: types.Message, state: FSMContext):
    # название таблицы и номер строки для удаления
    data = await state.get_data()
    table_name = data['table_name']
    eng_table_name = text.tables_name_reversed[table_name]
    row_number = data['row_number']

    # удаляем строчку таблицы в БД
    conn.delete_from_table(eng_table_name, row_number)

    await message.reply(
        "Выбранная вами строчка успешно удалена из базы!",
        reply_markup=get_table_menu_kb(table_name)
    )
    await state.set_state(DBStates.in_table)


@router.message(DBStates.waiting_delete_row_agree, F.text.lower() == "нет")
async def no_delete_row(message: types.Message, state: FSMContext):
    # название таблицы
    data = await state.get_data()
    table_name = data['table_name']

    await message.reply(
        "Удаление отменено!",
        reply_markup=get_table_menu_kb(table_name)
    )
    await message.answer(
        "Выберите строку таблицы, которую хотите удалить. "
        "При выборе номера проверьте, что такая строчка существует!",
        reply_markup=get_delete_row_kb(table_name)
    )
    await state.set_state(DBStates.waiting_delete_row_number)


@router.message(DBStates.waiting_delete_row_agree, ~F.text.lower().in_(("да", "нет")))
async def wrong_delete_row(message: types.Message, state: FSMContext):
    # название таблицы
    data = await state.get_data()
    table_name = data['table_name']

    await message.reply(
        "Я вас не понимаю. Попробуйте ещё раз",
        reply_markup=get_yes_no_delete_row_kb(table_name)
    )

@router.message(DBStates.in_table, F.text.startswith("Очистить"))
async def clear_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    eng_table_name = text.tables_name_reversed[table_name]

    # проверка доступна ли операция для таблицы
    if "clear_table" in text.tables_operations[eng_table_name]:
        await message.answer(
            "Вы уверены, что хотите очистить таблицу? Отменить изменения не получится!",
            reply_markup=get_clear_table_kb(table_name)
        )
        await state.set_state(DBStates.waiting_clear_table)
    else:
        await message.reply(
            "К сожалению, в данный момент данная операция для этой таблицы недоступна. "
            "Попробуйте позже",
            reply_markup=get_table_menu_kb(table_name)
        )


@router.message(DBStates.waiting_clear_table, F.text.lower() == "да")
async def yes_clear_tables(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    eng_table_name = text.tables_name_reversed[table_name]

    # очитска таблицы в БД
    conn.clear_table(eng_table_name)

    await message.reply(
        "Выбранная вами таблица успешно очищена!",
        reply_markup=get_table_menu_kb(table_name)
    )
    await state.set_state(DBStates.in_table)


@router.message(DBStates.waiting_clear_table, F.text.lower() == "нет")
async def no_clear_tables(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    eng_table_name = text.tables_name_reversed[table_name]

    await message.reply(
        "Операция успешно отменена!",
        reply_markup=get_table_menu_kb(table_name)
    )
    await state.set_state(DBStates.in_table)


@router.message(DBStates.waiting_clear_table, ~F.text.lower().in_(("да", "нет")))
async def wrong_clear_tables(message: types.Message, state: FSMContext):
    data = await state.get_data()
    table_name = data['table_name']
    eng_table_name = text.tables_name_reversed[table_name]

    await message.reply(
        "Я вас не понимаю. Попробуйте ещё раз",
        reply_markup=get_clear_table_kb(table_name)
    )
    await state.set_state(DBStates.in_table)


@router.message(DBStates.db_exist, ~F.text.in_(text.all_commands))
async def not_a_command(message: types.Message):
    await message.reply("Я вас не понимаю! Воспользуйтесь вкладкой 'Меню'")
