import unittest
import json
import tempfile
import os
import sys
import shutil
from unittest.mock import patch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from src import app
from src.data_store import read, write
from flask_jwt_extended import create_access_token

class TestDataStore(unittest.TestCase):

    def setUp(self):
        # Create temporary database file for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Set DATA_STORE_PATH to our temp database
        self.env_patcher = patch.dict(os.environ, {'DATA_STORE_PATH': self.db_path})
        self.env_patcher.start()

        # Re-import data_store to pick up the new environment variable
        import importlib
        import src.data_store
        importlib.reload(src.data_store)
        from src.data_store import read, write
        globals()['read'] = read
        globals()['write'] = write

        # Test data
        self.test_user_id = 'testuser1'
        self.test_data = {'key': 'value', 'data': [1, 2, 3]}
        self.empty_data = {}
        self.none_data = None

    def tearDown(self):
        self.env_patcher.stop()
        # Clean up temp database file
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_write_valid_data(self):
        """Test writing valid data"""
        status, code = write(self.test_data, self.test_user_id)
        self.assertEqual(status, 'ok')
        self.assertEqual(code, 200)

        # Verify data was stored and can be read back
        data, read_code = read(self.test_user_id)
        self.assertEqual(read_code, 200)
        self.assertEqual(data, self.test_data)

    def test_write_empty_data(self):
        """Test writing empty dictionary"""
        status, code = write(self.empty_data, self.test_user_id)
        self.assertEqual(status, 'ok')
        self.assertEqual(code, 200)

        data, read_code = read(self.test_user_id)
        self.assertEqual(read_code, 200)
        self.assertEqual(data, {})

    def test_write_none_data(self):
        """Test writing None data (should be converted to empty dict)"""
        status, code = write(self.none_data, self.test_user_id)
        self.assertEqual(status, 'ok')
        self.assertEqual(code, 200)

        data, read_code = read(self.test_user_id)
        self.assertEqual(read_code, 200)
        self.assertEqual(data, {})

    def test_write_complex_data(self):
        """Test writing complex nested data"""
        complex_data = {
            'users': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}],
            'settings': {'theme': 'dark', 'notifications': True},
            'timestamp': '2025-11-10T16:59:40'
        }
        status, code = write(complex_data, self.test_user_id)
        self.assertEqual(status, 'ok')
        self.assertEqual(code, 200)

        data, read_code = read(self.test_user_id)
        self.assertEqual(read_code, 200)
        self.assertEqual(data, complex_data)

    def test_read_existing_user(self):
        """Test reading existing user data"""
        write(self.test_data, self.test_user_id)
        data, code = read(self.test_user_id)
        self.assertEqual(code, 200)
        self.assertEqual(data, self.test_data)

    def test_read_nonexistent_user(self):
        """Test reading non-existent user"""
        data, code = read('nonexistent_user')
        self.assertEqual(code, 404)
        self.assertEqual(data, 'User not found')

    def test_read_after_write_overwrite(self):
        """Test overwriting existing data"""
        # Write initial data
        write({'initial': 'data'}, self.test_user_id)

        # Overwrite with new data
        new_data = {'updated': 'data', 'version': 2}
        write(new_data, self.test_user_id)

        # Read should return new data
        data, code = read(self.test_user_id)
        self.assertEqual(code, 200)
        self.assertEqual(data, new_data)

    def test_multiple_users_isolation(self):
        """Test that different users have isolated data"""
        user1_data = {'user': 'user1', 'value': 100}
        user2_data = {'user': 'user2', 'value': 200}

        write(user1_data, 'user1')
        write(user2_data, 'user2')

        data1, code1 = read('user1')
        data2, code2 = read('user2')

        self.assertEqual(code1, 200)
        self.assertEqual(code2, 200)
        self.assertEqual(data1, user1_data)
        self.assertEqual(data2, user2_data)
        self.assertNotEqual(data1, data2)

    def test_database_file_creation(self):
        """Test that database file is created"""
        # Write some data to ensure database is created
        write(self.test_data, self.test_user_id)

        # Check if database file exists
        self.assertTrue(os.path.exists(self.db_path))

    def test_environment_variable_data_store_path(self):
        """Test that DATA_STORE_PATH environment variable is respected"""
        # With our mocking, data should go to temp_db
        write(self.test_data, self.test_user_id)

        # Verify we can read it back
        data, code = read(self.test_user_id)
        self.assertEqual(code, 200)
        self.assertEqual(data, self.test_data)


class TestAPI(unittest.TestCase):

    def setUp(self):
        # Create temporary database file for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Set up test environment variables
        test_env = {
            'DATA_STORE_PATH': self.db_path,
            'JWT_SECRET': 'test_secret_key',
            'JWT_USERS': 'testuser1,testuser2',
            'PORT': '5000',
            'HOST': '127.0.0.1'
        }
        
        self.env_patcher = patch.dict(os.environ, test_env)
        self.env_patcher.start()

        # Create Flask test client
        self.app = app.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Create valid JWT token for testuser1
        with self.app.app_context():
            self.valid_token = create_access_token(identity='testuser1')

        # Test data
        self.test_user_id = 'testuser1'
        self.test_data = {'key': 'value', 'data': [1, 2, 3]}

    def tearDown(self):
        self.env_patcher.stop()
        # Clean up temp database file
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_test_endpoint(self):
        """Test the /test endpoint (no auth required)"""
        response = self.client.get('/test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'ok')

    def test_sync_get_unauthorized(self):
        """Test GET /api/sync without token"""
        response = self.client.get('/api/sync')
        self.assertEqual(response.status_code, 422)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Missing or invalid token')

    def test_sync_get_invalid_token(self):
        """Test GET /api/sync with invalid token"""
        headers = {'Authorization': 'Bearer invalid_token'}
        response = self.client.get('/api/sync', headers=headers)
        self.assertEqual(response.status_code, 422)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Invalid token')

    def test_sync_get_valid_token_nonexistent_user(self):
        """Test GET /api/sync with valid token but nonexistent user data"""
        # Use testuser2 who is authorized but has no data written yet
        with self.app.app_context():
            token = create_access_token(identity='testuser2')
        
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/api/sync', headers=headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'User not found')

    def test_sync_put_valid_token(self):
        """Test PUT /api/sync with valid token"""
        headers = {'Authorization': f'Bearer {self.valid_token}'}
        response = self.client.put('/api/sync', 
                                 json=self.test_data, 
                                 headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'ok')

    def test_sync_get_after_put(self):
        """Test GET /api/sync after PUT to verify data persistence"""
        # First PUT some data
        headers = {'Authorization': f'Bearer {self.valid_token}'}
        self.client.put('/api/sync', json=self.test_data, headers=headers)
        
        # Then GET it back
        response = self.client.get('/api/sync', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, self.test_data)

    def test_sync_post_valid_token(self):
        """Test POST /api/sync with valid token (test endpoint)"""
        headers = {'Authorization': f'Bearer {self.valid_token}'}
        response = self.client.post('/api/sync', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'test ok')

    def test_sync_put_unauthorized_user(self):
        """Test PUT /api/sync with token for unauthorized user"""
        # Create token for unauthorized user
        with self.app.app_context():
            unauthorized_token = create_access_token(identity='unauthorized_user')
        
        headers = {'Authorization': f'Bearer {unauthorized_token}'}
        response = self.client.put('/api/sync', 
                                 json=self.test_data, 
                                 headers=headers)
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Unauthorized!')

    def test_sync_unsupported_method(self):
        """Test unsupported HTTP method on /api/sync"""
        headers = {'Authorization': f'Bearer {self.valid_token}'}
        response = self.client.patch('/api/sync', headers=headers)
        self.assertEqual(response.status_code, 405)
        # Flask returns HTML error page for 405, not JSON
        self.assertIn(b'Method Not Allowed', response.data)


if __name__ == '__main__':
    unittest.main()
