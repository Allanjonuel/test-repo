# Setup Guide

## Prerequisites

Before setting up the FastAPI S3 Application, ensure you have the following prerequisites:

1. **Python 3.8+**: Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. **AWS Account**: An AWS account with access to S3 is required. Ensure you have the necessary permissions to create and manage S3 buckets and objects.
3. **AWS CLI**: Install the AWS Command Line Interface (CLI) and configure it with your AWS credentials. You can follow the installation guide [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
4. **Git**: Ensure Git is installed to clone the repository. You can download it from [git-scm.com](https://git-scm.com/).

## Setup Instructions

Follow these steps to set up the FastAPI S3 Application:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/fastapi-s3-app.git
   cd fastapi-s3-app
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AWS Credentials**:
   Ensure your AWS credentials are configured in your environment. You can do this by running:
   ```bash
   aws configure
   ```
   Follow the prompts to enter your AWS Access Key, Secret Key, region, and output format.

5. **Run the Application**:
   Start the FastAPI application using Uvicorn:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
   ```

6. **Access the API**:
   Open your browser and navigate to `http://localhost:8005/docs` to access the automatically generated API documentation and test the endpoints.

## Usage Examples

### Upload a File
Use the following `curl` command to upload a file:
```bash
curl -X POST "http://localhost:8005/upload/" -F "file=@/path/to/your/file.jpg"
```

### List Files
To list all files in the S3 bucket, use:
```bash
curl -X GET "http://localhost:8005/files/"
```

### Get File Content
To retrieve the content of a specific file, use:
```bash
curl -X GET "http://localhost:8005/files/your_file_name.jpg" -o output.jpg
```

## Notes
- Ensure your AWS credentials have the necessary permissions to access the S3 bucket `bucket-for-ai-generated-content`.
- The application should be run in a secure environment, and it is recommended to use HTTPS for production deployments.
- Consider implementing additional security measures such as rate limiting and authentication for production use.