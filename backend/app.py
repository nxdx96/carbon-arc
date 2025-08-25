from flask import Flask, jsonify, request
import json
import pandas as pd

app = Flask(__name__)

"""
TASK DATA STRUCTURE:

{
  "id": "int or string",
  "title": "string", 
  "completed": "boolean"
}

"""

# -- ENDPOINTS --

@app.route('/tasks', methods=['GET'])
def get_tasks():
    
    
    return jsonify(), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    return jsonify(), 201

@app.route('/tasks/<id>/complete', methods=['PUT'])
def complete_task(id):
    
    return jsonify(), 200

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    
    return jsonify(), 200

@app.route('/tasks/stats', methods=['GET'])
def get_stats():
    
    return jsonify(), 200

if __name__ == '__main__':
    app.run(debug=True)