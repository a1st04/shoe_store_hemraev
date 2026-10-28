-- =====================================================
-- Задание 1. Простые JOIN
-- =====================================================

-- Запрос 1. Все заказы с ФИО клиента
SELECT o.order_id, o.order_date,
       u.last_name, u.first_name, u.middle_name
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id
ORDER BY o.order_id;

-- Запрос 2. Товарные позиции с названием модели и размером
SELECT si.stock_item_id,
       p.product_name,
       s.size_value,
       si.quantity_available
FROM stock_items si
INNER JOIN products p ON si.product_id = p.product_id
INNER JOIN sizes    s ON si.size_id    = s.size_id
ORDER BY si.stock_item_id;

-- Запрос 3. Заказы с ФИО клиента и названием товара
SELECT o.order_id,
       o.order_date,
       u.last_name || ' ' || u.first_name AS client,
       p.product_name,
       oi.quantity,
       oi.price
FROM orders o
INNER JOIN users       u  ON o.user_id        = u.user_id
INNER JOIN order_items oi ON o.order_id       = oi.order_id
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
ORDER BY o.order_id;

-- Запрос 4. Все пользователи и кол-во их заказов (LEFT JOIN)
SELECT u.user_id, u.last_name, u.first_name,
       o.order_id
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
ORDER BY u.user_id, o.order_id;

-- =====================================================
-- Задание 2. Базовые агрегатные функции
-- =====================================================

-- Запрос 5. Общее количество пользователей
SELECT COUNT(*) AS users_count FROM users;

-- Запрос 6. Средняя цена товаров
SELECT AVG(price) AS avg_price FROM products;

-- Запрос 7. Самый дорогой и самый дешёвый товар
SELECT MIN(price) AS min_price,
       MAX(price) AS max_price
FROM products;

-- Запрос 8. Общая выручка
SELECT SUM(quantity * price) AS revenue
FROM order_items;

-- =====================================================
-- Задание 3. Группировка GROUP BY
-- =====================================================

-- Запрос 9. Кол-во товаров по категориям
SELECT category, COUNT(*) AS products_count
FROM products
GROUP BY category
ORDER BY products_count DESC;

-- Запрос 10. Производители и средняя цена их товаров
SELECT manufacturer,
       AVG(price) AS avg_price
FROM products
GROUP BY manufacturer
ORDER BY avg_price DESC;

-- Запрос 11. ФИО и общая сумма заказов пользователя
SELECT u.user_id,
       u.last_name, u.first_name,
       COALESCE(SUM(oi.quantity * oi.price), 0) AS total
FROM users u
LEFT JOIN orders       o  ON u.user_id  = o.user_id
LEFT JOIN order_items  oi ON o.order_id = oi.order_id
GROUP BY u.user_id, u.last_name, u.first_name
ORDER BY total DESC;

-- Запрос 12. Продажи по моделям
SELECT p.product_name,
       SUM(oi.quantity) AS sold_pairs
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
GROUP BY p.product_name
ORDER BY sold_pairs DESC;

-- Запрос 13. Размер и кол-во товарных позиций в этом размере
SELECT s.size_value,
       COUNT(si.stock_item_id) AS stock_positions
FROM sizes s
LEFT JOIN stock_items si ON s.size_id = si.size_id
GROUP BY s.size_value
ORDER BY s.size_value;

-- =====================================================
-- Задание 4. HAVING
-- =====================================================

-- Запрос 14. Категории с более чем 3 моделями
SELECT category, COUNT(*) AS models_count
FROM products
GROUP BY category
HAVING COUNT(*) > 3;

-- Запрос 15. Клиенты с более чем 2 заказами
SELECT u.user_id, u.last_name, u.first_name,
       COUNT(o.order_id) AS orders_count
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.last_name, u.first_name
HAVING COUNT(o.order_id) > 2;

-- Запрос 16. Модели с суммой продаж > 100 000
SELECT p.product_name,
       SUM(oi.quantity * oi.price) AS total_sales
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
GROUP BY p.product_name
HAVING SUM(oi.quantity * oi.price) > 100000;

-- =====================================================
-- Задание 5. Комбинированный аналитический отчёт
-- =====================================================

-- Запрос 17. Топ-3 самых популярных размеров
SELECT s.size_value,
       SUM(oi.quantity) AS sold
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN sizes       s  ON si.size_id       = s.size_id
GROUP BY s.size_value
ORDER BY sold DESC
LIMIT 3;

-- Запрос 18. Пользователи без единого заказа
SELECT u.user_id, u.last_name, u.first_name
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id IS NULL;

-- Запрос 19. Средняя стоимость одного заказа
SELECT AVG(order_total) AS avg_order_value
FROM (
    SELECT o.order_id,
           SUM(oi.quantity * oi.price) AS order_total
    FROM orders o
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
) t;

-- Запрос 20. Производитель с наибольшей выручкой
SELECT p.manufacturer,
       SUM(oi.quantity * oi.price) AS revenue
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products    p  ON si.product_id    = p.product_id
GROUP BY p.manufacturer
ORDER BY revenue DESC
LIMIT 1;