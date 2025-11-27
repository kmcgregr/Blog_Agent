# chains/processing_chains.py
from typing import Optional, Dict, Any
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import logging

logger = logging.getLogger(__name__)

class ProcessingChains:
    """Manages all LangChain processing chains"""
    
    def __init__(self, llm: Ollama, prompts: Dict[str, ChatPromptTemplate]):
        """
        Initialize processing chains.
        
        Args:
            llm: Ollama LLM instance
            prompts: Dictionary of prompt templates
        """
        self.llm = llm
        self.prompts = prompts
        self.parser = StrOutputParser()
        
        # Initialize chains
        self._init_chains()
    
    def _init_chains(self) -> None:
        """Initialize all processing chains"""
        self.correction_chain = self._create_chain('correction')
        self.title_chain = self._create_chain('title')
        self.story_chain = self._create_chain('story')
        self.copy_edit_chain = self._create_chain('copy_edit')
        self.review_chain = self._create_chain('review')
        self.image_prompt_chain = self._create_chain('image_prompt')
    
    def _create_chain(self, prompt_name: str):
        """Create a processing chain from a prompt"""
        prompt = self.prompts.get(prompt_name)
        if prompt is None:
            logger.warning(f"Prompt '{prompt_name}' not found")
            return None
        return prompt | self.llm | self.parser
    
    def correct_dream(self, dream_text: str) -> Optional[str]:
        """Correct grammar and formatting of dream text"""
        if self.correction_chain is None:
            logger.error("Correction chain not initialized")
            return None
        
        try:
            logger.info("Correcting grammar and formatting...")
            result = self.correction_chain.invoke({"dream_text": dream_text})
            return result.strip()
        except Exception as e:
            logger.error(f"Error in correction chain: {e}")
            return None
    
    def generate_title(self, corrected_dream_text: str) -> Optional[str]:
        """Generate SEO-friendly title"""
        if self.title_chain is None:
            logger.error("Title chain not initialized")
            return None
        
        try:
            logger.info("Generating SEO-friendly title...")
            result = self.title_chain.invoke({"corrected_dream_text": corrected_dream_text})
            # Clean up the title
            title = result.strip().replace('\n', ' ').replace('Title:', '').strip()
            return title
        except Exception as e:
            logger.error(f"Error in title chain: {e}")
            return None
    
    def generate_story(self, corrected_dream_text: str) -> Optional[str]:
        """Generate short story from dream"""
        if self.story_chain is None:
            logger.error("Story chain not initialized")
            return None
        
        try:
            logger.info("Generating short story...")
            result = self.story_chain.invoke({"corrected_dream_text": corrected_dream_text})
            return result.strip()
        except Exception as e:
            logger.error(f"Error in story chain: {e}")
            return None
    
    def copy_edit_story(self, short_story: str) -> Optional[str]:
        """Copy-edit the short story"""
        if self.copy_edit_chain is None:
            logger.error("Copy edit chain not initialized")
            return None
        
        try:
            logger.info("Copy-editing the short story...")
            result = self.copy_edit_chain.invoke({"short_story": short_story})
            return result.strip()
        except Exception as e:
            logger.error(f"Error in copy edit chain: {e}")
            return None
    
    def review_story(self, final_short_story: str) -> Optional[str]:
        """Review the final story"""
        if self.review_chain is None:
            logger.error("Review chain not initialized")
            return None
        
        try:
            logger.info("Reviewing the short story...")
            result = self.review_chain.invoke({"final_short_story": final_short_story})
            return result.strip()
        except Exception as e:
            logger.error(f"Error in review chain: {e}")
            return None
    
    def generate_image_prompt(self, corrected_dream_text: str, short_story: str) -> Optional[str]:
        """Generate image prompt"""
        if self.image_prompt_chain is None:
            logger.error("Image prompt chain not initialized")
            return None
        
        try:
            logger.info("Generating image prompt...")
            result = self.image_prompt_chain.invoke({
                "corrected_dream_text": corrected_dream_text,
                "short_story": short_story
            })
            return result.strip()
        except Exception as e:
            logger.error(f"Error in image prompt chain: {e}")
            return None