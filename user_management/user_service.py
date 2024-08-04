import sqlite3

class UserService:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_user_table()

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        self.conn.execute(query, (username, password))
        self.conn.commit()

    def get_user(self, username):
        query = "SELECT * FROM users WHERE username = ?"
        cursor = self.conn.execute(query, (username,))
        return cursor.fetchone()
