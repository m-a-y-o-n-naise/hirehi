import pytest
import re
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
    page.locator('[id="searchInput"]').fill('python')
    page.locator('[id="searchInput"]').press("Enter")

    page.wait_for_selector('.job-card-body', state="visible", timeout=10000)
    expect(page.locator('.job-title').first).to_be_visible()

    # 1. Проверка типа в названии
    job_cards = page.locator('.jobs-container .job-card').all()
    # titles_texts = []
    # for card in job_cards:
    #     title = card.locator('.job-title').text_content()
    #     titles_texts.append(title) #  all_text_contents() - выдает все текстовые результаты списком
    # titles = []
    # for text in titles_texts:
    #     clean = re.search(r'\bmanual\b', text.lower())
    #     titles.append(clean.group()if clean else None)
    # assert all(t == 'manual' for t in titles), f'Проблемные вакансии: {titles}'
    titles_texts = [card.locator('.job-title').text_content() for card in job_cards if card.is_visible()]

    titles = [re.search(r'\bmanual\b', text.lower()).group()
              if re.search(r'\bmanual\b', text.lower())
              else None for text in titles_texts]
    assert None not in titles, f'Вакансии без manual: {titles_texts}'

    # 2. Проверка зарплаты
    salary_texts = page.locator('.job-salary').all_text_contents()
    salaries = []
    for text in salary_texts:
        clean = text.replace('до', '').replace('₽', '').replace(' ', '').strip().replace('от', '').replace('~', '').replace('-', '') # "до 200 000 ₽" → 200000
        try:
            salaries.append(int(clean))
        except:
            salaries.append(0)
    assert all(151000 <= s <= 250000 for s in salaries), \
        f'Не все зарплаты в диапазоне 150-200к: {salaries}'

    # 3. Проверка грейда
    levels = page.locator('.job-level').all_text_contents()
    assert all('middle' in l.lower() for l in levels), "Есть вакансии не middle"

