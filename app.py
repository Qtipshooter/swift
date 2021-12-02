# SWIFT Taskbook
# Web Application for Task Management 

# flask web objects
from flask import Flask
from flask import render_template
from flask import request

# the base Flask object
app = Flask(__name__)

# ---------------------------
# web application routes
# ---------------------------

@app.get('/')
@app.get('/tasks')
def tasks():
    return render_template("tasks.html") 

@app.get('/tasks-w3')
def tasks_w3():
    return render_template("tasks-w3.html") 

@app.get('/login')
def login():
    return render_template("login.html") 

@app.get('/register')
def register():
    return render_template("register.html") 

# ---------------------------
# task REST api 
# ---------------------------

import json
import dataset
import time

taskbook_db = dataset.connect('sqlite:///taskbook.db')  

@app.get('/api/tasks')
def get_tasks():
    'return a list of tasks sorted by submit/modify time'
    task_table = taskbook_db.get_table('task')
    tasks = [dict(x) for x in task_table.find(order_by='time')]
    return { "tasks": tasks }

@app.post('/api/tasks',)
def create_task():
    'create a new task in the database'
    try:
        data = request.get_json()
        for key in data.keys():
            assert key in ["description","list"], f"Illegal key '{key}'"
        assert type(data['description']) is str, "Description is not a string."
        assert len(data['description'].strip()) > 0, "Description is length zero."
        assert data['list'] in ["today","tomorrow"], "List must be 'today' or 'tomorrow'"
    except Exception as e:
        print(400, str(e))
        return ("400 Bad Request:"+str(e), 400)
    try:
        task_table = taskbook_db.get_table('task')
        task_table.insert({
            "time": time.time(),
            "description":data['description'].strip(),
            "list":data['list'],
            "completed":False
        })
    except Exception as e:
        print(409, str(e))
        return ("409 Bad Request:"+str(e), 409)
    # return Success
    return {'status':200, 'success': True}

@app.put('/api/tasks')
def update_task():
    'update properties of an existing task in the database'
    try:
        data = request.get_json()
        for key in data.keys():
            assert key in ["id","description","completed","list"], f"Illegal key '{key}'"
        assert type(data['id']) is int, f"id '{id}' is not int"
        if "description" in data:
            assert type(data['description']) is str, "Description is not a string."
            assert len(data['description'].strip()) > 0, "Description is length zero."
        if "completed" in data:
            assert type(data['completed']) is bool, "Completed is not a bool."
        if "list" in data:
            assert data['list'] in ["today","tomorrow"], "List must be 'today' or 'tomorrow'"
    except Exception as e:
        print(400, str(e))
        return ("400 Bad Request:"+str(e), 400)
    if 'list' in data: 
        data['time'] = time.time()
    try:
        task_table = taskbook_db.get_table('task')
        task_table.update(row=data, keys=['id'])
    except Exception as e:
        print(409, str(e))
        return ("409 Bad Request:"+str(e), 409)
    # return Success
    return {'status':200, 'success': True}

@app.delete('/api/tasks')
def delete_task():
    'delete an existing task in the database'
    try:
        data = request.get_json()
        assert type(data['id']) is int, f"id '{id}' is not int"
    except Exception as e:
        print(400, str(e))
        return ("400 Bad Request:"+str(e), 400)
    try:
        task_table = taskbook_db.get_table('task')
        task_table.delete(id=data['id'])
    except Exception as e:
        print(409, str(e))
        return ("409 Bad Request:"+str(e), 409)
    # return Success
    return {'status':200, 'success': True}