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
    "/random"
    "/create_db",
    "/show_db",
    "/scan_barcode"
]

tables_name = {
        "barcodes": "Штрихкоды",
        "eurocube": "Еврокубы",
        "actions": "События",
        "product": "Товары",
        "order_list": "Товары в заказе",
        "order": "Заказы",
        "partner": "Клиенты"
}

tables_name_reversed = {
    "Штрихкоды": "barcodes",
    "Еврокубы": "eurocube",
    "События": "actions",
    "Товары": "product",
    "Товары в заказе": "order_list",
    "Заказы": "order",
    "Клиенты": "partner"
 }

operations_starts = [
    "Показать",
    "Внести",
    "Заменить",
    "Удалить",
    "Очистить"
]

tables_operations = {
        "barcodes": ["show_table", "delete_row"],
        "eurocube": ["show_table"],
        "actions": ["show_table", "delete_row", "clear_table"],
        "product": ["show_table"],
        "order_list": ["show_table"],
        "order": ["show_table"],
        "partner": ["show_table"]
}

chemicals = [
    "Азотная кислота",
    "Соляная кислота",
    "Серная кислота",
    "Ортофосфорная кислота",
    "Натр едкий"
]

tables_columns = {
        "barcodes": ("id", "eurocube_id", "last_check"),
        "eurocube": ("id", "date_of_manufacture", "usage_count"),
        "actions": ("id", "eurocube_id", "status", "action_date"),
        "product": ("id", "name", "danger_level", "cost_per_ton"),
        "order_list": ("order_id", "eurocube_id", "product_id", "eurocube_return"),
        "order": ("id", "partner_id", "cost", "order_date"),
        "partner": ("id", "name", "tin", "ogrn", "city", "street", "building")
}
