from playwright.sync_api import Page, expect
import allure


class DashboardPages:
    def __init__(self, page: Page):
        self.page = page
        self.profile = page.locator('#username')
        self.logout = page.locator('#logout')

    def assert_welcome_messages(self, message):
        with allure.step(f"Проверка приветствия '{message}'"):
            expect(self.profile).to_have_text(message)

    def logout_user(self) -> None:
        with allure.step("Выход из системы"):
            self.logout.click()
            expect(self.page).to_have_url("**/login")