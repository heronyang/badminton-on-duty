import unittest
import sys
import os
import random
from datetime import datetime, date
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shuffler import (
    extract_request_content,
    get_random_seed,
    remove_exceptional_names,
    get_shuffle_response,
    get_printed_name,
    EXCEPTIONAL_NAMES
)

class TestShuffler(unittest.TestCase):
    def setUp(self):
        # Save the original random seed
        self.original_random_seed = random.getstate()
        # Set a fixed seed for consistent test results
        random.seed(42)
        
    def tearDown(self):
        # Restore the original random seed
        random.setstate(self.original_random_seed)
    
    def test_extract_request_content(self):
        """Test extracting content from request"""
        request = """Some header text
        1. @user1
        2. @user2
        - Venmo: @venmo_user
        Some footer text"""
        expected = "1. @user1\n        2. @user2"
        self.assertEqual(extract_request_content(request).strip(), expected.strip())
    
    def test_get_random_seed(self):
        """Test random seed generation from date"""
        test_date = date(2025, 6, 30)
        self.assertEqual(get_random_seed(test_date), 20250630)
    
    def test_remove_exceptional_names(self):
        """Test removing exceptional names"""
        names = [("@user1", "1"), ("@exceptional", "2"), ("@user3", "3")]
        with patch('shuffler.EXCEPTIONAL_NAMES', ["@exceptional"]):
            result = remove_exceptional_names(names)
            self.assertEqual(len(result), 2)
            self.assertNotIn(("@exceptional", "2"), result)
    
    def test_get_printed_name(self):
        """Test formatting of printed names"""
        self.assertEqual(get_printed_name(("@user1", "1"), False), "@user1")
        self.assertEqual(get_printed_name(("@user1", "1"), True), "@user1 (1)")
    
    @patch('random.shuffle')
    def test_get_shuffle_response_list_input(self, mock_shuffle):
        """Test shuffle response with list input"""
        names = ["@user1", "@user2", "@user3", "@user4"]
        test_date = date(2025, 6, 30)
        
        # Mock the shuffle to reverse the list for predictable results
        def mock_shuffle_side_effect(x):
            x.reverse()
        mock_shuffle.side_effect = mock_shuffle_side_effect
        
        result = get_shuffle_response(names, test_date)
        
        # Check the header
        self.assertIn("On-duty 2025-06-30 (4 attended)", result)
        # Check that all names appear in the output
        for name in names:
            self.assertIn(name, result)
        # Check that the output contains the expected structure
        self.assertIn("On-duty 2025-06-30 (4 attended)", result)
        self.assertIn("--", result)
        self.assertIn("1:30-2:00", result)
        self.assertIn("2:00-2:30", result)
        self.assertIn("Instruction", result)
    
    def test_get_shuffle_response_string_input(self):
        """Test shuffle response with string input (backward compatibility)"""
        raw_input = """1. @user1
        2. @user2
        3. @user3
        4. @user4"""
        test_date = date(2025, 6, 30)
        
        with patch('random.shuffle') as mock_shuffle:
            # Mock the shuffle to reverse the list for predictable results
            def mock_shuffle_side_effect(x):
                x.reverse()
            mock_shuffle.side_effect = mock_shuffle_side_effect
            
            result = get_shuffle_response(raw_input, test_date)
        
        # Check the header
        self.assertIn("On-duty 2025-06-30 (4 attended)", result)
        # Check that all names appear in the output
        self.assertIn("@user1", result)
        self.assertIn("@user2", result)
        self.assertIn("@user3", result)
        self.assertIn("@user4", result)
    
    def test_get_shuffle_response_empty_input(self):
        """Test shuffle response with empty input"""
        result = get_shuffle_response([], date.today())
        self.assertEqual(result, "Error: No valid names provided")
        
        result = get_shuffle_response("", date.today())
        self.assertEqual(result, "Error: No valid names provided")

if __name__ == '__main__':
    unittest.main()
