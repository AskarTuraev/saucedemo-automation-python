"""
Конфигурационный файл для автоматизированного тестирования
Содержит настройки окружения и параметры подключения к Applitools
"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()


class Config:
    """Класс с конфигурацией для тестов"""

    # Applitools настройки
    APPLITOOLS_API_KEY = os.getenv('APPLITOOLS_API_KEY', '')
    APPLITOOLS_SERVER_URL = 'https://eyes.applitools.com'

    # Настройки приложения
    BASE_URL = os.getenv('BASE_URL', 'https://www.saucedemo.com')

    # Настройки браузера
    BROWSER = os.getenv('BROWSER', 'chromium')
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    VIEWPORT_WIDTH = 1920
    VIEWPORT_HEIGHT = 1080

    # Тестовые учетные данные
    TEST_USERNAME = os.getenv('TEST_USERNAME', 'standard_user')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD', 'secret_sauce')

    # Таймауты (в миллисекундах для Playwright)
    DEFAULT_TIMEOUT = 30000
    NAVIGATION_TIMEOUT = 30000

    # Applitools настройки для тестов
    APP_NAME = 'SauceDemo'
    BATCH_NAME = 'SauceDemo Visual Regression Tests'
    TEST_NAME = 'SauceDemo E2E with Visual Checks'

    @classmethod
    def validate(cls):
        """Валидация обязательных настроек"""
        if not cls.APPLITOOLS_API_KEY:
            raise ValueError(
                "APPLITOOLS_API_KEY не установлен. "
                "Создайте .env файл на основе .env.example и добавьте ваш API ключ"
            )
