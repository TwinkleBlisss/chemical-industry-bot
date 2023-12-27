import psycopg2
import psycopg2.sql as sql
import os



class Connection:
    def __init__(self, database_name: str):
        try:
            self.conn = psycopg2.connect(dbname=database_name, user='postgres', password='0793', host='127.0.0.1')
            self.cursor = self.conn.cursor()
            self.conn.set_session(autocommit=True)
            # with open("database/sql/init_db.sql") as f:
            #     self.cursor.execute(f.read())
            #     self.conn.commit()
            #
            # with open("database/sql/create_all_tables.sql") as f:
            #     self.cursor.execute(f.read())
            #     self.conn.commit()
            #
            # # self.cursor.callproc("create_all_tables", [])
            # # self.conn.commit()
            #
            # with open("database/sql/requests.sql") as f:
            #     self.cursor.execute(f.read())
            #     self.conn.commit()
            #
            # with open("database/sql/get_all_tables.sql") as f:
            #     self.cursor.execute(f.read())
            #     self.conn.commit()
            #
            # with open("database/sql/clear_all_tables.sql") as f:
            #     self.cursor.execute(f.read())
            #     self.conn.commit()
            #
            # with open("database/sql/delete_all_tables.sql") as f:
            #     self.cursor.execute(f.read())
            #     self.conn.commit()
            #
            # with open("database/sql/update_all_tables.sql") as f:
            #     self.cursor.execute(f.read())
            #     self.conn.commit()

        except:
            raise RuntimeError('Can`t establish connection to database')


    def create_db(self, database_name: str):
        self.cursor.callproc("create_db", [database_name])

    def create_all_tables(self):
        self.cursor.callproc('create_all_tables', ())

    def get_table(self, table_name: str) -> list:
        self.cursor.callproc(f'get_{table_name}', ())
        return self.cursor.fetchall()

    def insert_into_table(self, table_name: str, *args):
        self.cursor.callproc(f'add_{table_name}', args)
        self.conn.commit()

    def add_action(self, id: int, text: str):
        self.cursor.callproc("add_actions", [id, sql.Identifier(text)])
        self.conn.commit()

    def clear_table(self, table_name: str):
        self.cursor.callproc(f'clear_{table_name}', ())

    def update_table(self, table_name: str, *args):
        self.cursor.callproc(f'update_{table_name}', args)

    def delete_from_table(self, table_name: str, *args):
        self.cursor.callproc(f'delete_from_{table_name}', args)

    def scan_barcode(self, barcode_id: int) -> list:
        self.cursor.callproc('scan_barcode', [barcode_id])
        return self.cursor.fetchall()

    def get_order(self, order_id: int) -> int:
        self.cursor.callproc('get_order', [order_id])
        return self.cursor.fetchall()

    def get_product_id(self, name: str) -> int:
        self.cursor.callproc('get_product_id', [name])
        return self.cursor.fetchall()

    def delete_products(self, name: str):
        self.cursor.callproc('delete_product', [name])

