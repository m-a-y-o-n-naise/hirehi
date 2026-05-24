FROM python:3.11-slim


# Установка системных зависимостей для Playwright
RUN apt-get update && apt-get install -y \
    unzip \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libatspi2-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Объяснение: дополнительные библиотеки нужны для корректной работы Chromium в Docker


# Установка Playwright и браузеров
RUN pip install playwright
RUN playwright install chromium

# Копирование файла зависимостей и установка Python‑пакетов
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создание рабочей директории и копирование кода приложения
WORKDIR /app
COPY . .

# Опционально: создание непривилегированного пользователя для повышения безопасности
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Указание команды по умолчанию (может быть переопределено при запуске контейнера)
CMD ["python", "-c", "print('Docker image ready for running tests')"]