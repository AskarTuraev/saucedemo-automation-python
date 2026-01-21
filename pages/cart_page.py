"""
Page Object для страницы корзины SauceDemo
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    """Страница корзины"""

    # Локаторы элементов страницы корзины
    CART_CONTAINER = '.cart_contents_container'
    CART_ITEM = '.cart_item'
    CART_ITEM_NAME = '.inventory_item_name'
    CART_ITEM_PRICE = '.inventory_item_price'
    CHECKOUT_BUTTON = '[data-test="checkout"]'
    CONTINUE_SHOPPING_BUTTON = '[data-test="continue-shopping"]'
    REMOVE_BUTTON = '[data-test^="remove"]'
    CART_QUANTITY = '.cart_quantity'

    def __init__(self, page: Page):
        """
        Инициализация страницы корзины

        Args:
            page: Playwright Page объект
        """
        super().__init__(page)
        self.url = 'https://www.saucedemo.com/cart.html'

    def is_page_loaded(self) -> bool:
        """
        Проверка загрузки страницы корзины

        Returns:
            True если страница загружена
        """
        return self.is_visible(self.CART_CONTAINER)

    def get_cart_items_count(self) -> int:
        """
        Получение количества товаров в корзине

        Returns:
            Количество товаров в корзине
        """
        return self.page.locator(self.CART_ITEM).count()

    def proceed_to_checkout(self):
        """Переход к оформлению заказа"""
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self):
        """Возврат к покупкам"""
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    def get_item_names(self) -> list:
        """
        Получение списка названий товаров в корзине

        Returns:
            Список названий товаров
        """
        items = self.page.locator(self.CART_ITEM_NAME).all()
        return [item.inner_text() for item in items]

    def remove_item(self, index: int = 0):
        """
        Удаление товара из корзины по индексу

        Args:
            index: Индекс товара (по умолчанию 0 - первый товар)
        """
        remove_buttons = self.page.locator(self.REMOVE_BUTTON).all()
        if index < len(remove_buttons):
            remove_buttons[index].click()

    def inject_cart_visual_defects(self):
        """
        Внедрение визуальных дефектов на странице корзины
        Дефект 3: Изменение цвета кнопки Checkout и нарушение layout
        """
        defect_script = """
        // Изменяем цвет кнопки Checkout на зеленый
        var checkoutBtn = document.querySelector('[data-test="checkout"]');
        if (checkoutBtn) {
            checkoutBtn.style.backgroundColor = '#00ff00';
            checkoutBtn.style.color = '#000000';
        }

        // Нарушаем layout - смещаем контейнер корзины
        var cartContainer = document.querySelector('.cart_contents_container');
        if (cartContainer) {
            cartContainer.style.marginLeft = '100px';
        }
        """
        self.inject_visual_defect(defect_script)
