import sqlite3
from datetime import datetime

# --- БЛОК 1: Пользовательские функции (UDF) ---

def calc_discount(price, discount_percent):
    if price is None or discount_percent is None:
        return 0.0
    if discount_percent < 0:
        discount_percent = 0
    if discount_percent > 100:
        discount_percent = 100
    return round(price - (price * discount_percent / 100), 2)

def pluralize_items(count):
    if count is None:
        return "0 товаров"
    count = abs(int(count))
    
    if 11 <= (count % 100) <= 14:
        return f"{count} товаров"
    
    last_digit = count % 10
    if last_digit == 1:
        return f"{count} товар"
    elif 2 <= last_digit <= 4:
        return f"{count} товара"
    else:
        return f"{count} товаров"

def format_full_name(last, first, middle):
    if not last or not first:
        return "Аноним"
    
    last = last.strip().title()
    first = first.strip().title()
    
    if middle and middle.strip():
        middle_initial = middle.strip()[0].upper() + "."
        return f"{last} {first[0]}.{middle_initial}"
    else:
        return f"{last} {first[0]}."

def get_client_tier(total_spent):
    if total_spent is None or total_spent < 0:
        return "Без статуса"
    if total_spent < 5000:
        return "Новичок"
    if total_spent < 20000:
        return "Бронза"
    if total_spent < 50000:
        return "Серебро"
    if total_spent < 100000:
        return "Золото"
    return "Платина"

def get_client_loyalty_days(first_order_date_str):
    if not first_order_date_str:
        return 0
    try:
        first_date = datetime.strptime(first_order_date_str, "%Y-%m-%d")
        delta = datetime.now() - first_date
        return delta.days
    except ValueError:
        return 0

# --- БЛОК 2: Эмуляция процедур (Транзакции) ---

def place_order(conn, user_id, product_id, size_id, quantity):
    try:
        cursor = conn.cursor()
        
        # 1. Проверка пользователя
        cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            return False
            
        # 2. Поиск позиции на складе
        cursor.execute("SELECT stock_item_id, quantity_available FROM stock_items WHERE product_id = ? AND size_id = ?", (product_id, size_id))
        stock_item = cursor.fetchone()
        if not stock_item:
            return False
            
        stock_item_id, available_qty = stock_item
        
        # 3. Проверка остатка
        if available_qty < quantity:
            print("Ошибка: Недостаточно товара на складе.")
            return False
            
        # 4. Получение цены товара
        cursor.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
        price = cursor.fetchone()[0]
        
        # 5. Вставка в orders
        cursor.execute("INSERT INTO orders (user_id, order_date) VALUES (?, ?)", (user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        order_id = cursor.lastrowid
        
        # 6. Вставка в order_items
        cursor.execute("INSERT INTO order_items (order_id, product_id, size_id, quantity, price) VALUES (?, ?, ?, ?, ?)", 
                       (order_id, product_id, size_id, quantity, price))
        
        # 7. Списание со склада
        cursor.execute("UPDATE stock_items SET quantity_available = quantity_available - ? WHERE stock_item_id = ?", 
                       (quantity, stock_item_id))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Транзакция отменена: {e}")
        return False

def cancel_order(conn, order_id):
    try:
        cursor = conn.cursor()
        
        # 1. Проверка заказа
        cursor.execute("SELECT order_id FROM orders WHERE order_id = ?", (order_id,))
        if not cursor.fetchone():
            return False
            
        # 2. Получение позиций заказа
        cursor.execute("SELECT product_id, size_id, quantity FROM order_items WHERE order_id = ?", (order_id,))
        items = cursor.fetchall()
        
        # 3. Возврат на склад
        for item in items:
            product_id, size_id, quantity = item
            cursor.execute("UPDATE stock_items SET quantity_available = quantity_available + ? WHERE product_id = ? AND size_id = ?", 
                           (quantity, product_id, size_id))
        
        # 4. Удаление позиций и заказа
        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Ошибка отмены: {e}")
        return False