# helpers/mailtm_helper.py
import requests
import time
import re
from typing import Optional, Dict, List


class MailTmHelper:
    """Хелпер для работы с временными email через mail.tm API"""

    def __init__(self):
        self.base_url = "https://api.mail.tm"
        self.email = None
        self.password = None
        self.token = None
        self.account_id = None

    def create_account(self) -> str:
        """Создает временный email аккаунт"""
        # Шаг 1: Получаем доступные домены
        # GET /domains - возвращает список доменов для создания email
        domains_response = requests.get(f"{self.base_url}/domains")
        domains_response.raise_for_status()
        domains = domains_response.json()

        # Берем первый доступный домен (например @cliptik.net или @mail.tm)
        domain = domains['hydra:member'][0]['domain']

        # Генерируем уникальный email
        import random
        import string
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.email = f"test_{random_string}@{domain}"
        self.password = "Test123!@#"  # Простой пароль для тестов

        # Шаг 2: Создаем аккаунт
        # POST /accounts - регистрирует новый почтовый ящик
        account_data = {
            "address": self.email,
            "password": self.password
        }
        account_response = requests.post(
            f"{self.base_url}/accounts",
            json=account_data
        )
        account_response.raise_for_status()
        account_info = account_response.json()
        self.account_id = account_info['id']

        # Шаг 3: Получаем токен для доступа к письмам
        # POST /token - аутентификация и получение JWT токена
        token_data = {
            "address": self.email,
            "password": self.password
        }
        token_response = requests.post(
            f"{self.base_url}/token",
            json=token_data
        )
        token_response.raise_for_status()
        self.token = token_response.json()['token']

        print(f"✅ Создан временный email: {self.email}")
        return self.email

    def wait_for_message(self, from_sender: str = None, timeout: int = 60) -> Optional[Dict]:
        """
        Ожидает появления нового письма
        Возвращает сообщение или None, если письмо не получено
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Шаг 4: Получаем список писем
            # GET /messages - возвращает все письма в ящике
            messages_response = requests.get(
                f"{self.base_url}/messages",
                headers=headers
            )
            messages_response.raise_for_status()
            messages_data = messages_response.json()

            # Проверяем, есть ли письма
            if messages_data['hydra:totalItems'] > 0:
                # Берем самое новое письмо (первое в списке)
                latest_message = messages_data['hydra:member'][0]

                # Если указан отправитель, проверяем соответствие
                if from_sender:
                    # Получаем детальную информацию о письме
                    # GET /messages/{id} - получает конкретное письмо
                    message_detail = requests.get(
                        f"{self.base_url}/messages/{latest_message['id']}",
                        headers=headers
                    )
                    message_detail.raise_for_status()
                    full_message = message_detail.json()

                    # Проверяем отправителя
                    if from_sender.lower() in full_message.get('from', {}).get('address', '').lower():
                        return full_message
                else:
                    return latest_message

            # Ждем 3 секунды перед следующей проверкой
            time.sleep(3)

        print(f"⏰ Письмо от {from_sender if from_sender else 'любого'} не получено за {timeout} сек")
        return None

    def extract_magic_link(self, message: Dict) -> Optional[str]:
        """Извлекает ссылку из письма"""
        # Получаем HTML или текст письма
        html_content = message.get('html', [''])[0]
        text_content = message.get('text', [''])[0]

        # Ищем ссылки в HTML
        # Паттерн для поиска URL (http:// или https://)
        url_pattern = r'https?://[^\s"\'<>]+'

        if html_content:
            links = re.findall(url_pattern, html_content)
            if links:
                # Обычно magic link - это длинная ссылка с токеном
                # Берем первую (или можно фильтровать по наличию определенных параметров)
                magic_link = links[0]
                print(f"🔗 Найдена ссылка: {magic_link}")
                return magic_link

        if text_content:
            links = re.findall(url_pattern, text_content)
            if links:
                return links[0]

        print("❌ Ссылка не найдена в письме")
        return None

    def delete_account(self):
        """Удаляет аккаунт после теста (чистим за собой)"""
        if self.token and self.account_id:
            headers = {"Authorization": f"Bearer {self.token}"}
            # DELETE /accounts/{id} - удаляет аккаунт
            requests.delete(
                f"{self.base_url}/accounts/{self.account_id}",
                headers=headers
            )
            print(f"🗑️ Аккаунт {self.email} удален")


# tests/test_auth.py
import pytest
from pages.login_page import LoginPage
from helpers.mailtm_helper import MailTmHelper


class TestAuth:

    def test_magic_link_login(self, page):
        # 1. СОЗДАЕМ ВРЕМЕННЫЙ EMAIL
        # Создаем экземпляр хелпера
        mail_helper = MailTmHelper()

        # Создаем аккаунт и получаем email
        # Внутри происходит:
        # - GET /domains (получаем домен)
        # - POST /accounts (создаем ящик)
        # - POST /token (получаем токен)
        test_email = mail_helper.create_account()
        print(f"📧 Используем email: {test_email}")

        try:
            # 2. ВХОДИМ НА САЙТ ВАКАНСИЙ
            # Открываем страницу логина
            login_page = LoginPage(page)
            login_page.navigate()  # переходим на сайт вакансий

            # Вводим email и отправляем magic link
            login_page.enter_email(test_email)  # вводим наш временный email
            login_page.submit()  # нажимаем "Отправить ссылку"

            # 3. ЖДЕМ ПИСЬМО ЧЕРЕЗ MAIL.TM API
            # Ожидаем письмо от сервиса вакансий
            # Внутри циклически вызывает GET /messages
            message = mail_helper.wait_for_message(
                from_sender="noreply@ваш-сайт-вакансий.ru",  # от кого ждем письмо
                timeout=60  # ждем до 60 секунд
            )

            # Проверяем, что письмо получено
            assert message is not None, "Письмо не пришло!"

            # 4. ИЗВЛЕКАЕМ ССЫЛКУ ИЗ ПИСЬМА
            # Парсим HTML письма и ищем URL
            magic_link = mail_helper.extract_magic_link(message)
            assert magic_link is not None, "Ссылка не найдена в письме!"

            # 5. ПЕРЕХОДИМ ПО MAGIC LINK
            # Переходим по ссылке в ТОМ ЖЕ браузере
            page.goto(magic_link)

            # 6. ПРОВЕРЯЕМ УСПЕШНУЮ АВТОРИЗАЦИЮ
            # Проверяем, что мы авторизованы
            assert page.is_visible(".user-profile"), "Пользователь не авторизован!"
            assert page.is_visible(f"text={test_email}"), "Email пользователя не отображается!"

        finally:
            # 7. ЧИСТИМ ЗА СОБОЙ
            # Удаляем временный аккаунт
            mail_helper.delete_account()


# pages/login_page.py
class LoginPage:
    """Page Object для страницы входа на сайте вакансий"""

    def __init__(self, page):
        self.page = page
        # Локаторы (подставь свои)
        self.email_input = page.locator("#email")  # поле ввода email
        self.submit_button = page.locator("button[type='submit']")  # кнопка отправки
        self.success_message = page.locator(".success-message")  # сообщение об успехе

    def navigate(self):
        """Открывает страницу логина"""
        self.page.goto("https://ваш-сайт-вакансий.ru/login")
        # Ждем загрузки страницы
        self.email_input.wait_for(state="visible")

    def enter_email(self, email: str):
        """Вводит email"""
        self.email_input.fill(email)

    def submit(self):
        """Отправляет форму"""
        self.submit_button.click()
        # Ждем сообщения об отправке письма
        self.success_message.wait_for(state="visible", timeout=10000)

    def enter_email_and_submit(self, email: str):
        """Комбо-метод: ввод email и отправка"""
        self.enter_email(email)
        self.submit()