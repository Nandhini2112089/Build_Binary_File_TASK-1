import unittest
from lib.validator import validate_password

class TestPasswordValidator(unittest.TestCase):
    def test_valid_password(self):
        result = validate_password("Nandhini@23")
        self.assertEqual(result["status"], "success")

    def test_short(self):
        result = validate_password("Ab@1")
        self.assertEqual(result["status"], "failed")
      
    def test_no_special_case(self):
        result=  validate_password("Abi")
        self.assertEqual(result["status"], "failed")

    def test_no_upper_case(self):
        result=  validate_password("abi")
        self.assertEqual(result["status"], "failed")
    
      
if __name__ == "__main__":
    unittest.main()
