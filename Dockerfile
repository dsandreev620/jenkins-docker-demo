# Используем официальный легкий образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код в контейнер
COPY . .

# Запускаем тесты через python -m pytest (это надежнее)
RUN python -m pytest tests/ -v

# Команда по умолчанию при запуске контейнера
CMD ["python", "-m", "pytest", "tests/", "-v"]