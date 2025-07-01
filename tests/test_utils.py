import unittest
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import extract_name, extract_name_from_raw

class TestUtils(unittest.TestCase):
    def test_extract_name_basic(self):
        """Test basic name extraction"""
        self.assertEqual(extract_name("1. @user1"), ("@user1", "1"))
        self.assertEqual(extract_name("10. @user10"), ("@user10", "10"))
        
    def test_extract_name_with_whitespace(self):
        """Test name extraction with various whitespace"""
        self.assertEqual(extract_name("1.    @user1"), ("@user1", "1"))
        self.assertEqual(extract_name("1.@user1"), ("@user1", "1"))
        self.assertEqual(extract_name("1  .  @user1"), ("@user1", "1"))
        
    def test_extract_name_with_parentheses(self):
        """Test name extraction with parentheses"""
        self.assertEqual(extract_name("1. User (user1)"), ("User (user1)", "1"))
        self.assertEqual(extract_name("1. User (@user1)"), ("User (@user1)", "1"))
        
    def test_extract_name_invalid(self):
        """Test invalid name extraction"""
        self.assertEqual(extract_name(""), ("", ""))
        self.assertEqual(extract_name("   "), ("", ""))
        self.assertEqual(extract_name("abc"), ("", ""))
        self.assertEqual(extract_name("1."), ("", ""))
        self.assertEqual(extract_name("1.   "), ("", ""))
        
    def test_extract_name_from_raw_basic(self):
        """Test extracting names from raw text"""
        raw = """1. @user1
        2. @user2
        3. @user3"""
        expected = [
            ("@user1", "1"),
            ("@user2", "2"),
            ("@user3", "3")
        ]
        self.assertEqual(extract_name_from_raw(raw), expected)
        
    def test_extract_name_from_raw_with_empty_lines(self):
        """Test extracting names with empty lines"""
        raw = """1. @user1
        
        2. @user2
        
        3. @user3
        
        """
        expected = [
            ("@user1", "1"),
            ("@user2", "2"),
            ("@user3", "3")
        ]
        self.assertEqual(extract_name_from_raw(raw), expected)
        
    def test_extract_name_from_raw_with_invalid_entries(self):
        """Test extracting names with invalid entries"""
        raw = """1. @user1
        2. 
        3. @user3
        4. 123
        5. @user5"""
        expected = [
            ("@user1", "1"),
            ("@user3", "3"),
            ("@user5", "5")
        ]
        self.assertEqual(extract_name_from_raw(raw), expected)

if __name__ == '__main__':
    unittest.main()
