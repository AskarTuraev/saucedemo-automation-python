from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

class InventoryPage(BasePage):
    """
    Класс страницы каталога товаров (Inventory).
    """

    # Локаторы
    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    # Динамический локатор для кнопки добавления (упрощенный пример)
    _ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    _REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")

    @allure.step("Получить заголовок страницы")
    def get_title(self):
        """
        Возвращает заголовок текущей страницы.
        :return: Текст заголовка
        """
        return self.get_text(self._PAGE_TITLE)

    @allure.step("Добавить рюкзак в корзину")
    def add_backpack_to_cart(self):
        """
        Добавляет товар 'Sauce Labs Backpack' в корзину.
        """
        self.click(self._ADD_TO_CART_BACKPACK)

    @allure.step("Получить количество товаров на значке корзины")
    def get_cart_badge_count(self):
        """
        Получает число товаров, отображаемое на иконке корзины.
        :return: Число товаров (int) или 0, если пусто
        """
        try:
            text = self.get_text(self._CART_BADGE)
            return int(text)
        except:
            return 0

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """
        Клик по иконке корзины для перехода на страницу корзины.
        """
        self.click(self._CART_LINK)
