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
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = int(os.environ.get('APP_PORT', 5000))
    app.run(host=host, port=port)