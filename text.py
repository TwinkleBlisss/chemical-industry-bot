"""
Все фразы бота.
"""

start_phrase = (
    "Здравствуйте!\n"
    "Я ваш бот для работы с еврокубами :)\n\n"
    "Откройте меню, чтобы увидеть список команд."
)

all_commands = [
    "/start",
    "/help",
    "bot_info",
    "/cancel",
    "/id",
    "/name",
    "/create_db",
    "/show_db",
    "/scan_barcode"
]

tables_name = {
        "barcodes": "Штрихкоды",
        "eurocubes": "Еврокубы",
        "actions": "События",
        "products": "Товары",
        "order_list": "Товары в заказе",
        "orders": "Заказы",
        "partners": "Клиенты"
    }

chemicals = [
    "Азотная кислота",
    "Соляная кислота",
    "Серная кислота",
    "Ортофосфорная кислота",
    "Натр едкий"
]