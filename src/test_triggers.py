import sqlite3
import os

def run_tests():
    db_path = os.path.join('db', 'shoe_store.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== Тест 1: Списание остатков при добавлении в заказ ===")
    # Получаем текущий остаток товара со ID 1
    cursor.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = 1")
    old_stock = cursor.fetchone()[0]
    
    # Создаем заказ и добавляем в него товар
    cursor.execute("INSERT INTO orders (user_id, order_date) VALUES (1, datetime('now'))")
    order_id = cursor.lastrowid
    cursor.execute("INSERT INTO order_items (order_id, stock_item_id, quantity) VALUES (?, 1, 2)", (order_id,))
    conn.commit()
    
    # Проверяем, уменьшился ли остаток
    cursor.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = 1")
    new_stock = cursor.fetchone()[0]
    print(f"Остаток до: {old_stock}, после: {new_stock}. Списано корректно: {new_stock == old_stock - 2}")
    
    print("\n=== Тест 2: Попытка удалить пользователя с активным заказом ===")
    try:
        cursor.execute("DELETE FROM users WHERE user_id = 1")
        conn.commit()
        print("ОШИБКА: Пользователь удалился, триггер не сработал!")
    except sqlite3.IntegrityError as e:
        print(f"ОШИБКА триггера поймана: {e}")
    except sqlite3.DatabaseError as e:
        print(f"ОШИБКА триггера (ABORT) поймана: {e}")
    
    conn.close()

if __name__ == "__main__":
    run_tests()