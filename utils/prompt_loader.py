# utils/prompt_loader.py
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
import logging

logger = logging.getLogger(__name__)

class PromptLoader:
    """Handles loading prompts from XML files"""
    
    @staticmethod
    def load_from_xml(file_path: Path) -> Optional[ChatPromptTemplate]:
        """
        Load a prompt template from an XML file.
        
        Args:
            file_path: Path to the XML file
            
        Returns:
            ChatPromptTemplate or None if loading fails
        """
        try:
            if not file_path.exists():
                logger.error(f"Prompt file not found: {file_path}")
                return None
                
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            system_elem = root.find('system')
            user_elem = root.find('user')
            
            if system_elem is None or user_elem is None:
                logger.error(f"Invalid prompt structure in {file_path}")
                return None
            
            system_message = system_elem.text.strip()
            user_message = user_elem.text.strip()
            
            return ChatPromptTemplate.from_messages([
                ("system", system_message),
                ("user", user_message)
            ])
            
        except ET.ParseError as e:
            logger.error(f"XML parsing error in {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading prompt from {file_path}: {e}")
            return None
    
    @staticmethod
    def load_multiple(file_paths: dict[str, Path]) -> dict[str, Optional[ChatPromptTemplate]]:
        """
        Load multiple prompts from XML files.
        
        Args:
            file_paths: Dictionary mapping prompt names to file paths
            
        Returns:
            Dictionary mapping prompt names to ChatPromptTemplates
        """
        prompts = {}
        for name, path in file_paths.items():
            prompts[name] = PromptLoader.load_from_xml(path)
        return prompts