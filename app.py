from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Venkydeexu18'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    topics = db.Column(db.String(200), nullable=False)

class CompletedTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    topic = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    task_date_str = request.form['task_date']
    task_date = datetime.strptime(task_date_str, '%Y-%m-%d').date()
    topics = request.form['topics']
    new_task = Task(date=task_date, topics=topics)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/tasks', methods=['POST', 'GET'])
def get_tasks():
    if request.method == 'POST':
        assigned_date_str = request.form['assigned_date']
        assigned_date = datetime.strptime(assigned_date_str, '%Y-%m-%d').date()
        assigned_tasks = Task.query.filter_by(date=assigned_date).all()
        completed_tasks = CompletedTask.query.filter_by(date=assigned_date).all()
        return render_template('tasks.html', assigned_date=assigned_date, assigned_tasks=assigned_tasks, completed_tasks=completed_tasks)
    else:
        return render_template('tasks.html', assigned_date=None, assigned_tasks=None, completed_tasks=None)

@app.route('/complete_task', methods=['POST'])
def complete_task():
    completion_date_str = request.form['completion_date']
    completion_date = datetime.strptime(completion_date_str, '%Y-%m-%d').date()
    topic = request.form['topics']
    completed_task = CompletedTask(date=completion_date, topic=topic)
    db.session.add(completed_task)
    db.session.commit()
    pending_tasks = Task.query.filter_by(date=completion_date).all()
    for task in pending_tasks:
        if task.topics == topic:
            try:
                db.session.delete(task)
                db.session.commit()
            except Exception as e:
                print("Error occurred during deletion:", e)
    return redirect(url_for('get_tasks'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

