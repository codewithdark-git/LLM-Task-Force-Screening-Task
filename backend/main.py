import os
import warnings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

# Import our application modules
from app.api.api import api_router
from app.core.config import settings

# Load environment variables
load_dotenv()

# Suppress Pydantic v2 warnings
warnings.filterwarnings(
    "ignore",
    message="Valid config keys have changed in V2"
)

# Initialize the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for the JioPay customer support chatbot using RAG",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME} API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)