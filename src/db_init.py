"""Создание схемы БД shoe_store (SQLite)."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def drop_all_tables():
    conn = get_connection()
    for t in ["order_items", "orders", "stock_items",
              "products", "users", "sizes", "roles"]:
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    conn.commit()
    conn.close()


def create_tables():
    conn = get_connection()
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            role_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sizes (
            size_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            size_value REAL NOT NULL UNIQUE CHECK (size_value > 20 AND size_value < 50)
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name   TEXT NOT NULL,
            first_name  TEXT NOT NULL,
            middle_name TEXT,
            login       TEXT NOT NULL UNIQUE CHECK (length(login) BETWEEN 3 AND 20),
            role_id     INTEGER NOT NULL,
            FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            category      TEXT NOT NULL,
            subcategory   TEXT,
            manufacturer  TEXT NOT NULL,
            product_name  TEXT NOT NULL CHECK (length(trim(product_name)) > 0),
            image_path    TEXT,
            composition   TEXT,
            description   TEXT,
            price         REAL NOT NULL CHECK (price > 0 AND price < 1000000)
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_items (
            stock_item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id         INTEGER NOT NULL,
            size_id            INTEGER NOT NULL,
            quantity_available INTEGER NOT NULL DEFAULT 0 CHECK (quantity_available >= 0),
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
            FOREIGN KEY (size_id)    REFERENCES sizes(size_id)       ON DELETE RESTRICT
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            order_date TEXT NOT NULL,
            user_id    INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id      INTEGER NOT NULL,
            stock_item_id INTEGER NOT NULL,
            quantity      INTEGER NOT NULL CHECK (quantity > 0),
            price         REAL    NOT NULL CHECK (price > 0),
            FOREIGN KEY (order_id)      REFERENCES orders(order_id)           ON DELETE CASCADE,
            FOREIGN KEY (stock_item_id) REFERENCES stock_items(stock_item_id) ON DELETE RESTRICT
        )""")

    for sql in [
        "CREATE INDEX IF NOT EXISTS idx_users_role_id       ON users(role_id)",
        "CREATE INDEX IF NOT EXISTS idx_orders_user_id      ON orders(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_orders_order_date   ON orders(order_date)",
        "CREATE INDEX IF NOT EXISTS idx_stock_items_product ON stock_items(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_stock_items_size    ON stock_items(size_id)",
        "CREATE INDEX IF NOT EXISTS idx_products_category   ON products(category)",
        "CREATE INDEX IF NOT EXISTS idx_order_items_order   ON order_items(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_order_items_stock   ON order_items(stock_item_id)",
    ]:
        cur.execute(sql)

    conn.commit()
    conn.close()


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    drop_all_tables()
    create_tables()
    print(f"База создана: {DB_PATH}")


if __name__ == "__main__":
    main()