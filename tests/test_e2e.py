import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

# Константы (в реальном проекте вынести в конфиг)
URL = "https://www.saucedemo.com/"
USER = "standard_user"
PASSWORD = "secret_sauce"
LOCKED_USER = "locked_out_user"

@allure.feature("Авторизация")
@allure.story("Успешный вход в систему")
def test_login_success(driver):
    """
    Тест проверяет успешную авторизацию валидного пользователя.
    """
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.open_url(URL)
    login_page.login(USER, PASSWORD)
    
    assert inventory_page.get_title() == "Products", "Заголовок страницы не соответствует ожидаемому"

@allure.feature("Авторизация")
@allure.story("Вход заблокированного пользователя")
def test_login_locked_out(driver):
    """
    Тест проверяет ошибку при входе заблокированного пользователя.
    """
    login_page = LoginPage(driver)
    
    login_page.open_url(URL)
    login_page.login(LOCKED_USER, PASSWORD)
    
    error_text = login_page.get_error_message()
    assert "Sorry, this user has been locked out" in error_text, "Сообщение об ошибке некорректно"

@allure.feature("Корзина")
@allure.story("Добавление товара в корзину")
def test_add_to_cart(driver):
    """
    Тест проверяет добавление товара в корзину и изменение счетчика.
    """
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    login_page.open_url(URL)
    login_page.login(USER, PASSWORD)
    
    inventory_page.add_backpack_to_cart()
    assert inventory_page.get_cart_badge_count() == 1, "Счетчик корзины должен быть равен 1"

@allure.feature("Корзина")
@allure.story("Удаление товара из корзины")
def test_remove_from_cart(driver):
    """
    Тест проверяет добавление, переход в корзину и удаление товара.
    """
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.open_url(URL)
    login_page.login(USER, PASSWORD)
    
    inventory_page.add_backpack_to_cart()
    inventory_page.go_to_cart()
    
    assert cart_page.is_product_in_cart("Sauce Labs Backpack"), "Товар не найден в корзине"
    
    cart_page.remove_backpack()
    assert not cart_page.is_product_in_cart("Sauce Labs Backpack"), "Товар не был удален из корзины"

@allure.feature("Покупка (Checkout)")
@allure.story("Полный цикл покупки (E2E)")
def test_full_checkout_process(driver):
    """
    Полный E2E сценарий: Логин -> Добавление -> Корзина -> Чекаут -> Финиш.
    """
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # 1. Логин
    login_page.open_url(URL)
    login_page.login(USER, PASSWORD)

    # 2. Добавление товара
    inventory_page.add_backpack_to_cart()
    inventory_page.go_to_cart()

    # 3. Переход к оформлению
    cart_page.click_checkout()

    # 4. Заполнение формы
    checkout_page.fill_information("Test", "User", "12345")

    # 5. Завершение заказа
    checkout_page.finish_order()

    # 6. Проверка
    assert checkout_page.get_complete_message() == "Thank you for your order!", "Заказ не был завершен успешно"
