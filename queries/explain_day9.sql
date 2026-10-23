-- 1. Поиск по индексированному полю — должен быть SEARCH ... USING INDEX
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE category = 'Кроссовки';

-- 2. Поиск по manufacturer (первое поле составного индекса)
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE manufacturer = 'Nike';

-- 3. JOIN orders + users (должны быть индексы)
EXPLAIN QUERY PLAN
SELECT * FROM orders o JOIN users u ON o.user_id = u.user_id;

-- 4. Проверка обновляемости простого VIEW (должно сработать)
UPDATE v_simple SET price = 100 WHERE product_id = 1;

-- 5. Проверка обновляемости сложного VIEW (должна быть ошибка)
UPDATE v_orders_full SET order_total = 0 WHERE order_id = 1;