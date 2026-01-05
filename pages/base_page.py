from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import setup_logger
import allure

logger = setup_logger("BasePage")

class BasePage:
    """
    Базовый класс для всех Page Objects.
    Содержит общие методы для взаимодействия с веб-страницей.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Явное ожидание 10 секунд

    @allure.step("Открыть URL: {url}")
    def open_url(self, url):
        """
        Открывает указанный URL.
        :param url: Адрес страницы
        """
        logger.info(f"Открытие страницы: {url}")
        self.driver.get(url)

    def find_element(self, locator):
        """
        Находит элемент на странице с ожиданием его появления.
        :param locator: Кортеж (By.ID, "value")
        :return: WebElement
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Элемент не найден: {locator}")
            raise

    def find_elements(self, locator):
        """
        Находит список элементов на странице.
        :param locator: Кортеж (By.ID, "value")
        :return: List[WebElement]
        """
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            logger.error(f"Элементы не найдены: {locator}")
            return []

    @allure.step("Кликнуть по элементу: {locator}")
    def click(self, locator):
        """
        Кликает по элементу.
        :param locator: Локатор элемента
        """
        logger.info(f"Клик по элементу: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Ввести текст '{text}' в элемент: {locator}")
    def input_text(self, locator, text):
        """
        Вводит текст в поле.
        :param locator: Локатор поля ввода
        :param text: Текст для ввода
        """
        logger.info(f"Ввод текста '{text}' в элемент: {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator):
        """
        Получает текст элемента.
        :param locator: Локатор элемента
        :return: Текст элемента (str)
        """
        element = self.find_element(locator)
        text = element.text
        logger.info(f"Получен текст '{text}' из элемента: {locator}")
        return text

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Возвращает текущий URL страницы"""
        return self.driver.current_url
