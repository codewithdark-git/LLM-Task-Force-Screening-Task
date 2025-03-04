import os
from typing import List, Tuple, Dict
import g4f
from sentence_transformers import SentenceTransformer
import logging
import re
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure g4f
g4f.debug.logging = True  # Enable logging for debugging
g4f.check_version = False  # Disable version checking

def clean_stream_response(response: str) -> str:
    """Clean the streamed response from g4f"""
    # Remove data: prefixes and JSON formatting
    cleaned = ""
    try:
        # Extract content from JSON-like structure
        content_parts = re.findall(r'"content":"([^"]*)"', response)
        cleaned = "".join(content_parts)
        
        # Remove markdown artifacts
        cleaned = re.sub(r'\*\*', '', cleaned)
        
        # Remove excessive whitespace
        cleaned = " ".join(cleaned.split())
        
        return cleaned
    except Exception as e:
        logger.error(f"Error cleaning response: {str(e)}")
        return response

def combine_contexts(contexts: List[Dict]) -> str:
    """Combine multiple contexts into a single coherent text"""
    combined_text = ""
    seen_content = set()  # Track unique content
    
    for ctx in contexts:
        content = ctx['content'].strip()
        # Skip if content is duplicate or empty
        if content and content not in seen_content:
            seen_content.add(content)
            # Add category/topic as section header if available
            if ctx['metadata'].get('category') and ctx['metadata'].get('topic'):
                combined_text += f"\n{ctx['metadata']['category']} - {ctx['metadata']['topic']}:\n"
            combined_text += f"{content}\n"
    
    return combined_text.strip()

def get_relevant_context(query: str, vector_store, top_k: int = 5) -> List[Dict]:
    """Retrieve relevant context from the vector store"""
    # Get embeddings model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query).tolist()
    
    # Query the vector store
    results = vector_store.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    contexts = []
    # FAISS returns results in a different format than ChromaDB
    for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
        contexts.append({
            "content": doc,
            "metadata": metadata
        })
    
    return contexts

def format_context(contexts: List[Dict]) -> str:
    """Format retrieved contexts into a prompt-friendly format"""
    # Combine and deduplicate contexts
    combined_text = combine_contexts(contexts)
    
    # Format with clear structure
    formatted = "Reference Information:\n\n"
    formatted += combined_text
    
    return formatted.strip()

def generate_response(query: str, vector_store, chat_history: List[Dict]) -> Tuple[str, List[Dict]]:
    """Generate a response using the g4f provider and retrieved context"""
    try:
        # Get relevant context
        contexts = get_relevant_context(query, vector_store)
        
        # Format the context
        formatted_context = format_context(contexts)
        
        # Prepare messages for g4f
        system_prompt = """You are a helpful JioPay customer support assistant. 
        Synthesize the provided reference information into a clear, direct response.
        Focus on accuracy and relevance. Avoid repetition and maintain a professional tone."""
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add filtered chat history (skip redundant or irrelevant messages)
        if chat_history:
            relevant_history = [
                msg for msg in chat_history[-2:]  # Only keep last 2 messages
                if not any(skip in msg.get('content', '').lower() 
                          for skip in ['hello', 'hi', 'hey', 'thanks'])
            ]
            messages.extend(relevant_history)
        
        # Add current query with context
        messages.append({
            "role": "user",
            "content": f"Reference Information:\n{formatted_context}\n\nQuestion: {query}\n\nProvide a clear, direct answer based on the reference information above."
        })
        
        # Generate response using g4f
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4o,
            messages=messages,
            stream=False
        )
        
        # Clean the response
        cleaned_response = clean_stream_response(response)
        
        # Filter sources to only include relevant ones
        relevant_sources = [
            {
                "type": "knowledge",
                "category": ctx["metadata"].get("category", "General"),
                "source": ctx["metadata"].get("source", "JioPay Knowledge Base"),
                "topic": ctx["metadata"].get("topic", "")
            }
            for ctx in contexts
            if ctx["metadata"].get("category") != "Repeat"  # Filter out repetitive sources
        ]
        
        return cleaned_response, relevant_sources
        
    except Exception as e:
        logger.error(f"Error in generate_response: {str(e)}")
        return "I apologize, but I encountered an error while processing your request. Please try again.", []