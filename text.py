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

tables_name_reversed = {
    "Штрихкоды": "barcodes",
    "Еврокубы": "eurocubes",
    "События": "actions",
    "Товары": "products",
    "Товары в заказе": "order_list",
    "Заказы": "orders",
    "Клиенты": "partners"
 }

tables_operations = {
        "barcodes": ["show_table", "add_row", "update_row", "delete_row"],
        "eurocubes": ["show_table", "add_row", "update_row", "delete_row", "clear_table"],
        "actions": ["show_table", "add_row", "update_row", "delete_row"],
        "products": ["show_table", "add_row", "update_row", "delete_row"],
        "order_list": ["show_table", "add_row", "update_row", "delete_row"],
        "orders": ["show_table", "add_row", "update_row", "delete_row"],
        "partners": ["show_table", "add_row", "update_row", "delete_row"]
}

chemicals = [
    "Азотная кислота",
    "Соляная кислота",
    "Серная кислота",
    "Ортофосфорная кислота",
    "Натр едкий"
]
