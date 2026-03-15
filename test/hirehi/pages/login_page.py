from playwright.sync_api import Page
import allure


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.entry = page.locator('#btnLogin')
        self.email_login = page.locator('#loginEmailInput')
        self.get_link_log = page.locator('#btnSendMagicLink')
        self.error_message = page.locator('.toast.error.show')  # сообщение об ошибке
        self.success_message = page.locator('.toast.success.show')  # сообщение об успехе

        # закомментил до лучших времен, если появится авторизация по логину и паролю
        # self.username_input = page.locator('#username')
        # self.password_input = page.locator('#password')
        # self.login_button = page.locator('#login')


    def navigate(self) -> None:
        with allure.step('Открыть страницу входа'):
            self.page.goto('https://hirehi.ru')
            self.email_login.wait_for(state="visible")

    def get_link_login(self, email) -> None:
        with allure.step('Ввод почты для получения ссылки'):
            self.email_login.fill(email)
            self.get_link_log.click()

    # def login(self, username: str, password: str) -> None:
    #     with allure.step(f'Авторизация с логином "{username}"'):
    #         with allure.step('Ввод логина'):
    #             self.username_input.fill(username)
    #
    #         with allure.step('Ввод пароля'):
    #             self.password_input.fill(password)
    #
    #         with allure.step('Нажатие кнопки входа'):
    #             self.login_button.click()

    def get_error_message(self) -> str:
        with allure.step('Получение текста ошибки'):
            return self.error_message.inner_text()

    def get_success_message(self) -> str:
        with allure.step('Получение текст успешной отправки'):
            return self.success_message.inner_text()