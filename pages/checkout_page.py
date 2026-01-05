from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

class CheckoutPage(BasePage):
    """
    Класс страницы оформления заказа (все шаги).
    """

    # Шаг 1: Информация
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _POSTAL_CODE = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")

    # Шаг 2: Обзор
    _FINISH_BUTTON = (By.ID, "finish")

    # Финал: Завершение
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    @allure.step("Заполнить информацию о покупателе")
    def fill_information(self, first_name, last_name, zip_code):
        """
        Ввод данных пользователя на первом шаге чекаута.
        :param first_name: Имя
        :param last_name: Фамилия
        :param zip_code: Почтовый индекс
        """
        self.input_text(self._FIRST_NAME, first_name)
        self.input_text(self._LAST_NAME, last_name)
        self.input_text(self._POSTAL_CODE, zip_code)
        self.click(self._CONTINUE_BUTTON)

    @allure.step("Завершить заказ (нажать Finish)")
    def finish_order(self):
        """
        Подтверждение заказа на шаге обзора.
        """
        self.click(self._FINISH_BUTTON)

    @allure.step("Получить сообщение об успешном заказе")
    def get_complete_message(self):
        """
        Получение текста заголовка на финальной странице.
        :return: Текст (например, 'Thank you for your order!')
        """
        return self.get_text(self._COMPLETE_HEADER)
