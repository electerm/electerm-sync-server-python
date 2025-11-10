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

from src import file_store
from src.file_store import read, write

class TestFileStore(unittest.TestCase):

    def setUp(self):
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp(prefix='test_file_store_')

        # Set FILE_STORE_PATH to our temp directory
        self.env_patcher = patch.dict(os.environ, {'FILE_STORE_PATH': self.temp_dir})
        self.env_patcher.start()

        # Re-import file_store to pick up the new environment variable
        import importlib
        importlib.reload(file_store)
        from src.file_store import read, write
        globals()['read'] = read
        globals()['write'] = write

        # Test data
        self.test_user_id = 'testuser1'
        self.test_data = {'key': 'value', 'data': [1, 2, 3]}
        self.empty_data = {}
        self.none_data = None

    def tearDown(self):
        self.env_patcher.stop()
        # Clean up temp directory
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_write_valid_data(self):
        """Test writing valid data"""
        status, code = write(self.test_data, self.test_user_id)
        self.assertEqual(status, 'ok')
        self.assertEqual(code, 200)

        # Verify file was created and contains correct data
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

    def test_read_existing_file(self):
        """Test reading existing file"""
        write(self.test_data, self.test_user_id)
        data, code = read(self.test_user_id)
        self.assertEqual(code, 200)
        self.assertEqual(data, self.test_data)

    def test_read_nonexistent_file(self):
        """Test reading non-existent file"""
        data, code = read('nonexistent_user')
        self.assertEqual(code, 404)
        self.assertEqual(data, 'File not found')

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

    def test_file_path_construction(self):
        """Test that files are created in the correct location"""
        write(self.test_data, self.test_user_id)

        # Check if file exists in temp directory
        expected_path = os.path.join(self.temp_dir, f"{self.test_user_id}.json")
        self.assertTrue(os.path.exists(expected_path))

        # Verify file contents
        with open(expected_path, 'r') as f:
            file_data = json.load(f)
        self.assertEqual(file_data, self.test_data)

    def test_write_creates_directory_if_needed(self):
        """Test that write creates necessary directories"""
        # This test assumes FILE_STORE_PATH is set to a temp directory
        # The write function should work even if subdirectories don't exist
        status, code = write(self.test_data, self.test_user_id)
        self.assertEqual(status, 'ok')
        self.assertEqual(code, 200)

    def test_read_file_corruption(self):
        """Test reading corrupted JSON file"""
        # Create a corrupted JSON file manually
        file_path = os.path.join(self.temp_dir, f"{self.test_user_id}.json")
        with open(file_path, 'w') as f:
            f.write('{"invalid": json syntax}')

        # This should raise a JSONDecodeError since the file_store doesn't handle corrupted JSON
        with self.assertRaises(json.JSONDecodeError):
            read(self.test_user_id)

    def test_environment_variable_file_store_path(self):
        """Test that FILE_STORE_PATH environment variable is respected"""
        # With our mocking, files should go to temp_dir
        write(self.test_data, self.test_user_id)
        expected_path = os.path.join(self.temp_dir, f"{self.test_user_id}.json")

        # The file should exist in the mocked temp directory
        self.assertTrue(os.path.exists(expected_path))

        # Clean up
        if os.path.exists(expected_path):
            os.remove(expected_path)

if __name__ == '__main__':
    unittest.main()
