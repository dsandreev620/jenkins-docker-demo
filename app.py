import os
import sys
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from main import add, multiply

app = Flask(__name__)

db_url = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
if db_url and db_url.startswith('postgresql://'):
    db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "value": self.value}

@app.route('/')
def home():
    return "Приложение успешно развернуто! API: /items"

@app.route('/add/<int:a>/<int:b>')
def add_route(a, b):
    return f"Результат сложения: {add(a, b)}"

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], value=data['value'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

if __name__ == '__main__':
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = int(os.environ.get('APP_PORT', 5000))
    app.run(host=host, port=port)