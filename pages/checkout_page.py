"""
Page Object для страницы оформления заказа SauceDemo
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Страница оформления заказа"""

    # Локаторы элементов страницы оформления заказа
    CHECKOUT_CONTAINER = '.checkout_info_container'
    FIRST_NAME_INPUT = '[data-test="firstName"]'
    LAST_NAME_INPUT = '[data-test="lastName"]'
    POSTAL_CODE_INPUT = '[data-test="postalCode"]'
    CONTINUE_BUTTON = '[data-test="continue"]'
    CANCEL_BUTTON = '[data-test="cancel"]'
    ERROR_MESSAGE = '[data-test="error"]'

    def __init__(self, page: Page):
        """
        Инициализация страницы оформления заказа

        Args:
            page: Playwright Page объект
        """
        super().__init__(page)
        self.url = 'https://www.saucedemo.com/checkout-step-one.html'

    def is_page_loaded(self) -> bool:
        """
        Проверка загрузки страницы оформления заказа

        Returns:
            True если страница загружена
        """
        return self.is_visible(self.CHECKOUT_CONTAINER)

    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str):
        """
        Заполнение формы оформления заказа

        Args:
            first_name: Имя
            last_name: Фамилия
            postal_code: Почтовый индекс
        """
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)

    def click_continue(self):
        """Клик по кнопке Continue"""
        self.click(self.CONTINUE_BUTTON)

    def click_cancel(self):
        """Клик по кнопке Cancel"""
        self.click(self.CANCEL_BUTTON)

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

    def inject_checkout_visual_defects(self):
        """
        Внедрение визуальных дефектов на странице оформления заказа
        Дефект 4: Скрытие поля First Name и изменение размера кнопки Continue
        """
        defect_script = """
        // Скрываем поле First Name
        var firstNameInput = document.querySelector('[data-test="firstName"]');
        if (firstNameInput) {
            firstNameInput.style.opacity = '0';
        }

        // Изменяем размер кнопки Continue - делаем её очень маленькой
        var continueBtn = document.querySelector('[data-test="continue"]');
        if (continueBtn) {
            continueBtn.style.width = '50px';
            continueBtn.style.fontSize = '8px';
        }
        """
        self.inject_visual_defect(defect_script)
