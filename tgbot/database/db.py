import sqlite3


class Database:
    def __init__(self, path_to_db):
        self.path_to_db = path_to_db
    
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)
    
    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        
        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data
    
    def create_tables(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                full_name TEXT NULL,
                username TEXT NULL,
                date_of_purchase DATE NULL
                );
    """
        self.execute(sql, commit=True)
    
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())
    
    def add_user(self, user_id: int, full_name: str, username):
        existing_user = self.execute("SELECT * FROM users WHERE telegram_id = ?", (user_id,),
                                     fetchone=True)
        if not existing_user:
            sql = """
                INSERT INTO users(telegram_id, full_name, username) VALUES(?, ?, ?)
                """
            self.execute(sql, parameters=(user_id, full_name, username), commit=True)
    
    def get_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def select_all_users(self):
        sql = "SELECT telegram_id FROM users"
        return self.execute(sql, fetchall=True)
    
    def select_users(self):
        sql = "SELECT * FROM users"
        return self.execute(sql, fetchall=True)
    
    def update_date_of_purchase(self, user_id, date_of_purchase):
        sql = f"""
            UPDATE users SET date_of_purchase=? WHERE telegram_id=?
            """
        return self.execute(sql, parameters=(date_of_purchase, user_id), commit=True)


db = Database(path_to_db="tgbot/database/users.db3")
db.create_tables()
