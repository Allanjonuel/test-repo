from fastapi import FastAPI
from src.controllers.file_operations_controller import router as file_operations_router

app = FastAPI(title="FastAPI S3 File Operations")

# Include the router for file operations
app.include_router(file_operations_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI S3 File Operations API"}