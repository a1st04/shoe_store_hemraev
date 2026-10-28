-- =====================================================
-- Задание 1. Представления (VIEW)
-- =====================================================

DROP VIEW IF EXISTS v_orders_full;
DROP VIEW IF EXISTS v_products_with_stock;
DROP VIEW IF EXISTS v_user_stats;
DROP VIEW IF EXISTS v_simple;

-- VIEW 1. Полная информация о заказах
CREATE VIEW v_orders_full AS
SELECT o.order_id,
       o.order_date,
       u.last_name || ' ' || u.first_name ||
           COALESCE(' ' || u.middle_name, '') AS client_full_name,
       SUM(oi.quantity * oi.price) AS order_total
FROM orders o
INNER JOIN users       u  ON o.user_id  = u.user_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date, u.last_name, u.first_name, u.middle_name;

-- VIEW 2. Товары с остатками
CREATE VIEW v_products_with_stock AS
SELECT p.product_name,
       p.price,
       s.size_value,
       si.quantity_available
FROM stock_items si
INNER JOIN products p ON si.product_id = p.product_id
INNER JOIN sizes    s ON si.size_id    = s.size_id;

-- VIEW 3. Статистика по клиентам
CREATE VIEW v_user_stats AS
SELECT u.last_name || ' ' || u.first_name AS client_full_name,
       u.login,
       COUNT(o.order_id) AS orders_count
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.last_name, u.first_name, u.login;

-- Простое представление (для теста обновляемости)
CREATE VIEW v_simple AS
SELECT product_id, price FROM products;

-- =====================================================
-- Задание 2. Индексы
-- =====================================================

-- 5. Индекс на products.category
CREATE INDEX IF NOT EXISTS idx_products_category
    ON products(category);

-- 6. Индекс на orders.order_date
CREATE INDEX IF NOT EXISTS idx_orders_order_date
    ON orders(order_date);

-- 7. Индексы на внешние ключи
CREATE INDEX IF NOT EXISTS idx_orders_user_id
    ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_stock_items_product
    ON stock_items(product_id);
CREATE INDEX IF NOT EXISTS idx_stock_items_size
    ON stock_items(size_id);

-- 8. Составной индекс (два поля)
CREATE INDEX IF NOT EXISTS idx_products_manuf_category
    ON products(manufacturer, category);