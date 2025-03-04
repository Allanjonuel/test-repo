# FastAPI S3 File Operations

This project is a FastAPI application designed to handle file operations with AWS S3 using default AWS credentials. The application allows users to upload files, list files, and retrieve file content from an S3 bucket named `bucket-for-ai-generated-content`.

## Features

1. **File Upload**: Upload files to the specified S3 bucket.
2. **List Files**: List all files stored in the S3 bucket.
3. **Retrieve File Content**: Retrieve the content of a specified file from the S3 bucket.

## Technical Specifications

- **Framework**: FastAPI
- **AWS SDK**: Boto3
- **Server**: Uvicorn
- **File Upload Handling**: python-multipart

## Prerequisites

- Python 3.7+
- AWS account with appropriate permissions to access S3
- AWS CLI configured with default credentials

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fastapi_s3_file_operations
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8005
```

The application will be accessible at `http://0.0.0.0:8005`.

## API Endpoints

- **POST** `/upload`: Upload a file to the S3 bucket.
- **GET** `/files`: List all files in the S3 bucket.
- **GET** `/files/{file_name}`: Retrieve the content of a specified file.

## Error Handling

The application includes robust error handling for AWS S3 operations, returning appropriate HTTP status codes and error messages.

## Logging

Logging is configured to provide insights into the application's operations, including successful uploads, listings, and retrievals, as well as errors.

## Security Considerations

- Ensure that your AWS credentials are kept secure and not hard-coded in the application.
- Use IAM roles and policies to restrict access to the S3 bucket as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or support, please contact [Your Name] at [Your Email].