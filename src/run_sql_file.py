"""Запуск SQL-файла и печать результата каждого запроса."""
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "db" / "shoe_store.sqlite"
sql_file = Path(sys.argv[1])

sql_text = sql_file.read_text(encoding="utf-8")
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

statements = [s.strip() for s in sql_text.split(";") if s.strip()]

for i, stmt in enumerate(statements, 1):
    print(f"\n===== ЗАПРОС {i} =====")
    print(stmt.splitlines()[0][:80])
    try:
        cur = conn.execute(stmt)
        rows = cur.fetchall()
        if rows:
            print(" | ".join(rows[0].keys()))
            for r in rows[:15]:
                print(" | ".join(str(v) for v in r))
            if len(rows) > 15:
                print(f"... всего {len(rows)} строк")
        else:
            print("(нет строк)")
    except sqlite3.Error as e:
        print("ОШИБКА:", e)

conn.close()