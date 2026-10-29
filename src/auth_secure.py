import sqlite3
import hashlib

def hash_password(password):
    """Возвращает хэш пароля SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(conn, login, password):
    """Регистрация пользователя с хэшированием пароля"""
    password_hash = hash_password(password)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (login, password_hash, role_id) VALUES (?, ?, ?)", 
        (login, password_hash, 3) # 3 - id роли reader по умолчанию
    )
    conn.commit()

def check_password(conn, login, password):
    """Проверка пароля и логирование попытки входа"""
    cursor = conn.cursor()
    
    # Получаем хэш из базы
    cursor.execute("SELECT password_hash FROM users WHERE login = ?", (login,))
    result = cursor.fetchone()
    
    if not result:
        _log_audit(conn, login, "fail")
        return False
        
    stored_hash = result[0]
    input_hash = hash_password(password)
    
    # Логируем результат
    status = "success" if stored_hash == input_hash else "fail"
    _log_audit(conn, login, status)
    
    return stored_hash == input_hash

def _log_audit(conn, login, status):
    """Внутренняя функция записи в audit"""
    cursor = conn.cursor()
    # Таблица login_audit должна быть создана: (id, login, status, login_time)
    cursor.execute(
        "INSERT INTO login_audit (login, status, login_time) VALUES (?, ?, datetime('now'))",
        (login, status)
    )
    conn.commit()