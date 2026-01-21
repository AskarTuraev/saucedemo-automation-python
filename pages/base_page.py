"""
Базовый класс для всех Page Objects
Содержит общие методы для работы со страницами
"""
from playwright.sync_api import Page, expect


class BasePage:
    """Базовая страница с общими методами"""

    def __init__(self, page: Page):
        """
        Инициализация базовой страницы

        Args:
            page: Playwright Page объект
        """
        self.page = page

    def navigate_to(self, url: str):
        """
        Переход на указанный URL

        Args:
            url: URL адрес страницы
        """
        self.page.goto(url)

    def get_title(self) -> str:
        """
        Получение заголовка страницы

        Returns:
            Заголовок страницы
        """
        return self.page.title()

    def wait_for_url(self, url: str, timeout: int = 30000):
        """
        Ожидание загрузки определенного URL

        Args:
            url: URL для ожидания
            timeout: Таймаут ожидания в миллисекундах
        """
        self.page.wait_for_url(url, timeout=timeout)

    def click(self, selector: str):
        """
        Клик по элементу

        Args:
            selector: CSS селектор элемента
        """
        self.page.click(selector)

    def fill(self, selector: str, text: str):
        """
        Заполнение текстового поля

        Args:
            selector: CSS селектор элемента
            text: Текст для ввода
        """
        self.page.fill(selector, text)

    def is_visible(self, selector: str) -> bool:
        """
        Проверка видимости элемента

        Args:
            selector: CSS селектор элемента

        Returns:
            True если элемент видим, иначе False
        """
        return self.page.is_visible(selector)

    def get_text(self, selector: str) -> str:
        """
        Получение текста элемента

        Args:
            selector: CSS селектор элемента

        Returns:
            Текст элемента
        """
        return self.page.locator(selector).inner_text()

    def inject_visual_defect(self, script: str):
        """
        Внедрение JavaScript кода для создания визуального дефекта

        Args:
            script: JavaScript код для выполнения
        """
        self.page.evaluate(script)
