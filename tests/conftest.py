import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для инициализации и закрытия веб-драйвера.
    Запускается перед каждым тестом и закрывается после.
    """
    # Настройка опций Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Раскомментируйте для запуска без графического интерфейса
    options.add_argument("--window-size=1920,1080")
    
    # Автоматическая установка драйвера
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    
    # Закрытие браузера после теста
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для создания скриншотов при падении тестов.
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
