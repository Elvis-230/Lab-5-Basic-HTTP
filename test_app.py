import unittest
import json
from app import app

class TestPubSub(unittest.TestCase):
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True
    
    def tearDown(self):
        """Clear subscribers after each test"""
        from app import subscribers
        subscribers.clear()
    
    # Tests for adding subscribers
    def test_add_subscriber_success(self):
        """Test adding a subscriber successfully"""
        response = self.client.post('/subscribe',
            data=json.dumps({'name': 'Alice', 'url': 'http://localhost:3000'}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('added successfully', response.get_json()['message'])
    
    def test_add_subscriber_missing_name(self):
        """Test adding subscriber without name"""
        response = self.client.post('/subscribe',
            data=json.dumps({'url': 'http://localhost:3000'}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing', response.get_json()['error'])
    
    def test_add_subscriber_missing_url(self):
        """Test adding subscriber without URL"""
        response = self.client.post('/subscribe',
            data=json.dumps({'name': 'Alice'}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    # Tests for listing subscribers
    def test_list_subscribers_empty(self):
        """Test listing when no subscribers exist"""
        response = self.client.get('/subscribers')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['subscribers'], {})
    
    def test_list_subscribers_multiple(self):
        """Test listing multiple subscribers"""
        # Add subscribers
        self.client.post('/subscribe',
            data=json.dumps({'name': 'Alice', 'url': 'http://localhost:3000'}),
            content_type='application/json')
        self.client.post('/subscribe',
            data=json.dumps({'name': 'Bob', 'url': 'http://localhost:3001'}),
            content_type='application/json')
        
        response = self.client.get('/subscribers')
        data = response.get_json()['subscribers']
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertIn('Alice', data)
        self.assertIn('Bob', data)
    
    # Tests for deleting subscribers
    def test_delete_subscriber_success(self):
        """Test deleting an existing subscriber"""
        # Add a subscriber
        self.client.post('/subscribe',
            data=json.dumps({'name': 'Alice', 'url': 'http://localhost:3000'}),
            content_type='application/json')
        
        # Delete it
        response = self.client.delete('/unsubscribe',
            data=json.dumps({'name': 'Alice'}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('deleted successfully', response.get_json()['message'])
    
    def test_delete_subscriber_not_found(self):
        """Test deleting a non-existent subscriber"""
        response = self.client.delete('/unsubscribe',
            data=json.dumps({'name': 'NonExistent'}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
    
    def test_delete_subscriber_missing_name(self):
        """Test deleting without providing name"""
        response = self.client.delete('/unsubscribe',
            data=json.dumps({}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    # Tests for publishing
    def test_publish_success(self):
        """Test publishing a subject"""
        response = self.client.post('/publish',
            data=json.dumps({'subject': 'Breaking News!'}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['subject'], 'Breaking News!')
    
    def test_publish_to_subscribers(self):
        """Test publishing notifies subscribers"""
        # Add subscribers
        self.client.post('/subscribe',
            data=json.dumps({'name': 'Alice', 'url': 'http://localhost:3000'}),
            content_type='application/json')
        self.client.post('/subscribe',
            data=json.dumps({'name': 'Bob', 'url': 'http://localhost:3001'}),
            content_type='application/json')
        
        # Publish
        response = self.client.post('/publish',
            data=json.dumps({'subject': 'Update'}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Published to 2 subscriber(s)')
    
    def test_publish_missing_subject(self):
        """Test publishing without subject"""
        response = self.client.post('/publish',
            data=json.dumps({}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()