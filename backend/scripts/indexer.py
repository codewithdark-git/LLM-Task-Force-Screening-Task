import os
import json
import sys
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import faiss
from tqdm import tqdm

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.utils.vector_store import VectorStore
from app.core.config import settings

# Define the chunk size for text splitting
CHUNK_SIZE = settings.CHUNK_SIZE
CHUNK_OVERLAP = settings.CHUNK_OVERLAP

def load_raw_data() -> tuple:
    """Load the raw data from the JSON files.
    
    Returns:
        Tuple of (pages, faqs)
    """
    # Load the pages
    pages_file = os.path.join(settings.RAW_DATA_DIR, "pages.json")
    if os.path.exists(pages_file):
        with open(pages_file, 'r', encoding='utf-8') as f:
            pages = [json.load(f)]  # Load as a list containing a single dictionary
    else:
        pages = []
        
    # Load the FAQs
    faqs_file = os.path.join(settings.RAW_DATA_DIR, "faqs.json")
    if os.path.exists(faqs_file):
        with open(faqs_file, 'r', encoding='utf-8') as f:
            faqs = json.load(f)
    else:
        faqs = []
        
    return pages, faqs

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks.
    
    Args:
        text: The text to split
        chunk_size: The size of each chunk
        chunk_overlap: The overlap between chunks
        
    Returns:
        List of text chunks
    """
    # Split the text into words
    words = text.split()
    
    # If the text is shorter than the chunk size, return it as is
    if len(words) <= chunk_size:
        return [text]
    
    # Split the text into chunks
    chunks = []
    for i in range(0, len(words), chunk_size - chunk_overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        # If we've reached the end of the text, break
        if i + chunk_size >= len(words):
            break
            
    return chunks

def process_pages(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process the pages into chunks for indexing.
    
    Args:
        pages: List of page dictionaries
        
    Returns:
        List of document dictionaries
    """
    documents = []
    
    for page in tqdm(pages, desc="Processing pages"):
        # Split the content into chunks
        if isinstance(page, dict) and 'content' in page:
            chunks = chunk_text(page['content'])
        else:
            print(f"Skipping invalid page: {page}")
            continue
        
        # Create a document for each chunk
        for i, chunk in enumerate(chunks):
            documents.append({
                'title': f"Page from {page['location']} (Part {i+1}/{len(chunks)})",
                'content': chunk,
                'url': page['location'],
                'source_type': 'page'
            })
            
    return documents

def process_faqs(faqs: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process the FAQs for indexing."""
    documents = []
    
    # Get the FAQ pairs dictionary
    faq_pairs = faqs.get("faq_pairs", {})
    location = faqs.get("location", "https://jiopay.com/business/help-center")
    
    # Process each category
    for category, qa_pairs in faq_pairs.items():
        # Process each Q&A pair in the category
        for faq in qa_pairs:
            documents.append({
                'title': faq['question'],
                'content': f"Question: {faq['question']}\nAnswer: {faq['answer']}",
                'url': location,
                'source_type': 'faq',
                'category': category
            })
            
    return documents

def main():
    """Main function to process the data and create the vector index."""
    # Create output directories
    os.makedirs(settings.PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(settings.EMBEDDINGS_DIR, exist_ok=True)
    
    # Load and process data
    print("Loading raw data...")
    pages, faqs = load_raw_data()
    
    # Process pages
    print(f"Processing {len(pages)} pages...")
    page_documents = process_pages(pages)
    
    # Process FAQs - note that faqs is now treated as a dictionary
    print("Processing FAQs...")
    faq_documents = process_faqs(faqs)
    
    # Combine and save documents
    all_documents = page_documents + faq_documents
    print(f"Total documents: {len(all_documents)}")
    
    # Save processed documents
    with open(settings.DOCUMENTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_documents, f, ensure_ascii=False, indent=2)
    
    # Create embeddings and vector store
    print("Creating vector embeddings...")
    embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    vector_store = VectorStore(
        embedding_model=embedding_model,
        index_path=str(settings.FAISS_INDEX_PATH),
        documents_path=str(settings.DOCUMENTS_PATH)
    )
    
    vector_store.load_or_create()
    vector_store.add_documents(all_documents)
    
    print("Vector index created successfully!")

if __name__ == "__main__":
    main()