# FastAPI S3 File Manager

A FastAPI application to manage file operations with AWS S3 using default AWS credentials.

## Features

- **File Upload**: Upload files to the S3 bucket named `bucket-for-ai-generated-content`.
- **List Files**: List all files stored in the specified S3 bucket.
- **Retrieve File Content**: Retrieve the content of a specified file from the bucket.

## Requirements

- Python 3.7+
- AWS account with access to S3
- AWS credentials configured in your environment

## Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd fastapi_s3_file_manager
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS Credentials**

   Ensure your AWS credentials are set up in your environment. You can configure them using the AWS CLI:

   ```bash
   aws configure
   ```

   This will prompt you to enter your AWS Access Key, Secret Key, region, and output format.

4. **Run the application**

   Use `uvicorn` to run the FastAPI application:

   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8005
   ```

   The application will be accessible at `http://0.0.0.0:8005`.

## Usage

- **Upload a File**

  Send a POST request to `/upload` with the file to be uploaded.

  ```bash
  curl -X POST "http://0.0.0.0:8005/upload" -F "file=@<path-to-your-file>"
  ```

- **List Files**

  Send a GET request to `/files` to retrieve a list of all files in the S3 bucket.

  ```bash
  curl -X GET "http://0.0.0.0:8005/files"
  ```

- **Retrieve File Content**

  Send a GET request to `/files/{file_name}` to retrieve the content of a specific file.

  ```bash
  curl -X GET "http://0.0.0.0:8005/files/<file_name>"
  ```

## Docker

To run the application in a Docker container:

1. **Build the Docker image**

   ```bash
   docker build -t fastapi-s3-file-manager .
   ```

2. **Run the Docker container**

   ```bash
   docker run -p 8005:8005 fastapi-s3-file-manager
   ```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or support, please contact [your-email@example.com].