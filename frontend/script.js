const API_URL = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', function() {
    loadTasks();
    loadStats();
    
    // Add this event listener
    document.getElementById('addTaskBtn').addEventListener('click', addTask);
    
    document.getElementById('taskInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTask();
        }
    });
});

// load tasks from API and display in a table
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        const tasks = await response.json();
        
        const tasksBody = document.getElementById('tasksBody');
        
        if (tasks.length === 0) {
            tasksBody.innerHTML = '<tr><td colspan="4" class="no-tasks">No tasks yet. Add one above!</td></tr>';
            return;
        }

        // create table rows for each task
        tasksBody.innerHTML = tasks.map(task => `
            <tr>
                <td>${task.id}</td>
                <td class="${task.completed ? 'task-completed' : ''}">${task.title}</td>
                <td>
                    <span class="${task.completed ? 'status-completed' : 'status-pending'}">
                        ${task.completed ? 'Completed' : 'Pending'}
                    </span>
                </td>
                <td>
                    <div class="action-buttons">
                        ${!task.completed ? 
                            `<button class="complete-btn" onclick="completeTask(${task.id})">Complete</button>` : 
                            '<span class="completed-text">✓ Done</span>'
                        }
                        <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
                    </div>
                </td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error loading tasks:', error);
        showError('Could not load tasks. Make sure the backend is running.');
        document.getElementById('tasksBody').innerHTML = 
            '<tr><td colspan="4" class="error">Failed to load tasks</td></tr>';
    }
}

// statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/tasks/stats`);
        const stats = await response.json();
        
        document.getElementById('total').textContent = stats.total;
        document.getElementById('completed').textContent = stats.completed;
        document.getElementById('pending').textContent = stats.pending;
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// add new task
async function addTask() {
    const input = document.getElementById('taskInput');
    const title = input.value.trim();

    if (!title) {
        showError('Please enter a task title');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: title })
        });

        

        // on success, clear input and refresh tasks and stats
        if (response.ok) {
            input.value = ''; 
            hideError();
            loadTasks(); 
            loadStats(); 
        } else {
            const errorData = await response.json();
            showError(errorData.error || 'Failed to add task');
        }
    } catch (error) {
        console.error('Error adding task:', error);
        showError('Could not add task. Make sure the backend is running.');
    }
}

// complete task
async function completeTask(id) {
    try {
        const response = await fetch(`${API_URL}/tasks/${id}/complete`, {
            method: 'PUT'
        });

        // on success, refresh tasks and stats
        if (response.ok) {
            loadTasks(); 
            loadStats(); 
        } else {
            showError('Failed to complete task');
        }
    } catch (error) {
        console.error('Error completing task:', error);
        showError('Could not complete task');
    }
}

// delete task
async function deleteTask(id) {
    if (confirm('Are you sure you want to delete this task?')) {
        try {
            const response = await fetch(`${API_URL}/tasks/${id}`, {
                method: 'DELETE'
            });

            // on success, refresh tasks and stats
            if (response.ok) {
                loadTasks(); 
                loadStats(); 
            } else {
                showError('Failed to delete task');
            }
        } catch (error) {
            console.error('Error deleting task:', error);
            showError('Could not delete task');
        }
    }
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Auto-hide error after 5 seconds
    setTimeout(hideError, 5000);
}

// Hide error message
function hideError() {
    const errorDiv = document.getElementById('error');
    errorDiv.style.display = 'none';
}