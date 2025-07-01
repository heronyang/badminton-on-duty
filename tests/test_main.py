import unittest
import sys
import os
import io
import tempfile
from datetime import datetime, date
from unittest.mock import patch, mock_open, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main
from utils import extract_name_from_raw

class TestMain(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_argv = sys.argv
        self.original_stdout = sys.stdout
        sys.stdout = io.StringIO()
    
    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()
        sys.argv = self.original_argv
        sys.stdout = self.original_stdout
    
    def create_test_file(self, filename, content):
        """Helper method to create a test file"""
        filepath = os.path.join(self.test_dir.name, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath
    
    def test_validate_and_parse_filename_valid(self):
        """Test valid filename parsing"""
        test_file = "2025-07-20-original.txt"
        cleaned, parsed_date = main.validate_and_parse_filename(test_file)
        self.assertEqual(cleaned, "2025-07-20.txt")
        self.assertEqual(parsed_date, date(2025, 7, 20))
    
    def test_validate_and_parse_filename_invalid_suffix(self):
        """Test invalid filename suffix"""
        with self.assertRaises(ValueError) as context:
            main.validate_and_parse_filename("2025-07-20.txt")
        self.assertIn("must end with '-original.txt'", str(context.exception))
    
    def test_validate_and_parse_filename_invalid_date(self):
        """Test invalid date in filename"""
        with self.assertRaises(ValueError) as context:
            main.validate_and_parse_filename("2025-13-45-original.txt")
        self.assertIn("must start with a valid date", str(context.exception))
    
    @patch('main.get_shuffle_response')
    @patch('main.extract_name_from_raw')
    @patch('builtins.open')
    @patch('os.path.exists', return_value=True)
    def test_main_success(self, mock_exists, mock_file, mock_extract, mock_shuffle):
        """Test successful execution of main"""
        # Setup test data
        test_content = "1. @user1\n2. @user2\n3. @user3"
        mock_file.return_value.__enter__.return_value.read.return_value = test_content
        
        # Setup mocks
        mock_extract.return_value = [("@user1", "1"), ("@user2", "2"), ("@user3", "3")]
        mock_shuffle.return_value = "Mocked shuffle output"
        
        # Mock file writing
        mock_file_write = mock_open()
        with patch('builtins.open', mock_file_write):
            with patch('sys.argv', ['main.py', '2025-07-20-original.txt']):
                main.main()
        
        # Verify the cleaned output file was written
        mock_file_write.assert_any_call('2025-07-20.txt', 'w')
        
        # Verify the output file was written
        mock_file_write.assert_any_call('2025-07-20-output.txt', 'w')
    
    def test_main_missing_argument(self):
        """Test missing command line argument"""
        sys.argv = ['main.py']
        with self.assertRaises(SystemExit) as cm:
            main.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage:", sys.stdout.getvalue())
    
    @patch('builtins.open', side_effect=FileNotFoundError("File not found"))
    def test_main_file_not_found(self, mock_open):
        """Test file not found error"""
        with patch('sys.argv', ['main.py', '2025-07-20-original.txt']):
            with self.assertRaises(SystemExit) as cm:
                main.main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("File not found", sys.stdout.getvalue())
    
    @patch('builtins.print')
    @patch('main.validate_and_parse_filename')
    def test_main_prints_output(self, mock_validate, mock_print):
        """Test that main prints the output"""
        # Setup test data
        test_file = self.create_test_file("2025-07-20-original.txt", "1. @user1")
        
        # Setup mocks
        mock_validate.return_value = ("2025-07-20.txt", date(2025, 7, 20))
        
        # Mock file operations
        with patch('builtins.open', mock_open(read_data="1. @user1")) as mock_file:
            # Mock extract_name_from_raw
            with patch('main.extract_name_from_raw') as mock_extract:
                mock_extract.return_value = [("@user1", "1")]
                
                # Mock get_shuffle_response
                with patch('main.get_shuffle_response') as mock_shuffle:
                    mock_shuffle.return_value = "Mocked shuffle output"
                    
                    # Run the test
                    sys.argv = ['main.py', test_file]
                    main.main()
        
        # Verify print was called with the expected output
        mock_print.assert_any_call("Mocked shuffle output")
        mock_print.assert_any_call("\nOutput also saved to: 2025-07-20-output.txt")

if __name__ == '__main__':
    unittest.main()
