import pytest
import allure
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def page(request):
    """Фикстура страницы с обработкой ошибок и скриншотами"""
    with sync_playwright() as playwright: # 1. Запуск Playwright
        # Конфигурация из параметров или переменных окружения
        headless = request.config.getoption("--headless", default=False)
        browser_type = request.config.getoption("--browser", default="chromium")

        # Выбор браузера
        if browser_type == "firefox":
            browser = playwright.firefox.launch(headless=headless,
        args=["--start-maximized"])
        else:
            browser = playwright.chromium.launch(headless=headless,
        args=["--start-maximized"])
        # elif browser_type == "webkit":
        #     browser = playwright.webkit.launch(headless=headless,
        #         args=["--start-maximized"]) #  движок Safari

        # Контекст с настройками
        context = browser.new_context(
            no_viewport=True,
            # viewport={'width': 1536, 'height': 864}, # 1920*0.8, 1080*0.8
            locale='ru-RU'
        ) #  метод, который создает новый контекст браузера
        # создаются свои cookies, локальное хранилище (localStorage), история, настройки (размер окна, геолокация и т.д.)
        # Это позволяет изолировать тесты друг от друга. Ты можешь создать >=2 контекста в одном браузере

        page = context.new_page() #  создает новую вкладку (страницу) внутри текущего контекста
        page.set_default_timeout(30000)  # 30 секунд

        # Передаём страницу тесту
        yield page

        # Скриншот если тест упал
        if request.node.rep_call.failed: #
            screenshot = page.screenshot(full_page=True) #
            allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG) #

        # Очистка
        context.close()
        browser.close()


# Хук для отслеживания результата теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield # ← Здесь выполняется сам тест
    rep = outcome.get_result()  # ← Результат после выполнения
    setattr(item, "rep_" + rep.when, rep) # ← Сохраняем результат