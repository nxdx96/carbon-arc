class TaskManager {
    constructor() {
        // Use localhost for development, can be changed to backend service name if needed
        this.apiUrl = 'http://localhost:5001';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadTasks();
        this.loadStats();
    }

    bindEvents() {
        document.getElementById('add-task-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTask();
        });
    }

    async apiCall(endpoint, options = {}) {
        try {
            this.showLoading(true);
            const response = await fetch(`${this.apiUrl}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            
            return data;
        } catch (error) {
            this.showError(error.message);
            throw error;
        } finally {
            this.showLoading(false);
        }
    }

    async loadTasks() {
        try {
            const tasks = await this.apiCall('/tasks');
            this.renderTasks(tasks);
            this.loadStats(); // Update stats after loading tasks
        } catch (error) {
            console.error('Error loading tasks:', error);
        }
    }

    async loadStats() {
        try {
            const stats = await this.apiCall('/tasks/stats');
            this.renderStats(stats);
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    async addTask() {
        const titleInput = document.getElementById('task-title');
        const title = titleInput.value.trim();
        
        if (!title) {
            this.showError('Please enter a task title');
            return;
        }

        try {
            await this.apiCall('/tasks', {
                method: 'POST',
                body: JSON.stringify({ title })
            });
            
            titleInput.value = '';
            this.loadTasks();
            this.hideError();
        } catch (error) {
            console.error('Error adding task:', error);
        }
    }

    async completeTask(taskId) {
        try {
            await this.apiCall(`/tasks/${taskId}/complete`, {
                method: 'PUT'
            });
            
            this.loadTasks();
        } catch (error) {
            console.error('Error completing task:', error);
        }
    }

    async deleteTask(taskId) {
        if (!confirm('Are you sure you want to delete this task?')) {
            return;
        }

        try {
            await this.apiCall(`/tasks/${taskId}`, {
                method: 'DELETE'
            });
            
            this.loadTasks();
        } catch (error) {
            console.error('Error deleting task:', error);
        }
    }

    renderTasks(tasks) {
        const tasksList = document.getElementById('tasks-list');
        const noTasksMessage = document.getElementById('no-tasks-message');
        
        if (tasks.length === 0) {
            tasksList.style.display = 'none';
            noTasksMessage.style.display = 'block';
            return;
        }

        tasksList.style.display = 'flex';
        noTasksMessage.style.display = 'none';
        
        tasksList.innerHTML = tasks.map(task => `
            <div class="task-item ${task.completed ? 'completed' : ''}">
                <div class="task-title">${this.escapeHtml(task.title)}</div>
                <div class="task-status ${task.completed ? 'completed' : 'pending'}">
                    ${task.completed ? 'Completed' : 'Pending'}
                </div>
                <div class="task-actions">
                    ${!task.completed ? `
                        <button class="complete" onclick="taskManager.completeTask(${task.id})">
                            Complete
                        </button>
                    ` : ''}
                    <button class="delete" onclick="taskManager.deleteTask(${task.id})">
                        Delete
                    </button>
                </div>
            </div>
        `).join('');
    }

    renderStats(stats) {
        document.getElementById('total-tasks').textContent = stats.total;
        document.getElementById('completed-tasks').textContent = stats.completed;
        document.getElementById('pending-tasks').textContent = stats.pending;
    }

    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
    }

    showError(message) {
        const errorElement = document.getElementById('error-message');
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        
        // Auto-hide error after 5 seconds
        setTimeout(() => this.hideError(), 5000);
    }

    hideError() {
        document.getElementById('error-message').style.display = 'none';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.taskManager = new TaskManager();
});
