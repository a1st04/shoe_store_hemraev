import sqlite3
from app_functions import calc_discount, pluralize_items, format_full_name, get_client_tier, get_client_loyalty_days

def register_functions(conn):
    """
    Регистрирует Python-функции как SQL-функции в текущем подключении.
    """
    conn.create_function("calc_discount", 2, calc_discount)
    conn.create_function("pluralize_items", 1, pluralize_items)
    conn.create_function("format_full_name", 3, format_full_name)
    conn.create_function("get_client_tier", 1, get_client_tier)
    conn.create_function("get_client_loyalty_days", 1, get_client_loyalty_days)
    print("Функции успешно зарегистрированы в SQLite.")

if __name__ == "__main__":
    # Запускаем этот скрипт, чтобы проверить регистрацию
    conn = sqlite3.connect('shop.db')
    register_functions(conn)
    
    # Быстрая проверка прямо в консоли
    cursor = conn.cursor()
    cursor.execute("SELECT calc_discount(1000, 15)")
    print("Результат calc_discount:", cursor.fetchone()[0])
    
    cursor.execute("SELECT pluralize_items(23)")
    print("Результат pluralize_items:", cursor.fetchone()[0])
    
    cursor.execute("SELECT format_full_name('иванов', 'иван', 'сергеевич')")
    print("Результат format_full_name:", cursor.fetchone()[0])
    
    conn.close()