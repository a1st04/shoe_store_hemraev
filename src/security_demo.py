import sqlite3

def vulnerable_login(conn, login):
    """Уязвимый запрос через f-строку"""
    cursor = conn.cursor()
    # ОПАСНО: данные пользователя вставляются прямо в строку
    cursor.execute(f"SELECT * FROM users WHERE login = '{login}'")
    return cursor.fetchall()

def secure_login(conn, login):
    """Безопасный параметризованный запрос"""
    cursor = conn.cursor()
    # БЕЗОПАСНО: данные передаются отдельно
    cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
    return cursor.fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect("db/shoe_store.sqlite")
    
    print("--- Демонстрация уязвимости ---")
    print("Поиск ivanov (нормально):", len(vulnerable_login(conn, "ivanov")))
    print("Взлом ' OR '1'='1 (уязвимый):", len(vulnerable_login(conn, "' OR '1'='1")))
    
    print("\n--- Демонстрация защиты ---")
    print("Поиск ' OR '1'='1 (защищенный):", len(secure_login(conn, "' OR '1'='1")))
    
    conn.close()