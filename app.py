from flask import Flask, render_template, request, jsonify
from task_manager import Task, TaskBuilder, TaskManager

app = Flask(__name__)
task_manager = TaskManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    description = request.form['description']
    due_date = request.form['due_date']
    tags = request.form.getlist('tags[]')

    builder = TaskBuilder(description)
    if due_date:
        builder.set_due_date(due_date)
    if tags:
        builder.add_tags(tags)
    task = builder.build()
    task_manager.add_task(task)
    return jsonify({'message': 'Task added successfully!'})
   

@app.route('/view_tasks')
def view_tasks():
    filter_option = request.args.get('filter_option')

    if filter_option == "completed":
        filtered_tasks = [str(task) for task in task_manager.tasks if task.completed]
    elif filter_option == "pending":
        filtered_tasks = [str(task) for task in task_manager.tasks if not task.completed]
    else:
        filtered_tasks = [str(task) for task in task_manager.tasks]

    return jsonify({'tasks': filtered_tasks})

@app.route('/undo')
def undo():
    task_manager.undo()
    return jsonify({'message': 'Undo successful!'})

if __name__ == "__main__":
    app.run(debug=True)
