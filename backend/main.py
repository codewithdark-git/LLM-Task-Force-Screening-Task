from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import List, Optional
import json
import os
from dotenv import load_dotenv
from utils.embeddings import get_embeddings, setup_vector_store
from utils.chat import generate_response

# Load environment variables
load_dotenv()

app = FastAPI(title="JioPay Support Chatbot")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load and initialize vector store
vector_store = None

@app.on_event("startup")
async def startup_event():
    global vector_store
    # Load the JSON data
    with open("data/FAQs.json", "r", encoding="utf-8") as f:
        faqs_data = json.load(f)
    with open("data/pages.json", "r", encoding="utf-8") as f:
        pages_data = json.load(f)
    
    # Initialize vector store
    vector_store = setup_vector_store(faqs_data, pages_data)

class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[dict]] = []
    
    @validator('message')
    def message_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

class ChatResponse(BaseModel):
    response: str
    sources: List[dict]
    
    @validator('response')
    def response_not_empty(cls, v):
        if not v or not v.strip():
            return "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
        return v

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Validate input
        if not vector_store:
            raise HTTPException(status_code=500, detail="Vector store not initialized")
            
        # Generate response
        response, sources = generate_response(
            request.message,
            vector_store,
            request.chat_history
        )
        
        # Handle empty response
        if not response or not response.strip():
            return ChatResponse(
                response="I apologize, but I couldn't generate a proper response. Please try rephrasing your question.",
                sources=sources if sources else []
            )
            
        # Ensure we have valid sources
        if not sources:
            sources = [{
                "type": "knowledge",
                "category": "General",
                "source": "JioPay Knowledge Base",
                "topic": ""
            }]
            
        return ChatResponse(response=response, sources=sources)
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)