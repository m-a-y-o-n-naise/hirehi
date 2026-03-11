from playwright.sync_api import Page, expect


class DashboardPages:
    def __init__(self, page: Page):
        self.page = page
        self.profile = page.locator('#username')
        self.logout = page.locator('#logout')

    def assert_welcome_messages(self, message):
        expect(self.profile).to_have_text(message)