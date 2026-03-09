"""
Document processing for RAG pipeline
Handles file loading, chunking, and text extraction
"""

import os
import tempfile
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentProcessor:
    """
    Process uploaded documents for RAG pipeline
    Supports PDF, TXT, and Markdown files
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize document processor
        
        Args:
            chunk_size: Size of text chunks in characters
            chunk_overlap: Overlap between chunks for context preservation
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def process_uploaded_file(self, uploaded_file) -> List:
        """
        Process a single uploaded file from Streamlit
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            List of document chunks with metadata
        """
        # Save to temporary file (loaders need file paths)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            # Load based on file type
            file_extension = uploaded_file.name.lower().split('.')[-1]
            
            if file_extension == 'pdf':
                loader = PyPDFLoader(tmp_path)
            elif file_extension == 'md':
                loader = UnstructuredMarkdownLoader(tmp_path)
            else:  # txt
                loader = TextLoader(tmp_path, encoding='utf-8')
            
            # Load documents
            documents = loader.load()
            
            # Add source metadata
            for doc in documents:
                doc.metadata['source'] = uploaded_file.name
                doc.metadata['file_type'] = file_extension
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            return chunks
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def process_multiple_files(self, uploaded_files: List) -> List:
        """
        Process multiple uploaded files
        
        Args:
            uploaded_files: List of Streamlit UploadedFile objects
            
        Returns:
            Combined list of all document chunks
        """
        all_chunks = []
        
        for file in uploaded_files:
            try:
                chunks = self.process_uploaded_file(file)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"Error processing {file.name}: {str(e)}")
                # Continue with other files
        
        return all_chunks
    
    def get_chunk_stats(self, chunks: List) -> dict:
        """
        Get statistics about processed chunks
        
        Args:
            chunks: List of document chunks
            
        Returns:
            Dictionary with chunk statistics
        """
        if not chunks:
            return {
                'total_chunks': 0,
                'total_characters': 0,
                'avg_chunk_size': 0,
                'sources': []
            }
        
        total_chars = sum(len(chunk.page_content) for chunk in chunks)
        sources = list(set(chunk.metadata.get('source', 'unknown') for chunk in chunks))
        
        return {
            'total_chunks': len(chunks),
            'total_characters': total_chars,
            'avg_chunk_size': total_chars // len(chunks),
            'sources': sources
        }


# Test function
if __name__ == "__main__":
    print("Document processor module loaded successfully")
    print("Ready to process PDF, TXT, and Markdown files")