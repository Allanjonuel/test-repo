import pytest
from fastapi.testclient import TestClient
from moto import mock_s3
import boto3
from app.main import app

# Initialize the test client
client = TestClient(app)

# Mock S3 setup
BUCKET_NAME = "bucket-for-ai-generated-content"

@pytest.fixture(scope='function')
def s3_mock():
    with mock_s3():
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket=BUCKET_NAME)
        yield


def test_upload_file(s3_mock):
    # Prepare a sample file
    file_content = b"This is a test file."
    files = {'file': ('test.txt', file_content, 'text/plain')}

    # Perform the upload request
    response = client.post("/upload", files=files)

    # Assert the response
    assert response.status_code == 201
    assert response.json()["message"] == "File uploaded successfully"


def test_list_files(s3_mock):
    # Upload a file to ensure the bucket is not empty
    s3 = boto3.client('s3')
    s3.put_object(Bucket=BUCKET_NAME, Key='test.txt', Body=b"This is a test file.")

    # Perform the list files request
    response = client.get("/files")

    # Assert the response
    assert response.status_code == 200
    assert 'test.txt' in response.json()


def test_get_file_content(s3_mock):
    # Upload a file to retrieve
    s3 = boto3.client('s3')
    s3.put_object(Bucket=BUCKET_NAME, Key='test.txt', Body=b"This is a test file.")

    # Perform the get file content request
    response = client.get("/files/test.txt")

    # Assert the response
    assert response.status_code == 200
    assert response.content == b"This is a test file."


def test_get_file_content_not_found(s3_mock):
    # Attempt to retrieve a non-existent file
    response = client.get("/files/non_existent.txt")

    # Assert the response
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found."