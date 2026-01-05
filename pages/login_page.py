from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

class LoginPage(BasePage):
    """
    Класс страницы авторизации (https://www.saucedemo.com/).
    """

    # Локаторы
    _USERNAME_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    @allure.step("Выполнить вход с логином: {username}")
    def login(self, username, password):
        """
        Авторизация пользователя.
        :param username: Имя пользователя
        :param password: Пароль
        """
        self.input_text(self._USERNAME_INPUT, username)
        self.input_text(self._PASSWORD_INPUT, password)
        self.click(self._LOGIN_BUTTON)

    @allure.step("Получить сообщение об ошибке")
    def get_error_message(self):
        """
        Возвращает текст ошибки при неудачном входе.
        :return: Текст ошибки
        """
        return self.get_text(self._ERROR_MESSAGE)
