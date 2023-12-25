from aiogram.fsm.state import StatesGroup, State


class DBStates(StatesGroup):
    """Класс, реализующий состояния базы данных."""
    creating_db = State()
    db_exist = State()
    show_db = State()
    table_menu = State()
    in_table = State()
    waiting_add_row = State()
    waiting_update_row_number = State()
    waiting_update_row_data = State()
    waiting_delete_row_number = State()
    waiting_delete_row_agree = State()
    waiting_clear_table = State()


class ScanBarcode(StatesGroup):
    """Класс, реализующий состояния режима сканирования штрихкодов."""
    choosing_barcode_existance = State()
    waiting_for_new_photo = State()
    waiting_for_existing_photo = State()
    eurocube_found = State()
    waiting_for_add_photo = State()
    waiting_for_status = State()
    waiting_for_order_id = State()
    waiting_for_product = State()
