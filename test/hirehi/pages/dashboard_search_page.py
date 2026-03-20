from playwright.sync_api import Page, expect
import allure
import re
from typing import List, Dict, Optional, Tuple


class DashboardPages:
    def __init__(self, page: Page):
        self.page = page
        self.profile = page.locator('#btnLogin')
        self.logout = page.locator('#profileLogoutDesktop')

    # def assert_welcome_messages(self, message):
    #     with allure.step(f"Проверка приветствия '{message}'"):
    #         expect(self.profile).to_have_text(message)

    def logout_user(self) -> None:
        with allure.step("Выход из системы"):
            self.logout.click()
            expect(self.page).to_have_url("**/?category=all")

class SearchPage:
    """Page Object для страницы поиска вакансий"""

    # Категории вакансий
    CATEGORIES = {
        'all': 'все вакансии',
        'design': 'дизайнерам',
        'development': 'разработчикам',
        'management': 'менеджерам',
        'qa': 'тестировщикам',
        'analytics': 'аналитикам',
        'devops': 'девопсам'
    }

    # Подкатегории для каждой категории
    SUBCATEGORIES = {
        'qa': {
            'manual': 'Manual',
            'auto': 'Auto'
        },
        'design': {
            'ux_ui': 'UX/UI',
            'product': 'Product Design',
            'web': 'Web',
            'graphic': 'Graphic',
            'illustration': 'Illustration'
        },
        'development': {
            'python': 'Python',
            'java': 'Java',
            'go': 'Go',
            'backend': 'Backend',
            'data_engineer': 'Data Engineer',
            'kotlin': 'Kotlin',
            'rust': 'Rust',
            'onec': '1C',
            'ml_ai': 'ML/AI',
            'netc': '.NET/C#',
            'cpp': 'C++',
            'php': 'PHP',
            'nodejs': 'Node.js',
            'frontend': 'Frontend',
            'mobile': 'Mobile',
            'fullstack': 'Fullstack'
        },
        'management': {
            'product_manager': 'Product Manager',
            'project_manager': 'Project Manager'
        },
        'analytics': {
            'data_analyst': 'Data Analyst',
            'business_analyst': 'Business Analyst',
            'product_analyst': 'Product Analyst',
            'system_analyst': 'System Analyst'
        },
        'devops': {
            'ci_cd': 'CI/CD',
            'kubernetes': 'Kubernetes',
            'cloud': 'Cloud',
            'infra': 'Infrastructure',
            'security': 'Security',
            'iac': 'IaC',
            'observability': 'Observability',
            'sre_platform': 'SRE/Platform'
        }
    }

    # Форматы работы
    FORMATS = ['удалённо', 'офис', 'гибрид', 'удалённо по РФ']

    # Грейды
    GRADES = ['intern', 'junior', 'middle', 'senior', 'lead', 'head']

    # Зарплатные диапазоны
    SALARY_RANGES = ['до 80k', '81–150k', '151–250k', '250k+']

    # Дополнительные фильтры
    EXTRA_FILTERS = ['hirehi', 'direct_contact', 'english']

    def __init__(self, page: Page):
        self.page = page

        # Основные элементы
        self.category_button = page.locator('[id="categoryButton"]')
        self.category_dropdown = page.locator('#categoryDropdown')
        self.sort_button = page.locator('[id="sortButton"]')
        self.sort_dropdown = page.locator('#sortDropdown')
        self.search_input = page.locator('[id="searchInput"]')
        self.jobs_container = page.locator('.jobs-container')
        self.job_cards = page.locator('.jobs-container .job-card')
        self.subcategory_chips = page.locator('#subcategoryChipsWrapper .filter-chip')

        # Элементы фильтров
        self.filter_chips = page.locator('.filter-chip')
        self.geo_filter_chip = page.locator('#regionFilterChip')
        self.country_filter_chip = page.locator('#countryFilterChip')
        self.reset_filters_button = page.locator('#resetFiltersButton')

    @allure.step('Открыть главную страницу')
    def navigate(self) -> 'SearchPage':
        """Открыть главную страницу"""
        self.page.goto('https://hirehi.ru')
        self.page.wait_for_load_state("networkidle")  # ждет пока все сетевые запросы завершатся
        return self

    @allure.step('Выбрать категорию "{category_key}"')
    def select_category(self, category_key: str) -> 'SearchPage':
        """Выбрать категорию вакансий"""
        self.category_button.click()

        category_locator = self.page.locator(
            f'a.category-option:has-text("{self.CATEGORIES[category_key]}")')
        category_locator.click()

        self.page.wait_for_load_state("networkidle")
        return self

    @allure.step('Выбрать подкатегорию "{subcategory_key}"')
    def select_subcategory(self, subcategory_key: str) -> 'SearchPage':
        """
        Выбрать подкатегорию.
        Автоматически определяет, какая сейчас выбрана категория.
        """
        current_url = self.page.url  # получаем текущую категорию из URL /?category=qa
        current_category = None

        for k in self.CATEGORIES.keys():
            if f"category={k}" in current_url:
                current_category = k
                break

        if not current_category:
            raise ValueError("Не удалось определить текущую категорию")

        if current_category not in self.SUBCATEGORIES:
            raise ValueError(f"Категория '{current_category}' не имеет подкатегорий")

        if subcategory_key not in self.SUBCATEGORIES[current_category]:
            available = list(self.SUBCATEGORIES[current_category].keys())
            raise ValueError(
                f"Подкатегория '{subcategory_key}' не найдена для '{current_category}'. "
                f"Доступны: {available}"
            )

        subcategory_locator = self.page.locator(f'[data-subcategory-id="{subcategory_key}"]')
        subcategory_locator.click()
        self.page.wait_for_load_state("networkidle")
        return self

    @allure.step('Выбрать случайную подкатегорию для "{category_key}"')
    def select_random_subcategory(self, category_key: str) -> str:
        """Выбрать случайную подкатегорию и вернуть её ключ"""
        import random

        if category_key not in self.SUBCATEGORIES:
            raise ValueError(f"Категория '{category_key}' не имеет подкатегорий")

        subcategory_keys = list(self.SUBCATEGORIES[category_key].keys())
        chosen = random.choice(subcategory_keys)
        self.select_subcategory(chosen)
        return chosen

    def get_available_subcategories(self, category_key: str) -> List[str]:
        """Получить список доступных подкатегорий для категории"""
        if category_key not in self.SUBCATEGORIES:
            return []
        return list(self.SUBCATEGORIES[category_key].keys())

    def get_subcategory_display_name(self, category_key: str, subcategory_key: str) -> str:
        """Получить отображаемое название подкатегории"""
        return self.SUBCATEGORIES.get(category_key, {}).get(subcategory_key, subcategory_key)

    @allure.step('Выбрать сортировку "{sort_option}"')
    def select_sort(self, sort_option: str) -> 'SearchPage':
        """Выбрать опцию сортировки (recent/salary-high)"""
        self.sort_button.click()
        sort_locator = self.page.locator(f'[data-value="{sort_option}"]')
        sort_locator.click()
        self.page.wait_for_load_state("networkidle")
        return self

    @allure.step('Выбрать фильтр "{filter_name}" со значением "{filter_value}"')
    def select_filter(self, filter_name: str, filter_value: str = '') -> 'SearchPage':
        """
        Выбрать фильтр
        Универсальный метод выбора фильтра.
    filter_name может быть: 'format', 'level', 'salary', 'hirehi', 'direct_contact', 'english', 'region', 'country'
        """
    # Определяем тип фильтра по константам класса
    #     if filter_name == 'format':
    #         pattern = re.compile(f"^{filter_value}")
    #         filter_locator = self.page.locator(f".filter-chip").filter(has_text=pattern).first
        if filter_name == 'format':
            filter_locator = self.page.locator(f'.chip-text:text-is("{filter_value}")').locator('xpath=..')

        elif filter_name == 'level':
            # Проверяем, что значение есть в списке GRADES
            if filter_value not in self.GRADES:
                raise ValueError(f"Неверный грейд: {filter_value}. Доступны: {self.GRADES}")
            filter_locator = self.page.locator(f".filter-chip:has-text('{filter_value}')")

        elif filter_name == 'salary':
            # Проверяем, что значение есть в списке SALARY_RANGES
            if filter_value not in self.SALARY_RANGES:
                raise ValueError(f"Неверный диапазон зарплат: {filter_value}. Доступны: {self.SALARY_RANGES}")
            filter_locator = self.page.locator(f".filter-chip:has-text('{filter_value}')")

        elif filter_name in self.EXTRA_FILTERS:
            filter_locator = self.page.locator(f'.filter-checkbox-item[data-filter-type="{filter_name}"]')

        elif filter_name in ['region', 'country']:
            filter_locator = self.page.locator(f'#{filter_name}FilterChip')

        else:
            raise ValueError(f"Неизвестный фильтр: {filter_name}")

        filter_locator.click()
        self.page.wait_for_load_state("networkidle")
        return self

    @allure.step('Выполнить поиск по тексту "{search_text}"')
    def search(self, search_text: str) -> 'SearchPage':
        """Ввести текст в поиск и выполнить поиск"""
        self.search_input.fill(search_text)
        self.search_input.press("Enter")
        self.page.wait_for_load_state("networkidle")
        return self

    @allure.step('Дождаться загрузки результатов поиска')
    def wait_for_results(self, timeout: int = 10000) -> 'SearchPage':
        """Дождаться загрузки карточек вакансий"""
        self.page.wait_for_selector('.job-card-body', state="visible", timeout=timeout)
        return self

    def get_job_cards(self) -> List:
        """Получить все видимые карточки вакансий"""
        self.page.wait_for_timeout(500)
        visible_cards = [card for card in self.job_cards.all() if card.is_visible()]
        # для отладки
        all_cards = self.job_cards.all()
        print(f"Всего карточек в DOM: {len(all_cards)}, видимых: {len(visible_cards)}")
        return visible_cards  # без отладки можно было сразу вернуть [card for card in self.job_cards.all() if card.is_visible()]

    @allure.step('Получить названия вакансий')
    def get_job_titles(self) -> List[str]:
        """Получить тексты названий всех видимых вакансий"""
        cards = self.get_job_cards()
        titles = []

        for i, card in enumerate(cards):
            try:
                # Добавляем небольшую задержку только на получение текста
                title = card.locator('.job-title').text_content(timeout=2000)
                if title and title.strip():
                    titles.append(title)
            except Exception as e:
                print(f"Карточка {i}: ошибка получения текста - {e}")
                continue

        return titles # без отладки можно было сразу вернуть [card.locator('.job-title').text_content() for card in self.get_job_cards()]

    @allure.step('Получить зарплаты вакансий')
    def get_job_salaries(self) -> List[int]:
        """Получить зарплаты всех видимых вакансий в числовом формате"""
        salary_texts = self.page.locator('.job-salary').all_text_contents()
        salaries = []
        for text in salary_texts:
            clean = re.sub(r'[^\d]', '', text)
            try:
                salaries.append(int(clean))
            except:
                salaries.append(0)
        return salaries

    @allure.step('Получить грейды вакансий')
    def get_job_grades(self) -> List[str]:
        """Получить грейды всех видимых вакансий"""
        return self.page.locator('.job-level').all_text_contents()

    @allure.step('Проверить наличие подстроки "{substring}" в названиях')
    def assert_titles_contain(self, substring: str, case_sensitive: bool = False) -> 'SearchPage':
        """Проверить, что все названия содержат указанную подстроку"""
        titles = self.get_job_titles()
        if not case_sensitive:
            substring = substring.lower()
            titles = [t.lower() for t in titles]

        assert any(substring in t for t in titles), \
            f'Ни одна вакансия не содержит "{substring}": {titles}'
        return self

    @allure.step('Проверить диапазон зарплат')
    def assert_salaries_in_range(self, min_salary: int, max_salary: int) -> 'SearchPage':
        """Проверить, что все зарплаты в указанном диапазоне"""
        salaries = self.get_job_salaries()
        assert all(min_salary <= s <= max_salary for s in salaries), \
            f'Не все зарплаты в диапазоне {min_salary}-{max_salary}: {salaries}'
        return self

    @allure.step('Проверить грейд вакансий')
    def assert_grades_equal(self, expected_grade: str, case_sensitive: bool = False) -> 'SearchPage':
        """Проверить, что все вакансии имеют указанный грейд"""
        grades = self.get_job_grades()
        if not case_sensitive:
            expected_grade = expected_grade.lower()
            grades = [g.lower() for g in grades]

        assert all(expected_grade in g for g in grades), \
            f'Не все вакансии имеют грейд {expected_grade}: {grades}'
        return self

    @allure.step('Проверить отображение первой карточки')
    def assert_first_card_visible(self) -> 'SearchPage':
        """Проверить, что первая карточка вакансии видима"""
        expect(self.page.locator('.job-title').first).to_be_visible()
        return self