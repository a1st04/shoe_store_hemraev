-- =====================================================
-- Задание 1. Скалярные подзапросы
-- =====================================================

-- Запрос 1. Товары дороже средней цены
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;

-- Запрос 2. Клиент самого дорогого заказа
SELECT u.last_name, u.first_name
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id = (
    SELECT order_id
    FROM order_items
    GROUP BY order_id
    ORDER BY SUM(quantity * price) DESC
    LIMIT 1
);

-- =====================================================
-- Задание 2. IN / EXISTS
-- =====================================================

-- Запрос 3. Клиенты с хотя бы одним заказом (IN)
SELECT last_name
FROM users
WHERE user_id IN (SELECT user_id FROM orders);

-- Запрос 4. Клиенты без заказов (NOT EXISTS)
SELECT u.last_name, u.first_name
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.user_id
);

-- Запрос 5. Товары, которые ни разу не заказывали (NOT IN)
SELECT p.product_name
FROM products p
WHERE p.product_id NOT IN (
    SELECT si.product_id
    FROM order_items oi
    INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
);

-- =====================================================
-- Задание 3. Ранжирование (оконные функции)
-- =====================================================

-- Запрос 6. Ранжирование клиентов по сумме заказов
SELECT u.user_id, u.last_name,
       COALESCE(SUM(oi.quantity * oi.price), 0) AS total,
       RANK() OVER (
           ORDER BY COALESCE(SUM(oi.quantity * oi.price), 0) DESC
       ) AS rnk
FROM users u
LEFT JOIN orders       o  ON u.user_id  = o.user_id
LEFT JOIN order_items  oi ON o.order_id = oi.order_id
GROUP BY u.user_id, u.last_name
ORDER BY rnk;

-- Запрос 7. Порядковый номер заказа клиента (от старых к новым)
SELECT o.order_id, o.user_id, u.last_name, o.order_date,
       ROW_NUMBER() OVER (
           PARTITION BY o.user_id
           ORDER BY o.order_date
       ) AS rn
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id
ORDER BY o.user_id, o.order_date;

-- Запрос 8. Нумерация товаров в категории по убыванию цены
SELECT p.category, p.product_name, p.price,
       ROW_NUMBER() OVER (
           PARTITION BY p.category
           ORDER BY p.price DESC
       ) AS rn
FROM products p
ORDER BY p.category, rn;

-- Запрос 9. Самый дорогой товар в каждой категории (топ-1 через FROM-подзапрос)
SELECT category, product_name, price
FROM (
    SELECT p.category, p.product_name, p.price,
           ROW_NUMBER() OVER (
               PARTITION BY p.category
               ORDER BY p.price DESC
           ) AS rn
    FROM products p
) t
WHERE rn = 1
ORDER BY category;

-- =====================================================
-- Задание 4. Нарастающие итоги и LAG
-- =====================================================

-- Запрос 10. Накопительная сумма заказов по датам
SELECT o.order_id,
       o.order_date,
       SUM(oi.quantity * oi.price) AS order_total,
       SUM(SUM(oi.quantity * oi.price)) OVER (
           ORDER BY o.order_date
       ) AS running_total
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date
ORDER BY o.order_date;

-- Запрос 11. Дата текущего и предыдущего заказа клиента + разница в днях
SELECT o.user_id,
       o.order_id,
       o.order_date AS curr_date,
       LAG(o.order_date) OVER (
           PARTITION BY o.user_id
           ORDER BY o.order_date
       ) AS prev_date,
       julianday(o.order_date) - julianday(
           LAG(o.order_date) OVER (
               PARTITION BY o.user_id
               ORDER BY o.order_date
           )
       ) AS days_diff
FROM orders o
ORDER BY o.user_id, o.order_date;