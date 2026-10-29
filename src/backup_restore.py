import sqlite3
import shutil
import os
from datetime import datetime

def backup_simple(db_path="db/shoe_store.sqlite"):
    """Бэкап через shutil (быстрый, но потенциально небезопасный при записи)"""
    backup_dir = "db/backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}.sqlite")
    
    shutil.copy(db_path, backup_path)
    print(f"Простой бэкап создан: {backup_path}")
    return backup_path

def backup_safe(db_path="db/shoe_store.sqlite"):
    """Безопасный бэкап через API SQLite"""
    backup_dir = "db/backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    backup_path = os.path.join(backup_dir, f"backup_safe_{timestamp}.sqlite")
    
    # Открываем соединение с основной базой
    with sqlite3.connect(db_path) as conn:
        # Создаем соединение с новой базой
        with sqlite3.connect(backup_path) as bck_conn:
            # Делаем снимок
            conn.backup(bck_conn)
            
    print(f"Безопасный бэкап создан: {backup_path}")
    return backup_path

def check_integrity(conn):
    """Проверка целостности базы через PRAGMA"""
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()[0]
    print(f"Результат integrity_check: {result}")
    return result

def restore(backup_path, target_path="db/shoe_store.sqlite"):
    """Восстановление базы из файла бэкапа"""
    # Важно: перед копированием все соединения с целевой БД должны быть закрыты
    print(f"Восстановление базы из {backup_path}...")
    shutil.copy(backup_path, target_path)
    print("Восстановление завершено.")

def get_db_stats(conn):
    """Сбор статистики базы"""
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA page_size;")
    page_size = cursor.fetchone()[0]
    
    cursor.execute("PRAGMA page_count;")
    page_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [t[0] for t in tables]
    
    stats = {
        "page_size": page_size,
        "page_count": page_count,
        "total_size_bytes": page_size * page_count,
        "tables": table_names
    }
    
    print("Статистика БД:", stats)
    return stats

def clear_old_logs(conn, days=30):
    """Очистка старых логов (таблица audit_log из Дня 11)"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM audit_log WHERE changed_at < date('now', ?)", (f"-{days} days",))
    deleted = cursor.rowcount
    conn.commit()
    print(f"Удалено старых логов: {deleted}")