-- 1. Название товара, цена и цена со скидкой 20%
SELECT 
    product_name, 
    price, 
    calc_discount(price, 20) AS price_with_discount
FROM products;

-- 2. ФИО клиентов без отчества
SELECT 
    user_id,
    format_full_name(last_name, first_name, middle_name) AS full_name
FROM users;

-- 3. Количество проданных единиц с правильным склонением
SELECT 
    oi.order_id,
    SUM(oi.quantity) AS total_qty,
    pluralize_items(SUM(oi.quantity)) AS qty_text
FROM order_items oi
GROUP BY oi.order_id;

-- 4. Имя клиента и сумма его заказа со скидкой 10%
SELECT 
    u.first_name || ' ' || u.last_name AS client_name,
    SUM(oi.quantity * oi.price) AS total_sum,
    calc_discount(SUM(oi.quantity * oi.price), 10) AS total_with_discount
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.user_id;

-- 5. Аналитика: уровень клиента и стаж
SELECT 
    u.first_name || ' ' || u.last_name AS client_name,
    COALESCE(SUM(oi.quantity * oi.price), 0) AS total_spent,
    get_client_tier(COALESCE(SUM(oi.quantity * oi.price), 0)) AS tier,
    get_client_loyalty_days((SELECT MIN(order_date) FROM orders WHERE user_id = u.user_id)) AS loyalty_days
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id;