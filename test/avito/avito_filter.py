import pytest
from playwright.sync_api import expect


def test_iphone_filters(page):
    """Тест: применение фильтров для iPhone 15"""

    # 1. Открыть сайт
    page.goto("https://www.avito.ru/")

    # 2. Поиск iPhone 15
    page.locator('[data-marker="search-form/suggest/input"]').click()
    page.locator('[data-marker="search-form/suggest/input"]').fill("iPhone 15")
    page.locator('[data-marker="search-form/submit-button"]').click()

    # 3. Открыть фильтры и выбрать объёмы памяти все попытки одного и того же
    # memory_block = page.get_by_role("heading", name="Память").locator("..").locator("..")
    # memory_block.get_by_role("button", name="Показать ещё").click() функционал плавающий
    # Находим заголовок
    memory_header = page.get_by_role("heading", name="Память").first
    # Поднимаемся до общего родительского блока
    filter_block = memory_header.locator(
        "xpath=ancestor::div[contains(@class, 'styles-module-root-yVYmx')]"
    )
    filter_block.locator('div.expand-list-expandButton-MBDEk a').click()
    # page.locator('[data-marker="params[112691]/show-button"]').click()
    # page.locator('input[value="757884"]').check()  # 256 ГБ
    # page.get_by_text("256 ГБ", exact=False).first.click()
    # page.locator('input[value="757885"]').check()  # 512 ГБ
    # page.get_by_text("512 ГБ", exact=False).first.click()
    # page.locator('input[value="757884"]').locator('..').click(force=True)
    # page.locator('input[value="757885"]').locator('..').click(force=True)
    page.locator('label:has-text("256 ГБ")').first.click()
    page.locator('label:has-text("512 ГБ")').first.click()

    # 5. Выбрать тип SIM
    # page.locator('input[value="3338066"]').check()  # SIM + e-SIM
    # page.locator('input[value="3338066"]').locator('..').click(force=True)
    page.locator('label:has-text("SIM + eSIM")').first.click()

    # 6. Выбрать состояние
    # page.locator('input[value="2850684"]').locator('..').click(force=True)  # Новое
    # page.locator('input[value="2850685"]').check()  # Отличное
    # page.locator('input[value="2850686"]').check()  # Хорошее
    page.locator('label:has-text("Новое")').first.click()
    page.locator('label:has-text("Отличное")').first.click()
    page.locator('label:has-text("Хорошее")').first.click()
    page.locator("label").filter(has_text="Хорошее").click()  # Хорошее нажатие по label для отмены

    # 7. Дополнительные опции
    page.locator("label").filter(has_text="Есть возврат").click()

    # 8. Приоритет по локации
    # page.locator('[name="localPriority"]').check()
    page.locator('label:has([name="localPriority"])').first.click()

    # 9. Сортировка
    # page.locator('[data-marker="sort/title"]').click()
    # Клик по кнопке с точным названием
    page.get_by_role("button", name="Сортировка").click()
    # page.locator('[data-marker="sort/custom-option(1)"]').click()  # Сначала дешевле
    page.get_by_role("button", name="Сортировка").click()

    # ✅ ДОБАВЛЯЕМ ПРОВЕРКИ
    # Проверка, что результаты загрузились
    expect(page.locator('[data-marker="catalog-serp"]')).to_be_visible() #  есть список
    expect(page.locator('[data-marker="item"]')).to_be_visible() #  для конкретного результата в списках

    # Проверка, что в результатах есть iPhone
    first_item = page.locator('[data-marker="item"]').first
    expect(first_item).to_contain_text("iPhone", timeout=10000)

    # Проверка, что цены отображаются
    prices = page.locator('[data-marker="item-price-value"]').all_text_contents()
    assert len(prices) > 0, "Цены не найдены"

    # Проверка цены (что сортировка сработала)
    prices_num = [int(p.replace('₽', '').replace(' ', '')) for p in prices[:10]]
    assert all(prices_num[i] <= prices_num[i + 1] for i in range(len(prices_num) - 1))

    # Можно сохранить скриншот для отчёта
    page.screenshot(path="results/avito_filters.png")