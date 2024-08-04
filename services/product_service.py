import sqlite3

class ProductService:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_product(self, name, quantity, price):
        query = "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)"
        self.conn.execute(query, (name, quantity, price))
        self.conn.commit()

    def get_all_products(self):
        query = "SELECT * FROM products"
        cursor = self.conn.execute(query)
        products = cursor.fetchall()
        return products

    def update_product(self, product_id, name, quantity, price):
        query = "UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?"
        self.conn.execute(query, (name, quantity, price, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE id = ?"
        self.conn.execute(query, (product_id,))
        self.conn.commit()
