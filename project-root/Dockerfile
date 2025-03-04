# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app /app/app

# Expose the port the app runs on
EXPOSE 8005

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]

# TODO: Consider using a multi-stage build to reduce the final image size by separating the build environment from the runtime environment. This can help in optimizing the image for production deployments. Also, explore using a more minimal base image like `alpine` for further size reduction. Ensure all security patches are applied to the base image. Implement health checks to monitor the application's status. Consider adding a non-root user for running the application to enhance security. Add labels for metadata like version, description, and maintainer for better image management. Implement logging to a centralized system for better monitoring and debugging. Use environment variables for configuration to avoid hardcoding sensitive information. Ensure the application is stateless and can be scaled horizontally.