import sqlite3
from backup_restore import backup_safe, check_integrity, get_db_stats, clear_old_logs

def run_maintenance():
    conn = sqlite3.connect("db/shoe_store.sqlite")
    
    try:
        print("--- Запуск обслуживания базы ---")
        
        # 1. Проверка целостности
        integrity = check_integrity(conn)
        
        # 2. Бэкап (только если база здорова)
        if integrity == "ok":
            backup_safe()
        
        # 3. Статистика
        get_db_stats(conn)
        
        # 4. Очистка логов
        clear_old_logs(conn, days=30)
        
        print("--- Обслуживание завершено ---")
    finally:
        conn.close()

if __name__ == "__main__":
    run_maintenance()