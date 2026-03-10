from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('#username')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('#login')
        self.error_message = page.locator('#errorAlert')

    def navigate(self) -> None:
        self.page.goto("https://hirehi.ru")

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def error_massage(self) -> str:
        return self.error_message.inner_text()
