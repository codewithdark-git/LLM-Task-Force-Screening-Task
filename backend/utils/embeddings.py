from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
from typing import Dict, List, Tuple
import pickle

class FAISSVectorStore:
    def __init__(self, dimension: int):
        """Initialize FAISS index with the specified dimension"""
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity
        self.documents = []
        self.metadatas = []

    def add(self, documents: List[str], embeddings: List[List[float]], metadatas: List[Dict]):
        """Add documents and their embeddings to the index"""
        if not documents or not embeddings or not metadatas:
            return

        # Convert embeddings to numpy array
        embeddings_np = np.array(embeddings).astype('float32')
        
        # Add to FAISS index
        self.index.add(embeddings_np)
        
        # Store documents and metadata
        self.documents.extend(documents)
        self.metadatas.extend(metadatas)

    def query(self, query_embeddings: List[List[float]], n_results: int = 3, **kwargs) -> Dict:
        """Search for similar documents using query embeddings"""
        query_np = np.array(query_embeddings).astype('float32')
        
        # Search the index
        distances, indices = self.index.search(query_np, n_results)
        
        # Filter out invalid indices
        valid_results = []
        valid_metadatas = []
        
        for idx_list in indices:
            docs = []
            metas = []
            for idx in idx_list:
                if idx < len(self.documents):
                    docs.append(self.documents[idx])
                    metas.append(self.metadatas[idx])
            valid_results.append(docs)
            valid_metadatas.append(metas)
        
        # Return in the same format as before
        return {
            'documents': valid_results,
            'metadatas': valid_metadatas
        }

    def save(self, directory: str):
        """Save the vector store to disk"""
        os.makedirs(directory, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, os.path.join(directory, "index.faiss"))
        
        # Save documents and metadata
        with open(os.path.join(directory, "store_data.pkl"), "wb") as f:
            pickle.dump({
                "documents": self.documents,
                "metadatas": self.metadatas
            }, f)

    @classmethod
    def load(cls, directory: str):
        """Load a vector store from disk"""
        # Load FAISS index
        index = faiss.read_index(os.path.join(directory, "index.faiss"))
        
        # Load documents and metadata
        with open(os.path.join(directory, "store_data.pkl"), "rb") as f:
            data = pickle.load(f)
        
        # Create instance and restore data
        instance = cls(index.d)
        instance.index = index
        instance.documents = data["documents"]
        instance.metadatas = data["metadatas"]
        
        return instance

def get_embeddings():
    """Initialize and return the sentence transformer model"""
    return SentenceTransformer('all-MiniLM-L6-v2')

def process_faqs(faqs_data: Dict) -> List[Dict]:
    """Process FAQs data into a format suitable for vector storage, 
    focusing only on answers and removing questions"""
    documents = []
    for category, qa_pairs in faqs_data["faq_pairs"].items():
        for qa in qa_pairs:
            # Create a document with just the answer
            doc = {
                "text": qa['answer'],
                "metadata": {
                    "category": category,
                    "type": "knowledge",
                    "source": "JioPay FAQs",
                    "topic": qa["question"]  # Keep the question as a topic for reference
                }
            }
            documents.append(doc)
    return documents

def process_pages(pages_data: Dict) -> List[Dict]:
    """Process website pages data into chunks suitable for vector storage"""
    content = pages_data["content"]
    # Split content into paragraphs
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    
    documents = []
    for i, paragraph in enumerate(paragraphs):
        if len(paragraph.split()) > 10:  # Only include substantial paragraphs
            doc = {
                "text": paragraph,
                "metadata": {
                    "type": "knowledge",
                    "source": pages_data["location"],
                    "chunk_id": i
                }
            }
            documents.append(doc)
    return documents

def setup_vector_store(faqs_data: Dict, pages_data: Dict) -> FAISSVectorStore:
    """Set up and return the FAISS vector store with processed documents"""
    # Get embeddings model
    model = get_embeddings()
    
    # Process documents
    faq_docs = process_faqs(faqs_data)
    page_docs = process_pages(pages_data)
    
    # Merge all documents into a unified knowledge base
    all_docs = faq_docs + page_docs
    
    # Prepare data for vector store
    texts = [doc["text"] for doc in all_docs]
    metadatas = [doc["metadata"] for doc in all_docs]
    
    # Generate embeddings
    embeddings = model.encode(texts)
    
    # Initialize and populate vector store
    vector_store = FAISSVectorStore(dimension=embeddings.shape[1])
    vector_store.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )
    
    # Save the vector store
    save_dir = os.path.join("data", "faiss_index")
    vector_store.save(save_dir)
    
    return vector_store 