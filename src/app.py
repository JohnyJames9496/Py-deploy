import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

db_url = os.environ.get("DB_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}: {self.text}>'

with app.app_context():
    try:
        db.create_all()
        print("Database tables created or already exist")
    except Exception as e:
        print(f"Warning: Could not create tables on startup: {e}")

@app.route('/')
def index():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task_text')
    if task_text:
        new_task = Todo(text=task_text)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))
