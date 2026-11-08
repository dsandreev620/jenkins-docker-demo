from flask import Flask
import sys
import os

# Добавляем папку src в пути поиска, чтобы импортировать функции
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from main import add, multiply

app = Flask(__name__)

@app.route('/')
def home():
    return "Приложение успешно развернуто! Перейти на /add/?/? для сложения и /multiply/?/? для умножения."

@app.route('/add/<int:a>/<int:b>')
def add_route(a, b):
    return f"Результат сложения: {add(a, b)}"

if __name__ == '__main__':
    # Запускаем сервер на всех интерфейсах, чтобы он был доступен извне контейнера
    app.run(host='0.0.0.0', port=5000)