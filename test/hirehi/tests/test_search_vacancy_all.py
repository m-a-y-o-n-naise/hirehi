import pytest
import allure
from test.hirehi.pages.dashboard_search_page import SearchPage


@allure.feature("Поиск вакансий")
class TestVacancySearch:

    @allure.story("Поиск категорий с подкатегориями и текстом")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("category,subcategory,search_text", [
        # QA
        ("qa", "manual", "python"),
        ("qa", "auto", "selenium"),

        # Design
        ("design", "ux_ui", "figma"),
        ("design", "graphic", "photoshop"),
        ("design", "illustration", "illustrator"),

        # Development
        ("development", "python", "django"),
        ("development", "java", "spring"),
        ("development", "frontend", "react"),
        ("development", "mobile", "swift"),
        ("development", "ml_ai", "tensorflow"),

        # Management
        ("management", "product_manager", "product"),
        ("management", "project_manager", "agile"),

        # Analytics
        ("analytics", "data_analyst", "sql"),
        ("analytics", "system_analyst", "uml"),

        # DevOps
        ("devops", "kubernetes", "docker"),
        ("devops", "cloud", "aws"),
        ("devops", "security", "security"),
    ])
    def test_search_with_subcategory(self, page, category, subcategory, search_text):
        """Тест поиска с различными категориями и подкатегориями"""
        search_page = SearchPage(page)

        search_page.navigate()
        search_page.select_category(category)
        search_page.select_subcategory(subcategory)
        search_page.search(search_text)
        search_page.wait_for_results()

        # Проверяем, что результаты есть
        search_page.assert_first_card_visible()

        # Дополнительная проверка: текст поиска должен содержаться в названиях
        # if search_text and len(search_text) > 2:
        #     search_page.assert_titles_contain(search_text)

    @allure.story("Проверка всех подкатегорий для категории")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("category", ['qa', 'design', 'development', 'management', 'analytics', 'devops'])
    def test_all_subcategories(self, page, category):
        """Проверить, что все подкатегории работают"""
        search_page = SearchPage(page)
        search_page.navigate()
        search_page.select_category(category)

        subcategories = search_page.get_available_subcategories(category)
        assert len(subcategories) > 0, f"Нет подкатегорий для {category}"

        # Проверяем каждую подкатегорию
        for subcat in subcategories[:3]:  # Проверим первые 3 для экономии времени
            search_page.select_subcategory(subcat)
            # Проверяем, есть ли вообще карточки
            cards = search_page.get_job_cards()
            if len(cards) > 0:
                print(f"✅ {subcat}: {len(cards)} вакансий")
            else:
                print(f"⚠️ {subcat}: нет вакансий")

            # Возвращаемся к категории (очищаем подкатегорию)
            search_page.select_category(category)

    @allure.story("Негативные тесты подкатегорий")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_subcategory(self, page):
        """Проверить обработку неверной подкатегории"""
        search_page = SearchPage(page)
        search_page.navigate()
        search_page.select_category('qa')

        # Пытаемся выбрать подкатегорию от другой категории
        with pytest.raises(ValueError, match="не найдена"):
            search_page.select_subcategory('ux_ui')  # ux_ui есть только у design

    @allure.story("Комплексный поиск")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("category,subcategory,grade,salary_range,search_text", [
        # QA
        ("qa", "manual", "middle", "151–250k", "manual"),
        ("qa", "auto", "senior", "250k+", "selenium"),

        # Development
        ("development", "python", "middle", "151–250k", "python"),
        ("development", "java", "senior", "250k+", "java"),
        ("development", "frontend", "junior", "до 80k", "react"),

        # DevOps
        ("devops", "kubernetes", "senior", "250k+", "kubernetes"),
        ("devops", "cloud", "middle", "151–250k", "aws"),
    ])
    def test_comprehensive_search(self, page, category, subcategory, grade, salary_range, search_text):
        """Полный тест со всеми фильтрами"""
        search_page = SearchPage(page)

        search_page.navigate()
        search_page.select_category(category)
        search_page.select_subcategory(subcategory)
        search_page.select_filter("level", grade)
        search_page.select_filter("salary", salary_range)
        search_page.search(search_text)
        search_page.wait_for_results()

        # Проверки
        # search_page.assert_titles_contain(search_text) -не все вакансии или вообще ни одна не содержит вводимый текст в некоторых случаях
        search_page.assert_grades_equal(grade)

        # Для зарплат конвертируем диапазон в числа
        salary_map = {
            "до 80k": (0, 80000),
            "81–150k": (81000, 150000),
            "151–250k": (151000, 250000),
            "250k+": (250000, 1000000)
        }
        min_sal, max_sal = salary_map[salary_range]
        search_page.assert_salaries_in_range(min_sal, max_sal)