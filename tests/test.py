import unittest
import json
import tempfile
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from src.file_store import read, write

class TestExample(unittest.TestCase):

    def setUp(self):
        self.test_user_id = 'test_user_id'
        self.test_data = {'key': 'value'}

    def test_write(self):
        # Use temporary file for testing
        with tempfile.NamedTemporaryFile() as f:

            # Write to file
            write_status, write_code = write(self.test_data, self.test_user_id)

            # Test status and code
            self.assertEqual(write_status, 'ok')
            self.assertEqual(write_code, 200)

            # Read from file
            read_data, read_code = read(self.test_user_id)

            # Test read data and code
            self.assertEqual(read_data, self.test_data)
            self.assertEqual(read_code, 200)

    def test_read_not_found(self):
        # Use temporary file for testing
        with tempfile.TemporaryDirectory() as tempdir:
            os.environ['FILE_STORE_PATH'] = tempdir

            # Read from unexisting file
            read_data, read_code = read(self.test_user_id + '0000')

            # Test not found data and code
            self.assertEqual(read_data, 'File not found')
            self.assertEqual(read_code, 404)

    def test_read(self):
        # Use temporary file for testing
        with tempfile.TemporaryDirectory() as tempdir:
            # Read from unexisting file
            write(self.test_data, self.test_user_id)
            read_data, read_code = read(self.test_user_id)

            # Test not found data and code
            self.assertEqual(read_data, self.test_data)
            self.assertEqual(read_code, 200)

if __name__ == '__main__':
    unittest.main()
