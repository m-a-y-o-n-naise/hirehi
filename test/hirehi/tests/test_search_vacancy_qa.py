from test.hirehi.pages.dashboard_search_page import SearchPage
import pytest
# import re
# from playwright.sync_api import expect


def test_search_vacancy(page) -> None:
    """Проверка поиска вакансии тестировщика"""
    search_page = SearchPage(page)
    search_page.navigate()
    search_page.select_category('qa')
    search_page.select_subcategory('manual')
    search_page.select_sort('salary-high')
    search_page.select_filter('format', 'удалённо')
    search_page.select_filter('level', 'middle')
    search_page.select_filter('salary', '151–250k')
    search_page.search('python')
    search_page.wait_for_results()

    search_page.assert_first_card_visible()
    search_page.assert_titles_contain('manual')
    search_page.assert_salaries_in_range(151000, 250000)
    search_page.assert_grades_equal('middle')

    # page.goto('https://hirehi.ru')
    # page.locator('[id="categoryButton"]').click()
    # page.locator('a:has-text("тестировщикам")[href*="category=qa"]').click()
    # page.locator('[data-subcategory-id="manual"]').click()
    # page.locator('[id="sortButton"]').click()
    # page.locator('[data-value="salary-high"]').click()
    # page.get_by_role("main").get_by_text("удалённо", exact=True).click()
    # page.locator(".filter-chip:has-text('middle')").click()
    # page.locator(".filter-chip:has-text('151–250k')").click()
    # page.locator('[id="searchInput"]').fill('python')
    # page.locator('[id="searchInput"]').press("Enter")

    # page.wait_for_selector('.job-card-body', state="visible", timeout=10000)
    # expect(page.locator('.job-title').first).to_be_visible()

    # # 1. Проверка типа в названии
    # job_cards = page.locator('.jobs-container .job-card').all()
    # titles_texts = [card.locator('.job-title').text_content() for card in job_cards if card.is_visible()]
    #
    # titles = [re.search(r'\bmanual\b', text.lower()).group()
    #           if re.search(r'\bmanual\b', text.lower())
    #           else None for text in titles_texts]
    # assert None not in titles, f'Вакансии без manual: {titles_texts}'
    #
    # # 2. Проверка зарплаты
    # salary_texts = page.locator('.job-salary').all_text_contents()
    # salaries = []
    # for text in salary_texts:
    #     clean = re.sub(r'[^\d]', '', text)  # только цифры
    #     try:
    #         salaries.append(int(clean))
    #     except:
    #         salaries.append(0)
    # assert all(151000 <= s <= 250000 for s in salaries), \
    #     f'Не все зарплаты в диапазоне 150-200к: {salaries}'
    #
    # # 3. Проверка грейда
    # levels = page.locator('.job-level').all_text_contents()
    # assert all('middle' in l.lower() for l in levels), "Есть вакансии не middle"

