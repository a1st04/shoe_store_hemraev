from src.app_functions import calc_discount, pluralize_items, format_full_name, get_client_tier

def run_tests():
    print("Запуск Unit-тестов...")
    
    # Тесты calc_discount
    assert calc_discount(1000, 10) == 900.0
    assert calc_discount(1000, 0) == 1000.0
    assert calc_discount(1000, 100) == 0.0
    assert calc_discount(1000, 150) == 0.0
    assert calc_discount(1000, -10) == 1000.0
    assert calc_discount(None, 10) == 0.0
    
    # Тесты pluralize_items
    assert pluralize_items(1) == "1 товар"
    assert pluralize_items(2) == "2 товара"
    assert pluralize_items(5) == "5 товаров"
    assert pluralize_items(21) == "21 товар"
    assert pluralize_items(22) == "22 товара"
    assert pluralize_items(11) == "11 товаров"
    assert pluralize_items(0) == "0 товаров"
    assert pluralize_items(None) == "0 товаров"
    
    # Тесты format_full_name
    assert format_full_name("иванов", "иван", "иванович") == "Иванов И.И."
    assert format_full_name("петров", "петр", "") == "Петров П."
    assert format_full_name(None, "сергей", "викторович") == "Аноним"
    assert format_full_name("сидоров", None, None) == "Аноним"
    
    # Тесты get_client_tier
    assert get_client_tier(4000) == "Новичок"
    assert get_client_tier(5000) == "Бронза"
    assert get_client_tier(25000) == "Серебро"
    assert get_client_tier(75000) == "Золото"
    assert get_client_tier(150000) == "Платина"
    assert get_client_tier(None) == "Без статуса"
    
    print("Все тесты пройдены успешно!")

if __name__ == "__main__":
    run_tests()