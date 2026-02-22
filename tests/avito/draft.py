import re
import pytest
from playwright.sync_api import Playwright, sync_playwrightц


def run(playwright: Playwright) -> None: #  playwright: Playwright — это аннотация типа.
    # Она говорит, что в переменную playwright мы ожидаем объект класса Playwright.
    # Сам объект playwright — это главная "входная точка" в библиотеку.
    # Через него мы получаем доступ ко всем браузерам (chromium, firefox, webkit)
    browser = playwright.chromium.launch(headless=False)  #  метод, который физически запускает браузер
    context = browser.new_context() #  метод, который создает новый контекст браузера
    # создаются свои cookies, локальное хранилище (localStorage), история, настройки (размер окна, геолокация и т.д.)
    # Это позволяет изолировать тесты друг от друга. Ты можешь создать >=2 контекста в одном браузере
    page = context.new_page() #  создает новую вкладку (страницу) внутри текущего контекста
    page.goto("https://www.avito.ru/")

    page.locator('[data-marker="search-form/suggest/input"]').click()
    page.locator('[data-marker="search-form/suggest/input"]').fill("iPhone 15")
    page.locator('[data-marker="search-form/submit-button"]').click()

    page.locator('[data-marker="params[112691]/show-button"]').click()
    page.locator('input[value="757884"]').check() #  объем 256
    page.locator('input[value="757885"]').check() #  объем 512
    # page.get_by_role("button", name="Показать ещё").first.click()

    page.locator('input[value="3338066"]').check() #  sim + e-sim

    page.locator('input[value="2850684"]').check() #  состояние новое
    page.locator('input[value="2850685"]').check() #  Отличное
    page.locator('input[value="2850686"]').check() #  Хорошее
    page.locator("label").filter(has_text="Хорошее").click() #  Хорошее нажатие по label

    page.locator("label").filter(has_text="Есть возврат").click() #  дополнительная опция

    page.locator('[name="localPriority"]').check() #  приоритет по локации

    page.locator('[data-marker="sort/title"]').click() #  сортировка
    page.locator('[data-marker="sort/custom-option(1)"]').click() #  сначала дешевле

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)