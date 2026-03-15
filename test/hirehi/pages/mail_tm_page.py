import requests
import random
import string
import time
import re
from typing import Optional, Dict


class MailTmHelper:
    """Хелпер для работы с временными email через mail.tm API"""

    def __init__(self):
        self.base_url = "https://api.mail.tm"
        self.email = None
        self.password = None
        self.token = None
        self.account_id = None
        self.last_message = None  # сохраняем последнее сообщение
        self.last_html = None  # сохраняем html
        self.last_text = None  # сохраняем текст

    def create_account(self) -> str:
        """Создает временный email аккаунт"""

        domains_response = requests.get(f"{self.base_url}/domains")  # возвращает список доменов для создания email
        domains_response.raise_for_status()  # проверка успешности статуса
        domains = domains_response.json()  # парсим в словарь

        # Берем первый доступный домен из списка по ключу
        domain = domains['hydra:member'][0]['domain']

        # Генерируем уникальный email с хардкорным простым паролем
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        self.email = f"test_{random_string}@{domain}"
        self.password = "Test123!@#"

        account_data = {
            "address": self.email,
            "password": self.password
        }
        account_response = requests.post(
            f"{self.base_url}/accounts",
            json=account_data
        )  # регистрирует новый почтовый ящик, application/json передается благодаря "json="
        account_response.raise_for_status()  # проверка успешности статуса
        account_info = account_response.json()  # парсим в словарь
        self.account_id = account_info['id']

        token_response = requests.post(
            f"{self.base_url}/token",
            json=account_data
        )
        token_response.raise_for_status()
        self.token = token_response.json()['token']  # получаем токен для доступа к письмам

        print(f"Создан временный email: {self.email}")
        return self.email

    def wait_for_message(self, sender_domain: str = None, timeout: int = 60) -> Optional[Dict]:
        """
        Ожидает появления нового письма
        Возвращает сообщение или None, если письмо не получено
        При этом указываем отправителя или сами, при запросе функции или будет поиск по любому
        """
        headers = {"Authorization": f"Bearer {self.token}"}

        start_time = time.time()
        while time.time() - start_time < timeout:
            messages_response = requests.get(
                f"{self.base_url}/messages",
                headers=headers
            ) #  возвращает все письма в ящике
            messages_response.raise_for_status()  # проверка успешности статуса
            messages_data = messages_response.json()  #  парсим в словарь

            if messages_data['hydra:totalItems'] > 0:  # Проверяем, есть ли письма
                latest_message = messages_data['hydra:member'][0]  # Берем самое новое письмо (первое в списке)

                message_detail = requests.get(
                    f"{self.base_url}/messages/{latest_message['id']}",
                    headers=headers
                )
                message_detail.raise_for_status()
                full_message = message_detail.json()

                self.last_message = full_message
                self.last_html = full_message.get('html', [''])[0] if full_message.get('html') else None
                self.last_text = full_message.get('text', None)

            #  Если указали при запросе отправителя, то
                if sender_domain:
                    sender = full_message.get('from', {}).get('address', '')
                    if '@' in sender:
                        domain = sender.split('@')[1]
                        if sender_domain.lower() == domain.lower():
                            return full_message
                    else:
                        return full_message

            time.sleep(3) # ждем 3 секунды перед следующей проверкой наличия писем

        print(f"Письмо от {sender_domain if sender_domain else 'любого'} не получено за {timeout} сек")
        return None

    def extract_magic_link(self) -> Optional[str]:
        """Извлекает ссылку из последнего сохраненного сообщения"""
        if not self.last_html and not self.last_text:
            print("❌ Нет сохраненного сообщения")
            return None

        url_pattern = r'https?://[^\s"\'<>]+'

        # Ищем в HTML
        if self.last_html:
            links = re.findall(url_pattern, self.last_html)
            if links:
                print(f"Найдена ссылка: {links[0]}")
                return links[0]

        # Ищем в тексте
        if self.last_text:
            links = re.findall(url_pattern, self.last_text)
            if links:
                return links[0]

        print("Ссылка не найдена")
        return None

    def delete_account(self):
        """Удаляет аккаунт после теста"""
        if self.token and self.account_id:
            headers = {"Authorization": f"Bearer {self.token}"}
            requests.delete(
                f"{self.base_url}/accounts/{self.account_id}",
                headers=headers
            )
            print(f"Аккаунт {self.email} удален")