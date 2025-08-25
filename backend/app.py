from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os


app = Flask(__name__, static_folder='../frontend/static')
CORS(app)

"""
TASK DATA STRUCTURE:

{
  "id": "int or string",
  "title": "string", 
  "completed": "boolean"
}

"""

tasks = {}
task_id = 1

# -- endpoints --

@app.route('/')
def index():
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
        print(f"Trying to serve: {frontend_path}")
        with open(frontend_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/html'}
    except Exception as e:
        print(f"Error serving index.html: {e}")
        return f"Error: {e}", 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # return all tasks
    return jsonify(list(tasks.values())), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    # create a new task
    data = request.get_json()

    # make sure title is provided
    if not data or 'title' not in data or not data['title'].strip():
        return jsonify({'error': 'Title is required'}), 400
    
    global task_id
    task = {
        'id': task_id,
        'title': data['title'].strip(),
        'completed': False
    }
    
    tasks[task_id] = task
    task_id += 1
    
    return jsonify(task), 201

@app.route('/tasks/<id>/complete', methods=['PUT'])
def complete_task(id):
    # mark a task as completed
    task_id_int = int(id)
    if task_id_int not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    tasks[task_id_int]['completed'] = True
    return jsonify(tasks[task_id_int]), 200
    

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    # delete a task
    task_id_int = int(id)
    if task_id_int not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    deleted_task = tasks.pop(task_id_int)
    return jsonify({'message': 'Task deleted successfully'}), 200
    

@app.route('/tasks/stats', methods=['GET'])
def get_stats():
    # return task statistics
    all_tasks = list(tasks.values())
    total = len(all_tasks)
    completed = sum(1 for task in all_tasks if task['completed'])
    pending = total - completed
    
    return jsonify({
        'total': total,
        'completed': completed,
        'pending': pending
    }), 200
    

if __name__ == '__main__':
    tasks[1] = {'id': 1, 'title': 'Test Title 1', 'completed': False}
    tasks[2] = {'id': 2, 'title': 'Testing Title 2', 'completed': True}
    task_id = 3
    
    print("Start API on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True)