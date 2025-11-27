# loaders/document_loader.py
from pathlib import Path
from typing import Optional
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import logging

logger = logging.getLogger(__name__)

class DocumentLoader:
    """Handles loading documents from various file formats"""
    
    @staticmethod
    def load_document(file_path: Path) -> Optional[str]:
        """
        Load text content from a document file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content or None if loading fails
        """
        try:
            suffix = file_path.suffix.lower()
            
            if suffix == '.pdf':
                return DocumentLoader._load_pdf(file_path)
            elif suffix == '.txt':
                return DocumentLoader._load_text(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_path}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {e}")
            return None
    
    @staticmethod
    def _load_pdf(file_path: Path) -> Optional[str]:
        """Load content from a PDF file"""
        try:
            loader = PyPDFLoader(str(file_path))
            documents = loader.load()
            text = "\n".join([doc.page_content for doc in documents])
            
            if not text.strip():
                logger.warning(f"No text extracted from PDF: {file_path}")
                return None
                
            logger.info(f"Successfully extracted text from PDF: {file_path}")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {e}")
            return None
    
    @staticmethod
    def _load_text(file_path: Path) -> Optional[str]:
        """Load content from a text file"""
        try:
            loader = TextLoader(str(file_path), encoding="utf-8")
            documents = loader.load()
            text = "\n".join([doc.page_content for doc in documents])
            
            if not text.strip():
                logger.warning(f"No text found in file: {file_path}")
                return None
                
            logger.info(f"Successfully loaded text file: {file_path}")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error loading text file {file_path}: {e}")
            return None