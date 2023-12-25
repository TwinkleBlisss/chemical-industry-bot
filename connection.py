from database.db_usage import Connection

conn = Connection('test')
conn.insert_into_table("actions", 1, "arrived")