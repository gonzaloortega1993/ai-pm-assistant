"""
Pinecone vector store manager for RAG
Handles embeddings and similarity search
"""

from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
import time

load_dotenv()


class VectorStoreManager:
    """
    Manage Pinecone vector store for RAG pipeline
    """
    
    def __init__(self, index_name: str = None):
        """
        Initialize Pinecone vector store
        
        Args:
            index_name: Name of Pinecone index (from .env if not provided)
        """
        self.index_name = index_name or os.getenv("PINECONE_INDEX_NAME", "pm-assistant-docs")
        
        # Initialize Pinecone
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY not found in .env file")
        
        self.pc = Pinecone(api_key=api_key)
        
        # Initialize embeddings (using OpenAI for consistency with Pinecone's 1536 dimensions)
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY required for embeddings (even when using Claude for generation)")
        
        self.embeddings = OpenAIEmbeddings(api_key=openai_key)
        
        # Ensure index exists
        self._ensure_index_exists()
        
        # Get index
        self.index = self.pc.Index(self.index_name)
    
    def _ensure_index_exists(self):
        """Create index if it doesn't exist"""
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        
        if self.index_name not in existing_indexes:
            print(f"Creating new index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,  # OpenAI embedding dimension
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            # Wait for index to be ready
            time.sleep(1)
    
    def add_documents(self, chunks: list, namespace: str = "default") -> int:
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of LangChain document chunks
            namespace: Pinecone namespace for organization
            
        Returns:
            Number of chunks added
        """
        if not chunks:
            return 0
        
        # Create vector store and add documents
        vector_store = PineconeVectorStore.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            index_name=self.index_name,
            namespace=namespace
        )
        
        return len(chunks)
    
    def search(self, query: str, k: int = 3, namespace: str = "default") -> list:
        """
        Search for similar documents
        
        Args:
            query: Search query
            k: Number of results to return
            namespace: Pinecone namespace to search
            
        Returns:
            List of relevant document chunks
        """
        # Create vector store for searching
        vector_store = PineconeVectorStore(
            index=self.index,
            embedding=self.embeddings,
            namespace=namespace
        )
        
        # Similarity search
        results = vector_store.similarity_search(query, k=k)
        
        return results
    
    def get_context_for_query(self, query: str, k: int = 3, namespace: str = "default") -> str:
        """
        Get formatted context string for LLM from search results
        
        Args:
            query: Search query
            k: Number of results
            namespace: Pinecone namespace
            
        Returns:
            Formatted context string
        """
        results = self.search(query, k=k, namespace=namespace)
        
        if not results:
            return ""
        
        # Format context
        context_parts = []
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'unknown')
            content = doc.page_content.strip()
            context_parts.append(f"[Source {i}: {source}]\n{content}")
        
        return "\n\n".join(context_parts)
    
    def clear_namespace(self, namespace: str = "default"):
        """
        Clear all vectors from a namespace
        
        Args:
            namespace: Namespace to clear
        """
        self.index.delete(delete_all=True, namespace=namespace)
    
    def get_stats(self) -> dict:
        """Get index statistics"""
        return self.index.describe_index_stats()


# Test function
if __name__ == "__main__":
    print("Testing Vector Store Manager...")
    
    try:
        vsm = VectorStoreManager()
        print(f"✓ Connected to index: {vsm.index_name}")
        
        stats = vsm.get_stats()
        print(f"✓ Index stats: {stats}")
        
        print("\n✅ Vector store ready!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
