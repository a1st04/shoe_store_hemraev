-- Удаляем старые таблицы, если они есть
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS stock_items;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sizes;
DROP TABLE IF EXISTS users;

-- Таблица пользователей
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    email TEXT UNIQUE NOT NULL
);

-- Таблица размеров
CREATE TABLE sizes (
    size_id INTEGER PRIMARY KEY AUTOINCREMENT,
    size_name TEXT UNIQUE NOT NULL -- S, M, L, XL
);

-- Таблица товаров
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0)
);

-- Таблица остатков на складе (связка товара и размера)
CREATE TABLE stock_items (
    stock_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    size_id INTEGER NOT NULL,
    quantity_available INTEGER NOT NULL CHECK (quantity_available >= 0),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (size_id) REFERENCES sizes(size_id)
);

-- Таблица заказов
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Таблица позиций в заказе
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    size_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price REAL NOT NULL CHECK (price >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (size_id) REFERENCES sizes(size_id)
);

-- Заполняем справочники
INSERT INTO users (first_name, last_name, middle_name, email) VALUES
('Иван', 'Иванов', 'Иванович', 'ivan@example.com'),
('Петр', 'Петров', NULL, 'petr@example.com'),
('Анна', 'Сидорова', 'Викторовна', 'anna@example.com');

INSERT INTO sizes (size_name) VALUES ('S'), ('M'), ('L'), ('XL');

INSERT INTO products (product_name, price) VALUES
('Футболка', 1500.00),
('Джинсы', 4500.00),
('Кроссовки', 8000.00);

-- Заполняем склад (по 10 штук каждого размера для каждого товара)
INSERT INTO stock_items (product_id, size_id, quantity_available)
SELECT p.product_id, s.size_id, 10 
FROM products p, sizes s;

-- Создаем один тестовый заказ
INSERT INTO orders (user_id, order_date) VALUES (1, datetime('now'));
INSERT INTO order_items (order_id, product_id, size_id, quantity, price) 
VALUES (1, 1, 2, 2, 1500.00); -- Иван Иванов купил 2 футболки размера M