import pytest
import allure


@allure.feature("Авторизация")
@allure.story("Ошибка авторизации")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тест авторизации с невалидными данными")
def test_valid_login(login_page):
    login_page.navigate()
    login_page.login('invalid_user', 'invalid_password')
    
    assert login_page.get_error_message() == 'Invalid credentials. Please try again.'

@pytest.mark.parametrize('username, password', [
    ('user', 'user'),
    ('admin', 'admin')
])
@allure.feature("Авторизация")
@allure.story("Успешный вход")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тест авторизации с валидными данными")
def test_login_success(login_page, dashboard_page, username, password):
    login_page.navigate()
    login_page.login(username, password)

    dashboard_page.assert_welcome_messages('Welcome to Dashboard')
