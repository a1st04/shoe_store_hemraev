"""Заполнение тестовыми данными."""
from db_init import get_connection


def seed_all():
    conn = get_connection()
    cur = conn.cursor()

    cur.executemany("INSERT INTO roles(role_name) VALUES (?)",
                    [("администратор",), ("менеджер",), ("авторизованный пользователь",)])

    cur.executemany(
        "INSERT INTO users(last_name, first_name, middle_name, login, role_id) VALUES (?,?,?,?,?)",
        [("Иванов","Иван","Иванович","ivanov",1),
         ("Петров","Пётр",None,"petrov",2),
         ("Сидорова","Анна","Сергеевна","sidorova",3)])

    cur.executemany("INSERT INTO sizes(size_value) VALUES (?)",
                    [(36,), (37,), (38,), (39,), (40,)])

    cur.executemany(
        """INSERT INTO products(category, subcategory, manufacturer, product_name,
                                image_path, composition, description, price)
           VALUES (?,?,?,?,?,?,?,?)""",
        [("Кроссовки","Бег","Nike","Air Zoom",None,"текстиль","лёгкие",8990),
         ("Кроссовки","Баскетбол","Adidas","Hoops",None,"кожа","прочные",9990),
         ("Туфли","Классика","Ecco","City",None,"кожа","офисные",12990),
         ("Ботинки","Зима","Timberland","6-inch",None,"кожа","тёплые",15990),
         ("Сандалии","Лето","Rieker","Sand",None,"текстиль","лёгкие",3990)])

    stock = [(1,1,10),(1,2,15),(2,3,8),(2,4,12),(3,1,5),
             (3,2,7),(4,4,20),(4,5,9),(5,3,30),(5,5,25)]
    cur.executemany(
        "INSERT INTO stock_items(product_id, size_id, quantity_available) VALUES (?,?,?)",
        stock)

    cur.executemany("INSERT INTO orders(order_date, user_id) VALUES (?,?)",
                    [("2024-01-10",1),("2024-02-15",2),("2024-03-20",1)])

    cur.executemany(
        "INSERT INTO order_items(order_id, stock_item_id, quantity, price) VALUES (?,?,?,?)",
        [(1,1,2,8990),(1,3,1,9990),
         (2,5,1,12990),(2,7,3,15990),
         (3,9,2,3990),(3,10,1,3990)])

    conn.commit()
    conn.close()
    print("Данные загружены")


if __name__ == "__main__":
    seed_all()