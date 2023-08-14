# views.py 路由+视图函数

#蓝图
from flask import Blueprint
from .models import *

blue = Blueprint('AA', __name__)

@blue.route('/')
def index():
    return "hello"

@blue.route('/add', methods=['POST'])
def add_todo():
    return
    content = request.form.get('content')
    new_todo = Todo(content=content)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@blue.route('/complete/<int:id>')
def complete_todo(id):
    return
    todo = Todo.query.get(id)
    todo.completed = True
    db.session.commit()
    return redirect(url_for('index'))

@blue.route('/delete/<int:id>')
def delete_todo(id):
    return
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))