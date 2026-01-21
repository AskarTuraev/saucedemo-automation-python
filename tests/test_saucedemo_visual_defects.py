"""
Тест с внесенными визуальными дефектами для проверки работы Applitools Eyes
Этот тест должен быть запущен после создания baseline
"""
import pytest
from applitools.playwright import Target
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config import Config


@pytest.mark.visual_defects
@pytest.mark.regression
class TestSauceDemoVisualDefects:
    """
    Тестовый класс с внесенными визуальными дефектами
    Applitools Eyes должен обнаружить отличия от baseline
    """

    def test_e2e_checkout_flow_with_visual_defects(self, eyes_page, eyes, config):
        """
        E2E тест с визуальными дефектами для проверки детектирования изменений

        Внесенные дефекты:
        1. Login Page: Скрытие кнопки Login (display: none)
        2. Inventory Page: Изменение цвета фона первого товара + скрытие цены
        3. Cart Page: Изменение цвета кнопки Checkout + смещение layout
        4. Checkout Page: Скрытие поля First Name + изменение размера кнопки Continue

        Args:
            eyes_page: Playwright Page с открытой Eyes сессией
            eyes: Applitools Eyes инстанс
            config: Конфигурация проекта
        """
        page = eyes_page

        # ============================================================
        # ШАГ 1: Авторизация на странице Login (С ДЕФЕКТОМ)
        # ============================================================
        print("\n[STEP 1] Открытие страницы авторизации...")
        login_page = LoginPage(page)
        login_page.open()

        # Ожидание полной загрузки страницы
        page.wait_for_load_state("networkidle")

        print("[STEP 1] Выполнение авторизации (до внесения дефекта)...")
        login_page.login(config.TEST_USERNAME, config.TEST_PASSWORD)

        # Ожидание перехода на страницу inventory до возврата на login
        page.wait_for_url("**/inventory.html", timeout=5000)

        # Возвращаемся на страницу login для демонстрации дефекта
        print("[STEP 1] Возврат на страницу Login для внесения визуального дефекта...")
        login_page.open()
        page.wait_for_load_state("networkidle")

        # ВНЕСЕНИЕ ДЕФЕКТА 1: Скрытие кнопки Login
        print("[STEP 1] ⚠️  ВНЕСЕНИЕ ДЕФЕКТА 1: Скрытие кнопки Login")
        login_page.inject_login_visual_defects()

        # Небольшая задержка для применения стилей
        page.wait_for_timeout(500)

        # ВИЗУАЛЬНАЯ КОНТРОЛЬНАЯ ТОЧКА 1: Login Page (с дефектом)
        print("[STEP 1] Создание визуального снимка: Login Page (с дефектом)")
        eyes.check("Login Page", Target.window().fully())

        # Снова авторизуемся для продолжения теста
        print("[STEP 1] Повторная авторизация для продолжения теста...")
        page.goto(config.BASE_URL)
        page.wait_for_load_state("networkidle")
        login_page.login(config.TEST_USERNAME, config.TEST_PASSWORD)

        # ============================================================
        # ШАГ 2: Каталог товаров - Inventory Page (С ДЕФЕКТОМ)
        # ============================================================
        print("\n[STEP 2] Ожидание загрузки страницы каталога...")
        inventory_page = InventoryPage(page)

        # Ожидание загрузки страницы каталога
        page.wait_for_url("**/inventory.html")
        page.wait_for_load_state("networkidle")

        # Проверка что страница загружена
        assert inventory_page.is_page_loaded(), "Страница каталога не загружена"

        # ВНЕСЕНИЕ ДЕФЕКТА 2: Изменение цвета фона и скрытие цены
        print("[STEP 2] ⚠️  ВНЕСЕНИЕ ДЕФЕКТА 2: Красный фон первого товара + скрытие цены")
        inventory_page.inject_inventory_visual_defects()

        # Небольшая задержка для применения стилей
        page.wait_for_timeout(500)

        # ВИЗУАЛЬНАЯ КОНТРОЛЬНАЯ ТОЧКА 2: Inventory Page (с дефектом)
        print("[STEP 2] Создание визуального снимка: Inventory Page (с дефектом)")
        eyes.check("Inventory Page", Target.window().fully())

        # ============================================================
        # ШАГ 3: Добавление товара в корзину
        # ============================================================
        print("\n[STEP 3] Добавление товара 'Sauce Labs Backpack' в корзину...")
        inventory_page.add_item_to_cart_by_name("sauce-labs-backpack")

        # Проверка что товар добавлен
        cart_count = inventory_page.get_cart_items_count()
        print(f"[STEP 3] Количество товаров в корзине: {cart_count}")
        assert cart_count == "1", f"Ожидалось 1 товар в корзине, получено: {cart_count}"

        # ============================================================
        # ШАГ 4: Переход в корзину - Cart Page (С ДЕФЕКТОМ)
        # ============================================================
        print("\n[STEP 4] Переход в корзину...")
        inventory_page.go_to_cart()

        cart_page = CartPage(page)

        # Ожидание загрузки страницы корзины
        page.wait_for_url("**/cart.html")
        page.wait_for_load_state("networkidle")

        # Проверка что страница корзины загружена
        assert cart_page.is_page_loaded(), "Страница корзины не загружена"

        # ВНЕСЕНИЕ ДЕФЕКТА 3: Зеленая кнопка Checkout + смещение layout
        print("[STEP 4] ⚠️  ВНЕСЕНИЕ ДЕФЕКТА 3: Зеленая кнопка Checkout + смещение контейнера")
        cart_page.inject_cart_visual_defects()

        # Небольшая задержка для применения стилей
        page.wait_for_timeout(500)

        # ВИЗУАЛЬНАЯ КОНТРОЛЬНАЯ ТОЧКА 3: Cart Page (с дефектом)
        print("[STEP 4] Создание визуального снимка: Cart Page (с дефектом)")
        eyes.check("Cart Page", Target.window().fully())

        # ============================================================
        # ШАГ 5: Начало оформления заказа - Checkout Page (С ДЕФЕКТОМ)
        # ============================================================
        print("\n[STEP 5] Переход к оформлению заказа...")
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(page)

        # Ожидание загрузки страницы оформления заказа
        page.wait_for_url("**/checkout-step-one.html")
        page.wait_for_load_state("networkidle")

        # Проверка что страница оформления заказа загружена
        assert checkout_page.is_page_loaded(), "Страница оформления заказа не загружена"

        # ВНЕСЕНИЕ ДЕФЕКТА 4: Скрытие поля First Name + маленькая кнопка Continue
        print("[STEP 5] ⚠️  ВНЕСЕНИЕ ДЕФЕКТА 4: Скрытие First Name + уменьшение кнопки Continue")
        checkout_page.inject_checkout_visual_defects()

        # Небольшая задержка для применения стилей
        page.wait_for_timeout(500)

        # ВИЗУАЛЬНАЯ КОНТРОЛЬНАЯ ТОЧКА 4: Checkout Page (с дефектом)
        print("[STEP 5] Создание визуального снимка: Checkout Page - Step One (с дефектом)")
        eyes.check("Checkout Page - Step One", Target.window().fully())

        print("\n" + "="*80)
        print("VISUAL DEFECTS TEST COMPLETED")
        print("="*80)
        print("\nВнесенные визуальные дефекты:")
        print("  1. Login Page: Кнопка Login скрыта (display: none)")
        print("  2. Inventory Page: Красный фон первого товара + скрытая цена")
        print("  3. Cart Page: Зеленая кнопка Checkout + смещение layout на 100px")
        print("  4. Checkout Page: Скрытое поле First Name + маленькая кнопка Continue")
        print("\nОткройте Applitools Dashboard для анализа обнаруженных отличий.")
        print("Статус теста должен быть 'Unresolved' до ручного подтверждения изменений.")
        print("="*80 + "\n")
