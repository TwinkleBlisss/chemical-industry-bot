from database.db_usage import Connection

conn = Connection('test')

# conn.clear_table("actions")
# conn.clear_table("barcodes")
# conn.clear_table("eurocube")
# conn.clear_table("product")
# conn.clear_table("order")
# conn.clear_table("partner")

# заполняем таблицу химикатов
# product(name, danger_level, cost_per_ton)
# conn.insert_into_table("product", "Азотная кислота", 1, 10000)
# conn.insert_into_table("product", "Соляная кислота", 2, 25000)
# conn.insert_into_table("product", "Серная кислота1", 3, 50000)
# conn.insert_into_table("product", "Ортофосф. кисл.", 3, 45000)
# conn.insert_into_table("product", "Натр едкий C256", 2, 30000)

# заполняем таблицу партнеров
# partner(name, tin, ogrn, city, street, building)
# conn.insert_into_table("partner", "Рогокоп", 23487, 111, "Бор", "Птичья", 5)
# conn.insert_into_table("partner", "Вандекс", 62956, 112, "Бор", "Трудна", 7)
# conn.insert_into_table("partner", "HomeBrr", 92312, 113, "Бор", "Лесная", 2)

# заполняем таблицу заказов
# "order"(partner_id, cost, order_date)
# conn.insert_into_table("order", 4, 200000, "2023-10-01")
# conn.insert_into_table("order", 5, 135000, "2023-12-17")
# conn.insert_into_table("order", 6, 500000, "2023-12-20")

# заполняем таблицу событий
# их лучше заполнить через сканирование штрихкодов
# actions(eurocube_id, status)
# conn.insert_into_table("actions", 5, "arrived")
# conn.insert_into_table("actions", 6, "arrived")
# conn.insert_into_table("actions", 7, "arrived")
# conn.insert_into_table("actions", 8, "arrived")
