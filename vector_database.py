"""
Vector Database Module for RAG System
Handles PDF processing, chunking, embeddings, and FAISS vector store
Uses DeepSeek R1 with Ollama for embeddings
"""

import os
import io
from pathlib import Path
from typing import List, Optional
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class VectorDatabase:
    """Manages PDF processing and vector storage using FAISS"""
    
    def __init__(self, pdfs_directory: str = "pdfs", model_name: str = "deepseek-r1:1.5b"):
        """
        Initialize the Vector Database
        
        Args:
            pdfs_directory: Directory to store uploaded PDFs
            model_name: Ollama model name for embeddings (default: deepseek-r1:1.5b)
        """
        self.pdfs_directory = pdfs_directory
        self.model_name = model_name
        self.vector_store = None
        self.embeddings = None
        
        # Create pdfs directory if it doesn't exist
        Path(self.pdfs_directory).mkdir(parents=True, exist_ok=True)
    
    def upload_pdf(self, file_content: bytes, filename: str) -> str:
        """
        Save uploaded PDF to the pdfs directory
        
        Args:
            file_content: PDF file content as bytes
            filename: Name of the PDF file
            
        Returns:
            Path to the saved PDF file
        """
        file_path = os.path.join(self.pdfs_directory, filename)
        with open(file_path, "wb") as f:
            f.write(file_content)
        return file_path
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """
        Load and extract text from PDF using PDFPlumber
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of LangChain Document objects
        """
        loader = PDFPlumberLoader(file_path)
        documents = loader.load()
        return documents
    
    def create_chunks(self, documents: List[Document], chunk_size: int = 1000, 
                     chunk_overlap: int = 300) -> List[Document]:
        """
        Split documents into chunks with HIGHER overlap to avoid splitting key info
        
        Args:
            documents: List of Document objects
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks (increased to 300 for better context)
            
        Returns:
            List of chunked Document objects with page metadata
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,  # Increased overlap to prevent splitting important info
            length_function=len,
            separators=["\n\n", "\n", " ", ""]  # Split on paragraphs first
        )
        chunks = text_splitter.split_documents(documents)
        return chunks
    
    def setup_embeddings(self, base_url: str = "http://localhost:11434") -> OllamaEmbeddings:
        """
        Initialize DeepSeek R1 embeddings model with Ollama
        
        Args:
            base_url: Ollama server URL
            
        Returns:
            OllamaEmbeddings instance
        """
        self.embeddings = OllamaEmbeddings(
            model=self.model_name,
            base_url=base_url
        )
        return self.embeddings
    
    def create_vector_store(self, chunks: List[Document]) -> FAISS:
        """
        Create FAISS vector store from document chunks
        
        Args:
            chunks: List of chunked Document objects
            
        Returns:
            FAISS vector store instance
        """
        if self.embeddings is None:
            self.setup_embeddings()
        
        self.vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        return self.vector_store
    
    def save_vector_store(self, folder_path: str = "faiss_index"):
        """
        Save FAISS vector store to disk
        
        Args:
            folder_path: Path to save the FAISS index
        """
        if self.vector_store is None:
            raise ValueError("No vector store to save. Create one first.")
        
        self.vector_store.save_local(folder_path)
    
    def load_vector_store(self, folder_path: str = "faiss_index") -> FAISS:
        """
        Load FAISS vector store from disk
        
        Args:
            folder_path: Path to the saved FAISS index
            
        Returns:
            FAISS vector store instance
        """
        if self.embeddings is None:
            self.setup_embeddings()
        
        self.vector_store = FAISS.load_local(
            folder_path, 
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        return self.vector_store
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Search for similar documents in the vector store
        
        Args:
            query: Search query
            k: Number of similar documents to return
            
        Returns:
            List of similar Document objects
        """
        if self.vector_store is None:
            raise ValueError("No vector store available. Process a PDF first.")
        
        similar_docs = self.vector_store.similarity_search(query, k=k)
        return similar_docs
    
    def process_pdf_pipeline(self, file_content: bytes, filename: str, 
                            chunk_size: int = 1000, chunk_overlap: int = 200) -> dict:
        """
        Complete pipeline: Upload -> Load -> Chunk -> Embed -> Store
        
        Args:
            file_content: PDF file content as bytes
            filename: Name of the PDF file
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            Dictionary with processing results
        """
        # Step 1: Upload PDF
        file_path = self.upload_pdf(file_content, filename)
        
        # Step 2: Load PDF
        documents = self.load_pdf(file_path)
        
        # Step 3: Create Chunks
        chunks = self.create_chunks(documents, chunk_size, chunk_overlap)
        
        # Step 4: Setup Embeddings (DeepSeek R1 with Ollama)
        self.setup_embeddings()
        
        # Step 5: Create and Store in FAISS
        self.create_vector_store(chunks)
        
        return {
            "file_path": file_path,
            "num_documents": len(documents),
            "num_chunks": len(chunks),
            "status": "success"
        }


# Utility function for quick testing
def test_vector_database():
    """Test the vector database functionality"""
    vdb = VectorDatabase()
    
    # Test with a sample PDF (if available)
    print("Vector Database initialized successfully!")
    print(f"PDFs directory: {vdb.pdfs_directory}")
    print(f"Model: {vdb.model_name}")


if __name__ == "__main__":
    test_vector_database()
