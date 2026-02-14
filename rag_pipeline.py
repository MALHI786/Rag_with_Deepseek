"""
RAG Pipeline Module
Handles retrieval-augmented generation using DeepSeek R1 with Groq
"""

import os
from typing import List, Optional
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from vector_database import VectorDatabase


class RAGPipeline:
    """Manages the RAG pipeline with DeepSeek R1 via Groq"""
    
    def __init__(self, groq_api_key: Optional[str] = None, 
                 model_name: str = "deepseek-r1-distill-llama-70b",
                 temperature: float = 0.1):
        """
        Initialize the RAG Pipeline
        
        Args:
            groq_api_key: Groq API key (or set GROQ_API_KEY env variable)
            model_name: Groq model name for DeepSeek R1
            temperature: Model temperature (0.0 to 1.0) - low for factual RAG
        """
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.model_name = model_name
        self.temperature = temperature
        self.llm = None
        self.vector_database = None
        self.retrieval_k = 8  # Increased from 4 to 8 for better retrieval
        
        if not self.groq_api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass it directly.")
    
    def setup_llm(self):
        """Initialize the DeepSeek R1 LLM via Groq"""
        self.llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=self.model_name,
            temperature=self.temperature,
            max_tokens=8000
        )
        return self.llm
    
    def create_prompt_template(self) -> PromptTemplate:
        """Create a STRICT prompt template to prevent hallucinations"""
        template = """You are a precise AI assistant that ONLY answers based on the provided context.

IMPORTANT RULES:
1. ONLY use information from the Context below
2. DO NOT use any external knowledge or make assumptions
3. If the Context doesn't contain the answer, say: "The provided document does not contain information about [topic]"
4. Quote relevant parts of the context when answering
5. If you find the answer, cite it clearly with relevant excerpts

Context from the document:
{context}

Question: {question}

Answer (using ONLY the context above):"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        return prompt
    
    def setup_qa_chain(self, vector_database: VectorDatabase, k: int = 4):
        """
        Setup the QA chain with retriever
        
        Args:
            vector_database: VectorDatabase instance with loaded vector store
            k: Number of documents to retrieve
        """
        if self.llm is None:
            self.setup_llm()
        
        if vector_database.vector_store is None:
            raise ValueError("Vector store is not initialized. Process a PDF first.")
        
        # Store vector database reference for retrieval
        self.vector_database = vector_database
        self.retrieval_k = k
        
        return True
    
    def answer_question(self, question: str) -> dict:
        """
        Answer a question using RAG with strict context adherence
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer, source documents, and citations
        """
        if self.llm is None:
            self.setup_llm()
        
        if not hasattr(self, 'vector_database') or self.vector_database is None:
            raise ValueError("Vector database is not set up. Call setup_qa_chain() first.")
        
        # Retrieve relevant documents with increased k
        relevant_docs = self.vector_database.similarity_search(question, k=self.retrieval_k)
        
        # Build context with chunk numbers for citation
        context_parts = []
        for i, doc in enumerate(relevant_docs):
            context_parts.append(f"[Chunk {i+1}]\n{doc.page_content}")
        context = "\n\n".join(context_parts)
        
        # Strict prompt that prevents hallucination
        prompt = f"""You are a precise AI assistant that ONLY answers based on the provided context.

IMPORTANT RULES:
1. ONLY use information from the Context below
2. DO NOT use any external knowledge or make assumptions
3. If the Context doesn't contain the answer, say: "The provided document does not contain information about this topic."
4. Quote relevant parts of the context when answering
5. If you find the answer, cite which chunks ([Chunk N]) contain the information

Context from the document:
{context}

Question: {question}

Answer (using ONLY the context above):"""
        
        # Get response from LLM
        response = self.llm.invoke(prompt)
        
        return {
            "question": question,
            "answer": response.content,
            "source_documents": relevant_docs,
            "num_chunks_retrieved": len(relevant_docs)
        }
    
    def answer_question_simple(self, question: str, vector_database: VectorDatabase, k: int = 8) -> str:
        """
        Simplified method with strict context adherence
        
        Args:
            question: User's question
            vector_database: VectorDatabase instance
            k: Number of documents to retrieve (default 8 for better coverage)
            
        Returns:
            Answer string with citations
        """
        if self.llm is None:
            self.setup_llm()
        
        # Retrieve relevant documents with higher k
        relevant_docs = vector_database.similarity_search(question, k=k)
        
        # Build context with chunk markers for citation
        context_parts = []
        for i, doc in enumerate(relevant_docs):
            # Add metadata if available
            page_info = f" (Page {doc.metadata.get('page', 'unknown')})" if hasattr(doc, 'metadata') and 'page' in doc.metadata else ""
            context_parts.append(f"[Chunk {i+1}{page_info}]\n{doc.page_content}")
        context = "\n\n".join(context_parts)
        
        # Strict prompt to prevent hallucination
        prompt = f"""You are a precise AI assistant that ONLY answers based on the provided context.

CRITICAL RULES:
1. ONLY use information from the Context below - NO external knowledge
2. If the answer is in the context, quote the relevant parts and cite the chunk number
3. If the context does NOT contain the answer, you MUST say: "The document does not contain information about this topic."
4. DO NOT make assumptions or add information not in the context
5. Be accurate and cite your sources from the chunks

Context from the document:
{context}

Question: {question}

Answer (strictly from context only):"""
        
        # Get response from LLM
        response = self.llm.invoke(prompt)
        
        return response.content
    
    def get_relevant_documents(self, question: str, vector_database: VectorDatabase, k: int = 4) -> List[Document]:
        """
        Retrieve relevant documents for a question
        
        Args:
            question: User's question
            vector_database: VectorDatabase instance
            k: Number of documents to retrieve
            
        Returns:
            List of relevant Document objects
        """
        return vector_database.similarity_search(question, k=k)


class RAGApplication:
    """Complete RAG application combining vector database and pipeline"""
    
    def __init__(self, groq_api_key: Optional[str] = None, 
                 ollama_model: str = "deepseek-r1:1.5b",
                 groq_model: str = "deepseek-r1-distill-llama-70b",
                 temperature: float = 0.1):
        """
        Initialize the complete RAG application with strict settings
        
        Args:
            groq_api_key: Groq API key
            ollama_model: Ollama model for embeddings
            groq_model: Groq model for LLM
            temperature: Low temperature (0.1) for factual answers
        """
        self.vector_db = VectorDatabase(model_name=ollama_model)
        self.rag_pipeline = RAGPipeline(groq_api_key=groq_api_key, model_name=groq_model, temperature=temperature)
        self.is_initialized = False
    
    def process_pdf(self, file_content: bytes, filename: str) -> dict:
        """
        Process a PDF file through the complete pipeline
        
        Args:
            file_content: PDF file content
            filename: PDF filename
            
        Returns:
            Processing results
        """
        result = self.vector_db.process_pdf_pipeline(file_content, filename)
        self.is_initialized = True
        return result
    
    def ask_question(self, question: str) -> str:
        """
        Ask a question about the processed document
        
        Args:
            question: User's question
            
        Returns:
            Answer from the RAG pipeline
        """
        if not self.is_initialized:
            raise ValueError("No PDF has been processed. Process a PDF first.")
        
        answer = self.rag_pipeline.answer_question_simple(question, self.vector_db)
        return answer


# Utility function for testing
def test_rag_pipeline():
    """Test the RAG pipeline"""
    print("RAG Pipeline module loaded successfully!")
    print("Available models:")
    print("- Embeddings: DeepSeek R1 with Ollama")
    print("- LLM: DeepSeek R1 with Groq")


if __name__ == "__main__":
    test_rag_pipeline()
