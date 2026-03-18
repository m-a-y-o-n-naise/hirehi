import pytest
import allure
from test.hirehi.pages.mail_tm_page import MailTmHelper


@allure.feature("Получение ссылки для входа")
@allure.story("Невалидный email")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тест получения ссылки для входа с невалидными данными")
def test_valid_login(login_page):
    login_page.navigate()
    login_page.login_btn_click()
    login_page.get_link_login('некорректный_email')

    assert login_page.get_error_message() == 'Введите корректный email'

@allure.feature("Получение ссылки для входа")
@allure.story("Валидный email")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тест авторизации с валидными данными")
def test_login_success(login_page):
    login_page.navigate()
    login_page.login_btn_click()
    email = MailTmHelper().create_account()
    login_page.get_link_login(email)

    assert login_page.get_error_message() == 'Письмо со ссылкой отправлено! Если не пришло – проверьте спам'

@allure.feature("Авторизация")
@allure.story("Успешный вход")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тест авторизации с валидными данными")
def test_login_success(login_page, page):
    login_page.navigate()
    login_page.login_btn_click()
    mail_helper = MailTmHelper()
    email = mail_helper.create_account()
    login_page.get_link_login(email)

    message = mail_helper.wait_for_message(sender_domain ='hirehi.ru')
    assert message is not None, "Письмо не пришло!"

    magic_link = mail_helper.extract_magic_link()

    # with page.context.expect_page() as new_page_info:
    #     page.get_by_text("Подтвердить регистрацию").click()
    temp_page = page.context.new_page()
    temp_page.set_content(f"<a href='{magic_link}' target='_blank'>Войти</a>")
    with page.context.expect_page() as new_page_info:
        temp_page.get_by_text("Войти").click()
    auth_page = new_page_info.value
    auth_page.wait_for_load_state("networkidle")

    assert magic_link is not None, "Ссылка не найдена в письме!"

    # Ждем появления в DOM
    auth_page.locator('.toast.success.show').first.wait_for(state="attached", timeout=15000)

    toast_text = auth_page.locator('.toast.success.show .toast-message').inner_text()
    assert toast_text == 'Авторизация успешна'