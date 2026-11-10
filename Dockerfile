FROM python:3.11-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Переменная окружения для Flask
ENV APP_HOST=0.0.0.0

# Применяем миграции и запускаем приложение одной командой.
CMD alembic upgrade head && python app.py