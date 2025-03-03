# FastAPI S3 File Operations

This project is a FastAPI application designed to handle file operations with AWS S3 using default AWS credentials. The application provides endpoints for uploading files, listing files, and retrieving file content from the S3 bucket `bucket-for-ai-generated-content`.

## Features

- **File Upload**: Upload files to the specified S3 bucket.
- **List Files**: List all files currently stored in the bucket.
- **Retrieve File Content**: Fetch and return the content of a specified file from the bucket.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- **Boto3**: The AWS SDK for Python, used to interact with AWS services including S3.
- **Uvicorn**: A lightning-fast ASGI server for running FastAPI applications.

## Prerequisites

- Python 3.7+
- AWS CLI configured with default credentials

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd fastapi_s3_file_operations
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:

   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8005 --reload
   ```

   The application will be available at `http://0.0.0.0:8005`.

## Usage

### Upload a File

- **Endpoint**: `/upload`
- **Method**: `POST`
- **Request**: Multipart form data with the file to upload
- **Response**: JSON with the status of the upload and the file URL

### List Files

- **Endpoint**: `/files`
- **Method**: `GET`
- **Response**: JSON with the list of files in the bucket

### Retrieve File Content

- **Endpoint**: `/files/{file_name}`
- **Method**: `GET`
- **Response**: JSON with the file content

## Error Handling

The application includes robust error handling to manage exceptions and provide meaningful error messages to the client.

## Logging

Logging is configured to provide insights into the application's operations and help with debugging and monitoring.

## Security Considerations

- Ensure that your AWS credentials are managed securely and not hardcoded in the application.
- Use IAM roles and policies to restrict access to the S3 bucket as necessary.

## License

This project is licensed under the MIT License.