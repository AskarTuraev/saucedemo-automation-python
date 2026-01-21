"""
Page Object для страницы авторизации SauceDemo
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница авторизации"""

    # Локаторы элементов страницы авторизации
    USERNAME_INPUT = '[data-test="username"]'
    PASSWORD_INPUT = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'
    LOGIN_LOGO = '.login_logo'

    def __init__(self, page: Page):
        """
        Инициализация страницы авторизации

        Args:
            page: Playwright Page объект
        """
        super().__init__(page)
        self.url = 'https://www.saucedemo.com/'

    def open(self):
        """Открытие страницы авторизации"""
        self.navigate_to(self.url)

    def login(self, username: str, password: str):
        """
        Выполнение авторизации

        Args:
            username: Имя пользователя
            password: Пароль
        """
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_error_displayed(self) -> bool:
        """
        Проверка отображения ошибки

        Returns:
            True если ошибка отображается
        """
        return self.is_visible(self.ERROR_MESSAGE)

    def get_error_message(self) -> str:
        """
        Получение текста сообщения об ошибке

        Returns:
            Текст сообщения об ошибке
        """
        return self.get_text(self.ERROR_MESSAGE)

    def inject_login_visual_defects(self):
        """
        Внедрение визуальных дефектов на странице авторизации
        Дефект 1: Скрытие кнопки Login
        """
        defect_script = """
        // Скрываем кнопку Login
        document.querySelector('[data-test="login-button"]').style.display = 'none';
        """
        self.inject_visual_defect(defect_script)
