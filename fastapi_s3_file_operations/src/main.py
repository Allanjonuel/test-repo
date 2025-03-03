from fastapi import FastAPI
from src.controllers import file_controller

app = FastAPI(title="FastAPI S3 File Operations")

# Include the file operations router
app.include_router(file_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI S3 File Operations API!"}