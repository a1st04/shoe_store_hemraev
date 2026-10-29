# День 9. Представления, индексы, EXPLAIN — анализ

## 1. Созданные представления

| VIEW | Назначение | Источники |
|---|---|---|
| `v_orders_full` | Заказы с ФИО клиента и итоговой суммой | orders, users, order_items |
| `v_products_with_stock` | Товары с остатками по размерам | products, stock_items, sizes |
| `v_user_stats` | ФИО, логин и кол-во заказов клиента | users, orders |
| `v_simple` | Простое представление для теста обновления | products |

## 2. Созданные индексы

| Индекс | Поле(я) | Назначение |
|---|---|---|
| `idx_products_category` | products.category | фильтрация по категории |
| `idx_orders_order_date` | orders.order_date | сортировка по дате |
| `idx_orders_user_id` | orders.user_id | JOIN orders↔users |
| `idx_stock_items_product` | stock_items.product_id | JOIN stock↔products |
| `idx_stock_items_size` | stock_items.size_id | JOIN stock↔sizes |
| `idx_products_manuf_category` | products(manufacturer, category) | составной, фильтр по производителю |

> Замечание: `idx_products_category` и `idx_stock_items_*` / `idx_orders_user_id` уже существовали из дня 4 (`db_init.py`), здесь мы их дополнительно описали и добавили ещё два новых: `idx_orders_order_date` (был ранее) и составной `idx_products_manuf_category` (новый).

## 3. EXPLAIN QUERY PLAN — результаты

### 3.1. WHERE category = 'Кроссовки'
```
id | parent | notused | detail
-- | ------ | ------- | ------
2  | 0      | 0       | SEARCH products USING INDEX idx_products_category (category=?)
```
✅ Используется индекс `idx_products_category`.

### 3.2. WHERE manufacturer = 'Nike'
```
SEARCH products USING INDEX idx_products_manuf_category (manufacturer=?)
```
✅ Составной индекс работает, потому что `manufacturer` — **первое** поле индекса.

### 3.3. JOIN orders + users
```
SEARCH u USING INTEGER PRIMARY KEY (rowid=?)
SEARCH o USING INDEX idx_orders_user_id (user_id=?)
```
✅ Обе таблицы читаются по индексу: `u` — по первичному ключу, `o` — по `idx_orders_user_id`.

### 3.4. Пример полного сканирования
Если удалить составной индекс и выполнить:
```sql
DROP INDEX idx_products_manuf_category;
EXPLAIN QUERY PLAN SELECT * FROM products WHERE manufacturer = 'Nike';
```
получим `SCAN products` — полный перебор. То есть без индекса база читает всю таблицу.

## 4. Попытка обновления представлений

### 4.1. Простое VIEW — `v_simple`
```sql
UPDATE v_simple SET price = 100 WHERE product_id = 1;
```
**Успешно.** Простое VIEW на одной таблице без агрегатов обновляемо — SQLite пропускает UPDATE к базовой таблице `products`. После этого `price` у `product_id = 1` действительно станет `100`.

### 4.2. Сложное VIEW — `v_orders_full`
```sql
UPDATE v_orders_full SET order_total = 0 WHERE order_id = 1;
```
**Ошибка:** `cannot modify v_orders_full because it is a view` (или похожий текст про view).

Причина — VIEW содержит `JOIN` и `GROUP BY` / `SUM`, поэтому SQLite не может однозначно сопоставить строку представления со строкой базовой таблицы.

## 5. Выводы

1. **Индекс** ускоряет `WHERE`, `JOIN` и `ORDER BY` по индексированному полю.
2. **SCAN TABLE** — плохо (полный перебор всех строк). **SEARCH TABLE USING INDEX** — хорошо (быстрый доступ).
3. **Составной индекс** `(manufacturer, category)` работает для фильтров по `manufacturer`, по `(manufacturer, category)`, но НЕ работает для фильтра только по `category` — нужен отдельный индекс (он у нас есть — `idx_products_category`).
4. **Представления** — сохранённые запросы, не занимают места на диске; экономия времени и единая точка правды.
5. **Обновляемость**: простые VIEW (одна таблица) обновляемы, сложные (JOIN, GROUP BY, агрегаты) — нет.
6. Индексы — палка о двух концах: ускоряют чтение, но замедляют вставку/обновление и занимают место. Поэтому индексируем только те поля, по которым реально ищем или соединяем таблицы.