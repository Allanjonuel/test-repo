# FastAPI S3 File Operations

A FastAPI application to handle file operations with AWS S3 using default AWS credentials.

## Project Structure

```
fastapi_s3_file_operations/
│
├── src/
│   ├── controllers/
│   │   └── file_operations_controller.py
│   ├── models/
│   │   └── __init__.py
│   ├── services/
│   │   └── s3_service.py
│   ├── utils/
│   │   └── __init__.py
│   └── main.py
│
├── requirements.txt
├── README.md
└── Dockerfile
```

## Setup Instructions

### Prerequisites

- Python 3.7+
- AWS CLI configured with default credentials

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fastapi_s3_file_operations
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To start the FastAPI application, run the following command:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8005 --reload
```

The application will be accessible at `http://0.0.0.0:8005`.

### Docker

To run the application using Docker:

1. Build the Docker image:
   ```bash
   docker build -t fastapi-s3-file-operations .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8005:8005 fastapi-s3-file-operations
   ```

## API Endpoints

### Upload File

- **Endpoint**: `/upload`
- **Method**: `POST`
- **Description**: Upload a file to the S3 bucket.
- **Request**: Multipart form data with the file to upload.
- **Response**: JSON with the status of the upload and file URL.

### List Files

- **Endpoint**: `/files`
- **Method**: `GET`
- **Description**: Retrieve a list of all files stored in the S3 bucket.
- **Response**: JSON with the list of file names.

### Retrieve File Content

- **Endpoint**: `/files/{file_name}`
- **Method**: `GET`
- **Description**: Fetch and return the content of a specified file from the S3 bucket.
- **Response**: JSON with the content of the file.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Contact

For any inquiries, please contact the project maintainer.