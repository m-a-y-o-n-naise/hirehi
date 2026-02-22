import pytest
from playwright.sync_api import expect


def test_search_vacancy(page):
    """Проверка поиска вакансии тестировщика"""
    page.goto('https://hirehi.ru')

    page.locator('[id="categoryButton"]').click()

    page.locator('a:has-text("тестировщикам")[href*="category=qa"]').click()

    page.locator('[data-subcategory-id="manual"]').click()

    page.locator('[id="sortButton"]').click()

    page.locator('[data-value="salary-high"]').click()

    page.get_by_role("main").get_by_text("удалённо", exact=True).click()

    page.locator(".filter-chip:has-text('middle')").click()

    page.locator(".filter-chip:has-text('151–250k')").click()

    page.locator('[id="searchInput"]').click()
    page.locator('[id="searchInput"]').fill('python')
    page.locator('[id="searchInput"]').press("Enter")

