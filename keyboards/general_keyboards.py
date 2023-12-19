from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_bot_info_kb():
    """Клавиатура для команды вывода информации о боте."""
    kb = InlineKeyboardBuilder()
    # кнопка с гитхабом бота
    kb.row(types.InlineKeyboardButton(
        text="GitHub бота",
        url="https://github.com/TwinkleBlisss/chemical-industry-bot/"
    ))
    # кнопка с тг-ссылкой на бота
    kb.row(types.InlineKeyboardButton(
        text="Телеграм бота",
        url="https://t.me/chemical_industry_bot"
    ))
    # кнопка с тг-ссылкой на первого админа
    """
    admin_id1 = 498450978
    chat_info = await bot.get_chat(admin_id1)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text="Админ 1",
            url=f"tg://user?id={admin_id1}"
        ))
    """
    kb.row(types.InlineKeyboardButton(
        text="Админ 1",
        url=f"https://t.me/YarovTimur"
    ))
    # кнопка с тг-ссылкой на второго админа
    """
    admin_id2 = 498450978  # пока нет информации об id Жени
    chat_info = await bot.get_chat(admin_id2)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text="Админ 2",
            url=f"https://t.me/krosha31"
        ))
    """
    kb.row(types.InlineKeyboardButton(
        text="Админ 2",
        url=f"https://t.me/krosha31"
    ))
    return kb.as_markup()


def get_random_kb():
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(
        text="Нажмите сюда",
        callback_data="random_value"
    ))
    return kb.as_markup()
