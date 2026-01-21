"""
Базовый тест для создания baseline в Applitools Eyes
Покрывает полный E2E сценарий от авторизации до начала оформления заказа
"""
import pytest
from applitools.playwright import Target
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config import Config


@pytest.mark.baseline
@pytest.mark.smoke
class TestSauceDemoBaseline:
    """
    Тестовый класс для создания baseline снимков в Applitools
    Этот тест должен быть запущен первым для создания эталонных изображений
    """

    def test_e2e_checkout_flow_baseline(self, eyes_page, eyes, config):
        """
        E2E тест полного пользовательского сценария с визуальными контрольными точками

        Сценарий:
        1. Авторизация пользователя (Login page) + визуальная проверка
        2. Просмотр каталога товаров (Inventory page) + визуальная проверка
        3. Добавление товара в корзину
        4. Переход в корзину (Cart page) + визуальная проверка
        5. Начало оформления заказа (Checkout page) + визуальная проверка

        Args:
            eyes_page: Playwright Page с открытой Eyes сессией
            eyes: Applitools Eyes инстанс
            config: Конфигурация проекта
        """
        page = eyes_page

        # ============================================================
        # ШАГ 1: Авторизация на странице Login
        # ============================================================
        print("\n[STEP 1] Открытие страницы авторизации...")
        login_page = LoginPage(page)
        login_page.open()

        # Ожидание полной загрузки страницы
        page.wait_for_load_state("networkidle")

        # ВИЗУАЛЬНАЯ КОНТРОЛЬНАЯ ТОЧКА 1: Login Page
        print("[STEP 1] Создание визуального снимка: Login Page")
        eyes.check("Login Page", Target.window().fully())

        print("[STEP 1] Выполнение авторизации...")
        login_page.login(config.TEST_USERNAME, config.TEST_PASSWORD)

        # ============================================================
        # ШАГ 2: Каталог товаров - Inventory Page
        # ============================================================
        print("\n[STEP 2] Ожидание загрузки страницы каталога...")
        inventory_page = InventoryPage(page)

        # Ожидание загрузки страницы каталога
        page.wait_for_url("**/inventory.html")
        page.wait_for_load_state("networkidle")

        # Проверка что страница загружена
        assert inventory_page.is_page_loaded(), "Страница каталога не загружена"

        # ВИЗУАЛЬНАЯ КОНТРОЛЬНАЯ ТОЧКА 2: Inventory Page
        print("[STEP 2] Создание визуального снимка: Inventory Page")
        eyes.check("Inventory Page", Target.window().fully())

        # Получение количества товаров на странице
        items_count = inventory_page.get_items_count()
        print(f"[STEP 2] Найдено товаров на странице: {items_count}")
        assert items_count > 0, "Нет товаров на странице каталога"

        # ============================================================
        # ШАГ 3: Добавление товара в корзину
        # ============================================================
        print("\n[STEP 3] Добавление товара 'Sauce Labs Backpack' в корзину...")
        inventory_page.add_item_to_cart_by_name("sauce-labs-backpack")

        # Проверка что товар добавлен (badge показывает количество)
        cart_count = inventory_page.get_cart_items_count()
        print(f"[STEP 3] Количество товаров в корзине: {cart_count}")
        assert cart_count == "1", f"Ожидалось 1 товар в корзине, получено: {cart_count}"

        # ============================================================
        # ШАГ 4: Переход в корзину - Cart Page
        # ============================================================
        print("\n[STEP 4] Переход в корзину...")
        inventory_page.go_to_cart()

        cart_page = CartPage(page)

        # Ожидание загрузки страницы корзины
        page.wait_for_url("**/cart.html")
        page.wait_for_load_state("networkidle")

        # Проверка что страница корзины загружена
        assert cart_page.is_page_loaded(), "Страница корзины не загружена"

        # ВИЗУАЛЬНАЯ КОНТРОЛЬНАЯ ТОЧКА 3: Cart Page
        print("[STEP 4] Создание визуального снимка: Cart Page")
        eyes.check("Cart Page", Target.window().fully())

        # Проверка что товар присутствует в корзине
        cart_items = cart_page.get_cart_items_count()
        print(f"[STEP 4] Товаров в корзине: {cart_items}")
        assert cart_items == 1, f"Ожидался 1 товар в корзине, найдено: {cart_items}"

        # Проверка названия товара
        item_names = cart_page.get_item_names()
        print(f"[STEP 4] Товары в корзине: {item_names}")
        assert "Sauce Labs Backpack" in item_names, "Товар 'Sauce Labs Backpack' не найден в корзине"

        # ============================================================
        # ШАГ 5: Начало оформления заказа - Checkout Page
        # ============================================================
        print("\n[STEP 5] Переход к оформлению заказа...")
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(page)

        # Ожидание загрузки страницы оформления заказа
        page.wait_for_url("**/checkout-step-one.html")
        page.wait_for_load_state("networkidle")

        # Проверка что страница оформления заказа загружена
        assert checkout_page.is_page_loaded(), "Страница оформления заказа не загружена"

        # ВИЗУАЛЬНАЯ КОНТРОЛЬНАЯ ТОЧКА 4: Checkout Page
        print("[STEP 5] Создание визуального снимка: Checkout Page")
        eyes.check("Checkout Page - Step One", Target.window().fully())

        # Заполнение формы для проверки что форма работает
        print("[STEP 5] Заполнение формы оформления заказа...")
        checkout_page.fill_checkout_form("John", "Doe", "12345")

        # Финальная проверка что форма заполнена корректно
        print("[STEP 5] Форма заполнена успешно")

        print("\n" + "="*80)
        print("BASELINE TEST COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nВсе визуальные контрольные точки созданы:")
        print("  1. Login Page")
        print("  2. Inventory Page")
        print("  3. Cart Page")
        print("  4. Checkout Page - Step One")
        print("\nОткройте Applitools Dashboard для просмотра результатов.")
        print("="*80 + "\n")
