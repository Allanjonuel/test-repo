import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome to the FastAPI S3 Application"})

    def test_upload_file_endpoint(self):
        with open("test_image.jpg", "rb") as file:
            response = self.client.post("/upload/", files={"file": ("test_image.jpg", file, "image/jpeg")})
            self.assertEqual(response.status_code, 200)
            self.assertIn("File uploaded successfully", response.json()["message"])

    def test_list_files_endpoint(self):
        response = self.client.get("/files/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("files", response.json())

    def test_get_file_endpoint(self):
        response = self.client.get("/files/test_image.jpg")
        if response.status_code == 404:
            self.assertEqual(response.json()["detail"], "File not found")
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["content-type"], "application/octet-stream")

if __name__ == '__main__':
    unittest.main()
