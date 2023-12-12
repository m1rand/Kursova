import pypyodbc

class DatabaseFacade:
    def __init__(self, database_path):
        self.database_path = database_path

    def get_table_data(self, table_name):
        conn = pypyodbc.connect(f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={self.database_path}")
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name};")
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()

        conn.close()
        return columns, data

    def get_client_by_id(self, client_id):
        conn = pypyodbc.connect(f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={self.database_path}")
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM Клієнт WHERE Клієнт.ID = ?;", (client_id,))
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()

        conn.close()
        return columns, data

class DatabaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            cls._instance.initialize_database()
        return cls._instance

    def initialize_database(self):
        self.DATABASE_PATH = r"F:\TEX\qq.accdb"
        self.TABLE_NAMES = ['Замовлення', 'Клієнт', 'Менеджер', 'Меню', 'Оплата', 'Персонал']
        self.facade = DatabaseFacade(self.DATABASE_PATH)

    def get_table_data(self, table_name):
        return self.facade.get_table_data(table_name)

    def get_client_by_id(self, client_id):
        return self.facade.get_client_by_id(client_id)
