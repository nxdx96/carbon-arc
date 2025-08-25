import unittest
import json
from app import app

class TaskAPITestCase(unittest.TestCase):
    
    def setUp(self):
        """setup test client"""
        self.app = app.test_client()
        self.app.testing = True
        
        # clear tasks and reset ID counter
        from app import tasks, task_id
        tasks.clear()
        app.task_id = 1

    def test_get_empty_tasks(self):
        #test GET /tasks returns empty list initially
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data, [])

    def test_create_task(self):
        #test POST /tasks creates a new task
        task_data = {'title': 'Test task'}
        response = self.app.post('/tasks', 
                                data=json.dumps(task_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test task')
        self.assertEqual(data['completed'], False)
        self.assertIn('id', data)

    def test_create_task_validation(self):
        """Test POST /tasks validates required fields"""
        # Test empty title
        response = self.app.post('/tasks', 
                                data=json.dumps({'title': ''}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test missing title
        response = self.app.post('/tasks', 
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_complete_task(self):
        """Test PUT /tasks/<id>/complete marks task as completed"""
        # First create a task
        task_data = {'title': 'Task to complete'}
        create_response = self.app.post('/tasks', 
                                       data=json.dumps(task_data),
                                       content_type='application/json')
        created_task = json.loads(create_response.data)
        task_id = created_task['id']
        
        # Complete the task
        response = self.app.put(f'/tasks/{task_id}/complete')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['completed'])

    def test_complete_nonexistent_task(self):
        """Test PUT /tasks/<id>/complete returns 404 for nonexistent task"""
        response = self.app.put('/tasks/999/complete')
        self.assertEqual(response.status_code, 404)

    def test_delete_task(self):
        """Test DELETE /tasks/<id> removes task"""
        # Create a task first
        task_data = {'title': 'Task to delete'}
        create_response = self.app.post('/tasks', 
                                       data=json.dumps(task_data),
                                       content_type='application/json')
        created_task = json.loads(create_response.data)
        task_id = created_task['id']
        
        # Delete the task
        response = self.app.delete(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify task is gone
        get_response = self.app.get('/tasks')
        tasks = json.loads(get_response.data)
        self.assertEqual(len(tasks), 0)

    def test_get_stats(self):
        """Test GET /tasks/stats returns correct statistics"""
        # Create some test tasks
        self.app.post('/tasks', 
                     data=json.dumps({'title': 'Task 1'}),
                     content_type='application/json')
        self.app.post('/tasks', 
                     data=json.dumps({'title': 'Task 2'}),
                     content_type='application/json')
        
        # Complete one task
        self.app.put('/tasks/1/complete')
        
        # Check stats
        response = self.app.get('/tasks/stats')
        self.assertEqual(response.status_code, 200)
        
        stats = json.loads(response.data)
        self.assertEqual(stats['total'], 2)
        self.assertEqual(stats['completed'], 1)
        self.assertEqual(stats['pending'], 1)

    def test_full_crud_workflow(self):
        """Integration test: full CRUD workflow"""
        # 1. Start with empty tasks
        response = self.app.get('/tasks')
        self.assertEqual(len(json.loads(response.data)), 0)
        
        # 2. Create a task
        create_response = self.app.post('/tasks', 
                                       data=json.dumps({'title': 'Integration test task'}),
                                       content_type='application/json')
        self.assertEqual(create_response.status_code, 201)
        task = json.loads(create_response.data)
        
        # 3. Read tasks - should have 1
        get_response = self.app.get('/tasks')
        tasks = json.loads(get_response.data)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], 'Integration test task')
        self.assertFalse(tasks[0]['completed'])
        
        # 4. Update task - mark as complete
        complete_response = self.app.put(f'/tasks/{task["id"]}/complete')
        self.assertEqual(complete_response.status_code, 200)
        
        # 5. Verify completion
        get_response = self.app.get('/tasks')
        updated_tasks = json.loads(get_response.data)
        self.assertTrue(updated_tasks[0]['completed'])
        
        # 6. Check stats
        stats_response = self.app.get('/tasks/stats')
        stats = json.loads(stats_response.data)
        self.assertEqual(stats['total'], 1)
        self.assertEqual(stats['completed'], 1)
        self.assertEqual(stats['pending'], 0)
        
        # 7. Delete task
        delete_response = self.app.delete(f'/tasks/{task["id"]}')
        self.assertEqual(delete_response.status_code, 200)
        
        # 8. Verify deletion
        final_response = self.app.get('/tasks')
        final_tasks = json.loads(final_response.data)
        self.assertEqual(len(final_tasks), 0)

if __name__ == '__main__':
    unittest.main()