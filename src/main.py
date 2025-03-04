from fastapi import FastAPI
from src.controllers import file_controller

app = FastAPI()

# Include the router from file_controller
app.include_router(file_controller.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI S3 File Manager!"}