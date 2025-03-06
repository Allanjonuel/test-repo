import unittest
from unittest.mock import MagicMock
from fastapi import UploadFile, HTTPException
from app.utils.validation import validate_file_type, validate_file_size

class TestValidation(unittest.TestCase):
    def setUp(self):
        self.mock_file = MagicMock(spec=UploadFile)

    def test_validate_file_type_success(self):
        self.mock_file.content_type = 'image/jpeg'
        try:
            validate_file_type(self.mock_file)
        except HTTPException:
            self.fail("validate_file_type raised HTTPException unexpectedly!")

    def test_validate_file_type_failure(self):
        self.mock_file.content_type = 'text/plain'
        with self.assertRaises(HTTPException) as context:
            validate_file_type(self.mock_file)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Unsupported file type.")

    def test_validate_file_size_success(self):
        self.mock_file.file = MagicMock()
        self.mock_file.file.tell.return_value = 1024  # 1 KB
        try:
            validate_file_size(self.mock_file)
        except HTTPException:
            self.fail("validate_file_size raised HTTPException unexpectedly!")

    def test_validate_file_size_failure(self):
        self.mock_file.file = MagicMock()
        self.mock_file.file.tell.return_value = 6 * 1024 * 1024  # 6 MB
        with self.assertRaises(HTTPException) as context:
            validate_file_size(self.mock_file)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "File size exceeds the maximum limit of 5 MB.")

if __name__ == '__main__':
    unittest.main()