# API Documentation

## Overview
This document provides detailed information about the API endpoints available in the FastAPI S3 Application. The application allows users to upload files to an AWS S3 bucket, list files in the bucket, and retrieve file content.

## Base URL
```
http://0.0.0.0:8005
```

## Endpoints

### 1. Root Endpoint
- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns a welcome message.
- **Response:**
  - **Status Code:** `200 OK`
  - **Body:**
    ```json
    {
      "message": "Welcome to the FastAPI S3 Application"
    }
    ```

### 2. Upload File
- **URL:** `/upload/`
- **Method:** `POST`
- **Description:** Uploads a file to the S3 bucket.
- **Request:**
  - **Headers:**
    - `Content-Type: multipart/form-data`
  - **Body:**
    - `file`: The file to be uploaded (type: `UploadFile`).
- **Response:**
  - **Status Code:** `200 OK`
  - **Body:**
    ```json
    {
      "message": "File uploaded successfully",
      "file_url": "https://bucket-for-ai-generated-content.s3.amazonaws.com/{filename}"
    }
    ```
  - **Error Responses:**
    - `400 Bad Request`: Validation error (e.g., unsupported file type or size exceeds limit).
    - `500 Internal Server Error`: Server error during file upload.

### 3. List Files
- **URL:** `/files/`
- **Method:** `GET`
- **Description:** Lists all files in the S3 bucket.
- **Response:**
  - **Status Code:** `200 OK`
  - **Body:**
    ```json
    {
      "files": ["file1.txt", "file2.jpg", ...]
    }
    ```
  - **Error Responses:**
    - `500 Internal Server Error`: Server error during file listing.

### 4. Get File Content
- **URL:** `/files/{file_name}`
- **Method:** `GET`
- **Description:** Retrieves the content of a specified file from the S3 bucket.
- **Path Parameters:**
  - `file_name`: The name of the file to retrieve.
- **Response:**
  - **Status Code:** `200 OK`
  - **Body:**
    - Returns the file content as a stream.
  - **Headers:**
    - `Content-Type: application/octet-stream`
  - **Error Responses:**
    - `404 Not Found`: File not found.
    - `500 Internal Server Error`: Server error during file retrieval.

## Error Handling
The API provides meaningful error messages and appropriate HTTP status codes for different error scenarios, such as validation errors, file not found, and server errors.

## Security
- Ensure all requests are made over HTTPS to secure data transmission.
- Implement rate limiting to prevent abuse of the API.

## Example Usage
### Upload File Example
```bash
curl -X POST "http://0.0.0.0:8005/upload/" -F "file=@/path/to/your/file.jpg"
```

### List Files Example
```bash
curl -X GET "http://0.0.0.0:8005/files/"
```

### Get File Content Example
```bash
curl -X GET "http://0.0.0.0:8005/files/your_file_name.jpg" -o output.jpg
```

## Notes
- Ensure AWS credentials are properly configured in the environment where the application is running.
- The S3 bucket name used is `bucket-for-ai-generated-content`.