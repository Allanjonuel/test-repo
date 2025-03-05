from fastapi import FastAPI
from app.routers import upload, list_files, get_file

app = FastAPI()

# Include routers
app.include_router(upload.router)
app.include_router(list_files.router)
app.include_router(get_file.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI S3 Application"}