from test.hirehi.pages.login_page import LoginPage
from test.hirehi.pages.dashboard_page import DashboardPages


def test_valid_login(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login('invalid_user', 'invalid_password')
    
    assert login_page.get_error_message() == 'Invalid credentials. Please try again.'

def test_login_success(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPages(page)

    login_page.navigate()
    login_page.login('valid_user', 'valid_password')

    dashboard_page.assert_welcome_messages('Welcome to Dashboard')
