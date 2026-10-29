import sqlite3

# Словарь прав доступа
PERMISSIONS = {
    "admin_db": ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"],
    "developer": ["SELECT", "INSERT", "UPDATE"],
    "reader": ["SELECT"]
}

def check_permission(conn, user_id, action):
    """
    Проверяет, разрешено ли пользователю с user_id выполнять действие action.
    Возвращает True или False.
    """
    cursor = conn.cursor()
    
    # 1. Получаем роль пользователя
    cursor.execute("SELECT role_id FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    
    if not result:
        return False
        
    role_id = result[0]
    
    # 2. Получаем название роли
    cursor.execute("SELECT name FROM roles WHERE id = ?", (role_id,))
    role_result = cursor.fetchone()
    
    if not role_result:
        return False
        
    role_name = role_result[0]
    
    # 3. Проверяем наличие действия в словаре
    allowed_actions = PERMISSIONS.get(role_name, [])
    
    return action.upper() in allowed_actions

# Тестирование (можно запустить отдельно)
if __name__ == "__main__":
    conn = sqlite3.connect("db/shoe_store.sqlite")
    
    # Предположим, в базе есть пользователь reader с id=2 и admin с id=1
    print("Проверка для reader (id=2) на DELETE:", check_permission(conn, 2, "DELETE")) # Должно быть False
    print("Проверка для admin (id=1) на DELETE:", check_permission(conn, 1, "DELETE")) # Должно быть True
    
    conn.close()