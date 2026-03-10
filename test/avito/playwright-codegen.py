import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.avito.ru/")
    page.get_by_placeholder("Поиск по объявлениям").click()
    page.get_by_label("", exact=True).fill("iPhone 15")
    page.get_by_role("button", name="Найти").click()
    page.get_by_role("button", name="Показать ещё").first.click()
    page.locator("label").filter(has_text="512 ГБ").click()
    page.locator("label").filter(has_text="1 ТБ").click()
    page.get_by_role("button", name="Показать ещё").first.click()
    page.locator("label").filter(has_text="SIM + eSIM").click()
    page.locator("label").filter(has_text="Новое").click()
    page.locator("label").filter(has_text="Отличное").click()
    page.locator("label").filter(has_text="Хорошее").click()
    page.locator("label").filter(has_text="Отличное").click()
    page.locator("label").filter(has_text="Хорошее").click()
    page.locator("label").filter(has_text="Есть возврат").click()
    page.locator(".styles-module-switcherCircle-PlbWD").click()
    page.locator(".styles-module-toggle-tnaHU").first.click()
    page.get_by_role("button", name="Сортировка").click()
    page.get_by_role("checkbox", name="Дешевле").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)