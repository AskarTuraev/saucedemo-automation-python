from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

class CartPage(BasePage):
    """
    Класс страницы корзины.
    """

    # Локаторы
    _CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BUTTON = (By.ID, "checkout")
    _REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")

    @allure.step("Проверить наличие товара в корзине: {product_name}")
    def is_product_in_cart(self, product_name):
        """
        Проверяет, есть ли товар с заданным именем в корзине.
        :param product_name: Название товара
        :return: True, если товар найден
        """
        items = self.find_elements(self._CART_ITEM_NAME)
        for item in items:
            if item.text == product_name:
                return True
        return False

    @allure.step("Удалить рюкзак из корзины")
    def remove_backpack(self):
        """
        Удаляет рюкзак из корзины (если он там есть).
        """
        self.click(self._REMOVE_BACKPACK)

    @allure.step("Нажать кнопку Checkout")
    def click_checkout(self):
        """
        Переход к оформлению заказа.
        """
        self.click(self._CHECKOUT_BUTTON)
