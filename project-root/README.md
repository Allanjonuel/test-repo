# FastAPI Application for AWS S3 File Management

This project is a FastAPI application designed to manage files on AWS S3. It provides endpoints for uploading, listing, and retrieving files from a specified S3 bucket. The application leverages AWS's default credential provider chain, ensuring secure and efficient file operations without the need for hardcoded credentials.

## Features

- **Upload Files**: Allows users to upload files to the S3 bucket.
- **List Files**: Retrieves a list of all files stored in the bucket.
- **Retrieve File Content**: Fetches and returns the content of a specified file from the bucket.

## Project Structure

- **/app**: Contains the main application code.
  - **/routers**: Houses FastAPI routers for different functionalities.
  - **/services**: Contains business logic for interacting with AWS S3.
  - **/models**: Defines data models or schemas.
  - **/utils**: Includes utility functions, such as error handling and input validation.
- **/tests**: Contains unit tests for the application.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- AWS CLI configured with appropriate permissions

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build and run the application using Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   The application will be available at `http://localhost:8005`.

## Usage

### Upload a File

- **Endpoint**: `/upload`
- **Method**: `POST`
- **Description**: Upload a file to the S3 bucket.
- **Request**: Multipart form data with a file.

### List Files

- **Endpoint**: `/files`
- **Method**: `GET`
- **Description**: List all files in the S3 bucket.

### Retrieve File Content

- **Endpoint**: `/files/{file_name}`
- **Method**: `GET`
- **Description**: Retrieve the content of a specified file from the S3 bucket.

## Testing

Run the tests using pytest:

```bash
pytest
```

## Security Considerations

- Ensure the application is accessed over HTTPS in production environments.
- Implement rate limiting to prevent abuse.
- Log all requests and errors for monitoring and debugging purposes.

## Deployment

The application is containerized using Docker, making it easy to deploy in various environments. Ensure that the AWS credentials are properly configured in the environment where the application is deployed.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Docker](https://www.docker.com/)