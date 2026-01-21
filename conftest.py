"""
Конфигурация pytest и фикстуры для тестов
"""
import pytest
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
from applitools.playwright import Eyes, Target, BatchInfo, Configuration as EyesConfiguration, ClassicRunner
from config import Config
import os


@pytest.fixture(scope="session")
def config():
    """
    Фикстура для загрузки конфигурации
    Валидирует наличие API ключа Applitools
    """
    Config.validate()
    return Config


@pytest.fixture(scope="session")
def runner():
    """
    Фикстура для создания ClassicRunner
    Используется для сбора результатов всех тестов
    """
    classic_runner = ClassicRunner()
    yield classic_runner

    # Получение результатов всех тестов после завершения сессии
    all_test_results = classic_runner.get_all_test_results(False)
    print(f"\n{'='*80}")
    print("APPLITOOLS TEST RESULTS SUMMARY")
    print(f"{'='*80}")
    print(f"Total tests: {len(all_test_results.all_results)}")

    for result in all_test_results.all_results:
        status = "✓ PASSED" if result.test_results.is_passed else "✗ FAILED"
        print(f"{status}: {result.test_results.name}")
        print(f"  URL: {result.test_results.url}")
    print(f"{'='*80}\n")


@pytest.fixture(scope="session")
def playwright_instance():
    """
    Фикстура для создания экземпляра Playwright
    Scope: session - создается один раз на всю сессию тестов
    """
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="function")
def browser(playwright_instance, config):
    """
    Фикстура для создания браузера
    Scope: function - создается для каждого теста
    """
    # Выбор типа браузера из конфигурации
    if config.BROWSER == "chromium":
        browser = playwright_instance.chromium.launch(headless=config.HEADLESS)
    elif config.BROWSER == "firefox":
        browser = playwright_instance.firefox.launch(headless=config.HEADLESS)
    elif config.BROWSER == "webkit":
        browser = playwright_instance.webkit.launch(headless=config.HEADLESS)
    else:
        browser = playwright_instance.chromium.launch(headless=config.HEADLESS)

    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser, config):
    """
    Фикстура для создания контекста браузера
    Устанавливает viewport и другие настройки
    """
    context = browser.new_context(
        viewport={
            'width': config.VIEWPORT_WIDTH,
            'height': config.VIEWPORT_HEIGHT
        }
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """
    Фикстура для создания новой страницы
    """
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def eyes(runner, config):
    """
    Фикстура для создания и настройки Applitools Eyes
    Интегрируется с Playwright для визуального тестирования
    """
    # Создание экземпляра Eyes
    eyes = Eyes(runner)

    # Настройка конфигурации Eyes
    eyes_config = EyesConfiguration()
    eyes_config.set_api_key(config.APPLITOOLS_API_KEY)
    eyes_config.set_app_name(config.APP_NAME)

    # Настройка batch для группировки тестов
    batch = BatchInfo(config.BATCH_NAME)
    eyes_config.set_batch(batch)

    # Применение конфигурации
    eyes.set_configuration(eyes_config)

    yield eyes

    # Закрытие Eyes и получение результатов теста
    try:
        # Важно: вызываем close_async() для корректного завершения
        eyes.close_async()
    except Exception as e:
        print(f"Ошибка при закрытии Eyes: {e}")
    finally:
        # Прерывание сессии в случае ошибки
        eyes.abort_async()


@pytest.fixture(scope="function")
def eyes_page(page, eyes, config, request):
    """
    Фикстура для создания страницы с открытой Eyes сессией
    Автоматически открывает и закрывает Eyes для каждого теста
    """
    # Получение имени теста из pytest request
    test_name = request.node.name

    # Открытие Eyes сессии
    eyes.open(
        page,
        app_name=config.APP_NAME,
        test_name=test_name,
        viewport_size={
            'width': config.VIEWPORT_WIDTH,
            'height': config.VIEWPORT_HEIGHT
        }
    )

    yield page

    # Eyes будет закрыт в фикстуре eyes


def pytest_configure(config):
    """
    Хук pytest для настройки при запуске
    """
    # Создание директорий для отчетов если их нет
    os.makedirs('reports', exist_ok=True)

    print("\n" + "="*80)
    print("STARTING SAUCEDEMO VISUAL REGRESSION TESTS")
    print("="*80 + "\n")


def pytest_sessionfinish(session, exitstatus):
    """
    Хук pytest после завершения всех тестов
    """
    print("\n" + "="*80)
    print("TESTS COMPLETED")
    print("="*80 + "\n")
