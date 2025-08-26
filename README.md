# Task Manager Application

----- CORRECT UI WITH TEST CASES -------

<img width="1870" height="884" alt="Screenshot 2025-08-26 123841" src="https://github.com/user-attachments/assets/c290c3e0-0bcb-4e31-9003-d1c0fc8bac16" />

A simple task management web application built with Flask (backend) and vanilla HTML/CSS/JavaScript (frontend).

## Features

- Create new tasks
- Mark tasks as completed
- Delete tasks
- View task statistics (total, completed, pending)
- Real-time task management with a clean web interface

## Project Structure

```
carbon-arc/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile         # Backend Docker configuration
│   
├── frontend/
│   ├── index.html         # Main web interface
│   
│   ├── style.css          
│   ├── script.js          
│   ├── templates/         
│   └── Dockerfile         
└── docker-compose.yml    
```

## API Endpoints

- `GET /` - Serve the web interface
- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `PUT /tasks/<id>/complete` - Mark a task as completed
- `DELETE /tasks/<id>` - Delete a task
- `GET /tasks/stats` - Get task statistics

## Quick Start

### Option 1: Run with Python directly

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   Open your browser and go to `http://127.0.0.1:5001`

### Option 2: Run with Docker Compose

1. **Build and run:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   Open your browser and go to `http://localhost:5000`

## Development

### Running Tests

```bash
cd backend
python -m pytest tests/
# or
python -m unittest tests/test_app.py
```

### API Usage Examples

**Create a task:**
```bash
curl -X POST http://127.0.0.1:5001/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My new task"}'
```

**Get all tasks:**
```bash
curl http://127.0.0.1:5001/tasks
```

**Complete a task:**
```bash
curl -X PUT http://127.0.0.1:5001/tasks/1/complete
```

**Delete a task:**
```bash
curl -X DELETE http://127.0.0.1:5001/tasks/1
```

**Get statistics:**
```bash
curl http://127.0.0.1:5001/tasks/stats
```

## Task Data Structure

```json
{
  "id": 1,
  "title": "Task title",
  "completed": false
}
```

## Technologies Used

- **Backend:** Python, Flask, Flask-CORS
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Development:** Docker, Docker Compose
- **Testing:** Python unittest

## Notes

- The application runs on port 5001 by default when running with Python directly
- When using Docker Compose, the application is accessible on port 5000
- The application includes CORS support for frontend-backend communication
- All data is stored in memory and will be lost when the server restarts

