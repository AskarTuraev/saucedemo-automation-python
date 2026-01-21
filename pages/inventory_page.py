"""
Page Object для страницы каталога товаров SauceDemo
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Страница каталога товаров"""

    # Локаторы элементов страницы каталога
    INVENTORY_CONTAINER = '.inventory_container'
    INVENTORY_ITEM = '.inventory_item'
    INVENTORY_ITEM_NAME = '.inventory_item_name'
    INVENTORY_ITEM_PRICE = '.inventory_item_price'
    ADD_TO_CART_BUTTON = '[data-test^="add-to-cart"]'
    REMOVE_BUTTON = '[data-test^="remove"]'
    SHOPPING_CART_BADGE = '.shopping_cart_badge'
    SHOPPING_CART_LINK = '.shopping_cart_link'
    BURGER_MENU = '#react-burger-menu-btn'
    LOGOUT_LINK = '#logout_sidebar_link'

    def __init__(self, page: Page):
        """
        Инициализация страницы каталога

        Args:
            page: Playwright Page объект
        """
        super().__init__(page)
        self.url = 'https://www.saucedemo.com/inventory.html'

    def is_page_loaded(self) -> bool:
        """
        Проверка загрузки страницы каталога

        Returns:
            True если страница загружена
        """
        return self.is_visible(self.INVENTORY_CONTAINER)

    def add_first_item_to_cart(self):
        """Добавление первого товара в корзину"""
        # Получаем первую кнопку "Add to cart"
        first_add_button = f"{self.INVENTORY_ITEM}:first-child {self.ADD_TO_CART_BUTTON}"
        self.click(first_add_button)

    def add_item_to_cart_by_name(self, item_name: str):
        """
        Добавление товара в корзину по имени

        Args:
            item_name: Название товара
        """
        # Формируем data-test атрибут на основе имени товара
        item_name_formatted = item_name.lower().replace(' ', '-')
        add_button = f'[data-test="add-to-cart-{item_name_formatted}"]'
        self.click(add_button)

    def get_cart_items_count(self) -> str:
        """
        Получение количества товаров в корзине

        Returns:
            Количество товаров в корзине
        """
        if self.is_visible(self.SHOPPING_CART_BADGE):
            return self.get_text(self.SHOPPING_CART_BADGE)
        return '0'

    def go_to_cart(self):
        """Переход в корзину"""
        self.click(self.SHOPPING_CART_LINK)

    def get_items_count(self) -> int:
        """
        Получение количества товаров на странице

        Returns:
            Количество товаров
        """
        return self.page.locator(self.INVENTORY_ITEM).count()

    def inject_inventory_visual_defects(self):
        """
        Внедрение визуальных дефектов на странице каталога
        Дефект 2: Изменение цвета фона первого товара и скрытие цены
        """
        defect_script = """
        // Изменяем цвет фона первого товара на ярко-красный
        document.querySelector('.inventory_item').style.backgroundColor = '#ff0000';

        // Скрываем цену первого товара
        document.querySelector('.inventory_item_price').style.visibility = 'hidden';
        """
        self.inject_visual_defect(defect_script)
