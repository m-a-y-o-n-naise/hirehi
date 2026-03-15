import pytest
import allure
from test.hirehi.pages.mail_tm_page import MailTmHelper


@allure.feature("Авторизация")
@allure.story("Ошибка авторизации")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тест получения ссылки для входа с невалидными данными")
def test_valid_login(login_page):
    login_page.navigate()
    login_page.get_link_login('некорректный_email')

    assert login_page.get_error_message() == 'Введите корректный email'

@allure.feature("Авторизация")
@allure.story("Успешный вход")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тест авторизации с валидными данными")
def test_login_success(login_page, dashboard_page):
    login_page.navigate()
    email = MailTmHelper().create_account()
    login_page.get_link_login(email)

    assert login_page.get_error_message() == 'Письмо со ссылкой отправлено! Если не пришло – проверьте спам'
    dashboard_page.assert_welcome_messages('Welcome to Dashboard')